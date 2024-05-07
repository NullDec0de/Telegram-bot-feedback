from aiogram import Router
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_routers() -> Router:
    """
    Sets up and returns a router with included sub-routers for various bot functionalities.

    :return: Router with included sub-routers.
    :rtype: aiogram.Router
    """
    try:
        # Import necessary sub-routers
        from . import unsupported_reply, admin_no_reply, bans, adminmode, message_edit, usermode

        # Create router
        router = Router()

        # Include sub-routers in main router
        router.include_router(unsupported_reply.router)
        router.include_router(bans.router)
        router.include_router(admin_no_reply.router)
        router.include_router(adminmode.router)
        router.include_router(message_edit.router)
        router.include_router(usermode.router)

        # Log successful setup of routers
        logger.info("Routers successfully set up.")

        return router

    except Exception as e:
        # Log error if setup fails
        logger.error("Error setting up routers: %s", e)
        raise e