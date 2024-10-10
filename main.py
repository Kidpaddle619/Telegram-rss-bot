import feedparser
import asyncio
import re
from telegram import Bot

# Initialize your Telegram bot with the token
bot_token = "7840950619:AAEjNXunlZ8FzMp98nNRJqwBlsLzCD-Gk6I"  # Your bot token
bot = Bot(token=bot_token)

# Your Telegram channel ID (for posting)
channel_id = "@globalpulse2025"

# List of RSS feed URLs to fetch from
rss_feeds = [
    "https://rss.app/feeds/1if46XOTAQek16Gz.xml",
    "https://www.israelnationalnews.com/Rss.aspx",
    "https://middleeastmnt.disqus.com/latest.rss",
    "https://www.albawaba.com/rss/all",
    "https://www.greenprophet.com/feed/",
    "https://israelagainstterror.blogspot.com/feeds/posts/default?alt=rss",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://nypost.com/us-news/feed/",
    "https://nypost.com/world-news/feed/",
    "https://www.cbsnews.com/latest/rss/world",
    "https://www.cbsnews.com/latest/rss/us",
    "https://www.cbsnews.com/latest/rss/politics",
    "https://abcnews.go.com/abcnews/topstories",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml?PostingId=2007731105943979989",
    "https://www.anandtech.com/rss/",
    "https://chaski.huffpost.com/us/auto/vertical/front-page",
    "https://feeds.nbcnews.com/nbcnews/public/news",
    "https://feeds.npr.org/1002/rss.xml",
    "https://futurism.com/feed",
    "https://gizmodo.com/feed",
    "https://mashable.com/feeds/rss/tech",
    "https://rss.news.yahoo.com/rss/topstories",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://rss.slashdot.org/Slashdot/slashdot",
    "https://techcrunch.com/feed/",
    "https://thenextweb.com/feed",
    "https://www.cnet.com/rss/news/",
    "https://www.digitaltrends.com/feed/",
    "https://www.engadget.com/rss.xml",
    "https://www.ft.com/world?format=rss",
    "https://www.geekwire.com/feed/",
    "https://www.independent.co.uk/rss",
    "https://www.telegraph.co.uk/rss.xml",
    "https://www.theinformation.com/feed",
    "https://feeds.skynews.com/feeds/rss/world.xml",
    "https://feeds.skynews.com/feeds/rss/strange.xml",
    "https://www.middleeasteye.net/rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://warontherocks.com/feed/",
    "https://www.bellingcat.com/feed/",
    "https://www.juancole.com/feed",
    "https://www.justsecurity.org/feed/",
    "https://www.middleeastmonitor.com/feed",
    "https://www.syria-report.com/feed",
    "http://feeds.boingboing.net/boingboing/iBag",
    "http://feeds.feedburner.com/DrudgeReportFeed",
    "http://feeds.feedburner.com/TechCrunch/",
    "https://gizmodo.com/rss",
    "https://mashable.com/feed/",
    "https://theintercept.com/feed/?rss",
    "https://www.nakedcapitalism.com/feed",
    "https://news.google.com/news/rss",
    "https://flipboard.com/@flipboard/news.rss",
    "https://www.huffpost.com/section/world-news/feed",
    "https://www.france24.com/en/rss",
    "https://www.mnnonline.org/rss/countries/lbn.xml",
    "https://www.lbcgroup.tv/rss/",
    "https://english.almanar.com.lb/rss",
    "https://libnanews.com/en/feed/",
    "https://www.express.co.uk/posts/rss/77/news",
    "https://www.lemonde.fr/en/international/rss_full.xml",
    "https://sana.sy/en/?feed=rss2",
    "https://www.msf.org/rss/lebanon",
    "https://www.msf.org/rss/syria",
    "https://www.msf.org/rss/topics",
    "https://www.msf.org/rss/countries",
    "https://breakingdefense.com/full-rss-feed/?v=2",
    "https://www.chathamhouse.org/path/whatsnew.xml",
    "https://www.aa.com.tr/en/rss/default?cat=live",
    "https://saudigazette.com.sa/ — https://saudigazette.com.sa/rssFeed/0",
    "https://saudigazette.com.sa/ — https://saudigazette.com.sa/rssFeed/31",
    "https://english.alarabiya.net/feed/rss2/en.xml",
    "https://www.arabnews.com/rss",
    "https://www.meed.com/classifications/analysis/special-report/feed/",
    "https://www.meed.com/countries/levant/lebanon/rss/feed",
    "https://www.argaam.com/en/rss/ho-main-news?sectionid=1524",
    "https://en.mehrnews.com/rss?pl=225",
    "https://en.mehrnews.com/rss",
    "https://iranwire.com/en/feed/",
    "https://www.tehrantimes.com/rss?pl=617",
    "https://www.tehrantimes.com/rss",
    "https://www.militarytimes.com/arc/outboundfeeds/rss/category/news/?outputType=xml",
    "https://defence-blog.com/feed/",
    "https://rsshub.app/reddit/subreddit/worldnews",
    "https://www.reddit.com/r/worldnews/.rss",
    "https://rss.app/feeds/JLZp1fRDgsTbPBCP.xml",
    "https://rss.app/feeds/YnJGf7Z9SE1S9fK2.xml",
    "https://rss.app/feeds/MfRmjHeOIRdRIJmu.xml",
    "https://rss.app/feeds/EvzE3kDGJjNRIpiu.xml",
    "https://rss.app/feeds/lxqS2eeZfHBkK3QL.xml",
    "https://rss.app/feeds/mDBI7sJhzMcY0LDR.xml",
]

# Function to send a message to the Telegram channel
async def send_message(title, summary, link):
    clean_summary = re.sub(r'<[^>]+>', '', summary)  # Remove HTML tags
    message = f"<b>{title.upper()}</b>\n\n{clean_summary}\n\n<a href='{link}'>CLICK HERE FOR MORE ABOUT THIS STORY</a>"
    await bot.send_message(channel_id, message, parse_mode="HTML")

# Main function to fetch RSS feeds and send messages
async def fetch_and_send():
    for url in rss_feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.title
                summary = entry.summary if hasattr(entry, 'summary') else "No summary available."
                link = entry.link
                await send_message(title, summary, link)
            await asyncio.sleep(2)  # Sleep between requests to avoid hitting rate limits
        except Exception as e:
            print(f"An error occurred: {e}")

# Vercel handler function
def handler(request):
    asyncio.run(fetch_and_send())
    return "Messages sent!", 200

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # If there's no running loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(fetch_and_send())
