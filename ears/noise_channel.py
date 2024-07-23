class NoiseChannel:
    def __init__(self, apu, channel_id):
        self.apu = apu
        self.channel_id = channel_id
        self.enabled = False

        # Länge und Timer
        self.length_counter = 0
        self.timer = 0

        # Frequenz
        self.noise_period = 0  # Periode des Rauschgenerators

        # Rauschgenerator
        self.shift_register = 1  # Initialwert des Schieberegisters
        self.mode = 0  # Rauschmodus (0 oder 1)

        # Lautstärke
        self.envelope_enabled = False
        self.envelope_loop = False
        self.envelope_start = 0
        self.envelope_count = 0
        self.envelope_divider = 0
        self.envelope_value = 0

    def step(self):
        if not self.enabled:
            return

        self.timer -= 1
        if self.timer <= 0:
            self.timer = self.noise_period

            # Rauschgenerator aktualisieren
            feedback_bit = (self.shift_register & 0x01) ^ ((self.shift_register >> (6 if self.mode == 0 else 1)) & 0x01)
            self.shift_register >>= 1
            self.shift_register |= feedback_bit << 15

        if self.length_counter > 0:
            self.length_counter -= 1
        else:
            self.enabled = False

        # Lautstärkehüllkurve aktualisieren
        if self.envelope_enabled:
            # ... (Hüllkurven-Logik wie zuvor)

    def output(self):
        if not self.enabled:
            return 0

        # Lautstärke anwenden
        volume = self.envelope_value if self.envelope_enabled else self.apu.memory[0xF4 + self.channel_id]  # Lautstärke aus ARAM oder Hüllkurve
        return -volume if self.shift_register & 0x01 else volume  # Rauschwert ausgeben
