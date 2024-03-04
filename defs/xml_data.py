import json
from pathlib import Path

import aiofiles
from httpx import AsyncClient
from xml.dom.minidom import parse, Element

from defs.json_data import get_draws
from defs.models import ResourceCharacter, ResourceBg, GalCharacter

FILE_PATH = Path("files")
RESOURCE_PATH = FILE_PATH / "resource"
RES_XML_PATH = RESOURCE_PATH / "resources.xml"
RES_JSON_PATH = RESOURCE_PATH / "resources.json"
FILE_PATH_BOY = FILE_PATH / "aether"
FILE_PATH_GIRL = FILE_PATH / "lumine"
client = AsyncClient(timeout=60.0)


async def download(url: str, path: Path):
    async with client.stream("GET", url) as response:  # noqa
        async with aiofiles.open(path, "wb") as f:
            async for chunk in response.aiter_bytes():
                await f.write(chunk)


def xml_to_json_model(model_class, data: "Element"):
    data_json = {}
    for k, v in data.attributes.items():
        data_json[k] = v
    return model_class(**data_json)


async def xml_to_json():
    tree = parse(str(RES_XML_PATH))
    data = tree.documentElement
    chara = data.getElementsByTagName("chara")
    bg = data.getElementsByTagName("bg")
    characters = data.getElementsByTagName("c")
    chara_json = [xml_to_json_model(ResourceCharacter, c) for c in chara]
    bg_json = [xml_to_json_model(ResourceBg, b) for b in bg]
    characters_json = [xml_to_json_model(GalCharacter, c) for c in characters]
    all_data = {
        "chara": [i.dict() for i in chara_json],
        "bg": [i.dict() for i in bg_json],
        "c": [i.dict() for i in characters_json],
    }
    async with aiofiles.open(RES_JSON_PATH, "w", encoding="utf-8") as f:
        await f.write(json.dumps(all_data, ensure_ascii=False, indent=4))


async def download_resources():
    draws = await get_draws()
    draw = draws[0]
    await download(draw.gal_resource, RES_XML_PATH)
    await xml_to_json()
