# import asyncio
# import sys
# import traceback
# from aiogram import Bot
# from core.settings import settings
#
#
# class BeeException:
#     def __init__(self, bot: Bot):
#
#         self.bot = bot
#         # Переопределяем sys.excepthook
#         sys.excepthook = self.bee_excepthook
#
#     def bee_excepthook(self, exc_type, exc_value, exc_traceback):
#         # Изменение вывода ошибки
#         print("##------------Bee--------------##")
#         txt: str = "--------------------------" + "\n"
#         print("Exception type:", exc_type.__name__)
#         txt += "Exception type:", exc_type.__name__ + "\n"
#         print("Exception message:", exc_value)
#         txt += "Exception message: " + str(exc_value) + "\n"  # Convert exc_value to str
#         print("Stack trace:")
#         txt += "Stack trace:" + "\n"
#         traceback.print_tb(exc_traceback)
#         trace_lines = traceback.format_tb(exc_traceback)
#         txt += ''.join(trace_lines)
#
#         asyncio.run(self.send_error(message=txt))  # Добавлено для запуска корутины
#
#     async def send_error(self, message: str):
#         msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
#         for text in msgs:
#             await self.bot.send_message(chat_id=settings.bots.admin_id, text=f'Bee: You have error in code:\n{text}')
#
#
# sys.excepthook = BeeException.bee_excepthook
