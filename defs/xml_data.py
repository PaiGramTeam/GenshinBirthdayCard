import json
from pathlib import Path
from typing import TypeVar, Tuple, List, Union, Type

import aiofiles
from xml.dom.minidom import parse, Element

from tqdm import tqdm

from defs.client import download
from defs.json_data import get_draws
from defs.models import ResourceCharacter, ResourceBg, GalCharacter

FILE_PATH = Path("files")
RESOURCE_PATH = FILE_PATH / "resource"
RESOURCE_PATH.mkdir(exist_ok=True)
RES_XML_PATH = RESOURCE_PATH / "resources.xml"
RES_JSON_PATH = RESOURCE_PATH / "resources.json"
RESOURCE_CHARA_PATH = RESOURCE_PATH / "chara"
RESOURCE_BG_PATH = RESOURCE_PATH / "bg"
RESOURCE_CHARA_PATH.mkdir(exist_ok=True)
RESOURCE_BG_PATH.mkdir(exist_ok=True)
FILE_PATH_BOY = FILE_PATH / "aether"
FILE_PATH_GIRL = FILE_PATH / "lumine"
T = TypeVar("T")


def xml_to_json_model(model_class: Type[T], data: "Element") -> T:
    data_json = {}
    for k, v in data.attributes.items():
        data_json[k] = v
    return model_class(**data_json)


async def xml_to_json() -> Tuple[List[ResourceCharacter], List[ResourceBg], List[GalCharacter]]:
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
    return chara_json, bg_json, characters_json


async def download_images(data: List[Union[ResourceCharacter, ResourceBg]]):
    for d in tqdm(data):
        if isinstance(d, ResourceCharacter):
            path = RESOURCE_CHARA_PATH / f"{d.id}.{d.ext}"
        else:
            path = RESOURCE_BG_PATH / f"{d.id}.{d.ext}"
        await download(d.src, path)


async def download_resources():
    draws = await get_draws()
    draw = draws[-1]
    await download(draw.gal_resource, RES_XML_PATH, override=True)
    chara_json, bg_json, _ = await xml_to_json()
    await download_images(chara_json)
    await download_images(bg_json)
