class SquareWaveChannel:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.enabled = False
        self.length_counter = 0
        self.timer = 0
        self.duty_cycle = 0
        self.envelope_generator = EnvelopeGenerator()
        self.frequency = 0

    def step(self):
        if not self.enabled:
            return

        self.timer -= 1
        if self.timer <= 0:
            self.timer = self.frequency
            self.duty_cycle = (self.duty_cycle + 1) % 8

        if self.length_counter > 0:
            self.length_counter -= 1
        else:
            self.enabled = False

        self.envelope_generator.step()

    def output(self):
        if not self.enabled:
            return 0
        
        duty_patterns = [0x80, 0x60, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02]
        duty_index = (self.duty_cycle >> 1) & 0x07
        if duty_patterns[duty_index] & (1 << (self.duty_cycle & 0x01)):
            return self.envelope_generator.output()
        else:
            return 0
