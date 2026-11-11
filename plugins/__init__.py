# Don't Remove Credit @letswatchitnow
# Subscribe YouTube Channel For Amazing Bot @letswatchitnow
# Ask Doubt on telegram @letswatchitnow

from aiohttp import web
from .route import routes

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

