import asyncio
import logging
import os
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters
from openai import OpenAI

# Configuration
BOT_TOKEN = '8671267596:AAE2AQtyjHQ7INruHEgTsSF1JLgeF2ihTx8'
TARGET_CHANNEL_USERNAME = '@Voice_of_the_Buyer'
SOURCE_CHANNEL_USERNAMES = ['@durov', '@telegram'] # Public channels for testing
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # Assuming API key is set as an environment variable

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

async def rewrite_caption(caption: str) -> str:
    if not caption:
        return ""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1-mini", # Using gpt-4.1-mini as requested
            messages=[
                {"role": "system", "content": "You are a helpful assistant that paraphrases text to make it unique while retaining its original meaning."},
                {"role": "user", "content": f"Rewrite the following caption to make it unique: {caption}"}
            ],
            max_tokens=150
        )
        rewritten_text = response.choices[0].message.content.strip()
        logger.info(f"Original caption: {caption}")
        logger.info(f"Rewritten caption: {rewritten_text}")
        return rewritten_text
    except Exception as e:
        logger.error(f"Error rewriting caption with OpenAI: {e}")
        return f"[Original caption could not be rewritten due to an error: {e}]\n\n{caption}"

async def handle_new_post(update: Update, context) -> None:
    if update.channel_post and update.channel_post.chat.username in [uc.lstrip('@') for uc in SOURCE_CHANNEL_USERNAMES]:
        message = update.channel_post
        logger.info(f"New post detected in {message.chat.username}: {message.message_id}")

        if message.video:
            caption = message.caption if message.caption else ""
            rewritten_caption = await rewrite_caption(caption)

            try:
                # Forward the video
                await context.bot.send_video(
                    chat_id=TARGET_CHANNEL_USERNAME,
                    video=message.video.file_id,
                    caption=rewritten_caption,
                    supports_streaming=True
                )
                logger.info(f"Video from {message.chat.username} (ID: {message.message_id}) reposted to {TARGET_CHANNEL_USERNAME} with rewritten caption.")
            except Exception as e:
                logger.error(f"Error reposting video: {e}")
        else:
            logger.info(f"Post in {message.chat.username} (ID: {message.message_id}) is not a video. Skipping.")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handler for new channel posts
    application.add_handler(MessageHandler(filters.Chat(username=SOURCE_CHANNEL_USERNAMES) & filters.UpdateType.CHANNEL_POST, handle_new_post))

    logger.info("Bot started. Monitoring source channels...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
