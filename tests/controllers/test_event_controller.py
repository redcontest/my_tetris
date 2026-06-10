import pygame

from src.tetris.config import (
    GAME_OVER_MENU_Y,
    GAME_OVER_RETRY_Y,
    MENU_PLAY_Y,
    MENU_SETTINGS_Y,
    PAUSE_CONTINUE_Y,
    PAUSE_MENU_Y,
    SCREEN_WIDTH,
    SETTINGS_SAND_Y,
    SETTINGS_TOGGLE_BUTTON_WIDTH,
    SETTINGS_WRAP_Y,
    SAND_GRAVITY_DELAY,
    SOFT_FALL_DELAY,
    WRAP_BUTTON_GAP,
)
from src.tetris.controllers.event_controller import (
    A_KEY,
    D_KEY,
    EventController,
    S_KEY,
    W_KEY,
)
from src.tetris.controllers.state import GameState, GravityMode, StateType
from src.tetris.controllers.state import WrapMode
from src.tetris.models.tetromino import Tetromino


def make_event_controller(
        state_type: StateType = StateType.MENU
        ) -> tuple[GameState, EventController]:
    state = GameState(state_type)
    return state, EventController(state)


def test_menu_play_button_starts_game():
    state, controller = make_event_controller()

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(SCREEN_WIDTH // 2, MENU_PLAY_Y)
    )

    controller.handle_event(event)

    assert state.current == StateType.PLAYING


def test_escape_from_settings_returns_to_menu():
    state, controller = make_event_controller(StateType.SETTINGS)

    controller.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    )

    assert state.current == StateType.MENU


def test_menu_settings_button_opens_settings():
    state, controller = make_event_controller()

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(SCREEN_WIDTH // 2, MENU_SETTINGS_Y)
    )

    controller.handle_event(event)

    assert state.current == StateType.SETTINGS


def test_settings_button_changes_gravity_mode():
    state, controller = make_event_controller(StateType.SETTINGS)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(SCREEN_WIDTH // 2, SETTINGS_SAND_Y)
    )

    controller.handle_event(event)

    assert state.gravity_mode == GravityMode.SAND


def test_settings_button_changes_wrap_mode():
    state, controller = make_event_controller(StateType.SETTINGS)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(
            SCREEN_WIDTH // 2
            + SETTINGS_TOGGLE_BUTTON_WIDTH // 2
            + WRAP_BUTTON_GAP // 2,
            SETTINGS_WRAP_Y
        )
    )

    controller.handle_event(event)

    assert controller.session.wrap_mode == WrapMode.ON
    assert state.wrap_mode == WrapMode.ON


def test_settings_button_can_turn_wrap_mode_off():
    state, controller = make_event_controller(StateType.SETTINGS)
    controller.session.wrap_mode = WrapMode.ON
    controller.session.sync_state_models()

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(
            SCREEN_WIDTH // 2
            - SETTINGS_TOGGLE_BUTTON_WIDTH // 2
            - WRAP_BUTTON_GAP // 2,
            SETTINGS_WRAP_Y
        )
    )

    controller.handle_event(event)

    assert controller.session.wrap_mode == WrapMode.OFF
    assert state.wrap_mode == WrapMode.OFF


def test_pause_continue_button_returns_to_playing_state():
    state, controller = make_event_controller(StateType.PAUSED)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(SCREEN_WIDTH // 2, PAUSE_CONTINUE_Y)
    )

    controller.handle_event(event)

    assert state.current == StateType.PLAYING


def test_pause_menu_button_returns_to_menu_state():
    state, controller = make_event_controller(StateType.PAUSED)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(SCREEN_WIDTH // 2, PAUSE_MENU_Y)
    )

    controller.handle_event(event)

    assert state.current == StateType.MENU


def test_game_over_retry_button_starts_new_game():
    state, controller = make_event_controller(StateType.GAME_OVER)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(SCREEN_WIDTH // 2, GAME_OVER_RETRY_Y)
    )

    controller.handle_event(event)

    assert state.current == StateType.PLAYING


def test_game_over_menu_button_returns_to_menu():
    state, controller = make_event_controller(StateType.GAME_OVER)

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(SCREEN_WIDTH // 2, GAME_OVER_MENU_Y)
    )

    controller.handle_event(event)

    assert state.current == StateType.MENU


def test_physical_a_and_d_move_tetromino_regardless_layout():
    _, controller = make_event_controller(StateType.PLAYING)
    controller.session.current_tetromino = Tetromino("O", x=4, y=0)

    controller.handle_event(
        pygame.event.Event(
            pygame.KEYDOWN,
            key=0,
            scancode=A_KEY
        )
    )
    assert controller.session.current_tetromino.x == 3

    controller.handle_event(
        pygame.event.Event(
            pygame.KEYDOWN,
            key=0,
            scancode=D_KEY
        )
    )
    assert controller.session.current_tetromino.x == 4


def test_physical_s_uses_soft_drop_regardless_layout():
    _, controller = make_event_controller(StateType.PLAYING)
    controller.session.current_tetromino = Tetromino("O", x=0, y=0)

    controller.handle_event(
        pygame.event.Event(
            pygame.KEYDOWN,
            key=0,
            scancode=S_KEY
        )
    )
    assert controller.session.current_tetromino.y == 1

    controller.update(SOFT_FALL_DELAY)
    assert controller.session.current_tetromino.y == 2

    controller.handle_event(
        pygame.event.Event(
            pygame.KEYUP,
            key=0,
            scancode=S_KEY
        )
    )
    controller.update(SOFT_FALL_DELAY)
    assert controller.session.current_tetromino.y == 2


def test_physical_w_rotates_tetromino_regardless_layout():
    _, controller = make_event_controller(StateType.PLAYING)
    controller.session.current_tetromino = Tetromino("T", x=4, y=0)

    controller.handle_event(
        pygame.event.Event(
            pygame.KEYDOWN,
            key=0,
            scancode=W_KEY
        )
    )

    assert controller.session.current_tetromino.rotation == 1


def test_fall_delay_gets_shorter_with_level_but_has_minimum():
    _, controller = make_event_controller(StateType.PLAYING)
    controller.session.current_tetromino = Tetromino("O", x=0, y=0)

    controller.update(0.99)
    assert controller.session.current_tetromino.y == 0

    controller.update(0.011)
    assert controller.session.current_tetromino.y == 1

    controller.session.current_tetromino = Tetromino("O", x=0, y=0)
    controller.session.fall_timer = 0.0
    controller.session.score.level = 5

    controller.update(0.32)
    assert controller.session.current_tetromino.y == 0

    controller.update(0.02)
    assert controller.session.current_tetromino.y == 1

    controller.session.current_tetromino = Tetromino("O", x=0, y=0)
    controller.session.fall_timer = 0.0
    controller.session.score.level = 100

    controller.update(0.04)
    assert controller.session.current_tetromino.y == 0

    controller.update(0.011)
    assert controller.session.current_tetromino.y == 1


def test_sand_gravity_mode_moves_board_cells_during_update():
    _, controller = make_event_controller(StateType.PLAYING)

    controller.session.gravity_mode = GravityMode.SAND
    controller.session.current_tetromino = Tetromino("O", x=4, y=0)
    controller.session.board.fill_cell(0, 0, "T")

    controller.update(SAND_GRAVITY_DELAY)

    assert controller.session.board.get_cell(0, 0) is None
    assert controller.session.board.get_cell(0, 1) == "T"
