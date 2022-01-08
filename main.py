from boot_sector import Boot
from fat_table import FatTable
from file_description import FileDescriptor
from cui import ExplorerWindow


def initialize(filename: str):
    with open(filename, "rb") as f:
        f.seek(65536)
        boot = Boot(f)
        f.seek(int(boot.address_fat_table, 16))
        fat = FatTable(boot.size_fat, f)
        lst = get_list(f, boot, fat, 2)
        filtered = list(filter(lambda x: x.attrs != 8, lst))
        tom = next(filter(lambda x: x.attrs == 8, lst))
        window = ExplorerWindow(tom.get_name(), filtered)
        window.callback = find_folder(f, boot, fat, window)
        window.start()

    return boot, fat


def find_folder(f, boot, fat, window):
    def wrapper(elem: FileDescriptor):
        print(elem)
        if elem.attrs & FileDescriptor.DIRECTORY_FLAGS:
            list_dir = get_list(f, boot, fat, elem.cluster_address or 2)
            print(list_dir)
            window.replace_list(list_dir)
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


def main():
    boot, fat = initialize("gpt.vhd")


if __name__ == "__main__":
    main()
