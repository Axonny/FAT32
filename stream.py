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

    def get_cursor_position(self):
        return self.calc_address(self.start) + self.pointer

    def write(self, address, symbol):
        self.f.seek(address)
        print(hex(address), symbol)
        self.f.write(symbol)

    def delete(self, descriptor):
        self.write(descriptor.descr_address, 0xE5.to_bytes(1, "little"))
        chain = [descriptor.cluster_address]
        while cluster := self.fat.get_next_cluster_number(chain[-1]):
            chain.append(cluster)
        addr_fat = [int(self.boot.address_fat_table, 16) +
                    self.boot.size_fat * self.boot.size_sector * i for i in range(self.boot.count_fat_table)]
        for i in chain:
            for addr in addr_fat:
                self.f.seek(addr + 4 * i)
                self.f.write(0x00000000.to_bytes(4, "little"))
                self.fat._info[i] = 0
