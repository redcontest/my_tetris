"""
Модуль, отвечающий за запуск и главный цикл игры.

Описание зоны ответственности модуля:
Модуль создает окно pygame, связывает состояние, контроллер и рендерер, а также
управляет главным циклом приложения.

Модуль НЕ ОТВЕЧАЕТ за правила тетриса, отрисовку отдельных элементов и
обработку конкретных игровых действий.
"""
import sys
from pathlib import Path
import pygame

from src.tetris.controllers.event_controller import EventController
from src.tetris.controllers.state import GameState
from src.tetris.config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from src.tetris.views.main_renderer import MainRenderer


ICON_PATH = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "icons"
    / "icon.png"
)


class Game:
    """Класс, описывающий приложение игры и его главный цикл."""
    def __init__(self) -> None:
        """Метод, создающий окно игры и основные объекты приложения."""
        pygame.init()
        pygame.display.set_caption("Gravity Tetris")
        pygame.display.set_icon(pygame.image.load(str(ICON_PATH)))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.controller = EventController(self.state)
        self.renderer = MainRenderer(self.screen)
        self.running = True

    def start(self) -> None:
        """Метод, запускающий главный цикл игры."""
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000.0
            self._handle_input()
            self.controller.update(delta_time)
            if self.state.is_quit:
                self.running = False
                continue
            self.renderer.draw(self.state)
        self._quit()

    def _handle_input(self) -> None:
        """Метод, передающий события pygame в контроллер игры."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.controller.handle_event(event)

    def _quit(self) -> None:
        """Метод, завершающий работу pygame и закрывающий приложение."""
        pygame.quit()
        sys.exit()
