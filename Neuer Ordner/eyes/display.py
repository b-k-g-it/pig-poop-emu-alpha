import pygame

class Display:
    def __init__(self):
        self.screen = pygame.display.set_mode((256, 224))

    def update(self, frame):
        pygame.surfarray.blit_array(self.screen, frame)
        pygame.display.flip()
