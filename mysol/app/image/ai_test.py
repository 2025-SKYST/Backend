import os
import sys
from pathlib import Path
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
from typing import List

# 현재 디렉토리의 부모 디렉토리를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).parent.parent.parent))

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

    # Google API 키 설정 (실제 테스트 시에는 실제 API 키로 변경해야 함)
    google_api_key = "your_google_api_key_here"
    
    # ImageLangChainProcessor 초기화
    processor = ImageLangChainProcessor(google_api_key=google_api_key)
    
    # 이미지 로드 테스트
    await processor.load_images([test_file])
    
    # 캡션 생성 테스트
    processor.generate_captions()
    
    # 상세 설명 생성 테스트
    processor.detailed_descriptions()
    
    # 결과 확인
    results = processor.get_results()
    print("\n테스트 결과:")
    print(f"캡션: {results['captions'][0]}")
    print(f"상세 설명: {results['analysis']['detailed'][0]}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_image_processing())