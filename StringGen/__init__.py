import logging
import pyromod
from pyromod import listen
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode

import config

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("oldpyro").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

mongo = MongoCli(config.MONGO_DB_URI)
db = mongo.StringGen

r = web.RouteTableDef()

@r.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text='<h3 align="center"><b>I am Alive</b></h3>', content_type='text/html')

async def wsrvr():
    wa = web.Application(client_max_size=30000000)
    wa.add_routes(r)
    return wa

class Anony(Client):
    def __init__(self):
        super().__init__(
            name="Anonymous",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            lang_code="en",
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
        )

    async def start(self):
        app = web.AppRunner(await wsrvr())
        await app.setup()
        ba = "0.0.0.0"
        port = int(os.environ.get("PORT", 8080)) or 8080
        await web.TCPSite(app, ba, port).start()
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention
        LOGGER.info("Bot Started successfully..😎🤏")
        
    async def stop(self):
        await super().stop()
        LOGGER.info("Bot Stopped")

Anony = Anony()
