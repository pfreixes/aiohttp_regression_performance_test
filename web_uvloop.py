import asyncio
import uvloop

from aiohttp import web

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def handle(request):
    return web.Response(text='hellow world')

app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, access_log=None, host="127.0.0.1", port=5000)
