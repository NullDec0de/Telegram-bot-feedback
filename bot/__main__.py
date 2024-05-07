import asyncio
import logging
from pathlib import Path

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.telegram import TelegramAPIServer
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from fluent.runtime import FluentLocalization, FluentResourceLoader

from bot.commandsworker import set_bot_commands
from bot.handlers import setup_routers
from bot.middlewares import L10nMiddleware
from bot.config_reader import config


async def main():
    """
    Main function that starts the bot.

    :return: None
    """
    # Configure logging to stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Get path to locales directory relative to current file
    locales_dir = Path(__file__).parent.joinpath("locales")

    # Create Fluent objects
    l10n_loader = FluentResourceLoader(str(locales_dir) + "/{locale}")
    l10n = FluentLocalization(["ru"], ["strings.ftl", "errors.ftl"], l10n_loader)

    # Create bot and dispatcher objects
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    router = setup_routers()
    dp.include_router(router)

    # Set custom bot API server if specified in config
    if config.custom_bot_api:
        bot.session.api = TelegramAPIServer.from_base(config.custom_bot_api, is_local=True)

    # Register middleware for localization
    dp.message.middleware(L10nMiddleware(l10n))

    # Register /-commands in bot interface
    await set_bot_commands(bot)

    try:
        # If no webhook domain specified, start polling for updates
        if not config.webhook_domain:
            await bot.delete_webhook()
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        else:
            # Disable aiohttp access logs
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)

            # Set webhook
            await bot.set_webhook(
                url=config.webhook_domain + config.webhook_path,
                drop_pending_updates=True,
                allowed_updates=dp.resolve_used_update_types()
            )

            # Create and start aiohttp server
            app = web.Application()
            SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host=config.app_host, port=config.app_port)
            await site.start()

            # Infinite loop to keep server running
            await asyncio.Event().wait()
    finally:
        await bot.session.close()


asyncio.run(main())