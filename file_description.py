from typing import BinaryIO


class FileDescriptor:
    LONG_FLAGS = 15
    DIRECTORY_FLAGS = 16

    def __init__(self, io: BinaryIO):
        self.empty = False
        self.data = io.read(12)
        if self.data[0] == 0:
            self.empty = True
        self.flags = self.data[-1]
        self.data += io.read(20)

        if self.flags == FileDescriptor.LONG_FLAGS:
            count = self.data[0] - 64
            name = self._extract_name(self.data)
            for i in range(count - 1):
                data = io.read(32)
                name = self._extract_name(data) + name
            self.long_name = name.decode().strip()
            self.data = io.read(32)
        self._parse_common_descriptor(self.data)


    def _extract_name(self, bytes):
        temp = bytes[1:11] + bytes[14:25] + bytes[-4:]
        ans = b''
        for i in temp:
            if i != 255:
                ans += i.to_bytes(1, "little")
            else:
                return ans
        return ans

    def _parse_common_descriptor(self, data):
        self.short_name = data[:8].decode().strip()
        self.type = data[8:11].decode().strip()
        self.attrs = data[11]
        self.reserved = data[12]
        self.seconds_creation = data[13]
        self.time_creation = int.from_bytes(data[14:16], "little")
        self.date_creation = int.from_bytes(data[16:18], "little")
        self.date_acquired = int.from_bytes(data[18:20], "little")
        self.time_writed = int.from_bytes(data[22:24], "little")
        self.data_writed = int.from_bytes(data[24:26], "little")
        self.cluster_address = (int.from_bytes(data[20:22], "little") << 16) + int.from_bytes(data[26:28], "little")
        self.size = int.from_bytes(data[28:], "little")