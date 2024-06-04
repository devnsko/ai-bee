from core.settings import settings
import asyncio
from openai import AsyncOpenAI


client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=settings.bots.ai_token,
)


async def generate(user_message):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{user_message}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(chat_completion)
    return chat_completion.choices[0].message.content

