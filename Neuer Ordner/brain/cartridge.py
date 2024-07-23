class Cartridge:
    def __init__(self, rom_path):
        self.rom = open(rom_path, "rb").read()

    def load_rom(self, memory):
        memory[0x8000:0x8000 + len(self.rom)] = self.rom
