from src.tetris.controllers.state import (
    GameState,
    GravityMode,
    StateType,
    WrapMode,
)


def test_initial_state_has_default_modes():
    state = GameState()

    assert state.current == StateType.MENU
    assert state.gravity_mode == GravityMode.STANDARD
    assert state.wrap_mode == WrapMode.OFF
    assert state.ghost_tetromino is None


def test_state_can_be_changed():
    state = GameState()

    state.set_state(StateType.PLAYING)
    assert state.current == StateType.PLAYING


def test_is_quit_matches_quit_state():
    state = GameState()

    state.set_state(StateType.QUIT)
    assert state.is_quit
