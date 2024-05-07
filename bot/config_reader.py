from typing import Optional
from pydantic import BaseSettings, SecretStr
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Class for defining and storing application settings.
    """
    bot_token: SecretStr
    admin_chat_id: int
    remove_sent_confirmation: bool
    webhook_domain: Optional[str]
    webhook_path: Optional[str]
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    custom_bot_api: Optional[str]

    class Config:
        """
        Class for defining configuration settings for the Settings class.
        """
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

# Instantiate Settings object with values from .env file
try:
    config = Settings()
    logger.info("Settings successfully loaded.")
except Exception as e:
    logger.error("Error loading settings: %s", e)
    raise e