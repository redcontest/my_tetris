from src.tetris.controllers.game_session import GameSession
from src.tetris.controllers.state import GameState, GravityMode, StateType
from src.tetris.controllers.state import WrapMode


def test_session_syncs_models_to_state_on_creation():
    state = GameState()
    session = GameSession(state)

    assert state.board is session.board
    assert state.score is session.score
    assert state.current_tetromino is session.current_tetromino
    assert state.ghost_tetromino is session.ghost_tetromino
    assert state.gravity_mode == session.gravity_mode
    assert state.wrap_mode == session.wrap_mode


def test_start_resets_models_and_enters_playing_state():
    state = GameState(StateType.GAME_OVER)
    session = GameSession(state)
    session.score.points = 100
    session.board.fill_cell(0, 0, "T")
    session.soft_drop_key_is_pressed = True
    session.start()

    assert state.current == StateType.PLAYING
    assert session.score.points == 0
    assert session.board.get_cell(0, 0) is None
    assert not session.soft_drop_key_is_pressed
    assert state.current_tetromino is session.current_tetromino


def test_set_gravity_mode_syncs_state():
    state = GameState()
    session = GameSession(state)
    session.set_gravity_mode(GravityMode.SAND)

    assert session.gravity_mode == GravityMode.SAND
    assert state.gravity_mode == GravityMode.SAND


def test_set_wrap_mode_syncs_state():
    state = GameState()
    session = GameSession(state)
    session.set_wrap_mode(WrapMode.ON)

    assert session.wrap_mode == WrapMode.ON
    assert state.wrap_mode == WrapMode.ON


def test_spawn_tetromino_places_piece_in_start_position():
    session = GameSession(GameState())
    tetromino = session.spawn_tetromino()

    assert tetromino.x == (session.board.width - tetromino.width) // 2
    assert tetromino.y == 0
