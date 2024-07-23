import numpy as np
import pygame

class PPU:
    def __init__(self, memory):
        self.memory = memory

        # VRAM und Paletten
        self.vram = bytearray(0x20000)  # 128 KB VRAM
        self.cgram = bytearray(0x200)   # 512 Byte CGRAM (Farb-RAM)
        self.oam = bytearray(0x200)    # 512 Byte OAM (Object Attribute Memory - Sprites)

        # Framebuffer
        self.frame = np.zeros((224, 256, 3), dtype=np.uint8)  # 224 Zeilen, 256 Spalten, RGB

        # Register
        self.inidisp = 0x00    # Image display register
        self.obsel = 0x00      # Object size and data area designation
        self.oamaddr = 0x00    # OAM address
        self.oamdata = 0x00    # OAM data
        self.bgmode = 0x00     # Background mode
        self.mosaic = 0x00     # Mosaic size
        self.bg1sc = 0x00      # BG1 scroll
        self.bg2sc = 0x00      # BG2 scroll
        self.bg3sc = 0x00      # BG3 scroll
        self.bg4sc = 0x00      # BG4 scroll
        self.vram_incmode = 0  # VRAM address increment mode
        self.vram_addr = 0x0000 # VRAM address
        self.vram_data = 0x00  # VRAM data
        self.cgaddr = 0x00     # CGRAM address
        self.cgdata = 0x00     # CGRAM data
        self.dma_channel = 0   # DMA channel
        self.hdma_channel = 0  # HDMA channel
        # ... (weitere PPU-Register)

        # Timing
        self.scanline = 0
        self.cycle = 0
        self.nmi_pending = False

    def read_register(self, address):
        if address == 0x2104:  # INIDISP
            return self.inidisp
        if address == 0x2105:  # OBSEL
            return self.obsel
        # ... (weitere Register lesen)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def write_register(self, address, value):
        if address == 0x2104:  # INIDISP
            self.inidisp = value
        if address == 0x2105:  # OBSEL
            self.obsel = value
        # ... (weitere Register schreiben)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    # ... (render und get_frame Methoden)
# ... (Importe und PPU-Klasse aus Teil 1)

class PPU:
    # ... (Konstruktor und Register aus Teil 1)

    # VRAM access
    def vram_address_increment(self):
        if self.vram_incmode == 0:
            self.vram_addr += 1
        else:
            self.vram_addr += 32

    def vram_read(self):
        data = self.vram[self.vram_addr]
        self.vram_address_increment()
        return data

    def vram_write(self, value):
        self.vram[self.vram_addr] = value
        self.vram_address_increment()

    def render(self):
        # ... (Implementierung des Renderings, noch Platzhalter)

        # Timing
        self.cycle += 1
        if self.cycle >= 341:  # SNES hat 341 PPU-Zyklen pro Scanline
            self.cycle = 0
            self.scanline += 1
            if self.scanline >= 262:  # 262 Scanlines pro Frame
                self.scanline = 0
                # NMI auslösen, wenn VBlank beginnt
                if self.scanline == 241:
                    self.nmi_pending = True

                self.frame = np.roll(self.frame, -1, axis=0)  # Frame nach oben scrollen

    # ... (get_frame wie zuvor)
# ... (Importe und PPU-Klasse aus Teil 1)

class PPU:
    # ... (Konstruktor, Register, VRAM-Zugriffsmethoden aus Teil 1)

    def render(self):
        # ... (Timing-Logik wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                tile_x = (x + self.bg1sc.coarse_x) // 8  # Grobe X-Position der Kachel
                tile_y = (y + self.bg1sc.coarse_y) // 8  # Grobe Y-Position der Kachel

                tile_index = self.vram_read()             # Kachel-Index aus VRAM lesen
                tile_attributes = self.vram_read()      # Kachel-Attribute aus VRAM lesen
                tile_palette = tile_attributes & 0x03   # Palette auswählen (0-3)

                pattern_table_address = 0x0000  # Basisadresse der Pattern-Tabelle (abhängig vom BG-Modus)
                if tile_attributes & 0x80:  # Bit 7 bestimmt, ob die Kachel in der oberen oder unteren Hälfte des Pattern-Table liegt
                    pattern_table_address += 0x1000

                # Pixel innerhalb der Kachel bestimmen
                pixel_x = x % 8
                pixel_y = y % 8

                # Pixel aus der Pattern-Tabelle lesen
                low_byte = self.vram[pattern_table_address + tile_index * 16 + pixel_y]
                high_byte = self.vram[pattern_table_address + tile_index * 16 + pixel_y + 8]
                pixel_value = (1 if low_byte & (0x80 >> pixel_x) else 0) + (2 if high_byte & (0x80 >> pixel_x) else 0)

                # Farbe aus der CGRAM lesen
                color_index = self.cgram[tile_palette * 16 + pixel_value]

                # Farbe in RGB umwandeln (hier fehlt noch die Umrechnung von SNES-Farben in RGB)
                r, g, b = 0, 0, 0  # Dummy-Werte, müssen ersetzt werden

                self.frame[y, x] = (r, g, b)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame wie zuvor)
import numpy as np

class PPU:
    def __init__(self, memory):
        self.memory = memory

        # VRAM und Paletten
        self.vram = bytearray(0x20000)  # 128 KB VRAM (2 Ebenen à 64 KB)
        self.cgram = bytearray(0x200)   # 512 Byte CGRAM (Farb-RAM)
        self.oam = bytearray(0x200)    # 512 Byte OAM (Object Attribute Memory - Sprites)

        # Framebuffer
        self.framebuffer = np.zeros((240, 256, 3), dtype=np.uint8)  # 240 Zeilen, 256 Spalten, RGB

        # Register
        self.inidisp = 0x00    # Image display register
        self.obsel = 0x00      # Object size and data area designation
        self.oamaddr = 0x00    # OAM address
        self.oamdata = 0x00    # OAM data
        self.bgmode = 0x00     # Background mode
        self.mosaic = 0x00     # Mosaic size
        self.bg1sc = 0x00      # BG1 scroll
        self.bg2sc = 0x00      # BG2 scroll
        self.bg3sc = 0x00      # BG3 scroll
        self.bg4sc = 0x00      # BG4 scroll
        self.bg12nba = 0x00    # BG1 and BG2 name base address
        self.bg34nba = 0x00    # BG3 and BG4 name base address
        self.vram_incmode = 0  # VRAM address increment mode
        self.vram_addr = 0x0000 # VRAM address
        self.vram_data = 0x00  # VRAM data
        self.cgaddr = 0x00     # CGRAM address
        self.cgdata = 0x00     # CGRAM data
        self.dma_channel = 0   # DMA channel
        self.hdma_channel = 0  # HDMA channel
        # ... (weitere PPU-Register)

        # Timing
        self.scanline = 0
        self.cycle = 0
        self.nmi_pending = False

    def read_register(self, address):
        # Implementierung zum Lesen der PPU-Register (siehe unten)

    def write_register(self, address, value):
        # Implementierung zum Schreiben der PPU-Register (siehe unten)

    def render(self):
        # Implementierung des Renderings (siehe Teil 2)

    def get_frame(self):
        return self.framebuffer
# ... (Importe, PPU-Klasse, Konstruktor, VRAM-Zugriffsmethoden aus Teil 1 und 2)

class PPU:
    # ... (Register aus Teil 1)

    def read_register(self, address):
        if address == 0x2104:  # INIDISP
            return self.inidisp
        if address == 0x2105:  # OBSEL
            return self.obsel
        if address == 0x2106:  # OAMADDR
            return self.oamaddr
        if address == 0x2107:  # OAMDATA
            return self.oamdata
        if address == 0x2108:  # BGMODE
            return self.bgmode
        if address == 0x2109:  # MOSAIC
            return self.mosaic
        if address == 0x210A:  # BG1SC
            return self.bg1sc.value
        if address == 0x210B:  # BG2SC
            return self.bg2sc.value
        if address == 0x210C:  # BG3SC
            return self.bg3sc.value
        if address == 0x210D:  # BG4SC
            return self.bg4sc.value
        if address == 0x210E:  # BG12NBA
            return self.bg12nba
        if address == 0x210F:  # BG34NBA
            return self.bg34nba
        # ... (weitere Register lesen)
        if address == 0x2121:  # VRAMADDR
            return self.vram_addr & 0xFF  # Nur das untere Byte zurückgeben
        if address == 0x2122:  # VRAMDATA
            data = self.vram_data
            self.vram_data = self.vram_read()  # Neuen Wert aus VRAM lesen
            return data
        # ... (weitere Register lesen)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def write_register(self, address, value):
        if address == 0x2104:  # INIDISP
            self.inidisp = value
        if address == 0x2105:  # OBSEL
            self.obsel = value
        if address == 0x2106:  # OAMADDR
            self.oamaddr = value
        if address == 0x2107:  # OAMDATA
            self.oam[self.oamaddr] = value
            self.oamaddr = (self.oamaddr + 1) & 0xFF  # OAM-Adresse automatisch erhöhen
        if address == 0x2108:  # BGMODE
            self.bgmode = value
        if address == 0x2109:  # MOSAIC
            self.mosaic = value
        if address == 0x210A:  # BG1SC
            self.bg1sc.value = value
        if address == 0x210B:  # BG2SC
            self.bg2sc.value = value
        # ... (weitere Register schreiben)
        if address == 0x2121:  # VRAMADDR
            if self.w == 0:
                self.vram_addr = (self.vram_addr & 0xFF00) | value
            else:
                self.vram_addr = (self.vram_addr & 0x00FF) | (value << 8)
            self.w = 1 - self.w  # Toggle für oberes/unteres Byte
        if address == 0x2122:  # VRAMDATA
            self.vram_write(value)
        # ... (weitere Register schreiben)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden aus Teil 1, 2 und 3)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik wie zuvor)

        # Background Rendering
        for y in range(224):  # Nur sichtbarer Bereich (ohne Overscan)
            for x in range(256):
                if self.bgmode == 0:  # Mode 0: 4 Hintergrundebenen
                    # ... (Implementierung für Mode 0)
                if self.bgmode == 1:  # Mode 1: 3 Hintergrundebenen
                    # ... (Implementierung für Mode 1)
                if self.bgmode == 2:  # Mode 2: 2 Hintergrundebenen mit Direct Color
                    # ... (Implementierung für Mode 2)
                if self.bgmode == 3:  # Mode 3: 2 Hintergrundebenen, eine mit Direct Color
                    # ... (Implementierung für Mode 3)
                if self.bgmode == 4:  # Mode 4: 2 Hintergrundebenen, eine mit Direct Color und größerer Auflösung
                    # ... (Implementierung für Mode 4)
                if self.bgmode == 5:  # Mode 5: 2 Hintergrundebenen, eine mit Direct Color und erweitertem Modus
                    # ... (Implementierung für Mode 5)
                if self.bgmode == 6:  # Mode 6: 1 Hintergrundebene mit Direct Color und größerer Auflösung
                    # ... (Implementierung für Mode 6)
                if self.bgmode == 7:  # Mode 7: 1 Hintergrundebene mit Direct Color und Matrixtransformationen
                    # ... (Implementierung für Mode 7)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden aus Teil 1, 2 und 3)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik wie zuvor)

        # Background Rendering
        for y in range(224):  # Nur sichtbarer Bereich (ohne Overscan)
            for x in range(256):
                if self.bgmode == 0:  # Mode 0: 4 Hintergrundebenen
                    for bg in range(4):  # 4 Hintergrundebenen durchlaufen
                        # Scroll-Offsets für die aktuelle Ebene holen
                        bg_scroll = getattr(self, f"bg{bg+1}sc")

                        # Kachelkoordinaten berechnen
                        tile_x = (x + bg_scroll.coarse_x) // 8
                        tile_y = (y + bg_scroll.coarse_y) // 8

                        # Name-Table-Adresse berechnen
                        name_table_base = self.bg12nba if bg < 2 else self.bg34nba
                        name_table_address = name_table_base + (tile_y % 32) * 32 + (tile_x % 32)

                        # Kachel-Index aus Name Table lesen
                        tile_index = self.vram_read(name_table_address)

                        # Attribute-Byte aus Attribut-Tabelle lesen
                        attribute_table_address = name_table_base + 0x3C0 + (tile_y // 4) * 8 + (tile_x // 4)
                        attributes = self.vram_read(attribute_table_address)
                        palette = (attributes >> ((tile_y % 4) * 2 + (tile_x % 4))) & 0x03

                        # Pixelkoordinaten innerhalb der Kachel berechnen
                        pixel_x = x % 8
                        pixel_y = y % 8

                        # Pattern-Tabelle-Adresse berechnen
                        pattern_table_address = (tile_index * 16) + pixel_y
                        if bg >= 2:
                            pattern_table_address += 0x1000  # BG3 und BG4 verwenden die zweite Hälfte der Pattern-Tabelle

                        # Pixel-Farbindex aus Pattern-Tabelle lesen
                        low_byte = self.vram_read(pattern_table_address)
                        high_byte = self.vram_read(pattern_table_address + 8)
                        pixel_value = (1 if low_byte & (0x80 >> pixel_x) else 0) + (2 if high_byte & (0x80 >> pixel_x) else 0)

                        # Farbe aus CGRAM holen (hier noch vereinfacht)
                        color_index = self.cgram[tile_palette * 16 + pixel_value]

                        # Farbe in RGB umwandeln (hier fehlt noch die Umrechnung von SNES-Farben in RGB)
                        r, g, b = color_index, color_index, color_index  # Dummy-Werte, müssen ersetzt werden

                        self.framebuffer[y, x] = (r, g, b)
                # ... (Implementierung für Mode 1-7)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe aus Teil 1-4)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik und Background-Rendering wie zuvor)

        # Sprite Rendering
        for i in range(128):  # Maximal 128 Sprites
            sprite_y = self.oam[i * 4]
            tile_index = self.oam[i * 4 + 1]
            attributes = self.oam[i * 4 + 2]
            sprite_x = self.oam[i * 4 + 3]

            # Sprite Größe und Priorität ermitteln
            sprite_size = (8, 8) if self.obsel & 0x01 == 0 else (8, 16)
            priority = attributes & 0x20  # 0: vor BG, 1: hinter BG

            # Sprite-Palette ermitteln
            palette = 0x04 + (attributes & 0x03)  # Paletten 4-7 sind für Sprites reserviert

            # Sprite-Y-Position anpassen (0-239)
            if sprite_y >= 240:
                sprite_y -= 256

            # Sprite rendern (nur wenn sichtbar)
            if 0 <= sprite_y < 224:
                for py in range(sprite_size[1]):
                    for px in range(sprite_size[0]):
                        screen_x = sprite_x + px
                        screen_y = sprite_y + py

                        if 0 <= screen_x < 256 and 0 <= screen_y < 224:
                            # Pixel innerhalb des Bildschirms

                            # Pixel-Farbindex aus Pattern-Tabelle lesen (hier noch vereinfacht)
                            # Berücksichtigung von horizontalem und vertikalem Flipping fehlt noch
                            pattern_table_address = tile_index * 16 + py
                            low_byte = self.vram_read(pattern_table_address)
                            high_byte = self.vram_read(pattern_table_address + 8)
                            pixel_value = (1 if low_byte & (0x80 >> px) else 0) + (2 if high_byte & (0x80 >> px) else 0)

                            # Farbe aus CGRAM holen
                            color_index = self.cgram[palette * 16 + pixel_value]

                            # Farbe in RGB umwandeln (hier fehlt noch die Umrechnung von SNES-Farben in RGB)
                            r, g, b = color_index, color_index, color_index  # Dummy-Werte, müssen ersetzt werden

                            # Pixel in Framebuffer schreiben, wenn nicht transparent (0)
                            if pixel_value != 0:
                                self.framebuffer[screen_y, screen_x] = (r, g, b)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites aus Teil 1-5)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik wie zuvor)

        # Background Rendering
        for y in range(224):  # Nur sichtbarer Bereich (ohne Overscan)
            for x in range(256):
                if self.bgmode == 0:  # Mode 0: 4 Hintergrundebenen
                    for bg in range(4):  # 4 Hintergrundebenen durchlaufen
                        # ... (Berechnung von tile_x, tile_y, name_table_address, tile_index, attributes, palette wie zuvor)

                        # Pixelkoordinaten innerhalb der Kachel berechnen
                        pixel_x = x % 8
                        pixel_y = y % 8

                        # Pattern-Tabelle-Adresse berechnen
                        pattern_table_address = (tile_index * 16) + pixel_y
                        if bg >= 2:
                            pattern_table_address += 0x1000  # BG3 und BG4 verwenden die zweite Hälfte der Pattern-Tabelle

                        # Pixel-Farbindex aus Pattern-Tabelle lesen
                        low_byte = self.vram_read(pattern_table_address)
                        high_byte = self.vram_read(pattern_table_address + 8)
                        pixel_value = (1 if low_byte & (0x80 >> pixel_x) else 0) + (2 if high_byte & (0x80 >> pixel_x) else 0)

                        # Farbe aus CGRAM holen und in RGB umwandeln
                        color_index = self.cgram[tile_palette * 16 + pixel_value]
                        r, g, b = self.convert_color(color_index)

                        self.framebuffer[y, x] = (r, g, b)

                # ... (Implementierung für Mode 1-7)

        # Sprite Rendering
        # ... (Sprite-Rendering-Logik wie zuvor, aber mit Farbkonvertierung)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame wie zuvor)

    def convert_color(self, color_index):
        """Konvertiert einen SNES-Farbindex in RGB-Werte."""
        b = (color_index & 0x1F) << 3
        g = ((color_index >> 5) & 0x1F) << 3
        r = ((color_index >> 10) & 0x1F) << 3
        return (r, g, b)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites aus Teil 1-6)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik wie zuvor)

        # Background Rendering
        for y in range(224):  # Nur sichtbarer Bereich (ohne Overscan)
            for x in range(256):
                # ... (Implementierung für Mode 0 wie in Teil 6)

                if self.bgmode == 1:  # Mode 1: 3 Hintergrundebenen
                    # Ähnlich wie Mode 0, aber nur 3 Ebenen
                    pass  # (Implementierung für Mode 1)
                if self.bgmode == 2:  # Mode 2: 2 Hintergrundebenen mit Direct Color
                    # ... (Implementierung für Mode 2)
                if self.bgmode == 3:  # Mode 3: 2 Hintergrundebenen, eine mit Direct Color
                    # ... (Implementierung für Mode 3)
                
                # ... (Implementierung für Mode 4-7)

        # Sprite Rendering
        # ... (Sprite-Rendering-Logik wie zuvor, aber mit Farbkonvertierung)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites aus Teil 1-7)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik wie zuvor)

        # Background Rendering
        for y in range(224):  # Nur sichtbarer Bereich (ohne Overscan)
            for x in range(256):
                # ... (Implementierung für Mode 0-3 wie in Teil 6 und 7)

                if self.bgmode == 4:  # Mode 4: 2 Hintergrundebenen, eine mit Direct Color und größerer Auflösung
                    # ... (Implementierung für Mode 4)
                if self.bgmode == 5:  # Mode 5: 2 Hintergrundebenen, eine mit Direct Color und erweitertem Modus
                    # ... (Implementierung für Mode 5)
                if self.bgmode == 6:  # Mode 6: 1 Hintergrundebene mit Direct Color und größerer Auflösung
                    # ... (Implementierung für Mode 6)
                if self.bgmode == 7:  # Mode 7: 1 Hintergrundebene mit Direct Color und Matrixtransformationen
                    # ... (Implementierung für Mode 7)

        # Sprite Rendering
        # ... (Sprite-Rendering-Logik wie zuvor, aber mit Farbkonvertierung)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites aus Teil 1-8)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik, Background-Rendering, Sprite-Rendering wie zuvor)

        # HDMA (High-Speed Direct Memory Access)
        if self.hdma_enabled and self.cycle == 1:
            for channel in range(8):  # 8 HDMA-Kanäle
                if self.hdma_channels[channel].in_progress:
                    # HDMA-Transfer durchführen
                    address = self.hdma_channels[channel].address
                    for _ in range(self.hdma_channels[channel].length):
                        self.vram[self.vram_addr] = self.memory[address]
                        self.vram_addr += 1
                        address += 1

                    # HDMA-Kanal aktualisieren
                    self.hdma_channels[channel].length -= 1
                    if self.hdma_channels[channel].length == 0:
                        self.hdma_channels[channel].in_progress = False

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites aus Teil 1-8)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    class HDMAChannel:
        def __init__(self):
            self.in_progress = False
            self.address = 0
            self.length = 0

    def __init__(self, memory):
        # ... (Initialisierung wie zuvor)
        self.hdma_channels = [self.HDMAChannel() for _ in range(8)]
        self.hdma_enabled = False

    def read_register(self, address):
        # ... (Lesen anderer Register wie zuvor)
        if address == 0x420B:  # HDMAEN
            return self.hdma_enabled
        if address in range(0x4300, 0x4380):  # DMAPx
            channel = (address - 0x4300) // 4
            return self.hdma_channels[channel].address & 0xFF  # Nur das untere Byte zurückgeben
        # ... (weitere Register lesen)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def write_register(self, address, value):
        # ... (Schreiben anderer Register wie zuvor)
        if address == 0x420B:  # HDMAEN
            self.hdma_enabled = value & 0x80 != 0
            for channel in self.hdma_channels:
                channel.in_progress = False  # HDMA-Kanäle bei Deaktivierung zurücksetzen
        if address in range(0x4300, 0x4380):  # DMAPx
            channel = (address - 0x4300) // 4
            if address % 4 == 0:
                self.hdma_channels[channel].address = (self.hdma_channels[channel].address & 0xFF00) | value
            if address % 4 == 1:
                self.hdma_channels[channel].address = (self.hdma_channels[channel].address & 0x00FF) | (value << 8)
            if address % 4 == 2:
                self.hdma_channels[channel].address = (self.hdma_channels[channel].address & 0xFFFF) | ((value & 0x7F) << 16)
                self.hdma_channels[channel].length = (value & 0x80) * 0x10 + (self.memory[0x4300 + channel * 4 + 3] & 0x7F) + 1
                self.hdma_channels[channel].in_progress = True
        # ... (weitere Register schreiben)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def render(self):
        # ... (Timing-Logik, Background-Rendering, Sprite-Rendering, HDMA wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden aus Teil 1-10)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                if self.bgmode == 0:  # Mode 0: 4 Hintergrundebenen
                    for bg in range(4):
                        bg_scroll = getattr(self, f"bg{bg+1}sc")
                        tile_x = (x + bg_scroll.coarse_x) // 8
                        tile_y = (y + bg_scroll.coarse_y) // 8

                        name_table_base = self.bg12nba if bg < 2 else self.bg34nba
                        name_table_address = name_table_base + (tile_y % 32) * 32 + (tile_x % 32)
                        tile_index = self.vram_read(name_table_address)

                        attribute_table_address = name_table_base + 0x3C0 + (tile_y // 4) * 8 + (tile_x // 4)
                        attributes = self.vram_read(attribute_table_address)
                        palette = (attributes >> ((tile_y % 4) * 2 + (tile_x % 4))) & 0x03

                        pixel_x = x % 8
                        pixel_y = y % 8

                        pattern_table_address = (tile_index * 16) + pixel_y
                        if bg >= 2:
                            pattern_table_address += 0x1000

                        low_byte = self.vram_read(pattern_table_address)
                        high_byte = self.vram_read(pattern_table_address + 8)
                        pixel_value = (1 if low_byte & (0x80 >> pixel_x) else 0) + (2 if high_byte & (0x80 >> pixel_x) else 0)

                        color_index = self.cgram[tile_palette * 16 + pixel_value]
                        r, g, b = self.convert_color(color_index)

                        self.framebuffer[y, x] = (r, g, b)

                if self.bgmode == 1:  # Mode 1: 3 Hintergrundebenen
                    # Ähnlich wie Mode 0, aber nur 3 Ebenen
                    for bg in range(3):
                        # ... (Implementierung analog zu Mode 0)

                if self.bgmode == 2:  # Mode 2: 2 Hintergrundebenen mit Direct Color
                    for bg in range(2):
                        bg_scroll = getattr(self, f"bg{bg+1}sc")
                        tile_x = (x + bg_scroll.coarse_x) >> 3
                        tile_y = (y + bg_scroll.coarse_y) >> 3

                        name_table_address = self.bg12nba + (tile_y & 0x1F) * 32 + (tile_x & 0x1F)
                        tile_index = self.vram_read(name_table_address)

                        # Direct Color Modus: Farbindex direkt aus VRAM lesen
                        color_index = self.vram_read(0x10000 + tile_index * 4 + ((y & 7) * 2 + (x & 1)))

                        r, g, b = self.convert_color(color_index)
                        self.framebuffer[y, x] = (r, g, b)

                if self.bgmode == 3:  # Mode 3: 2 Hintergrundebenen, eine mit Direct Color
                    # BG1: Direct Color
                    bg_scroll = self.bg1sc
                    tile_x = (x + bg_scroll.coarse_x) >> 3
                    tile_y = (y + bg_scroll.coarse_y) >> 3

                    name_table_address = self.bg12nba + (tile_y & 0x1F) * 32 + (tile_x & 0x1F)
                    tile_index = self.vram_read(name_table_address)

                    color_index = self.vram_read(0x10000 + tile_index * 4 + ((y & 7) * 2 + (x & 1)))
                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

                    # BG2: Wie Mode 0
                    # ... (Implementierung analog zu Mode 0)
        # ... (Sprite-Rendering, NMI, get_frame, convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden aus Teil 1-11)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                # ... (Implementierung für Mode 0-3 wie in Teil 11)

                if self.bgmode == 4:  # Mode 4: 2 Hintergrundebenen, eine mit Direct Color und größerer Auflösung
                    # BG1: Direct Color, 256 Farben
                    bg_scroll = self.bg1sc
                    tile_x = (x + bg_scroll.coarse_x) >> 3
                    tile_y = (y + bg_scroll.coarse_y) >> 3
                    tilemap_address = self.bg12nba + (tile_y & 0x1F) * 32 + (tile_x & 0x1F)
                    tile = self.vram_read(tilemap_address)
                    color_index = self.vram_read(0x10000 + tile * 4 + ((y & 7) * 2 + (x & 1)))
                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

                    # BG2: Wie Mode 0, 4 Farben
                    bg_scroll = self.bg2sc
                    tile_x = (x + bg_scroll.coarse_x) // 8
                    tile_y = (y + bg_scroll.coarse_y) // 8
                    name_table_address = self.bg12nba + (tile_y % 32) * 32 + (tile_x % 32)
                    tile_index = self.vram_read(name_table_address)
                    attribute_table_address = self.bg12nba + 0x3C0 + (tile_y // 4) * 8 + (tile_x // 4)
                    attributes = self.vram_read(attribute_table_address)
                    palette = (attributes >> ((tile_y % 4) * 2 + (tile_x % 4))) & 0x03
                    pixel_x = x % 8
                    pixel_y = y % 8
                    pattern_table_address = (tile_index * 16) + pixel_y
                    low_byte = self.vram_read(pattern_table_address)
                    high_byte = self.vram_read(pattern_table_address + 8)
                    pixel_value = (1 if low_byte & (0x80 >> pixel_x) else 0) + (2 if high_byte & (0x80 >> pixel_x) else 0)
                    color_index = self.cgram[palette * 16 + pixel_value]
                    r, g, b = self.convert_color(color_index)
                    if pixel_value != 0:  # Transparenter Pixel nicht zeichnen
                        self.framebuffer[y, x] = (r, g, b)

                if self.bgmode == 5:  # Mode 5: 2 Hintergrundebenen, eine mit Direct Color und Pseudo-Hires
                    # BG1: Direct Color, 256 Farben, Pseudo-Hires (ähnlich Mode 4, aber mit doppelter horizontaler Auflösung)
                    bg_scroll = self.bg1sc
                    tile_x = (x + bg_scroll.coarse_x) >> 3
                    tile_y = (y + bg_scroll.coarse_y) >> 3
                    tilemap_address = self.bg12nba + (tile_y & 0x1F) * 32 + (tile_x & 0x1F)
                    tile = self.vram_read(tilemap_address)
                    color_index = self.vram_read(0x10000 + tile * 8 + ((y & 7) * 4 + (x & 3)))
                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

                    # BG2: Wie Mode 0, 4 Farben
                    # ... (Implementierung analog zu Mode 0)

                # ... (Implementierung für Mode 6 und 7)

        # ... (Sprite-Rendering, NMI, get_frame, convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-12)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                # ... (Implementierung für Mode 0-5 wie in Teil 11 und 12)

                if self.bgmode == 6:  # Mode 6: 1 Hintergrundebene mit Direct Color und größerer Auflösung (512x224)
                    bg_scroll = self.bg1sc
                    tile_x = (x + bg_scroll.coarse_x) >> 3
                    tile_y = (y + bg_scroll.coarse_y) >> 3
                    tilemap_address = self.bg12nba + (tile_y & 0x3F) * 64 + (tile_x & 0x3F)
                    tile = self.vram_read(tilemap_address)
                    color_index = self.vram_read(0x10000 + tile * 4 + ((y & 7) * 2 + (x & 1)))
                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

                if self.bgmode == 7:  # Mode 7: 1 Hintergrundebene mit Direct Color und Matrixtransformationen
                    # Matrix-Register lesen
                    matrix_a = (self.memory[0x211A] << 8) | self.memory[0x211B]
                    matrix_b = (self.memory[0x211C] << 8) | self.memory[0x211D]
                    matrix_c = (self.memory[0x211E] << 8) | self.memory[0x211F]
                    matrix_d = (self.memory[0x2120] << 8) | self.memory[0x2121]
                    center_x = (self.memory[0x210E] << 8) | self.memory[0x210F]
                    center_y = (self.memory[0x2110] << 8) | self.memory[0x2111]

                    # Pixelkoordinaten transformieren
                    transformed_x = (matrix_a * (x - center_x) + matrix_b * (y - center_y)) >> 8
                    transformed_y = (matrix_c * (x - center_x) + matrix_d * (y - center_y)) >> 8

                    # Texturkoordinaten berechnen
                    texture_x = transformed_x >> 3
                    texture_y = transformed_y >> 3

                    # Farbe aus VRAM lesen (Direct Color)
                    color_index = self.vram_read(0x10000 + (texture_y & 0xFF) * 128 + (texture_x & 0xFF))

                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

        # ... (Sprite-Rendering, NMI, get_frame, convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-13)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    # ... (render() für Hintergrundmodi 0-7 aus Teil 13)

    def hdma_transfer(self):
        """Führt einen HDMA-Transfer durch."""
        if self.hdma_enabled:
            for channel in range(8):
                if self.hdma_channels[channel].in_progress:
                    # Anzahl der zu übertragenden Bytes in diesem Zyklus berechnen
                    transfer_size = min(self.hdma_channels[channel].length, 16)  # Maximal 16 Bytes pro Zyklus

                    # Daten übertragen
                    for _ in range(transfer_size):
                        self.vram[self.vram_addr] = self.memory[self.hdma_channels[channel].address]
                        self.vram_addr += 1
                        self.hdma_channels[channel].address += 1

                    # Länge des Transfers aktualisieren
                    self.hdma_channels[channel].length -= transfer_size

                    # HDMA-Kanal deaktivieren, wenn der Transfer abgeschlossen ist
                    if self.hdma_channels[channel].length == 0:
                        self.hdma_channels[channel].in_progress = False

    def render(self):
        # ... (Timing-Logik wie zuvor)

        # HDMA-Transfer durchführen (am Anfang jedes Zyklus)
        self.hdma_transfer()

        # ... (Background-Rendering, Sprite-Rendering, NMI wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-14)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def read_register(self, address):
        # ... (Lesen anderer Register wie zuvor)
        if address == 0x2133:  # CGDATA
            data = self.cgdata
            self.cgaddr += 1  # CGRAM-Adresse automatisch erhöhen
            return data
        if address == 0x2134:  # TM
            # TODO: Implementierung für den Transfermodus
            return 0x00  # Dummy-Wert, muss ersetzt werden
        if address == 0x213C:  # OAMDATAREAD
            # TODO: Implementierung für das Lesen von OAM-Daten
            return 0x00  # Dummy-Wert, muss ersetzt werden
        if address == 0x213E:  # TMW
            # TODO: Implementierung für den Transfermodus (Schreiben)
            pass
        if address == 0x213F:  # CGWSEL
            # TODO: Implementierung für die CGRAM-Schreibauswahl
            pass
        # ... (weitere Register lesen)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def write_register(self, address, value):
        # ... (Schreiben anderer Register wie zuvor)
        if address == 0x2133:  # CGDATA
            self.cgram[self.cgaddr] = value
            self.cgaddr += 1  # CGRAM-Adresse automatisch erhöhen
        if address == 0x2134:  # TM
            # TODO: Implementierung für den Transfermodus
            pass
        if address == 0x213C:  # OAMDATAREAD
            # TODO: Implementierung für das Schreiben von OAM-Daten
            pass
        if address == 0x213E:  # TMW
            # TODO: Implementierung für den Transfermodus (Schreiben)
            pass
        if address == 0x213F:  # CGWSEL
            # TODO: Implementierung für die CGRAM-Schreibauswahl
            pass
        # ... (weitere Register schreiben)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-15)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3 und 15)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                # ... (Implementierung für Mode 0-4 wie in Teil 11 und 12)

                if self.bgmode == 5:  # Mode 5: 2 Hintergrundebenen, eine mit Direct Color und Pseudo-Hires
                    # BG1: Direct Color, 256 Farben, Pseudo-Hires
                    bg_scroll = self.bg1sc
                    tile_x = (x + bg_scroll.coarse_x) >> 3
                    tile_y = (y + bg_scroll.coarse_y) >> 3
                    tilemap_address = self.bg12nba + (tile_y & 0x1F) * 32 + (tile_x & 0x1F)
                    tile = self.vram_read(tilemap_address)

                    # Pseudo-Hires: Horizontale Auflösung verdoppelt
                    sub_tile_x = (x + bg_scroll.fine_x) & 0x07
                    color_index = self.vram_read(0x10000 + tile * 8 + ((y & 7) * 4 + (sub_tile_x // 2)))

                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

                    # BG2: Wie Mode 0, 4 Farben
                    # ... (Implementierung analog zu Mode 0)

                if self.bgmode == 6:  # Mode 6: 1 Hintergrundebene mit Direct Color und größerer Auflösung (512x224)
                    bg_scroll = self.bg1sc
                    tile_x = (x + bg_scroll.coarse_x) >> 3
                    tile_y = (y + bg_scroll.coarse_y) >> 3
                    tilemap_address = self.bg12nba + (tile_y & 0x3F) * 64 + (tile_x & 0x3F)  # Größere Tilemap
                    tile = self.vram_read(tilemap_address)
                    color_index = self.vram_read(0x10000 + tile * 4 + ((y & 7) * 2 + (x & 1)))
                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

                if self.bgmode == 7:  # Mode 7: 1 Hintergrundebene mit Direct Color und Matrixtransformationen
                    # ... (Implementierung von Mode 7 wie in Teil 13)

        # ... (Sprite-Rendering, NMI, get_frame, convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden aus Teil 1-14)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                if self.bgmode in range(4):  # Mode 0-3
                    # ... (Implementierung für Mode 0-3 wie in Teil 11)

                elif self.bgmode == 4 or self.bgmode == 5:
                    # ... (Implementierung für Mode 4-5 wie in Teil 12)

                elif self.bgmode == 6:  # Mode 6: 1 Hintergrundebene mit Direct Color und größerer Auflösung (512x224)
                    bg_scroll = self.bg1sc
                    tile_x = (x + bg_scroll.coarse_x) >> 3
                    tile_y = (y + bg_scroll.coarse_y) >> 3
                    tilemap_address = self.bg12nba + (tile_y & 0x3F) * 64 + (tile_x & 0x3F)  # Größere Tilemap
                    tile = self.vram_read(tilemap_address)
                    color_index = self.vram_read(0x10000 + tile * 4 + ((y & 7) * 2 + (x & 1)))
                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

                elif self.bgmode == 7:  # Mode 7: 1 Hintergrundebene mit Direct Color und Matrixtransformationen
                    # Matrix-Register lesen
                    matrix_a = (self.memory[0x211A] << 8) | self.memory[0x211B]
                    matrix_b = (self.memory[0x211C] << 8) | self.memory[0x211D]
                    matrix_c = (self.memory[0x211E] << 8) | self.memory[0x211F]
                    matrix_d = (self.memory[0x2120] << 8) | self.memory[0x2121]
                    center_x = (self.memory[0x210E] << 8) | self.memory[0x210F]
                    center_y = (self.memory[0x2110] << 8) | self.memory[0x2111]

                    # Pixelkoordinaten transformieren
                    transformed_x = (matrix_a * (x - center_x) + matrix_b * (y - center_y)) >> 8
                    transformed_y = (matrix_c * (x - center_x) + matrix_d * (y - center_y)) >> 8

                    # Texturkoordinaten berechnen
                    texture_x = transformed_x >> 3
                    texture_y = transformed_y >> 3

                    # Farbe aus VRAM lesen (Direct Color)
                    color_index = self.vram_read(0x10000 + (texture_y & 0xFF) * 128 + (texture_x & 0xFF))

                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

        # Sprite Rendering
        # ... (Sprite-Rendering-Logik wie zuvor, aber mit Farbkonvertierung)

        # NMI auslösen
        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-15)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3 und 15)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                # Clipping prüfen
                if not (self.clip_windows_enabled and (
                        (self.window1_enabled and self.is_in_window1(x, y)) or
                        (self.window2_enabled and self.is_in_window2(x, y)))):
                    # ... (Rendering-Logik für Mode 0-7 wie in Teil 11-15)

        # Sprite Rendering
        # ... (Sprite-Rendering-Logik wie zuvor, aber mit Clipping)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)

    def is_in_window1(self, x, y):
        """Prüft, ob ein Pixel innerhalb von Window 1 liegt."""
        return self.window1_left <= x <= self.window1_right and self.window1_top <= y <= self.window1_bottom

    def is_in_window2(self, x, y):
        """Prüft, ob ein Pixel innerhalb von Window 2 liegt."""
        return self.window2_left <= x <= self.window2_right and self.window2_top <= y <= self.window2_bottom
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-15)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3 und 15)

    def __init__(self, memory):
        # ... (Initialisierung wie zuvor)
        # Clipping und Windowing
        self.clip_windows_enabled = False
        self.window1_enabled = False
        self.window2_enabled = False
        self.window1_invert = False
        self.window2_invert = False
        self.window1_left = 0
        self.window1_right = 255
        self.window2_left = 0
        self.window2_right = 255
        self.window1_top = 0
        self.window1_bottom = 239
        self.window2_top = 0
        self.window2_bottom = 239

    def read_register(self, address):
        # ... (Lesen anderer Register wie zuvor)
        elif address == 0x2123:  # W12SEL (Window 1 & 2 Mask Select)
            return (self.window1_invert << 7) | (self.window2_invert << 6) | (self.window1_enabled << 5) | (self.window2_enabled << 4)
        elif address == 0x2124:  # W34SEL (Window 3 & 4 Mask Select)
            # TODO: Implementierung für Window 3 & 4 (nicht in SNES verwendet)
            return 0x00
        elif address == 0x2125:  # WOBJSEL (Window Mask for Objects)
            # TODO: Implementierung für Window-Maske für Sprites
            return 0x00
        elif address == 0x2126:  # WH0 (Window 1 Left Position)
            return self.window1_left
        elif address == 0x2127:  # WH1 (Window 1 Right Position)
            return self.window1_right
        elif address == 0x2128:  # WH2 (Window 2 Left Position)
            return self.window2_left
        elif address == 0x2129:  # WH3 (Window 2 Right Position)
            return self.window2_right
        elif address == 0x212A:  # WBGLOG (Window Mask for Backdrop and Color Windows)
            # TODO: Implementierung für Window-Maske für Backdrop und Color Windows
            return 0x00
        # ... (weitere Register lesen)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def write_register(self, address, value):
        # ... (Schreiben anderer Register wie zuvor)
        elif address == 0x2123:  # W12SEL
            self.window1_invert = (value >> 7) & 0x01
            self.window2_invert = (value >> 6) & 0x01
            self.window1_enabled = (value >> 5) & 0x01
            self.window2_enabled = (value >> 4) & 0x01
        elif address == 0x2124:  # W34SEL
            # TODO: Implementierung für Window 3 & 4 (nicht in SNES verwendet)
            pass
        elif address == 0x2125:  # WOBJSEL
            # TODO: Implementierung für Window-Maske für Sprites
            pass
        elif address == 0x2126:  # WH0
            self.window1_left = value
        elif address == 0x2127:  # WH1
            self.window1_right = value
        elif address == 0x2128:  # WH2
            self.window2_left = value
        elif address == 0x2129:  # WH3
            self.window2_right = value
        elif address == 0x212A:  # WBGLOG
            # TODO: Implementierung für Window-Maske für Backdrop und Color Windows
            pass
        # ... (weitere Register schreiben)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    # ... (render, get_frame, convert_color, is_in_window1, is_in_window2 wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-16)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15 und 16)

    def read_register(self, address):
        # ... (Lesen anderer Register wie zuvor)
        elif address == 0x2134:  # TM (Transfer Mode)
            # TODO: Implementierung für den Transfermodus
            return 0x00
        elif address == 0x213C:  # OAMDATAREAD
            data = self.oam[self.oamaddr]
            self.oamaddr = (self.oamaddr + 1) & 0xFF
            return data
        elif address == 0x213E:  # TMW (Transfer Mode Write)
            # TODO: Implementierung für den Transfermodus (Schreiben)
            pass
        elif address == 0x213F:  # CGWSEL (CGRAM Write Select)
            # TODO: Implementierung für die CGRAM-Schreibauswahl
            pass
        # ... (weitere Register lesen)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def write_register(self, address, value):
        # ... (Schreiben anderer Register wie zuvor)
        elif address == 0x2134:  # TM (Transfer Mode)
            # TODO: Implementierung für den Transfermodus
            pass
        elif address == 0x213C:  # OAMDATAREAD
            self.oam[self.oamaddr] = value
            self.oamaddr = (self.oamaddr + 1) & 0xFF
        elif address == 0x213E:  # TMW (Transfer Mode Write)
            # TODO: Implementierung für den Transfermodus (Schreiben)
            pass
        elif address == 0x213F:  # CGWSEL (CGRAM Write Select)
            # TODO: Implementierung für die CGRAM-Schreibauswahl
            pass
        # ... (weitere Register schreiben)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def convert_color(self, color_index):
        """Konvertiert einen SNES-Farbindex in RGB-Werte."""
        r = (color_index & 0x1F) << 3  # Extrahiere rote Komponente (5 Bits) und skaliere auf 8 Bits
        g = ((color_index >> 5) & 0x1F) << 3  # Extrahiere grüne Komponente (5 Bits) und skaliere auf 8 Bits
        b = ((color_index >> 10) & 0x1F) << 3  # Extrahiere blaue Komponente (5 Bits) und skaliere auf 8 Bits
        return (r, g, b)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-15)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15)

    def read_register(self, address):
        # ... (Lesen anderer Register wie zuvor)
        elif address == 0x2134:  # TM (Transfer Mode)
            return self.tm
        elif address == 0x213C:  # OAMDATAREAD
            data = self.oam[self.oamaddr]
            self.oamaddr = (self.oamaddr + 1) & 0xFF  # OAM-Adresse automatisch erhöhen
            return data
        elif address == 0x213E:  # TMW (Transfer Mode Write)
            return self.tmw
        elif address == 0x213F:  # CGWSEL (CGRAM Write Select)
            return self.cgwsel
        # ... (weitere Register lesen)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def write_register(self, address, value):
        # ... (Schreiben anderer Register wie zuvor)
        elif address == 0x2134:  # TM (Transfer Mode)
            self.tm = value
        elif address == 0x213C:  # OAMDATAREAD
            self.oam[self.oamaddr] = value
            self.oamaddr = (self.oamaddr + 1) & 0xFF
        elif address == 0x213E:  # TMW (Transfer Mode Write)
            self.tmw = value
        elif address == 0x213F:  # CGWSEL (CGRAM Write Select)
            self.cgwsel = value
        # ... (weitere Register schreiben)
        else:
            raise ValueError(f"Invalid PPU register address: {hex(address)}")

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                # ... (Implementierung für Mode 0-7 wie in Teil 11-15)

                # Hier müsstest du die Prioritäten der Ebenen berücksichtigen, um zu bestimmen, welcher Pixel sichtbar ist.

        # Sprite Rendering
        for i in range(128):  # Maximal 128 Sprites
            # ... (Sprite-Rendering-Logik wie zuvor, aber mit Priorität und Clipping)

            # Hier müsstest du die Priorität des Sprites berücksichtigen, um zu bestimmen, ob es vor oder hinter dem Hintergrund gezeichnet wird.

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, Farbkonvertierung aus Teil 1-16)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15 und 16)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                # Clipping prüfen
                if not (self.clip_windows_enabled and (
                        (self.window1_enabled and self.is_in_window1(x, y)) or
                        (self.window2_enabled and self.is_in_window2(x, y)))):

                    # Prioritäten der Ebenen berücksichtigen
                    bg_priority = [0, 0, 0, 0]  # Priorität für jede Ebene (0 = höchste Priorität)
                    for bg in range(4):
                        if self.bg_enabled[bg]:
                            # ... (Berechnung von tile_x, tile_y, name_table_address, tile_index, attributes, palette wie zuvor)
                            bg_priority[bg] = attributes & 0x20  # Bit 5 bestimmt die Priorität

                    # Ebene mit höchster Priorität finden
                    highest_priority_bg = min(range(4), key=lambda i: bg_priority[i])

                    # Pixel der Ebene mit höchster Priorität rendern
                    # ... (Rendering-Logik für Mode 0-7 wie in Teil 11-15, aber nur für highest_priority_bg)

        # Sprite Rendering
        for i in range(128):  # Maximal 128 Sprites
            # ... (Sprite-Rendering-Logik wie zuvor)

            # Priorität des Sprites berücksichtigen
            sprite_priority = attributes & 0x20  # 0: vor BG, 1: hinter BG

            # Pixel nur zeichnen, wenn Sprite Priorität hat
            if not (self.clip_windows_enabled and (
                    (self.window1_enabled and self.is_in_window1(x, y)) or
                    (self.window2_enabled and self.is_in_window2(x, y)))) and (
                    sprite_priority == 0 or bg_priority[highest_priority_bg] == 1):
                # ... (Pixel in Framebuffer schreiben)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites aus Teil 1-16)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15 und 16)

    # ... (render() für Hintergrundmodi 0-7 aus Teil 16)

    def convert_color(self, color_index):
        """Konvertiert einen SNES-Farbindex in RGB-Werte."""
        if color_index == 0:  # Transparent
            return (0, 0, 0, 0)  # Alpha auf 0 setzen für Transparenz

        # Farbwerte aus CGRAM lesen (unter Berücksichtigung von Farb-Arithmetik und Halbbright-Bit)
        raw_color = self.cgram[color_index]
        r = (raw_color & 0x1F) << 3
        g = ((raw_color >> 5) & 0x1F) << 3
        b = ((raw_color >> 10) & 0x1F) << 3

        # Helligkeit anpassen, falls Halbbright-Bit gesetzt ist
        if raw_color & 0x80:
            r //= 2
            g //= 2
            b //= 2

        return (r, g, b)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-17)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15 und 16)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        for y in range(224):
            for x in range(256):
                # ... (Implementierung für Mode 0-6 wie in Teil 11-16)

                elif self.bgmode == 7:  # Mode 7: 1 Hintergrundebene mit Direct Color und Matrixtransformationen
                    # Matrix-Register lesen (16-Bit-Werte)
                    matrix_a = (self.memory[0x211A] << 8) | self.memory[0x211B]
                    matrix_b = (self.memory[0x211C] << 8) | self.memory[0x211D]
                    matrix_c = (self.memory[0x211E] << 8) | self.memory[0x211F]
                    matrix_d = (self.memory[0x2120] << 8) | self.memory[0x2121]

                    # Ursprung der Transformation (Center-Koordinaten)
                    center_x = (self.memory[0x210E] << 8) | self.memory[0x210F]
                    center_y = (self.memory[0x2110] << 8) | self.memory[0x2111]

                    # Pixelkoordinaten relativ zum Ursprung
                    relative_x = x - center_x
                    relative_y = y - center_y

                    # Mode 7-Transformation anwenden
                    transformed_x = (matrix_a * relative_x + matrix_b * relative_y) / 256
                    transformed_y = (matrix_c * relative_x + matrix_d * relative_y) / 256

                    # Texturkoordinaten berechnen (mit Repeat-Modus)
                    texture_x = (transformed_x >> 3) & 0xFF  # Modulo 256
                    texture_y = (transformed_y >> 3) & 0xFF  # Modulo 256

                    # Farbe aus VRAM lesen (Direct Color)
                    color_index = self.vram_read(0x10000 + texture_y * 128 + texture_x)

                    r, g, b = self.convert_color(color_index)
                    self.framebuffer[y, x] = (r, g, b)

        # ... (Sprite-Rendering, NMI, get_frame, convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe, Farbkonvertierung aus Teil 1-15)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        # ... (Implementierung für Mode 0-7 wie in Teil 11-15)

        # Sprite Rendering
        for i in range(128):  # Maximal 128 Sprites
            sprite_y = self.oam[i * 4]
            tile_index = self.oam[i * 4 + 1]
            attributes = self.oam[i * 4 + 2]
            sprite_x = self.oam[i * 4 + 3]

            # Sprite Größe ermitteln
            if self.obsel & 0x01 == 0:
                sprite_height = 8
            else:
                sprite_height = 16 if tile_index & 0x01 == 0 else 8  # 8x16 Sprites haben ungerade Indizes

            # Sprite-Priorität, Palette und Y-Position anpassen
            sprite_priority = attributes & 0x20  # 0: vor BG, 1: hinter BG
            palette = 0x04 + (attributes & 0x03)  # Paletten 4-7 sind für Sprites reserviert
            if sprite_y >= 240:
                sprite_y -= 256

            # Sprite rendern (nur wenn sichtbar)
            if 0 <= sprite_y < 224:
                for py in range(sprite_height):
                    for px in range(8):
                        screen_x = sprite_x + px
                        screen_y = sprite_y + py

                        if 0 <= screen_x < 256 and 0 <= screen_y < 224:
                            # Pixel innerhalb des Bildschirms

                            # Pixel-Farbindex aus Pattern-Tabelle lesen
                            pattern_table_address = tile_index * 16 + py
                            if sprite_height == 16:
                                pattern_table_address += 8 * (tile_index & 0x01)  # 8x16 Sprites verwenden abwechselnd zwei Kacheln
                            if attributes & 0x40:  # Vertikales Flipping
                                pattern_table_address += (7 - py)
                            if attributes & 0x80:  # Horizontales Flipping
                                pixel_x = 7 - px

                            low_byte = self.vram_read(pattern_table_address)
                            high_byte = self.vram_read(pattern_table_address + 8)
                            pixel_value = (1 if low_byte & (0x80 >> pixel_x) else 0) + (2 if high_byte & (0x80 >> pixel_x) else 0)

                            # Farbe aus CGRAM holen und in RGB umwandeln
                            color_index = self.cgram[palette * 16 + pixel_value]
                            r, g, b = self.convert_color(color_index)

                            # Pixel in Framebuffer schreiben, wenn nicht transparent (0) und Priorität hat
                            if pixel_value != 0 and (sprite_priority == 0 or not self.framebuffer[screen_y, screen_x][3]):
                                self.framebuffer[screen_y, screen_x] = (r, g, b, 255)  # Alpha auf 255 für Opazität

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe, Farbkonvertierung aus Teil 1-17)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15 und 16)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        # ... (Implementierung für Mode 0-7 wie in Teil 11-16)

        # Sprite Rendering
        for i in range(128):  # Maximal 128 Sprites
            sprite_y = self.oam[i * 4]
            tile_index = self.oam[i * 4 + 1]
            attributes = self.oam[i * 4 + 2]
            sprite_x = self.oam[i * 4 + 3]

            # Sprite Größe ermitteln
            if self.obsel & 0x01 == 0:
                sprite_height = 8
            else:
                sprite_height = 16 if tile_index & 0x01 == 0 else 8  # 8x16 Sprites haben ungerade Indizes

            # Sprite-Priorität, Palette und Y-Position anpassen
            sprite_priority = attributes & 0x20  # 0: vor BG, 1: hinter BG
            palette = 0x04 + (attributes & 0x03)  # Paletten 4-7 sind für Sprites reserviert
            if sprite_y >= 240:
                sprite_y -= 256

            # Sprite rendern (nur wenn sichtbar und nicht geclippt)
            if 0 <= sprite_y < 224 and not self.is_sprite_clipped(sprite_x, sprite_y, sprite_height):
                for py in range(sprite_height):
                    for px in range(8):
                        screen_x = sprite_x + px
                        screen_y = sprite_y + py

                        if 0 <= screen_x < 256 and 0 <= screen_y < 224:
                            # Pixel innerhalb des Bildschirms

                            # Pixel-Farbindex aus Pattern-Tabelle lesen
                            pattern_table_address = tile_index * 16 + py
                            if sprite_height == 16:
                                pattern_table_address += 8 * (tile_index & 0x01)  # 8x16 Sprites verwenden abwechselnd zwei Kacheln
                            if attributes & 0x40:  # Vertikales Flipping
                                pattern_table_address += (7 - py)
                            if attributes & 0x80:  # Horizontales Flipping
                                pixel_x = 7 - px

                            low_byte = self.vram_read(pattern_table_address)
                            high_byte = self.vram_read(pattern_table_address + 8)
                            pixel_value = (1 if low_byte & (0x80 >> pixel_x) else 0) + (2 if high_byte & (0x80 >> pixel_x) else 0)

                            # Farbe aus CGRAM holen und in RGB umwandeln
                            color_index = self.cgram[palette * 16 + pixel_value]
                            r, g, b = self.convert_color(color_index)

                            # Pixel in Framebuffer schreiben, wenn nicht transparent (0) und Priorität hat
                            if pixel_value != 0 and (sprite_priority == 0 or not self.framebuffer[screen_y, screen_x][3]):
                                self.framebuffer[screen_y, screen_x] = (r, g, b, 255)  # Alpha auf 255 für Opazität

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)

    def is_sprite_clipped(self, x, y, height):
        """Prüft, ob ein Sprite geclippt wird."""
        # Hier müsstest du die Clipping-Logik für Sprites implementieren
        # ...
        return False  # Placeholder
# ... (Importe, PPU-Klasse, Konstruktor, Register, VRAM-Zugriffsmethoden, render() für Hintergründe und Sprites, Farbkonvertierung aus Teil 1-18)

class PPU:
    # ... (Register aus Teil 1)

    # ... (read_register und write_register Methoden aus Teil 3, 15 und 16)

    def render(self):
        # ... (Timing-Logik und HDMA wie zuvor)

        # Background Rendering
        # ... (Implementierung für Mode 0-7 wie in Teil 11-15)

        # Sprite Rendering
        # ... (Sprite-Rendering-Logik wie zuvor)

        # ... (NMI auslösen wie zuvor)

    # ... (get_frame und convert_color wie zuvor)

    def is_sprite_clipped(self, x, y, height):
        """Prüft, ob ein Sprite geclippt wird."""
        # Clipping durch Bildschirmränder
        if x >= 256 or x + 8 <= 0 or y >= 240 or y + height <= 0:
            return True

        # Clipping durch Fenster 1
        if self.window1_enabled and self.window1_invert:  # Window 1 maskiert Sprites
            if self.window1_left <= x <= self.window1_right and self.window1_top <= y <= self.window1_bottom:
                return True

        # Clipping durch Fenster 2
        if self.window2_enabled and self.window2_invert:  # Window 2 maskiert Sprites
            if self.window2_left <= x <= self.window2_right and self.window2_top <= y <= self.window2_bottom:
                return True

        return False
