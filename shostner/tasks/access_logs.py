from motor.motor_asyncio import AsyncIOMotorClient
from ..main import urls
from ..controllers.data import create_log
from ..models.data import Log

async def log_access_info(shortened_url: str, 
                    long_url: str , 
                    user_agent: str, 
                    referer: str, 
                    ip: str, 
                    language: str,
                    db: AsyncIOMotorClient
                    ):
    log = Log(
        shortened_url = shortened_url , 
        long_url = long_url, 
        user_agent = user_agent, 
        referer = referer, 
        ip = ip, 
        language = language
    )
    await create_log(db, log)
