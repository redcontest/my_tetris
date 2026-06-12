"""
Модуль, отвечающий за отрисовку игровой доски и ячеек уже упавших тетромино.
"""
import pygame

from src.tetris.config import (
    BOARD_BACKGROUND_COLOR,
    BOARD_BORDER_COLOR,
    BOARD_BORDER_WIDTH,
    BOARD_CELL_BORDER_RADIUS,
    BOARD_CELL_PADDING,
    BOARD_CELL_SIZE,
    BOARD_GRID_LINE_WIDTH,
    GRID_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TETROMINO_COLORS,
)
from src.tetris.models.board import Board
from src.tetris.models.tetromino import TetrominoType


class BoardRenderer:
    """Класс, отрисовывающий игровое поле."""

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Метод, создающий рендерер игрового поля.

        Args:
            screen (pygame.Surface): поверхность окна для отрисовки.
        """
        self.screen = screen

    def render_board(self, board: Board) -> None:
        """
        Метод, отрисовывающий всю игровую доску (собирает все нужные для этого
        методы).

        Args:
            board (Board): игровая доска.
        """
        board_rect = self.get_board_rect(board)
        # NOTE: замечу, что по моей логике здесь сетка рендерится поверх рамки
        # игровой доски. Это не баг, не недосмотренность и даже не бездумный
        # вайбкодинг, мне реально очень нравится, как это выглядит.
        self._render_board_background(board_rect)
        self._render_board_cells(board, board_rect)

    def get_board_rect(self, board: Board) -> pygame.Rect:
        """
        Метод, вычисляющий прямоугольник (именно объект pygame.Rect) игровой
        доски.

        Args:
            board (Board): игровая доска.

        Returns:
            pygame.Rect: прямоугольник игровой доски.
        """
        board_width = board.width * BOARD_CELL_SIZE
        board_height = board.height * BOARD_CELL_SIZE
        board_left = (SCREEN_WIDTH - board_width) // 2
        board_top = (SCREEN_HEIGHT - board_height) // 2

        return pygame.Rect(board_left, board_top, board_width, board_height)

    def _render_board_background(self, board_rect: pygame.Rect) -> None:
        """
        Служебный метод, отрисовывающий фон и рамку игровой доски.

        Args:
            board_rect (pygame.Rect): прямоугольник игровой доски.
        """
        pygame.draw.rect(self.screen, BOARD_BACKGROUND_COLOR, board_rect)
        pygame.draw.rect(
            self.screen,
            BOARD_BORDER_COLOR,
            board_rect,
            width=BOARD_BORDER_WIDTH
        )

    def _render_board_cells(
            self,
            board: Board,
            board_rect: pygame.Rect,
            ) -> None:
        """
        Служебный метод, отрисовывающий сетку доски и зафиксированные клетки
        тетромино.

        Args:
            board (Board): игровая доска.
            board_rect (pygame.Rect): прямоугольник игровой доски.
        """
        for y in range(board.height):
            for x in range(board.width):
                cell_rect = self.get_cell_rect(
                    board_rect,
                    x,
                    y
                )
                pygame.draw.rect(
                    self.screen,
                    GRID_COLOR,
                    cell_rect,
                    width=BOARD_GRID_LINE_WIDTH
                )

                cell_value = board.get_cell(x, y)
                if cell_value is not None:
                    self.render_cell(cell_value, cell_rect)

    def get_cell_rect(
            self,
            board_rect: pygame.Rect,
            x: int,
            y: int
            ) -> pygame.Rect:
        """
        Метод, вычисляющий прямоугольник клетки доски.

        Args:
            board_rect (pygame.Rect): прямоугольник игровой доски.
            x (int): координата X клетки.
            y (int): координата Y клетки.

        Returns:
            pygame.Rect: прямоугольник клетки доски.
        """
        return pygame.Rect(
            board_rect.left + x * BOARD_CELL_SIZE,
            board_rect.top + y * BOARD_CELL_SIZE,
            BOARD_CELL_SIZE,
            BOARD_CELL_SIZE
        )

    def render_cell(
            self,
            tetromino_type: TetrominoType,
            rect: pygame.Rect
            ) -> None:
        """
        Метод, отрисовывающий одну клетку тетромино.

        Args:
            tetromino_type (TetrominoType): тип тетромино.
            rect (pygame.Rect): прямоугольник клетки.
        """
        color = TETROMINO_COLORS[tetromino_type]
        inner_rect = rect.inflate(-BOARD_CELL_PADDING, -BOARD_CELL_PADDING)
        pygame.draw.rect(
            self.screen,
            color,
            inner_rect,
            border_radius=BOARD_CELL_BORDER_RADIUS
        )
