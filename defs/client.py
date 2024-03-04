from pathlib import Path

import aiofiles
from httpx import AsyncClient
from simnet import GenshinClient, Region

from .config import COOKIES, GENSHIN_PLAYER_ID

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
req_client = AsyncClient(timeout=60.0, headers=headers)


def get_genshin_client() -> GenshinClient:
    return GenshinClient(
        COOKIES,
        region=Region.CHINESE,
        player_id=GENSHIN_PLAYER_ID,
        lang="zh-cn",
    )


async def download(url: str, path: Path, override: bool = False):
    if path.exists() and not override:
        return
    head = await req_client.head(url)
    if head.status_code != 200:
        print(f"Failed to download {url}, status code: {head.status_code}")
        return
    async with req_client.stream("GET", url) as response:  # noqa
        async with aiofiles.open(path, "wb") as f:
            async for chunk in response.aiter_bytes():
                await f.write(chunk)


client = get_genshin_client()
