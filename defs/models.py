from typing import List, Optional

from pydantic import BaseModel


class MyDraw(BaseModel):
    draw_status: str
    take_picture: str
    unread_picture: str
    word_text: str
    year: int
    birthday: str
    is_new: bool
    role_id: int
    gal_xml: str
    gal_resource: str
    is_collected: bool
    op_id: int
    is_compensate: bool
    role_name: str

    @property
    def month(self) -> int:
        return int(self.birthday.split("/")[0])

    @property
    def day(self) -> int:
        return int(self.birthday.split("/")[1])

    @property
    def ext(self) -> str:
        return self.take_picture.split(".")[-1]

    @property
    def unread_ext(self) -> str:
        return self.unread_picture.split(".")[-1]


class MyDraws(BaseModel):
    my_draws: List[MyDraw]
    current_page: int
    total_page: int
    draw_notice: bool
    is_finish_task: bool
    guide_task: bool
    guide_compensate: bool
    guide_draw: bool
    current_compensate_num: int
    is_compensate_num: bool
    year_compensate_num: int


class ResourceCharacter(BaseModel):
    src: str
    src_os: str
    id: str
    rel: Optional[str] = ""
    group: Optional[str] = ""

    @property
    def ext(self) -> str:
        return self.src.split(".")[-1]


class ResourceBg(BaseModel):
    src: str
    src_os: str
    id: str
    group: Optional[str] = ""

    @property
    def ext(self) -> str:
        return self.src.split(".")[-1]


class GalCharacter(BaseModel):
    id: str
    name: str
    key: Optional[str] = ""


class PagePost(BaseModel, frozen=False):
    url: str
    title: Optional[str] = ""
    cover: Optional[str] = ""


class PageRole(BaseModel):
    role_name: str
    day: int
    src: str
    src_unread: str

    @property
    def day_str(self) -> str:
        return f"{self.day} 日"
