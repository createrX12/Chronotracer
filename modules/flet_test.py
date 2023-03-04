# coding=utf-8
"""
@author B1lli
@date 2023年02月25日 18:51:17
@File:flet_test.py
"""

import flet as ft
import time
import datetime
from flet_core import dropdown
from flet import Dropdown,UserControl,Container,Row,Icon,icons
class DateSelector(UserControl):
    """Date selector."""

    def __init__(self):
        super().__init__()

        self.day_dropdown = Dropdown(
            label="D",
            options=[
                dropdown.Option(day) for day in range (1, 32)
            ],
            width=50,
        )

        self.month_dropdown = Dropdown(
            label="M",
            options=[
                dropdown.Option(month) for month in range (1, 13)
            ],
            width=50,
        )

        self.year_dropdown = Dropdown(
            label="Y",
            options=[
                dropdown.Option(year) for year in range (2015, 2025)
            ],
            width=100,
        )


        self.view = Container(
            content=Row(
                [
                    Icon(
                        icons.CALENDAR_MONTH,
                    ),
                    self.day_dropdown,
                    self.month_dropdown,
                    self.year_dropdown,
                ],
                alignment="center",
            ),
            padding=10,
        )

    def build(self):
        return self.view

    def get_date(self) -> datetime.date:
        """Return the selected timeframe.
        :rtype: object
        """
        date = datetime.date(
            year=int(self.year_dropdown.value),
            month=int(self.month_dropdown.value),
            day=int(self.day_dropdown.value),
        )
        return date


def main(page: ft.Page):
    # t = ft.Text ( value="Hello, world!", color="green" )
    # page.add(t)

    # t = ft.Text ()
    # page.add (# it's a shortcut for page.controls.append(t) and then page.update()
    #     ft.Row ( controls=[
    #         ft.Text ( "A" ),
    #         ft.Text ( "B" ),
    #         ft.Text ( "C" ),
    #         t,
    #         ft.TextField ( label="Your name" ),
    #         ft.ElevatedButton ( text="Say my name!" )
    #     ] )
    # )
    # for i in range ( 10 ) :
    #     t.value = f"Step {i}"
    #     page.update ()
    #     time.sleep ( 0.5 )

    page.title = '溯时计'
    d = DateSelector()
    page.add(d)



    def button_clicked(e) :
        page.add ( ft.Text(d.get_date()) )

    page.add ( ft.ElevatedButton ( text="Click me", on_click=button_clicked ) )


    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        new_task.focus()
        new_task.update()

    new_task = ft.TextField(hint_text="Whats needs to be done?", width=300)
    page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))



    # first_name = ft.TextField(label="First name", autofocus=True)
    # last_name = ft.TextField(label="Last name")
    # greetings = ft.Column()
    #
    # def btn_click(e):
    #     greetings.controls.append(ft.Text(f"Hello, {first_name.value} {last_name.value}!"))
    #     first_name.value = ""
    #     last_name.value = ""
    #     page.update()
    #     first_name.focus()
    #
    # page.add(
    #     first_name,
    #     last_name,
    #     ft.ElevatedButton("Say hello!", on_click=btn_click),
    #     greetings,
    # )
    first_name = ft.Ref[ft.TextField]()
    last_name = ft.Ref[ft.TextField]()
    greetings = ft.Ref[ft.Column]()

    def btn_click(e):
        greetings.current.controls.append(
            ft.Text(f"Hello, {first_name.current.value} {last_name.current.value}!")
        )
        first_name.current.value = ""
        last_name.current.value = ""
        page.update()
        first_name.current.focus()

    page.add(
        ft.TextField(ref=first_name, label="First name", autofocus=True),
        ft.TextField(ref=last_name, label="Last name"),
        ft.ElevatedButton("Say hello!", on_click=btn_click),
        ft.Column(ref=greetings),
    )



if __name__ == '__main__':
    ft.app ( target=main )