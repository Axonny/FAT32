from typing import BinaryIO


class FatTable:

    def __init__(self, fat_size: int, io: BinaryIO):
        self._info = []
        for i in range(fat_size):
            self._info.append(int.from_bytes(io.read(4), 'little'))

    def get_next_cluster_number(self, cluster_number: int) -> int:
        return self._info[cluster_number]
