from typing import TYPE_CHECKING

from simnet.client.routes import Route
from simnet.utils.player import recognize_genshin_server, recognize_genshin_game_biz

from defs.models import MyDraws

if TYPE_CHECKING:
    from simnet import GenshinClient

DRAW_COLLECTION_API = Route(
    "https://hk4e-api.mihoyo.com/event/birthdaystar/account/draw_collection",
)


class BirthdayCard:
    @staticmethod
    async def get_hk4e_token(client: "GenshinClient") -> None:
        game_biz = recognize_genshin_game_biz(client.player_id)
        region = recognize_genshin_server(client.player_id)
        await client.get_hk4e_token_by_cookie_token(game_biz, region)

    @staticmethod
    async def get_my_draws(
            client: "GenshinClient",
            page_size: int = 2,
            draw_collection_type: int = 0,
            draw_collection_operate: int = 4,
            page: int = 0,
    ) -> "MyDraws":
        """获取我的画片

        Args:
            client (GenshinClient): 原神客户端
            page_size (int, optional): 每页数量. Defaults to 2.
            draw_collection_type (int, optional): 画片类型. Defaults to 0.
            draw_collection_operate (int, optional): 画片类型. Defaults to 4.
                4: 已收集
                5: 未收集
                6: 全部
            page (int, optional): 页码. Defaults to 0.

        Returns:
            MyDraws: 我的画片
        """
        params = {
            "badge_uid": client.player_id,
            "badge_region": recognize_genshin_server(client.player_id),
            "game_biz": recognize_genshin_game_biz(client.player_id),
            "lang": "zh-cn",
            "channel": "CHL_APP",
            "activity_id": "20220301153521",
            "page_size": page_size,
            "draw_collection_type": draw_collection_type,
            "draw_collection_operate": draw_collection_operate,
        }
        if page:
            params.update({
                "is_page": "true",
                "page": page,
            })
        data = await client.request_lab(DRAW_COLLECTION_API.get_url(), method="GET", params=params)
        return MyDraws(**data)
