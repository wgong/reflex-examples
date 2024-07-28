"""
Welcome to Reflex: ToDo app 
"""

import reflex as rx
from rxconfig import config

src_path = f"{config.app_name}/{config.app_name}.py"
src_code = open(src_path).read()

class State(rx.State):
    """The app state."""

    # The current items in the todo list.
    items = ["Write Code", "Sleep", "Have Fun"]

    def add_item(self, form_data: dict[str, str]):
        """Add a new item to the todo list."""
        new_item = form_data.get("new_item")
        if new_item:
            self.items.append(new_item)

    def finish_item(self, item: str):
        """Finish an item in the todo list.

        Args:
            item: The item to finish.
        """
        self.items.pop(self.items.index(item))


def todo_item(item: rx.Var[str]) -> rx.Component:
    """Render an item in the todo list.

    NOTE: When using `rx.foreach`, the item will be a Var[str] rather than a str.

    Args:
        item: The todo list item.

    Returns:
        A single rendered todo list item.
    """
    return rx.list_item(
        # A button to finish the item.
        rx.hstack(
            rx.icon_button(
                rx.icon(tag="check"),
                on_click=lambda: State.finish_item(item),
                margin_y="0.5em",
                variant="outline",
            ),
            # The item text.
            rx.text(item, as_="span"),
            align="center",
        ),
        class_name="list-none",
    )


def todo_list() -> rx.Component:
    """Render the todo list.

    Returns:
        The rendered todo list.
    """
    return rx.ordered_list(
        # rx.foreach is necessary to iterate over state vars.
        # see: https://reflex.dev/docs/library/layout/foreach
        rx.foreach(State.items, lambda item: todo_item(item)),
    )


def new_item() -> rx.Component:
    """Render the new item form.

    See: https://reflex.dev/docs/library/forms/form

    Returns:
        A form to add a new item to the todo list.
    """
    return rx.form(
        rx.hstack(
            rx.input.root(
                rx.input(
                    name="new_item",
                    placeholder="Add a todo...",
                    # bg="white",
                ),
                width="100%",
            ),
            rx.button("Add"),
        ),
        on_submit=State.add_item,
        reset_on_submit=True,
        width="100%",
    )



def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="6"),
            rx.text(
                "Get started by editing ",
                rx.code(src_path),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            # min_height="85vh",
        ),
        rx.divider(),
        rx.center(
            rx.vstack(
                rx.heading("Todos"),
                new_item(),
                rx.divider(),
                todo_list(),
                bg=rx.color("gray", 7),
                margin_top="3em",
                margin_x="25vw",
                padding="1em",
                border_radius="0.5em",
                spacing="3",
            ),
        ),
        rx.divider(),
        rx.heading(f"Source code: '{src_path}'", size="4"),
        rx.markdown("```python" + "\n" + src_code + '```'),
        rx.divider(),
        rx.logo(),
    )

# Create the app and add the state.
app = rx.App()
# Add the index page and set the title.
app.add_page(index, title="Todo App")
