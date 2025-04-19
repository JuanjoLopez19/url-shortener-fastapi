import random

from src.app.database.schemas.url import UrlSchema
from src.app.shared.constants import EndpointResponse


async def shorten_url_controller(data: str, base_url: str) -> EndpointResponse:
    try:
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
        print(e)
        return EndpointResponse(success=False, url=None, error=str(e))
