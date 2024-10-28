from core.settings import settings
import asyncio
from openai import AsyncOpenAI
from core.database import requests as rq

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=settings.bots.ai_token,
)

async def generate(tg_id: int, user_message: str):
    user_message = user_message.strip()
    user = await rq.get_user(tg_id=tg_id)
    if user.context is None or user.context.strip() == "":
        context = settings.basic.bot_context
    else:
        context = user.context
    histories = await rq.get_chat_history(tg_id=tg_id, u_limit=(settings.basic.memory_count))
    messages: list[dict[str, str]] = [{"role": "system", "content": f"max 4096 symbols.\n\n{context}"}]
    if histories:
        for history in histories:
            messages.append({"role": history.role, "content": history.content})
    messages.append({"role": "user", "content": f"{user_message}"})
    print(messages)
    await rq.add_chat_history(tg_id=tg_id, role="user", content=user_message)
    chat_completion = await client.chat.completions.create(
        messages=messages,

        model="gpt-4o-mini-2024-07-18",
        max_tokens=500
    )
    print('[chat_completion]:\n\n'+chat_completion.model_dump_json()+'\n\n')
    answer = chat_completion.choices[0].message.content
    await rq.add_chat_history(tg_id=tg_id, role="assistant", content=answer)
    return answer
