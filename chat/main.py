# main.py

import logging
import jinja2
import aiohttp_jinja2
from aiohttp import web
from views import index, fetch_news_periodically
import asyncio

async def init_app():
    app = web.Application()
    app['websockets'] = {}

    app.on_shutdown.append(shutdown)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('chat', 'templates'))

    app.router.add_get('/', index)

    # Start the superuser task
    app['superuser_task'] = asyncio.create_task(fetch_news_periodically(app))

    return app

async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()
    app['superuser_task'].cancel()
    await app['superuser_task']

def main():
    # Set the logging level to INFO to reduce verbosity
    logging.basicConfig(level=logging.INFO)
    app = init_app()
    web.run_app(app)

if __name__ == '__main__':
    main()
