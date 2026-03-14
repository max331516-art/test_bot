import requests
import time
import logging
import os
from openai import OpenAI

BOT_TOKEN = '8671267596:AAE2AQtyjHQ7INruHEgTsSF1JLgeF2ihTx8'
TARGET_CHANNEL = '@Voice_of_the_Buyer'
SOURCE_CHANNELS = ['durov', 'telegram']
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai_client = OpenAI(api_key=OPENAI_API_KEY)
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

def rewrite_caption(caption):
    if not caption:
        return ""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Paraphrase the text to make it unique while keeping the meaning."},
                {"role": "user", "content": f"Rewrite: {caption}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return caption

def get_updates(offset=0):
    try:
        r = requests.get(API_URL + 'getUpdates', params={'offset': offset, 'timeout': 30}, timeout=35)
        return r.json()
    except Exception as e:
        logger.error(f"getUpdates error: {e}")
        return {'ok': False, 'result': []}

def send_video(chat_id, file_id, caption):
    try:
        r = requests.post(API_URL + 'sendVideo', json={'chat_id': chat_id, 'video': file_id, 'caption': caption, 'supports_streaming': True})
        return r.json()
    except Exception as e:
        logger.error(f"sendVideo error: {e}")
        return {'ok': False}

def main():
    offset = 0
    logger.info("Bot started.")
    while True:
        updates = get_updates(offset)
        if updates.get('ok'):
            for update in updates['result']:
                offset = update['update_id'] + 1
                msg = update.get('channel_post', {})
                username = msg.get('chat', {}).get('username', '')
                if username in SOURCE_CHANNELS and 'video' in msg:
                    caption = rewrite_caption(msg.get('caption', ''))
                    result = send_video(TARGET_CHANNEL, msg['video']['file_id'], caption)
                    if result.get('ok'):
                        logger.info(f"Reposted video from @{username}")
        time.sleep(1)

if __name__ == '__main__':
    main()
