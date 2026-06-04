"""
Модуль, описывающий конечный автомат состояний игры.
"""
from enum import Enum, auto

from src.tetris.models.board import Board
from src.tetris.models.score import Score
from src.tetris.models.tetromino import Tetromino


class StateType(Enum):
    """Типы состояний, в которых может находиться игра."""
    MENU = auto()
    SETTINGS = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    QUIT = auto()


class WrapMode(Enum):
    """Варианты горизонтального переноса тетромино через границы доски по X."""
    OFF = auto()
    ON = auto()


class GravityMode(Enum):
    """Варианты гравитации игры."""
    STANDARD = auto()
    SAND = auto()


class GameState:
    """Конечный автомат, управляющий текущим состоянием игры."""
    def __init__(self, current: StateType = StateType.MENU) -> None:
        """
        Метод, создающий состояние игры.

        Args:
            current (StateType): начальное состояние игры.
        """
        self.current: StateType = current
        self.gravity_mode: GravityMode = GravityMode.STANDARD
        self.wrap_mode: WrapMode = WrapMode.OFF
        self.board: Board | None = None
        self.score: Score | None = None
        self.current_tetromino: Tetromino | None = None
        self.ghost_tetromino: Tetromino | None = None

    def set_state(self, state: StateType) -> None:
        """
        Метод, переводящий игру в указанное состояние.

        Args:
            state (StateType): состояние, в которое нужно перейти.
        """
        self.current = state

    @property
    def is_quit(self) -> bool:
        """
        Свойство, проверяющее, нужно ли завершить игру.

        Returns:
            bool: True, если игру нужно завершить, False в противном случае.
        """
        return self.current == StateType.QUIT
