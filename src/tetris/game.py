import pygame
import sys

from src.tetris.controllers.controller import Controller
from src.tetris.views.renderer import Renderer
from src.tetris.config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.controller = Controller()
        self.renderer = Renderer()
        self.running = True

    def start(self):
        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000.0
            self.handle_input()
            self.controller.update()
            self.renderer.draw()
        self.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.controller.handle_event(event)

    def quit(self):
        pygame.quit()
        sys.exit()
