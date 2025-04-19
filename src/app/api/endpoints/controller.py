import logging
import random

from src.app import settings
from src.app.database.mongo import ensure_db_connected, mongodb
from src.app.database.schemas.url import UrlSchema
from src.app.shared.constants import EndpointResponse

# Set up logging
logger = logging.getLogger(__name__)


async def shorten_url_controller(data: str, base_url: str) -> EndpointResponse:
    try:
        # For serverless environments, ensure the database is connected per-request
        if settings.is_vercel or not mongodb._initialized:
            await ensure_db_connected()

        id = random.random().hex()[4:10]

        res = await UrlSchema.find_one({"shortened": id})

        if res:
            id = random.random().hex()[4:10]

        url = UrlSchema(original=data, shortened=id)

        await url.insert()

        return EndpointResponse(
            success=True,
            url=f"{base_url}/{id}",
            error=None,
        )
    except Exception as e:
        logger.error(f"Error shortening URL: {str(e)}")
        return EndpointResponse(success=False, url=None, error=str(e))
