import pytest

from src.tetris.models.score import Score


def test_add_cleared_lines_updates_points_lines_and_level():
    score = Score()

    score.add_cleared_lines(4)
    score.add_cleared_lines(4)
    score.add_cleared_lines(2)

    assert score.points == 2700
    assert score.lines == 10
    assert score.level == 2


def test_zero_cleared_lines_does_not_change_score():
    score = Score()
    score.add_cleared_lines(0)

    assert score.points == 0
    assert score.lines == 0
    assert score.level == 1


def test_invalid_cleared_lines_count_raises():
    score = Score()

    with pytest.raises(ValueError):
        score.add_cleared_lines(5)


def test_drop_points_and_reset():
    score = Score()

    score.add_soft_drop_points(3)
    score.add_hard_drop_points(4)
    assert score.points == 11

    score.reset()
    assert (score.points, score.lines, score.level) == (0, 0, 1)
