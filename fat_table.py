from typing import BinaryIO


class FatTable:
    ROOT = 268435448
    DICH = 4294967295
    END = 268435455

    def __init__(self, fat_size: int, io: BinaryIO):
        self._info = []
        for i in range(fat_size):
            self._info.append(int.from_bytes(io.read(4), 'little'))

    def get_next_cluster_number(self, cluster_number: int) -> int:
        return self._info[cluster_number] if self._info[cluster_number] != FatTable.ROOT and self._info[
            cluster_number] != FatTable.END else None
