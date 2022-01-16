from typing import BinaryIO


class FatTable:
    ROOT = 0x0ffffff8
    DICH = 0xffffffff
    END  = 0x0fffffff

    def __init__(self, fat_size: int, io: BinaryIO):
        self._info = []
        for i in range(fat_size):
            self._info.append(int.from_bytes(io.read(4), 'little'))

    def get_next_cluster_number(self, cluster_number: int) -> int:
        return self._info[cluster_number] if self._info[cluster_number] != FatTable.ROOT and \
                                             self._info[cluster_number] != FatTable.END and \
                                             self._info[cluster_number] != FatTable.DICH else None
