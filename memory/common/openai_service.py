from openai import AsyncOpenAI
from memory.database.settings import GPTSettings

# 환경변수나 .env.gpt에서 키를 읽어 옵니다
GPT_SETTINGS = GPTSettings()
client = AsyncOpenAI(api_key=GPT_SETTINGS.OPENAI_API_KEY)

async def generate_continuous_story(
    previous_stories: list[str],
    file_url: str,              # S3에 업로드된 공개 혹은 presigned URL
    content_type: str,          # 이미지의 MIME 타입 (예: "image/png")
    keywords: str | None = None,
    user_query: str | None = None,
) -> str:
    """
    - previous_stories: 이전에 생성된 스토리들
    - file_url: S3에 올린 이미지의 URL
    - content_type: file.content_type
    - keywords, user_query: optional 추가 컨텍스트
    """
    system_prompt = (
        "당신은 사용자가 업로드한 사진으로 회고록을 생성하는 어시스턴트입니다. "
        "각 사진마다 이전 스토리와 자연스럽게 이어서 작성해 주세요."
    )
    messages: list[dict] = [
        {"role": "system", "content": system_prompt}
    ]

    if previous_stories:
        joined = "\n---\n".join(previous_stories)
        messages.append({
            "role": "user",
            "content": f"이전까지 생성된 스토리(순서대로):\n\n{joined}"
        })

    if keywords or user_query:
        extra = ""
        if keywords:
            extra += f"키워드: {keywords}\n"
        if user_query:
            extra += f"쿼리: {user_query}"
        messages.append({"role": "user", "content": f"추가 정보:\n{extra}"})

    # 멀티모달 블록: 텍스트 + 이미지 URL
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": (
                    "당신은 사용자가 업로드한 사진으로 회고록을 생성하는 어시스턴트입니다. "
                    "각 사진마다 이전 스토리와 자연스럽게 이어서 작성해 주세요."
                    "다음 사진을 보고, 이전 스토리와 자연스럽게 이어지는 "
                    "짧고 감성적인 스토리를 한 문단으로 1인칭 시점에서 과거를 추억하듯이 작성해 주세요:"
                )
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": file_url
                }
            }
        ]
    })

    # GPT-4o 호출
    resp = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    # 결과 반환
    return resp.choices[0].message.content.strip()
