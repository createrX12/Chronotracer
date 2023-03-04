# coding=utf-8
"""
@author B1lli
@date 2023年02月25日 16:30:00
@File:flet_interface.py
"""
import flet as ft

import datetime
from flet_core import dropdown
from flet import Dropdown, UserControl, Container, Row, Icon, icons, Text


class DateSelector ( UserControl ) :
    """Date selector."""

    def __init__(self) :
        super ().__init__ ()

        self.day_dropdown = Dropdown (
            label="D",
            options=[
                dropdown.Option ( day ) for day in range ( 1, 32 )
            ],
            width=50,
        )

        self.month_dropdown = Dropdown (
            label="M",
            options=[
                dropdown.Option ( month ) for month in range ( 1, 13 )
            ],
            width=50,
        )

        self.year_dropdown = Dropdown (
            label="Y",
            options=[
                dropdown.Option ( year ) for year in range ( 2015, 2025 )
            ],
            width=100,
        )

        self.view = Container (
            content=Row (
                [
                    Text ( '请选择搜索日期' ),
                    Icon (
                        icons.CALENDAR_MONTH,
                    ),
                    self.day_dropdown,
                    self.month_dropdown,
                    self.year_dropdown,
                ],
                alignment="left",
            ),
            padding=10,
        )

    def build(self) :
        return self.view

    def get_date(self) -> datetime.date :
        """Return the selected timeframe.
        :rtype: object
        """
        try :
            date = datetime.date (
                year=int ( self.year_dropdown.value ),
                month=int ( self.month_dropdown.value ),
                day=int ( self.day_dropdown.value ),
            )
            return date
        except TypeError :
            self.day_dropdown.error_text = "请输入查询日期"


from modules.search import search_pic


def main(page: ft.Page) :
    # 设置字体
    page.fonts = {
        'A75方正像素12' : '../assets/A75方正像素12.ttf'
    }
    page.theme = ft.Theme ( font_family='A75方正像素12' )
    page.dark_theme = page.theme

    # 当搜索按钮被按下时
    def search_button_clicked(e) :
        if not date_selector.get_date () :
            date_selector.error_text = "请输入查询日期"
            page.update ()
        elif not search_text.value :
            search_text.error_text = '请输入查询文字'
            page.update ()
        else :
            date_text = date_selector.get_date ()
            search_pic(search_text.value,date_text)


    date_selector = DateSelector ()
    search_text = ft.TextField ( label="输入查找文本" )

    page.add ( date_selector, search_text, ft.ElevatedButton ( "开始搜索", on_click=search_button_clicked ) )


ft.app ( target=main, assets_dir='../assets' )
