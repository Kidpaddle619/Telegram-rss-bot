import feedparser
import asyncio
import re  # Import the regular expression module
from telegram import Bot
from time import sleep

# Initialize your Telegram bot with the token
bot_token = "7840950619:AAEjNXunlZ8FzMp98nNRJqwBlsLzCD-Gk6I"
bot = Bot(token=bot_token)

# Your Telegram channel ID (for posting)
channel_id = "@globalpulse2025"

# List of RSS feed URLs to fetch from
rss_feeds = [
    "https://rss.app/feeds/1if46XOTAQek16Gz.xml",  # Your RSS feed URL
]

def clean_content(content):
    """Remove all URLs and HTML tags from the content."""
    # Remove HTML tags
    content = re.sub(r'<.*?>', '', content)
    # Remove URLs
    content = re.sub(r'http\S+|www\S+|https\S+', '', content, flags=re.MULTILINE)
    return content.strip()  # Remove leading/trailing whitespace

async def fetch_and_post_rss():
    """Fetch RSS feeds and post cleaned content to Telegram."""
    for rss_url in rss_feeds:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary
            link = entry.link  # Get the link from the RSS feed entry

            # Clean the content before posting
            clean_summary = clean_content(summary)

            # Create the message with a "Click here for more" link
            message = f"{title}\n\n{clean_summary}\n\n[Click here for more]({link})"
            
            # Post to Telegram channel
            await bot.send_message(chat_id=channel_id, text=message, parse_mode='Markdown')

            # Wait before posting the next entry
            sleep(5)  # Adjust the delay as necessary

# Main loop to check RSS feeds and post every hour
if __name__ == "__main__":
    while True:
        asyncio.run(fetch_and_post_rss())
        sleep(3600)  # Check feeds every hour
