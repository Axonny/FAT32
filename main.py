from boot_sector import Boot
from fat_table import FatTable
from file_description import FileDescriptor
from cui import ExplorerWindow, NotepadWindow


def find_folder(f, boot, fat, window):
    def wrapper(elem: FileDescriptor):
        if elem.attrs & FileDescriptor.DIRECTORY_FLAGS:
            list_dir = get_list(f, boot, fat, elem.cluster_address or 2)
            window.replace_list(list_dir)
        else:
            window.close()
            notepad = NotepadWindow(elem.get_name())
            try:
                notepad.set_text(get_file(f, boot, fat, elem.cluster_address).decode('utf-8'))
                notepad.start()
            except UnicodeDecodeError:
                window.view.show_error_popup("Reader error", "Can't open this file")
                window.view.move_focus(window.explorer_scroll_menu)
            window.start()
    return wrapper


def get_list(f, boot, fat, start_cluster):
    lst = []
    while True:
        n_ = int(boot.address_first_data_cluster, 16) + (start_cluster - 2) * boot.size_sector * boot.sectors_in_cluster
        f.seek(n_)
        i = 0
        while i < 16:
            fd = FileDescriptor(f)
            i += fd.count
            if fd.empty:
                return lst
            else:
                lst.append(fd)
        if (start_cluster := fat.get_next_cluster_number(start_cluster)) is None:
            return lst


def get_file(f, boot, fat, start_cluster):
    ans = bytes()
    while True:
        n_ = int(boot.address_first_data_cluster, 16) + (start_cluster - 2) * boot.size_sector * boot.sectors_in_cluster
        f.seek(n_)
        ans += f.read(boot.sectors_in_cluster * boot.size_sector)
        if (start_cluster := fat.get_next_cluster_number(start_cluster)) is None:
            return ans


def main():
    with open("gpt.vhd", "rb") as f:
        f.seek(65536)
        boot = Boot(f)
        f.seek(int(boot.address_fat_table, 16))
        fat = FatTable(boot.size_fat * boot.sectors_in_cluster * boot.size_sector // 4, f)
        lst = get_list(f, boot, fat, 2)
        filtered = list(filter(lambda x: x.attrs != 8, lst))
        tom = next(filter(lambda x: x.attrs == 8, lst))
        window = ExplorerWindow(tom.get_name(), filtered)
        window.callback = find_folder(f, boot, fat, window)
        window.start()


if __name__ == "__main__":
    main()
