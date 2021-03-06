from stream import FatStream


class FileDescriptor:
    LONG_FLAGS = 15
    DIRECTORY_FLAGS = 16

    def __init__(self, io: FatStream):
        self.io = io
        self.count = 0
        self.empty = False
        self.success = True
        self.descr_address = io.get_cursor_position()
        self.data = io.read(12)
        if self.data[0] == 0:
            self.empty = True
        self.flags = self.data[-1]
        self.data += io.read(20)

        if self.flags == FileDescriptor.LONG_FLAGS:
            count = self.data[0] - 64
            name = self._extract_name(self.data)
            self.count += 1
            for i in range(count - 1):
                data = io.read(32)
                name = self._extract_name(data) + name
                self.count += 1
            self.long_name = self.try_decode(name)
            self.descr_address = io.get_cursor_position()
            self.data = io.read(32)
        self.count += 1
        self._parse_common_descriptor(self.data)

    @staticmethod
    def _extract_name(_bytes):
        temp = _bytes[1:11] + _bytes[14:25] + _bytes[-4:]
        ans = b''
        for i in temp:
            if i != 255:
                if i != 0:
                    ans += i.to_bytes(1, "little")
            else:
                return ans
        return ans

    def _parse_common_descriptor(self, data):
        self.short_name = self.try_decode(data[:8])
        self.type = self.try_decode(data[8:11])
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

    def __str__(self):
        return self.get_name()

    def get_name(self):
        if hasattr(self, "long_name"):
            return self.long_name
        if self.type:
            return self.short_name + '.' + self.type.lower()
        return self.short_name

    def try_decode(self, _bytes: bytes) -> str:
        try:
            return _bytes.decode('utf-8').strip()
        except UnicodeDecodeError:
            self.success = False

    def delete(self):
        self.io.delete(self)
