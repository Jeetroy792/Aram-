# 𝖥𝗂𝗅𝖾: 𝗌𝖾𝗋𝗏𝖾𝗋.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

from aiohttp import web
import asyncio

# জিৎ, এটি একটি সিম্পল এইচটিএমএল রেসপন্স যা সার্ভার হেলথ চেক করবে
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("Elite Encoder X9 is Running Smoothly! 🚀")

async def web_server():
    """বটকে অনলাইনে রাখার জন্য ওয়েব সার্ভার স্টার্ট করার ফাংশন"""
    web_app = web.Application()
    web_app.add_routes(routes)
    return web_app

def start_server():
    """সার্ভার রান করার মেইন এন্ট্রি পয়েন্ট"""
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(web_server())
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    # ডাইনামিক পোর্ট হ্যান্ডলিং (Koyeb/Heroku এর জন্য জরুরি)
    import os
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    loop.run_until_complete(site.start())
    print(f"✅ 𝖶𝖾𝖻 𝖲𝖾𝗋𝗏𝖾𝗋 𝗂𝗌 𝖠𝖼𝗍𝗂𝗏𝖾 𝗈𝗇 𝖯𝗈𝗋𝗍: {port}")

# জিৎ, এটি main.py থেকে কল করা হবে

