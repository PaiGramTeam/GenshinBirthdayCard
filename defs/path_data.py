import json
from pathlib import Path

from defs.config import GENSHIN_GENDER_BOY
from defs.json_data import get_draws

FILE_PATH = Path("files")
FILE_PATH_BOY = FILE_PATH / "aether"
FILE_PATH_GIRL = FILE_PATH / "lumine"


async def create_path_data():
    draws = await get_draws()
    path = FILE_PATH_BOY if GENSHIN_GENDER_BOY else FILE_PATH_GIRL
    data = {}
    role_birthdays = {}
    for draw in draws:
        year, month = str(draw.year), str(draw.month)
        if year not in data:
            data[year] = {}
        if month not in data[year]:
            data[year][month] = []
        data[year][month].append(
            {
                "role_name": draw.role_name,
                "day": draw.day,
                "ext": draw.ext,
                "unread_ext": draw.unread_ext,
            }
        )
        if draw.role_name not in role_birthdays:
            role_birthdays[draw.role_name] = [[draw.year, draw.month, draw.day]]
        else:
            role_birthdays[draw.role_name].append([draw.year, draw.month, draw.day])
    role_birthdays = dict(sorted(role_birthdays.items(), key=lambda x: x[0]))
    with open(path / "birthday.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(path / "role_birthday.json", "w", encoding="utf-8") as f:
        json.dump(role_birthdays, f, ensure_ascii=False, indent=4)
