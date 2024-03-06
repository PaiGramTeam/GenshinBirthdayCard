import random
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import aiofiles
from dateutil.relativedelta import relativedelta
from jinja2 import FileSystemLoader, Environment

from .config import DOMAIN
from .models import PagePost, PageRole

loader = FileSystemLoader("templates")
env = Environment(loader=loader)
template = env.get_template("month.jinja2")
genders = ["aether", "lumine"]
FILE_PATH = Path("files")


def get_related_posts(gender: str, year: str, month: str) -> List[PagePost]:
    year = int(year)
    month = int(month)
    current_date = datetime(year, month, 1)
    dates = []
    for i in range(-3, 3):
        if i == 0:
            continue
        date = current_date + relativedelta(months=i)
        dates.append(date)
    url_path = f"{DOMAIN}/{gender}"
    return [
        PagePost(
            url=f"{url_path}/{date.strftime('%Y')}/{int(date.strftime('%m'))}/",
            title=date.strftime("%Y 年 %m 月 - 留影叙佳期 - PaiGramTeam"),
        ) for date in dates
        if (FILE_PATH / gender / date.strftime('%Y') / str(int(date.strftime('%m')))).exists()
    ]


def get_year_posts(gender: str, year: str) -> List[PagePost]:
    year = int(year)
    dates = [datetime(year, i, 1) for i in range(1, 13)]
    url_path = f"{DOMAIN}/{gender}"
    return [
        PagePost(
            url=f"{url_path}/{date.strftime('%Y')}/{int(date.strftime('%m'))}/",
            title=date.strftime("%Y 年 %m 月 - 留影叙佳期 - PaiGramTeam"),
            short_title=date.strftime("%Y 年 %m 月 - 留影叙佳期"),
            is_single_page=True,
        ) for date in dates
        if (FILE_PATH / gender / date.strftime('%Y') / str(int(date.strftime('%m')))).exists()
    ]


def get_gender_posts(gender: str, year: List[str]) -> List[PagePost]:
    year = [int(i) for i in year]
    url_path = f"{DOMAIN}/{gender}"
    return [
        PagePost(
            url=f"{url_path}/{y}/",
            title=f"{y} 年 - 留影叙佳期 - PaiGramTeam",
            short_title=f"{y} 年 - 留影叙佳期",
            is_single_page=True,
        ) for y in year
    ]


def get_files_posts() -> List[PagePost]:
    name_map = {"aether": "空（男主）", "lumine": "荧（女主）"}
    return [
        PagePost(
            url=f"{DOMAIN}/{gender}/",
            title=f"{name_map[gender]} - 留影叙佳期 - PaiGramTeam",
            short_title=f"{name_map[gender]} - 留影叙佳期",
            is_single_page=True,
        ) for gender in genders
    ]


async def get_scene_map(gender: str, year: str, month: str, roles: List[str]) -> Dict[str, List]:
    file_path = FILE_PATH / gender / year / month
    scene_map = {}
    for role in roles:
        path = file_path / f"{role}.json"
        if not path.exists():
            continue
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            scene_map[role] = json.loads(await f.read())
    return scene_map


async def create_month_html(gender: str, year: str, month: str, datas: List[Dict[str, str]]):
    url_path = f"{DOMAIN}/{gender}/{year}/{month}"
    file_path = FILE_PATH / gender / year / month
    post = PagePost(url=f"{url_path}/index.html")
    roles = []
    for data in datas:
        role_name = data["role_name"]
        roles.append(
            PageRole(
                role_name=role_name,
                day_str=f"{data['day']} 日",
                src=f"{url_path}/{role_name}.{data['ext']}",
                src_unread=f"{url_path}/{role_name}_unread.{data['unread_ext']}",
            )
        )
    scene_map = await get_scene_map(gender, year, month, [role.role_name for role in roles])
    post.cover = random.Random().choice([role.src for role in roles])
    related_posts = get_related_posts(gender, year, month)
    html = template.render(
        post=post.dict(),
        roles=[i.dict() for i in roles],
        scene_map=scene_map,
        related_posts=[i.dict() for i in related_posts],
        published_time=f"{year}-{month}-01T00:00:00+08:00",
        month=f"{year} 年 {month} 月",
        DOMAIN=DOMAIN,
    )
    file_path.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(file_path / "index.html", "w", encoding="utf-8") as f:
        await f.write(html)


async def create_year_html(gender: str, year: str):
    url_path = f"{DOMAIN}/{gender}/{year}"
    file_path = FILE_PATH / gender / year
    post = PagePost(url=f"{url_path}/index.html", cover=f"{DOMAIN}/bg.png")
    related_posts = get_year_posts(gender, year)
    html = template.render(
        post=post.dict(),
        related_posts=[i.dict() for i in related_posts],
        published_time=f"{year}-12-31T00:00:00+08:00",
        month=f"{year} 年"
    )
    file_path.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(file_path / "index.html", "w", encoding="utf-8") as f:
        await f.write(html)


async def create_gender_html(gender: str, years: List[str]):
    url_path = f"{DOMAIN}/{gender}"
    file_path = FILE_PATH / gender
    post = PagePost(url=f"{url_path}/index.html", cover=f"{DOMAIN}/bg.png")
    related_posts = get_gender_posts(gender, years)
    html = template.render(
        post=post.dict(),
        related_posts=[i.dict() for i in related_posts],
        published_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        month="空（男主）" if gender == "aether" else "荧（女主）"
    )
    file_path.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(file_path / "index.html", "w", encoding="utf-8") as f:
        await f.write(html)


async def create_files_html():
    post = PagePost(url=f"{DOMAIN}/telegram.html", cover=f"{DOMAIN}/bg.png")
    related_posts = get_files_posts()
    html = template.render(
        post=post.dict(),
        related_posts=[i.dict() for i in related_posts],
        published_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        month="米游社"
    )
    async with aiofiles.open(FILE_PATH / "telegram.html", "w", encoding="utf-8") as f:
        await f.write(html)


async def create_month_htmls():
    for gender in genders:
        file_path = FILE_PATH / gender / "birthday.json"
        if not file_path.exists():
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for year, months in data.items():
            for month, datas in months.items():
                await create_month_html(gender, year, month, datas)
            await create_year_html(gender, year)
        await create_gender_html(gender, list(data.keys()))
    await create_files_html()
