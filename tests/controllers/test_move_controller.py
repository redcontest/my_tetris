from src.tetris.controllers.game_session import GameSession
from src.tetris.controllers.move_controller import MoveController
from src.tetris.controllers.state import GameState, StateType, WrapMode
from src.tetris.models.tetromino import Tetromino


def make_move_controller() -> tuple[GameSession, MoveController]:
    state = GameState(StateType.PLAYING)
    session = GameSession(state)
    return session, MoveController(session)


def test_current_tetromino_moves_only_when_target_cell_is_valid():
    session, move_controller = make_move_controller()
    session.current_tetromino = Tetromino("O", x=0, y=0)

    move_controller.move_current_tetromino(-1, 0)
    assert session.current_tetromino.x == 0

    move_controller.move_current_tetromino(1, 0)
    assert session.current_tetromino.x == 1


def test_tetromino_moves_partly_past_left_edge_when_wrap_mode_is_on():
    session, move_controller = make_move_controller()
    session.wrap_mode = WrapMode.ON
    session.current_tetromino = Tetromino("O", x=0, y=0)
    move_controller.move_current_tetromino(-1, 0)

    assert session.current_tetromino.x == -1


def test_tetromino_moves_partly_past_right_edge_when_wrap_mode_is_on():
    session, move_controller = make_move_controller()
    session.wrap_mode = WrapMode.ON
    session.current_tetromino = Tetromino("O", x=8, y=0)
    move_controller.move_current_tetromino(1, 0)

    assert session.current_tetromino.x == 9


def test_tetromino_does_not_move_past_edge_when_wrapped_cell_is_blocked():
    session, move_controller = make_move_controller()
    session.wrap_mode = WrapMode.ON
    session.current_tetromino = Tetromino("O", x=8, y=0)
    session.board.fill_cell(0, 0, "T")
    move_controller.move_current_tetromino(1, 0)

    assert session.current_tetromino.x == 8


def test_wrapped_tetromino_is_locked_on_both_horizontal_sides():
    session, move_controller = make_move_controller()
    session.wrap_mode = WrapMode.ON
    session.current_tetromino = Tetromino("O", x=9, y=18)
    move_controller.hard_drop_current_tetromino()

    assert session.board.get_cell(9, 18) == "O"
    assert session.board.get_cell(0, 18) == "O"
    assert session.board.get_cell(9, 19) == "O"
    assert session.board.get_cell(0, 19) == "O"


def test_rotation_near_wall_uses_wall_kick():
    session, move_controller = make_move_controller()
    tetromino = Tetromino("T", x=-1, y=0)
    tetromino.rotate()

    session.current_tetromino = tetromino
    move_controller.rotate_current_tetromino()

    assert session.current_tetromino.rotation == 2
    assert session.current_tetromino.x == 0


def test_i_tetromino_rotates_from_right_wall_with_wall_kick():
    session, move_controller = make_move_controller()
    tetromino = Tetromino("I", x=7, y=0)
    tetromino.rotate()

    session.current_tetromino = tetromino
    move_controller.rotate_current_tetromino()

    assert session.current_tetromino.rotation == 2
    assert session.current_tetromino.x == 6


def test_move_controller_syncs_ghost_tetromino_to_state():
    session, move_controller = make_move_controller()
    session.current_tetromino = Tetromino("T", x=4, y=0)

    move_controller.update_ghost_tetromino()
    session.sync_state_models()

    assert session.ghost_tetromino is not None
    assert session.state.ghost_tetromino is session.ghost_tetromino
    assert session.ghost_tetromino is not session.current_tetromino
    assert session.ghost_tetromino.type == session.current_tetromino.type
    assert session.ghost_tetromino.x == session.current_tetromino.x
    assert (
        session.ghost_tetromino.rotation
        == session.current_tetromino.rotation
    )
    assert session.ghost_tetromino.y > session.current_tetromino.y


def test_ghost_tetromino_is_none_when_current_tetromino_cannot_fall():
    session, move_controller = make_move_controller()
    session.current_tetromino = Tetromino("O", x=4, y=18)

    move_controller.update_ghost_tetromino()
    session.sync_state_models()

    assert session.ghost_tetromino is None
    assert session.state.ghost_tetromino is None


def test_hard_drop_locks_tetromino_and_adds_drop_points():
    session, move_controller = make_move_controller()
    session.current_tetromino = Tetromino("O", x=0, y=0)
    move_controller.hard_drop_current_tetromino()

    assert session.score.points == 36
    assert session.board.get_cell(0, 18) == "O"
    assert session.board.get_cell(1, 18) == "O"
    assert session.board.get_cell(0, 19) == "O"
    assert session.board.get_cell(1, 19) == "O"


def test_locking_tetromino_sets_game_over_when_next_piece_cannot_spawn():
    session, move_controller = make_move_controller()
    session.current_tetromino = Tetromino("O", x=0, y=18)
    session.board.fill_cell(4, 0, "T")
    session.spawn_tetromino = lambda: Tetromino("O", x=4, y=0)
    move_controller.lock_current_tetromino()

    assert session.state.current == StateType.GAME_OVER
