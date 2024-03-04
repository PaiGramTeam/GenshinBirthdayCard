from typing import List

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
