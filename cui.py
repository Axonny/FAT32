from py_cui import PyCUI, GREEN_ON_BLACK, YELLOW_ON_BLACK, keys
from os import path


class ExplorerWindow:
    def __init__(self, start_list: list[str]):
        self.view = PyCUI(10, 10)
        self.view.toggle_unicode_borders()
        self.view.set_title("FAT32 Explorer")
        self.explorer_scroll_menu = None

        self.create_ui_content()
        self.replace_list(start_list)
        self.view.start()

    def create_ui_content(self):
        title = path.normpath("/")
        self.explorer_scroll_menu = self.view.add_scroll_menu(title, 0, 0, row_span=10, column_span=10)
        self.explorer_scroll_menu.add_key_command(keys.KEY_ENTER, self.select)
        self.explorer_scroll_menu.add_text_color_rule("Mounted at", YELLOW_ON_BLACK, "contains")
        self.explorer_scroll_menu.set_selected_color(GREEN_ON_BLACK)

        self.view.move_focus(self.explorer_scroll_menu)

    def replace_list(self, elements: list[str]):
        self.clear_list()
        self.explorer_scroll_menu.add_item_list(elements)

    def clear_list(self):
        self.explorer_scroll_menu.clear()

    def close(self):
        if self.view is None:
            return
        self.view.stop()

    def select(self):
        name = self.explorer_scroll_menu.get()
        title = self.explorer_scroll_menu.get_title()
        title = path.join(title, name)
        title = path.normpath(title)
        self.explorer_scroll_menu.set_title(title)
        # self.replace_list(['.', '..', *map(str, range(1, 10))])


if __name__ == '__main__':
    ExplorerWindow()
