from src.tetris.models.tetromino_bag import TETROMINO_TYPES, TetrominoBag


def test_bag_returns_each_tetromino_type_once_per_bag():
    bag = TetrominoBag()
    drawn_types = [bag.get_next().type for _ in range(len(TETROMINO_TYPES))]

    assert sorted(drawn_types) == sorted(TETROMINO_TYPES)
    assert bag.bag == []


def test_empty_bag_is_refilled_on_next_draw():
    bag = TetrominoBag()

    for _ in range(len(TETROMINO_TYPES)):
        bag.get_next()

    next_tetromino = bag.get_next()

    assert next_tetromino.type in TETROMINO_TYPES
    assert len(bag.bag) == len(TETROMINO_TYPES) - 1


def test_reset_refills_bag():
    bag = TetrominoBag()
    bag.get_next()
    bag.get_next()

    bag.reset()

    assert sorted(bag.bag) == sorted(TETROMINO_TYPES)
