"""
Модуль, хранящий модели и настройки текущей игровой партии.
"""
from src.tetris.controllers.state import (
    GameState,
    GravityMode,
    StateType,
    WrapMode,
)
from src.tetris.models.board import Board
from src.tetris.models.score import Score
from src.tetris.models.tetromino import Tetromino
from src.tetris.models.tetromino_bag import TetrominoBag


class GameSession:
    """Объект, который хранит логические данные для обработки сессии игры."""

    def __init__(self, state: GameState) -> None:
        """
        Метод, создающий игровую сессию.

        Args:
            state (GameState): объект состояния игры.
        """
        self.state = state
        self.board = Board()
        self.score = Score()
        self.tetromino_bag = TetrominoBag()
        self.current_tetromino = self.spawn_tetromino()
        self.ghost_tetromino: Tetromino | None = None

        self.fall_timer: float = 0.0
        self.sand_gravity_timer: float = 0.0

        self.soft_drop_key_is_pressed: bool = False
        self.gravity_mode: GravityMode = GravityMode.STANDARD
        self.wrap_mode: WrapMode = WrapMode.OFF

        self.sync_state_models()

    def reset(self) -> None:
        """Метод, сбрасывающий игровую сессию для новой партии."""
        self.board.reset()
        self.score.reset()
        self.tetromino_bag.reset()
        self.current_tetromino = self.spawn_tetromino()
        self.ghost_tetromino = None
        self.fall_timer = 0.0
        self.sand_gravity_timer = 0.0
        self.soft_drop_key_is_pressed = False
        self.sync_state_models()

    def start(self) -> None:
        """Метод, запускающий новую игровую партию."""
        self.reset()
        self.state.set_state(StateType.PLAYING)

    def set_gravity_mode(self, gravity_mode: GravityMode) -> None:
        """
        Метод, меняющий режим гравитации. Стандартный режим - поведение, как в
        классическом тетрисе. Песочный - когда каждый блок осыпается независимо
        от тетромино.

        Args:
            gravity_mode (GravityMode): новый режим гравитации.
        """
        self.gravity_mode = gravity_mode
        self.sync_state_models()

    def set_wrap_mode(self, wrap_mode: WrapMode) -> None:
        """
        Метод, меняющий режим горизонтального сдвига для тетромино. Если режим
        включен, тетромино можно двигать вправо и влево безгранично. При этом
        часть тетромино, которая уползла за край доски, появляется с другого
        края.

        Args:
            wrap_mode (WrapMode): режим горизонтального сдвига, который надо
                установить.
        """
        self.wrap_mode = wrap_mode
        self.sync_state_models()

    def spawn_tetromino(self) -> Tetromino:
        """
        Метод, создающий новое тетромино в стартовой позиции.

        Returns:
            Tetromino: новое тетромино по центру верхней части доски.
        """
        tetromino = self.tetromino_bag.get_next()
        tetromino.x = (self.board.width - tetromino.width) // 2
        tetromino.y = 0
        return tetromino

    def sync_state_models(self) -> None:
        """Метод, фиксирующий состояние игры для передачи в рендеринг."""
        self.state.board = self.board
        self.state.score = self.score
        self.state.current_tetromino = self.current_tetromino
        self.state.ghost_tetromino = self.ghost_tetromino
        self.state.gravity_mode = self.gravity_mode
        self.state.wrap_mode = self.wrap_mode
