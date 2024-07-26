import json
from pathlib import Path
from typing import TypeVar, Tuple, List, Union, Type, Dict

import aiofiles
from xml.dom.minidom import parse, Element

from tqdm import tqdm

from defs.client import download
from defs.json_data import get_draws
from defs.models import ResourceCharacter, ResourceBg, GalCharacter, Scene, SceneItem

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
gathers = ["aether", "lumine"]
T = TypeVar("T")


def xml_to_json_model(model_class: Type[T], data: "Element", extra: Dict = None) -> T:
    data_json = extra or {}
    data_json["type"] = data.nodeName
    for k, v in data.attributes.items():
        data_json[k] = v
    if data.nodeName == "simple_dialog":
        data_json["content"] = data.firstChild.nodeValue
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


async def get_resources_json() -> Tuple[List[ResourceCharacter], List[ResourceBg], List[GalCharacter]]:
    async with aiofiles.open(RES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.loads(await f.read())
    chara_json = [ResourceCharacter(**c) for c in data["chara"]]
    bg_json = [ResourceBg(**b) for b in data["bg"]]
    characters_json = [GalCharacter(**c) for c in data["c"]]
    return chara_json, bg_json, characters_json


async def scene_xml_to_json(file_path: Path, bg: Dict[str, ResourceBg], chara: Dict[str, ResourceCharacter]):
    tree = parse(str(file_path))
    data = tree.documentElement
    scenes = data.getElementsByTagName("scene")
    scene_data = []
    for scene in scenes:
        items = []
        for item in scene.childNodes:
            if isinstance(item, Element):
                scene_item = xml_to_json_model(SceneItem, item)
                if scene_item.type == "bg" and scene_item.img:
                    if bg_ := bg.get(scene_item.img):
                        scene_item.ext = bg_.ext
                if scene_item.type == "simple_dialog" and scene_item.img:
                    if ch_ := chara.get(scene_item.img):
                        scene_item.src = ch_.src_os or ch_.src
                items.append(scene_item)
        scene_model = xml_to_json_model(Scene, scene, {"items": items})
        scene_data.append(scene_model)
    async with aiofiles.open(file_path.with_suffix(".json"), "w", encoding="utf-8") as f:
        await f.write(json.dumps([i.dict() for i in scene_data], ensure_ascii=False, indent=4))


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


async def convert_dialog_xml_json():
    chara_json, bg, _ = await get_resources_json()
    bg_map = {b.id: b for b in bg}
    chara_map = {c.id: c for c in chara_json}
    for gather in gathers:
        path = FILE_PATH / gather / "birthday.json"
        if not path.exists():
            continue
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            data = json.loads(await f.read())
        for year, v in data.items():
            for month, v2 in v.items():
                for role in v2:
                    role_name = role["role_name"]
                    xml_path = FILE_PATH / gather / year / month / f"{role_name}.xml"
                    if not xml_path.exists():
                        continue
                    await scene_xml_to_json(xml_path, bg_map, chara_map)
