class EnvelopeGenerator:
    def __init__(self):
        # Initialisierung der Hüllkurvenparameter
        self.envelope_enabled = False
        self.envelope_loop = False
        self.envelope_start = 0
        self.envelope_count = 0
        self.envelope_divider = 0
        self.envelope_value = 0

    def step(self):
        if self.envelope_enabled:
            if self.envelope_count > 0:
                self.envelope_count -= 1
            else:
                if self.envelope_divider > 0:
                    self.envelope_divider -= 1
                else:
                    self.envelope_divider = self.envelope_start
                    if self.envelope_value > 0:
                        self.envelope_value -= 1
                    elif self.envelope_loop:
                        self.envelope_value = 15
                    self.envelope_count = 15
        else:
            self.envelope_value = self.envelope_start

    def output(self):
        return self.envelope_value
