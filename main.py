import ssl, os
import logging
from aiohttp import web
from config import admins
from app.dialogs import msg
from aiogram.dispatcher.webhook import get_new_configured_app

WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PORT = os.getenv("WEBHOOK_PORT")
WEBHOOK_URL_PATH = '/webhook'
WEBHOOK_SSL_CERT = './url_cert.pem'
WEBHOOK_SSL_PRIV = './url_private.key'
WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"
WEBAPP_HOST = '0.0.0.0'

async def on_startup(app):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, msg.admin_set_messages)
        except Exception as err:
            logging.exception(err)
    webhook = await bot.get_webhook_info()
    if webhook.url != WEBHOOK_URL:

        if not webhook.url:
            await bot.delete_webhook()

        await bot.set_webhook(WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'rb'))


async def on_shutdown(app):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    from app.bot import dp, bot
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
    web.run_app(app, host=WEBAPP_HOST, port=WEBHOOK_PORT, ssl_context=context)