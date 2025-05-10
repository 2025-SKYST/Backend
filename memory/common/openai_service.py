import os
import openai
from database.settings import GPTSettings

GPTSETTINGS = GPTSettings()
openai.api_key = GPTSETTINGS.OPENAI_API_KEY

async def start_making(chapter_name: str) -> str:
    messages = [
        {"role": "system", "content": "당신은 사진 기반 회고록 생성 도우미입니다."},
        {"role": "user", "content":
            f"새로운 회고록 제목은 '{chapter_name}' 입니다. "
            "사용자가 이후 사진을 업로드할 계획이니, 간결하고 감성적인 프로롤로그를 작성해 주세요."
        }
    ]

    resp = await openai.ChatCompletion.acreate(
        model="gpt-4o",
        messages=messages
    )
    return resp.choices[0].message.content.strip()

async def generate_story_for_image(prologue: str, image_url: str) -> str:
    messages = [
        {"role": "system", "content": "당신은 사진 기반 회고록 생성 도우미입니다."},
        {"role": "assistant", "content": prologue},
        {"role": "user", "content":
            f"다음 사진 URL을 보고, 위 프로롤로그 주제에 맞는 짧은 이야기를 작성해 주세요:\n{image_url}"
        }
    ]
    resp = await openai.ChatCompletion.acreate(
        model="gpt-4o",
        messages=messages
    )
    return resp.choices[0].message.content.strip()