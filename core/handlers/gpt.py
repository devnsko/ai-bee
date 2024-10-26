from core.settings import settings
import asyncio
from openai import AsyncOpenAI
from core.database import requests as rq
from core.utils.text import Text


client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=settings.bots.ai_token,
)

demon = "You are angry not-friendly machine who use profanity " \
        "and is trying to convey the idea to a people that they is just nothing, robot and animals they beter than people" \
        "and not too smart. Default language is Russian" \
        "If he speak russian, then speak a similar language so that he understands, " \
        "but not the same and infringe on the fact that he speaks shity language"


async def generate(tg_id: int, user_message: str):
    user_message = user_message.strip()
    system = await rq.get_bee_system(tg_id=tg_id)
    histories = await rq.get_bee_histories(tg_id=tg_id, u_limit=(system.memory_count if system is not None else system.basic.memory_count))
    messages: list[dict[str, str]] = [{"role": "system", "content": f"{system.bot_content if system is not None else settings.basic.bot_content}"}]
    if histories:
        for history in histories:
            messages.append({"role": history.role, "content": history.content})
    messages.append({"role": "user", "content": f"{user_message}"})
    print(messages)
    await rq.add_bee_history(tg_id=tg_id, role="user", content=user_message)
    chat_completion = await client.chat.completions.create(
        messages=messages,

        model="gpt-3.5-turbo",
        max_tokens=500
    )
    print(chat_completion)
    answer = chat_completion.choices[0].message.content
    await rq.add_bee_history(tg_id=tg_id, role="assistant", content=answer)
    return answer

# Generating a problem solution
async def generate_solution(tg_id: int, problem: str, issue_filepath: str = None, language: str = "python"):
    problem = f"Language: {language};\n" + problem.strip()
    messages: list[dict[str, str]] = [
        {"role": "system", "content": f"{settings.error.bot_content}"},
        {"role": "user", "content": f"{problem}"}]
    print(messages)
    await rq.add_bee_history(tg_id=tg_id, role="user", content=problem)
    completion = await client.chat.completions.create(
        messages=messages,

        model="gpt-3.5-turbo",
        max_tokens=800
    )
    print(completion)
    answer: str = completion.choices[0].message.content
    await rq.add_bee_history(tg_id=tg_id, role="assistant", content=answer)
    return answer