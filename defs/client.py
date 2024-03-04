from simnet import GenshinClient, Region

from .config import COOKIES, GENSHIN_PLAYER_ID


def get_genshin_client() -> GenshinClient:
    return GenshinClient(
        COOKIES,
        region=Region.CHINESE,
        player_id=GENSHIN_PLAYER_ID,
        lang="zh-cn",
    )


client = get_genshin_client()
