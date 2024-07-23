import pygame

class Controller:
    def __init__(self):
        self.button_state = {
            "A": False,
            "B": False,
            "X": False,
            "Y": False,
            "L": False,
            "R": False,
            "START": False,
            "SELECT": False,
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False,
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self._handle_key_down(event.key)
        elif event.type == pygame.KEYUP:
            self._handle_key_up(event.key)

    def _handle_key_down(self, key):
        key_map = {
            pygame.K_z: "A",
            pygame.K_x: "B",
            pygame.K_a: "X",
            pygame.K_s: "Y",
            pygame.K_q: "L",
            pygame.K_w: "R",
            pygame.K_RETURN: "START",
            pygame.K_RSHIFT: "SELECT",
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
        }
        if key in key_map:
            self.button_state[key_map[key]] = True

    def _handle_key_up(self, key):
        key_map = {
            pygame.K_z: "A",
            pygame.K_x: "B",
            pygame.K_a: "X",
            pygame.K_s: "Y",
            pygame.K_q: "L",
            pygame.K_w: "R",
            pygame.K_RETURN: "START",
            pygame.K_RSHIFT: "SELECT",
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
        }
        if key in key_map:
            self.button_state[key_map[key]] = False

    def get_button_state(self):
        return self.button_state
