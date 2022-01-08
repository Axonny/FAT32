from boot_sector import Boot
from fat_table import FatTable
from file_description import FileDescriptor


def initialize(filename: str):
    with open(filename, "rb") as f:
        f.seek(65536)
        boot = Boot(f)
        f.seek(int(boot.address_fat_table, 16))
        fat = FatTable(boot.size_fat, f)
        list = get_list(f, boot, fat, 2)


    return boot, fat


def get_list(f, boot, fat, start_cluster):
    list = []
    while True:
        n_ = int(boot.address_first_data_cluster, 16) + (start_cluster - 2) * 512 // 32
        f.seek(n_)
        for i in range(16):
            fd = FileDescriptor(f)
            if fd.empty:
                return list
            else:
                list.append(fd)
        if (start_cluster := fat.get_next_cluster_number(start_cluster)) is None:
            return list


def main():
    boot, fat = initialize("gpt.vhd")
    print(fat.get_next_cluster_number(0))


if __name__ == "__main__":
    main()
