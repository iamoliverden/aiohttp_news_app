# views.py

import logging
import aiohttp
import aiohttp_jinja2
from aiohttp import web
from faker import Faker
import asyncio
import json
from api_key import APIKeyRecord

api_key_record = APIKeyRecord()
API_KEY = api_key_record.get_api_key()
BASE_URL = 'https://newsapi.org/v2/top-headlines'
COUNTRY = 'us'
INTERVAL = 15  # Time interval in seconds between each fetch

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def get_random_name():
    fake = Faker()
    return fake.name()

async def get_news(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            news_data = await resp.json()
            return news_data['articles']
        else:
            log.error(f"Error: {resp.status}")
            return []

async def fetch_news_periodically(app):
    async with aiohttp.ClientSession() as session:
        while True:
            url = f'{BASE_URL}?country={COUNTRY}&apiKey={API_KEY}'
            news_articles = await get_news(session, url)

            if news_articles:
                for article in news_articles:
                    if 'url' in article and article['url']:
                        log.info(f"Article URL: {article['url']}")  # Log the URL
                        message = {
                            'action': 'sent',
                            'name': 'Superuser',
                            'text': article['title'],
                            'url': article['url']  # Ensure the URL is included
                        }
                        for ws in app['websockets'].values():
                            await ws.send_json(message)
                    else:
                        log.error("Article URL is missing or undefined.")
            else:
                log.error("No articles found or an error occurred.")

            await asyncio.sleep(INTERVAL)

async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})

    await ws_current.prepare(request)

    name = get_random_name()
    log.info('%s joined.', name)

    await ws_current.send_json({'action': 'connect', 'name': name})

    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'join', 'name': name})
    request.app['websockets'][name] = ws_current

    try:
        while True:
            msg = await ws_current.receive()

            if msg.type == aiohttp.WSMsgType.text:
                data = json.loads(msg.data)
                if data['action'] == 'ping':
                    await ws_current.send_json({'action': 'pong'})
                elif name == 'Superuser':  # Only allow the superuser to send messages
                    for ws in request.app['websockets'].values():
                        if ws is not ws_current:
                            await ws.send_json(
                                {'action': 'sent', 'name': name, 'text': msg.data})
            else:
                break
    except Exception as e:
        log.error(f"Error: {e}")
    finally:
        del request.app['websockets'][name]
        log.info('%s disconnected.', name)
        for ws in request.app['websockets'].values():
            await ws.send_json({'action': 'disconnect', 'name': name})

    return ws_current
