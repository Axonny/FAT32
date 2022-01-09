from os import path, mkdir
from boot_sector import Boot
from fat_table import FatTable
from file_description import FileDescriptor
from cui import ExplorerWindow, NotepadWindow
from stream import FatStream


def find_folder(f, boot, fat, window):
    def wrapper(elem: FileDescriptor):
        if elem.attrs & FileDescriptor.DIRECTORY_FLAGS:
            list_dir = get_list(f, boot, fat, elem.cluster_address or 2)
            filtered = list(filter(lambda x: x.attrs != 8, list_dir))
            window.replace_list(filtered)
        else:
            window.close()
            notepad = NotepadWindow(elem.get_name())
            try:
                print(hex(elem.cluster_address))
                notepad.set_text(get_file(f, boot, fat, elem.cluster_address).decode('utf-8'))
                notepad.start()
            except UnicodeDecodeError:
                window.view.show_error_popup("Reader error", "Can't open this file")
                window.view.move_focus(window.explorer_scroll_menu)
            window.start()
    return wrapper


def save_to_user(f, boot, fat):
    def wrapper(elem: FileDescriptor, p: str = "./"):
        p = path.normpath(p)
        if elem.attrs & FileDescriptor.DIRECTORY_FLAGS:
            if not path.exists(path.join(p, elem.get_name())):
                mkdir(path.join(p, elem.get_name()))
            lst = get_list(f, boot, fat, elem.cluster_address)
            for next_elem in lst:
                if next_elem.get_name() not in ['.', '..']:
                    wrapper(next_elem, path.join(p, elem.get_name()))
        else:
            _bytes = get_file(f, boot, fat, elem.cluster_address)
            with open(path.join(p, elem.get_name()), 'wb') as file:
                file.write(_bytes)
    return wrapper


def get_list(f, boot, fat, start_cluster):
    lst = []
    fat_stream = FatStream(boot, fat, f, start_cluster)
    while True:
        i = 0
        while i < 16:
            fd = FileDescriptor(fat_stream)
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
        window.save = save_to_user(f, boot, fat)
        window.start()


if __name__ == "__main__":
    main()
