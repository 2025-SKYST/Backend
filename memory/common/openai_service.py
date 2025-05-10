import base64
import openai

async def generate_continuous_story(
    previous_stories: list[str],
    image_bytes: bytes,
    content_type: str,
    keywords: str | None = None,
    user_query: str | None = None,
) -> str:
    """
    - system_prompt: chapter.system_prompt
    - previous_stories: 순서대로 쌓인 이전 이미지들의 story 리스트
    - image_bytes, content_type: 업로드된 파일 원본
    - keywords, user_query: optional 추가 context
    """
    # 1) 이미지 → data URI
    b64 = base64.b64encode(image_bytes).decode()
    data_uri = f"data:{content_type};base64,{b64}"

    system_prompt=(
        "당신은 사용자가 업로드한 사진으로 회고록을 생성하는 어시스턴트입니다. "
        "각 사진마다 이전 스토리와 자연스럽게 이어서 작성해 주세요."
    )


    messages = [
        {"role": "system", "content": system_prompt},
    ]

    if previous_stories:
        joined = "\n---\n".join(previous_stories)
        messages.append({
            "role": "user",
            "content": (
                "이전까지 생성된 스토리( 순서대로 ):\n\n"
                f"{joined}"
            )
        })

    if keywords or user_query:
        extra = ""
        if keywords:
            extra += f"키워드: {keywords}\n"
        if user_query:
            extra += f"쿼리: {user_query}"
        messages.append({"role": "user", "content": f"추가 정보:\n{extra}"})

    messages.append({
        "role": "user",
        "content": (
            "다음 사진을 보고, 이전 스토리와 자연스럽게 이어지는 "
            "짧고 감성적인 스토리를 한 문단으로 작성해 주세요:\n\n"
            f"{data_uri}"
        )
    })

    # 3) GPT 호출
    resp = await openai.ChatCompletion.acreate(
        model="gpt-4o",
        messages=messages
    )
    return resp.choices[0].message.content.strip()