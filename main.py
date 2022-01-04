from boot_sector import Boot
from fat_table import FatTable


def initialize(filename: str):
    with open(filename, "rb") as f:
        f.seek(65536)
        boot = Boot(f)
        f.seek(int(boot.address_fat_table, 16))
        fat = FatTable(boot.size_fat, f)

    return boot, fat


def main():
    boot, fat = initialize("gpt.vhd")
    print(fat.get_next_cluster_number(0))


if __name__ == "__main__":
    main()
