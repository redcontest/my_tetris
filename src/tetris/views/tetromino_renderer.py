"""
Модуль, отвечающий за отрисовку текущего тетромино и ghost piece.
"""
import pygame

from src.tetris.config import (
    BOARD_CELL_BORDER_RADIUS,
    BOARD_CELL_PADDING,
    GHOST_ALPHA,
    TETROMINO_COLORS,
)
from src.tetris.controllers.state import WrapMode
from src.tetris.models.board import Board
from src.tetris.models.tetromino import Tetromino, TetrominoType
from src.tetris.views.board_renderer import BoardRenderer


class TetrominoRenderer:
    """Класс, отрисовывающий текущее тетромино и ghost piece."""

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Метод, создающий рендерер тетромино.

        Args:
            screen (pygame.Surface): поверхность окна для отрисовки.
        """
        self.screen = screen
        self.board_renderer = BoardRenderer(screen)

    def render_tetrominoes(
            self,
            board: Board,
            ghost_tetromino: Tetromino | None,
            current_tetromino: Tetromino | None,
            wrap_mode: WrapMode
            ) -> None:
        """
        Метод, отрисовывающий призрачное и текущее тетромино.

        Args:
            board (Board): игровая доска.
            ghost_tetromino (Tetromino | None): призрачное тетромино.
            current_tetromino (Tetromino | None): текущее тетромино.
            wrap_mode (WrapMode): установленный режим горизонтального сдвига.
        """
        board_rect = self.board_renderer.get_board_rect(board)
        self._render_ghost_tetromino(
            board,
            ghost_tetromino,
            wrap_mode,
            board_rect
        )
        self._render_current_tetromino(
            board,
            current_tetromino,
            wrap_mode,
            board_rect
        )

    def _render_current_tetromino(
            self,
            board: Board,
            current_tetromino: Tetromino | None,
            wrap_mode: WrapMode,
            board_rect: pygame.Rect
            ) -> None:
        """
        Служебный метод, отрисовывающий текущее тетромино.

        Args:
            board (Board): игровая доска.
            current_tetromino (Tetromino | None): текущее тетромино.
            wrap_mode (WrapMode): текущий режим горизонтального сдвига.
            board_rect (pygame.Rect): прямоугольник игровой доски.
        """
        if current_tetromino is not None:
            for x, y in current_tetromino.get_cells():
                rendered_x = self._get_rendered_cell_x(board, x, wrap_mode)
                cell_rect = self.board_renderer.get_cell_rect(
                    board_rect,
                    rendered_x,
                    y
                )
                self.board_renderer.render_cell(
                    current_tetromino.type,
                    cell_rect
                )

    def _render_ghost_tetromino(
            self,
            board: Board,
            ghost_tetromino: Tetromino | None,
            wrap_mode: WrapMode,
            board_rect: pygame.Rect
            ) -> None:
        """
        Служебный метод, отрисовывающий призрачную позицию тетромино.

        Args:
            board (Board): игровая доска.
            ghost_tetromino (Tetromino | None): призрачное тетромино.
            wrap_mode (WrapMode): текущий режим горизонтального сдвига.
            board_rect (pygame.Rect): прямоугольник игровой доски.
        """
        if ghost_tetromino is not None:
            for x, y in ghost_tetromino.get_cells():
                rendered_x = self._get_rendered_cell_x(board, x, wrap_mode)
                cell_rect = self.board_renderer.get_cell_rect(
                    board_rect,
                    rendered_x,
                    y
                )
                self._render_ghost_cell(ghost_tetromino.type, cell_rect)

    def _render_ghost_cell(
            self,
            tetromino_type: TetrominoType,
            rect: pygame.Rect
            ) -> None:
        """
        Служебный метод, отрисовывающий призрачную клетку тетромино.

        Args:
            tetromino_type (TetrominoType): тип тетромино.
            rect (pygame.Rect): прямоугольник клетки.
        """
        color = TETROMINO_COLORS[tetromino_type]
        inner_rect = rect.inflate(-BOARD_CELL_PADDING, -BOARD_CELL_PADDING)
        cell_surface = pygame.Surface(inner_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            cell_surface,
            (*color, GHOST_ALPHA),
            cell_surface.get_rect(),
            border_radius=BOARD_CELL_BORDER_RADIUS
        )
        self.screen.blit(cell_surface, inner_rect)

    def _get_rendered_cell_x(
            self,
            board: Board,
            x: int,
            wrap_mode: WrapMode
            ) -> int:
        """
        Служебный метод, вычисляющий X клетки для отрисовки.

        Args:
            board (Board): игровая доска.
            x (int): исходная координата X.
            wrap_mode (WrapMode): текущий режим горизонтального переноса.

        Returns:
            int: координата X, по которой нужно нарисовать клетку.
        """
        if wrap_mode == WrapMode.ON:
            return x % board.width
        return x
