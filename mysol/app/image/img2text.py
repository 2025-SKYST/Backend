import os
from typing import List, Dict
from PIL import Image
from io import BytesIO
from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain.llms import GooglePalm
from langchain import PromptTemplate, LLMChain
from fastapi import UploadFile

class ImageLangChainProcessor:
    """
    순수 이미지에서 캡션(설명)을 생성하고,
    LangChain을 이용해 생성된 텍스트를 상세 분석하는 클래스.
    """

    def __init__(self, google_api_key: str, palm_model: str = "models/text-bison-001"):
        # Google API 키 설정
        os.environ["GOOGLE_API_KEY"] = google_api_key
        # Google Palm LLM 초기화
        self.llm = GooglePalm(model=palm_model)
        # BLIP 모델 및 프로세서 초기화
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        self.images: List[Image.Image] = []
        self.captions: List[str] = []
        self.analysis: Dict[str, List[str]] = {}

    async def load_images(self, images: List[UploadFile]) -> 'ImageLangChainProcessor':
        """UploadFile 객체 목록을 로드합니다."""
        for file in images:
            # UploadFile의 내용을 메모리에 로드
            content = await file.read()
            # 메모리에서 PIL 이미지로 변환
            img = Image.open(BytesIO(content))
            self.images.append(img)
        return self

    def generate_captions(self) -> 'ImageLangChainProcessor':
        """BLIP 모델을 활용해 각 이미지에 대한 캡션을 생성합니다."""
        captions = []
        for img in self.images:
            img = img.convert("RGB")
            inputs = self.processor(images=img, return_tensors="pt")
            outputs = self.model.generate(**inputs)
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            captions.append(caption)
        self.captions = captions
        return self

    def analyze(self, name: str, prompt_template: str) -> 'ImageLangChainProcessor':
        """
        주어진 프롬프트 템플릿으로 각 캡션을 LangChain LLMChain 분석합니다.

        :param name: 분석 결과 식별자 (예: 'detailed', 'summary')
        :param prompt_template: {text} 변수를 포함한 프롬프트 템플릿
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = LLMChain(llm=self.llm, prompt=prompt)
        results = []
        for text in self.captions:
            results.append(chain.run(text=text))
        self.analysis[name] = results
        return self

    def detailed_descriptions(self) -> 'ImageLangChainProcessor':
        """생성된 캡션을 더 상세하게 서술합니다."""
        template = (
            "다음 이미지 설명을 더 상세하게, 구체적인 장면과 감정을 담아 한국어로 서술해줘:\n\n{text}"
        )
        return self.analyze("detailed", template)

    def summarize_captions(self) -> 'ImageLangChainProcessor':
        """캡션을 요약하고 주요 특징을 강조합니다."""
        template = (
            "다음 설명을 폭넓은 관점에서 요약하고, 주요 특징을 강조해줘:\n\n{text}"
        )
        return self.analyze("summary", template)

    def get_results(self) -> Dict[str, any]:
        """모든 로드된 이미지, 생성된 캡션, 분석 결과를 반환합니다."""
        return {
            "images": self.image_paths,
            "captions": self.captions,
            "analysis": self.analysis
        }
