import json
from asyncio import sleep
from pathlib import Path
from typing import List

import aiofiles
from tqdm import tqdm

from defs.config import GENSHIN_GENDER_BOY
from defs.client import client
from defs.birthday_card import BirthdayCard
from defs.models import MyDraw

FILE_PATH = Path("files")
FILE_PATH_BOY = FILE_PATH / "aether"
FILE_PATH_GIRL = FILE_PATH / "lumine"
FILE_PATH.mkdir(exist_ok=True)
FILE_PATH_BOY.mkdir(exist_ok=True)
FILE_PATH_GIRL.mkdir(exist_ok=True)


async def get_my_draws() -> List["MyDraw"]:
    draws = []
    i = 1
    if "e_hk4e_token" not in client.cookies:
        await BirthdayCard.get_hk4e_token(client)
    data = await BirthdayCard.get_my_draws(client, page=i)
    draws.extend(data.my_draws)
    for i in tqdm(range(2, data.total_page + 1)):
        await sleep(.5)
        data = await BirthdayCard.get_my_draws(client, page=i)
        draws.extend(data.my_draws)
    return draws


async def get_draws(gender_boy: bool = True) -> List["MyDraw"]:
    data = []
    path = FILE_PATH_BOY if gender_boy else FILE_PATH_GIRL
    async with aiofiles.open(path / "my_draws.json", "r", encoding="utf-8") as f:
        for d in json.loads(await f.read()):
            data.append(MyDraw(**d))
    return data


async def save_raw_jsons():
    path = FILE_PATH_BOY if GENSHIN_GENDER_BOY else FILE_PATH_GIRL
    file_path = path / "my_draws.json"
    if file_path.exists():
        return
    draws = await get_my_draws()
    data = [draw.dict() for draw in draws if draw.take_picture]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
