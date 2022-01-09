from boot_sector import Boot
from fat_table import FatTable
from typing import BinaryIO


class FatStream:

    def __init__(self, boot: Boot, fat: FatTable, f: BinaryIO, start_cluster_num):
        self.boot = boot
        self.fat = fat
        self.f = f
        self.start = start_cluster_num
        self.full = None
        self.pointer = 0

    def read(self, n: int = 512) -> bytes:
        if self.full is None:
            self.full = self._full_read()
        ans = self.full[self.pointer: self.pointer + n]
        self.pointer += n
        return ans

    def _full_read(self):
        self.f.seek(self.calc_address(self.start))
        start_cluster = self.start
        ans = bytes()
        while True:
            n_ = self.calc_address(start_cluster)
            self.f.seek(n_)
            ans += self.f.read(self.boot.sectors_in_cluster * self.boot.size_sector)
            if (start_cluster := self.fat.get_next_cluster_number(start_cluster)) is None:
                return ans

    def calc_address(self, num: int):
        return int(self.boot.address_first_data_cluster, 16) + \
               (num - 2) * self.boot.size_sector * self.boot.sectors_in_cluster
