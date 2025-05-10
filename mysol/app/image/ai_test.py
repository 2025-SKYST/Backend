import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
from typing import List

# test_imports.py

try:
    from langchain.chains.llm import LLMChain
    from langchain_core.prompts import PromptTemplate
    print("✅ Import 성공")
except ModuleNotFoundError as e:
    print("❌ Import 실패:", e)

import os
from pathlib import Path

print("▶ 현재 작업 디렉터리:", os.getcwd())
print("▶ 파일 목록:", os.listdir())
# .env.llm 파일이 있는 경로 출력
print("▶ .env.llm 존재 여부:", (Path(os.getcwd()) / ".env.llm").exists())



# 현재 디렉토리의 부모 디렉토리를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).parent.parent.parent))
print(sys.path)

load_dotenv(".env.llm")
print(Path(__file__).resolve().parent.parent.parent)
from mysol.app.image.img2text import ImageLangChainProcessor

async def test_image_processing():
    # 테스트 이미지 생성
    def create_test_image() -> bytes:
        img = Image.new('RGB', (100, 100), color = 'red')
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    # 테스트 이미지 파일 생성
    test_image_bytes = create_test_image()
    test_file = UploadFile(
        filename="test_image.png",
        file=BytesIO(test_image_bytes)
    )
    print(os.getenv("GOOGLE_API_KEY"))
    # Google API 키 설정
    google_api_key = "AIzaSyAWZUKgmDWuPrJfpULp_WLHXjA9Ufi-Voo"#os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다")
    
    print(f"Using GOOGLE_API_KEY: {google_api_key[:10]}... (masked)")  # 키의 일부만 출력하여 확인
    
    # ImageLangChainProcessor 초기화
    processor = ImageLangChainProcessor(google_api_key=google_api_key)
    
    # 이미지 로드 테스트
    await processor.load_images([test_file])
    
    # 캡션 생성 테스트
    processor.generate_captions()
    processor.detailed_descriptions()
    
    # 결과 확인
    results = processor.get_results()
    print("\n테스트 결과:")
    print(f"캡션: {results['captions'][0]}")
    print(f"상세 설명: {results['analysis']['detailed'][0]}")
    processor.detailed_descriptions()
    
    # 결과 확인
    results = processor.get_results()
    print("\n테스트 결과:")
    print(f"캡션: {results['captions'][0]}")
    print(f"상세 설명: {results['analysis']['detailed'][0]}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_image_processing())