import pytest

from src.tetris.models.board import Board
from src.tetris.models.tetromino import Tetromino


def test_fill_get_and_empty_cell_checks():
    board = Board(width=4, height=4)

    assert board.cell_is_empty(1, 1)
    board.fill_cell(1, 1, "T")

    assert board.get_cell(1, 1) == "T"
    assert not board.cell_is_empty(1, 1)


def test_cell_access_outside_board_raises():
    board = Board(width=4, height=4)

    with pytest.raises(IndexError):
        board.get_cell(4, 0)


def test_can_place_and_put_tetromino_respect_collisions():
    board = Board(width=4, height=4)
    tetromino = Tetromino("O", x=1, y=1)

    assert board.can_place(tetromino, tetromino.x, tetromino.y)
    board.put_tetromino(tetromino)

    assert board.get_cell(1, 1) == "O"
    assert not board.can_place(tetromino, tetromino.x, tetromino.y)


def test_clear_full_lines_standard_shifts_whole_rows_down():
    board = Board(width=4, height=4)
    board.fill_cell(2, 0, "T")

    for x in range(board.width):
        board.fill_cell(x, 3, "I")

    assert board.clear_full_lines() == 1
    assert board.get_cell(2, 1) == "T"
    assert all(board.get_cell(x, 0) is None for x in range(board.width))
    assert all(board.get_cell(x, 3) is None for x in range(board.width))


def test_clear_multiple_full_lines_at_once():
    board = Board(width=4, height=4)
    board.fill_cell(1, 0, "T")

    for y in (2, 3):
        for x in range(board.width):
            board.fill_cell(x, y, "I")

    assert board.clear_full_lines() == 2
    assert board.get_cell(1, 2) == "T"
    assert all(board.get_cell(x, 0) is None for x in range(board.width))
    assert all(board.get_cell(x, 1) is None for x in range(board.width))
    assert all(board.get_cell(x, 3) is None for x in range(board.width))


def test_sand_gravity_step_respects_blocked_cells():
    board = Board(width=4, height=4)
    board.fill_cell(1, 1, "Z")

    assert not board.apply_sand_gravity_step(blocked_cells={(1, 2)})
    assert board.get_cell(1, 1) == "Z"

    assert board.apply_sand_gravity_step()
    assert board.get_cell(1, 2) == "Z"
