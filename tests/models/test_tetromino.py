from src.tetris.models.tetromino import Tetromino


def test_get_cells_uses_current_position_and_shape():
    tetromino = Tetromino("T", x=3, y=5)

    assert tetromino.get_cells() == [(4, 5), (3, 6), (4, 6), (5, 6)]


def test_move_changes_position():
    tetromino = Tetromino("I", x=2, y=3)

    tetromino.move(-1, 0)
    tetromino.move_down()
    tetromino.move(1, 0)

    assert (tetromino.x, tetromino.y) == (2, 4)


def test_rotate_cycles_through_available_shapes():
    tetromino = Tetromino("I")

    assert tetromino.width == 4
    assert tetromino.height == 4

    tetromino.rotate()

    assert tetromino.width == 4
    assert tetromino.height == 4

    tetromino.rotate()

    assert tetromino.width == 4
    assert tetromino.height == 4
