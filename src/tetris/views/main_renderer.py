"""
Модуль, орекстрирующий рендеринг игры.
"""
from collections.abc import Callable
import pygame

from src.tetris.config import BACKGROUND_COLOR
from src.tetris.controllers.state import GameState, StateType
from src.tetris.views.board_renderer import BoardRenderer
from src.tetris.views.tetromino_renderer import TetrominoRenderer
from src.tetris.views.ui_renderer import UiRenderer


type RenderHandler = Callable[[GameState], None]


class MainRenderer:
    """Главный рендерер, выбирающий нужный экран для отрисовки."""

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Метод, создающий главный рендерер игры.

        Args:
            screen (pygame.Surface): поверхность окна для отрисовки.
        """
        self.screen = screen
        self.ui_renderer = UiRenderer(screen)
        self.board_renderer = BoardRenderer(screen)
        self.tetromino_renderer = TetrominoRenderer(screen)
        self.render_handlers: dict[StateType, RenderHandler] = {
            StateType.MENU: self._render_menu,
            StateType.SETTINGS: self._render_settings,
            StateType.PLAYING: self._render_playing,
            StateType.PAUSED: self._render_pause,
            StateType.GAME_OVER: self._render_game_over,
        }

    def draw(self, state: GameState) -> None:
        """
        Метод, отрисовывающий кадр по текущему состоянию игры.

        Args:
            state (GameState): текущее состояние игры.
        """
        self.screen.fill(BACKGROUND_COLOR)

        handler = self.render_handlers.get(state.current)
        if handler is not None:
            handler(state)

        pygame.display.flip()

    def _render_menu(self, state: GameState) -> None:
        """
        Служебный метод, отрисовывающий экран главного меню.

        Args:
            state (GameState): текущее состояние игры.
        """
        self.ui_renderer.render_menu()

    def _render_settings(self, state: GameState) -> None:
        """
        Служебный метод, отрисовывающий экран настроек.

        Args:
            state (GameState): текущее состояние игры.
        """
        self.ui_renderer.render_settings(state)

    def _render_playing(self, state: GameState) -> None:
        """
        Служебный метод, отрисовывающий игровой экран.

        Args:
            state (GameState): текущее состояние игры.
        """
        if state.board is not None:
            self.board_renderer.render_board(state.board)
            self.tetromino_renderer.render_tetrominoes(
                state.board,
                state.ghost_tetromino,
                state.current_tetromino,
                state.wrap_mode
            )
            self.ui_renderer.render_game_info(state)

    def _render_pause(self, state: GameState) -> None:
        """
        Служебный метод, отрисовывающий игру и слой паузы поверх нее.

        Args:
            state (GameState): текущее состояние игры.
        """
        self._render_playing(state)
        self.ui_renderer.render_pause_overlay()

    def _render_game_over(self, state: GameState) -> None:
        """
        Служебный метод, отрисовывающий экран проигрыша.

        Args:
            state (GameState): текущее состояние игры.
        """
        self.ui_renderer.render_game_over(state)
