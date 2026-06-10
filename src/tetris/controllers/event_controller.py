"""
Модуль, отвечающий за обработку событий, состояний и обновление игры.
"""
from collections.abc import Callable
import pygame

from src.tetris.config import (
    GAME_OVER_MENU_Y,
    GAME_OVER_RETRY_Y,
    MENU_BUTTON_HEIGHT,
    MENU_BUTTON_WIDTH,
    MENU_PLAY_Y,
    MENU_QUIT_Y,
    MENU_SETTINGS_Y,
    MIN_FALL_DELAY,
    PAUSE_CONTINUE_Y,
    PAUSE_MENU_Y,
    SAND_GRAVITY_DELAY,
    SCREEN_WIDTH,
    SETTINGS_BACK_Y,
    SETTINGS_SAND_Y,
    SETTINGS_STANDARD_Y,
    SETTINGS_TOGGLE_BUTTON_WIDTH,
    SETTINGS_WRAP_Y,
    SOFT_FALL_DELAY,
    TETRIS_GRAVITY_BASE,
    TETRIS_GRAVITY_STEP,
    WRAP_BUTTON_GAP,
)
from src.tetris.controllers.game_session import GameSession
from src.tetris.controllers.move_controller import MoveController
from src.tetris.controllers.state import (
    GameState,
    GravityMode,
    StateType,
    WrapMode,
)


type EventHandler = Callable[[pygame.event.Event], None]
type UpdateHandler = Callable[[float], None]
type EventHandlers = dict[StateType, EventHandler]
type UpdateHandlers = dict[StateType, UpdateHandler]


A_KEY = 4
D_KEY = 7
S_KEY = 22
W_KEY = 26


class EventController:
    """Контроллер, обрабатывающий события и обновление игры."""

    def __init__(
            self,
            state: GameState,
            session: GameSession | None = None,
            move_controller: MoveController | None = None
            ) -> None:
        """
        Метод, создающий контроллер событий.

        Args:
            state (GameState): объект состояния игры.
            session (GameSession | None): объект текущей игровой сессии.
            move_controller (MoveController | None): контроллер движения
                тетромино.
        """
        self.session = session or GameSession(state)
        self.move_controller = move_controller or MoveController(self.session)

        self.event_handlers: EventHandlers = {
            StateType.MENU: self._handle_menu_event,
            StateType.SETTINGS: self._handle_settings_event,
            StateType.PLAYING: self._handle_playing_event,
            StateType.PAUSED: self._handle_paused_event,
            StateType.GAME_OVER: self._handle_game_over_event,
        }
        self.update_handlers: UpdateHandlers = {
            StateType.PLAYING: self._update_playing,
        }

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Метод, обрабатывающий одно событие игры.

        Args:
            event (pygame.event.Event): событие, которое нужно обработать.
        """
        handler = self.event_handlers.get(self.session.state.current)

        if handler is not None:
            handler(event)

    def update(self, delta_time: float) -> None:
        """
        Метод, обновляющий игровую логику каждый кадр.

        Args:
            delta_time (float): время в секундах, прошедшее с прошлого кадра.
        """
        handler = self.update_handlers.get(self.session.state.current)

        if handler is not None:
            handler(delta_time)

    def _handle_menu_event(self, event: pygame.event.Event) -> None:
        """
        Служебный метод, обрабатывающий события главного меню.

        Args:
            event (pygame.event.Event): событие, которое нужно обработать.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._point_is_in_button(event.pos, MENU_PLAY_Y):
                self.session.start()
                self.move_controller.update_ghost_tetromino()
                self.session.sync_state_models()
            elif self._point_is_in_button(event.pos, MENU_SETTINGS_Y):
                self.session.state.set_state(StateType.SETTINGS)
            elif self._point_is_in_button(event.pos, MENU_QUIT_Y):
                self.session.state.set_state(StateType.QUIT)

    def _handle_settings_event(self, event: pygame.event.Event) -> None:
        """
        Служебный метод, обрабатывающий события экрана настроек.

        Args:
            event (pygame.event.Event): событие, которое нужно обработать.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.session.state.set_state(StateType.MENU)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._point_is_in_button(event.pos, SETTINGS_STANDARD_Y):
                self.session.set_gravity_mode(GravityMode.STANDARD)
            elif self._point_is_in_button(event.pos, SETTINGS_SAND_Y):
                self.session.set_gravity_mode(GravityMode.SAND)
            elif self._point_is_in_button(event.pos, SETTINGS_BACK_Y):
                self.session.state.set_state(StateType.MENU)

            elif self._point_is_in_wrap_button(
                event.pos,
                SETTINGS_WRAP_Y,
                is_left_button=True
                    ):
                self.session.set_wrap_mode(WrapMode.OFF)
            elif self._point_is_in_wrap_button(
                event.pos,
                SETTINGS_WRAP_Y,
                is_left_button=False
                    ):
                self.session.set_wrap_mode(WrapMode.ON)

    def _handle_playing_event(self, event: pygame.event.Event) -> None:
        """
        Служебный метод, обрабатывающий события во время игрового процесса.

        Args:
            event (pygame.event.Event): событие, которое нужно обработать.
        """
        scancode = getattr(event, "scancode", None)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.session.soft_drop_key_is_pressed = False
                self.session.state.set_state(StateType.PAUSED)
            elif event.key == pygame.K_LEFT or scancode == A_KEY:
                self.move_controller.move_current_tetromino(-1, 0)
            elif event.key == pygame.K_RIGHT or scancode == D_KEY:
                self.move_controller.move_current_tetromino(1, 0)
            elif event.key == pygame.K_DOWN or scancode == S_KEY:
                self.session.soft_drop_key_is_pressed = True
                self.move_controller.soft_drop_current_tetromino()
            elif event.key == pygame.K_SPACE:
                self.move_controller.hard_drop_current_tetromino()
            elif event.key == pygame.K_UP or scancode == W_KEY:
                self.move_controller.rotate_current_tetromino()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or scancode == S_KEY:
                self.session.soft_drop_key_is_pressed = False

    def _handle_paused_event(self, event: pygame.event.Event) -> None:
        """
        Служебный метод, обрабатывающий события во время паузы.

        Args:
            event (pygame.event.Event): событие, которое нужно обработать.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.session.state.set_state(StateType.PLAYING)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._point_is_in_button(event.pos, PAUSE_CONTINUE_Y):
                self.session.state.set_state(StateType.PLAYING)
            elif self._point_is_in_button(event.pos, PAUSE_MENU_Y):
                self.session.state.set_state(StateType.MENU)

    def _handle_game_over_event(self, event: pygame.event.Event) -> None:
        """
        Служебный метод, обрабатывающий события экрана проигрыша.

        Args:
            event (pygame.event.Event): событие, которое нужно обработать.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.session.start()
                self.move_controller.update_ghost_tetromino()
                self.session.sync_state_models()
            elif event.key == pygame.K_ESCAPE:
                self.session.state.set_state(StateType.MENU)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._point_is_in_button(event.pos, GAME_OVER_RETRY_Y):
                self.session.start()
                self.move_controller.update_ghost_tetromino()
                self.session.sync_state_models()
            elif self._point_is_in_button(event.pos, GAME_OVER_MENU_Y):
                self.session.state.set_state(StateType.MENU)

    def _update_playing(self, delta_time: float) -> None:
        """
        Служебный метод, обновляющий игровой процесс.

        Args:
            delta_time (float): время в секундах, прошедшее с прошлого кадра.
        """
        self.session.fall_timer += delta_time
        fall_delay = (
            SOFT_FALL_DELAY
            if self.session.soft_drop_key_is_pressed
            else self._fall_delay
        )

        if self.session.fall_timer >= fall_delay:
            if self.session.soft_drop_key_is_pressed:
                self.move_controller.soft_drop_current_tetromino()
            else:
                self.move_controller.move_current_tetromino_down()
            self.session.fall_timer = 0.0

        self._update_sand_gravity(delta_time)

    def _update_sand_gravity(self, delta_time: float) -> None:
        """
        Служебный метод, реализующий песочное осыпание.

        Args:
            delta_time (float): время в секундах, прошедшее с прошлого кадра.
        """
        if self.session.gravity_mode != GravityMode.SAND:
            return

        self.session.sand_gravity_timer += delta_time

        if self.session.sand_gravity_timer < SAND_GRAVITY_DELAY:
            return

        self.session.sand_gravity_timer = 0.0
        blocked_cells = {
            (cell_x % self.session.board.width, cell_y) for cell_x, cell_y in
            self.session.current_tetromino.get_cells()
        }

        if self.session.board.apply_sand_gravity_step(blocked_cells):
            cleared_lines_count = self.session.board.clear_full_lines()
            self.session.score.add_cleared_lines(cleared_lines_count)
            self.move_controller.update_ghost_tetromino()
            self.session.sync_state_models()

    @property
    def _fall_delay(self) -> float:
        """
        Служебное свойство, вычисляющее задержку падения по текущему уровню.

        Returns:
            float: задержка между шагами падения в секундах.
        """
        level_index = self.session.score.level - 1
        gravity_base = TETRIS_GRAVITY_BASE - level_index * TETRIS_GRAVITY_STEP
        fall_delay = gravity_base ** level_index
        return max(MIN_FALL_DELAY, fall_delay)

    def _point_is_in_button(
            self,
            pos: tuple[int, int],
            center_y: int
            ) -> bool:
        """
        Служебный метод, проверяющий попадание курсора в кнопку.

        Args:
            pos (tuple[int, int]): координаты проверяемой точки курсора.
            center_y (int): координата Y центра кнопки.

        Returns:
            bool: True, если точка находится внутри кнопки, False в противном
                случае.
        """
        rect = pygame.Rect(0, 0, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        rect.center = (SCREEN_WIDTH // 2, center_y)
        return rect.collidepoint(pos)

    def _point_is_in_wrap_button(
            self,
            pos: tuple[int, int],
            center_y: int,
            is_left_button: bool
            ) -> bool:
        """
        Служебный метод, проверяющий попадание курсора в wrap-кнопку.

        Args:
            pos (tuple[int, int]): координаты проверяемой точки.
            center_y (int): координата Y центра кнопки.
            is_left_button (bool): True для левой кнопки, False в противном
                случае.

        Returns:
            bool: True, если точка находится внутри кнопки, False в противном
                случае.
        """
        center_offset = (
            SETTINGS_TOGGLE_BUTTON_WIDTH // 2 + WRAP_BUTTON_GAP // 2
        )
        center_x = (
            SCREEN_WIDTH // 2 - center_offset
            if is_left_button
            else SCREEN_WIDTH // 2 + center_offset
        )
        rect = pygame.Rect(
            0,
            0,
            SETTINGS_TOGGLE_BUTTON_WIDTH,
            MENU_BUTTON_HEIGHT
        )
        rect.center = (center_x, center_y)
        return rect.collidepoint(pos)
