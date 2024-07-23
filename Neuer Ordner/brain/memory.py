class Memory:
    def __init__(self):
        self.data = bytearray(0x1000000)  # 16 MB Speicher (vereinfacht)

    def __getitem__(self, address):
        return self.data[address]

    def __setitem__(self, address, value):
        self.data[address] = value
