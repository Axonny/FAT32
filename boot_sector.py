from typing import BinaryIO


class Boot:

    def __init__(self, io: BinaryIO):
        io.read(3 + 8)
        self.size_sector = int.from_bytes(io.read(2), "little")
        self.sectors_in_cluster = int.from_bytes(io.read(1), "little")
        self.boot_size = int.from_bytes(io.read(2), "little")
        self.count_fat_table = int.from_bytes(io.read(1), "little")
        int.from_bytes(io.read(2), "little")
        self.count_sectors = int.from_bytes(io.read(2), "little")
        int.from_bytes(io.read(1 + 2 + 2 + 2), "little")
        self.absolute_number = int.from_bytes(io.read(4), "little")
        if self.count_sectors == 0:
            self.count_sectors = int.from_bytes(io.read(4), "little")
        else:
            int.from_bytes(io.read(4), "little")
        self.size_fat = int.from_bytes(io.read(4), "little")
        self.number_main_fat_table = int.from_bytes(io.read(2), "little")
        self.version_fat = int.from_bytes(io.read(2), "little")
        self.first_cluster = io.read(4)
        self.first_cluster_int = int.from_bytes(self.first_cluster, "little")
        self.number_of_FSINFO = int.from_bytes(io.read(2), "little")
        int.from_bytes(io.read(2 + 12 + 1 + 1 + 1), "little")
        self.date = int.from_bytes(io.read(4), "little")
        self.mark = io.read(11)
        self.a_file_sys = io.read(8)



