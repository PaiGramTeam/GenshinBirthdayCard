from pathlib import Path

from tqdm import tqdm

from defs.client import download
from defs.config import GENSHIN_GENDER_BOY
from defs.json_data import get_draws

FILE_PATH = Path("files")
FILE_PATH_BOY = FILE_PATH / "aether"
FILE_PATH_GIRL = FILE_PATH / "lumine"


async def download_images():
    draws = await get_draws()
    path = FILE_PATH_BOY if GENSHIN_GENDER_BOY else FILE_PATH_GIRL
    for draw in tqdm(draws):
        temp_path = path / str(draw.year) / str(draw.month)
        temp_path.mkdir(parents=True, exist_ok=True)
        await download(draw.take_picture, temp_path / f"{draw.role_name}.{draw.ext}")
        await download(draw.unread_picture, temp_path / f"{draw.role_name}_unread.{draw.unread_ext}")
