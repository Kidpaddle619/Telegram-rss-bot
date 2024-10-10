import asyncio
from telegram import Bot

# Initialize your bot with the token
bot_token = "7840950619:AAEjNXunlZ8FzMp98nNRJqwBlsLzCD-Gk6I"
bot = Bot(token=bot_token)

# Function to send a message
async def send_message():
    await bot.send_message(chat_id="@globalpulse2025", text="Hello, this is a test!")

# Main function to run the async code
if __name__ == "__main__":
    asyncio.run(send_message())
