"""
Модуль, отвечающий за рандомную выдачу тетромино.

В основе решения лежит shuffle bag с алгоритмом Fisher-Yates shuffle для
гарантии того, что никакие одинаковые тетромино не могут выпасть подряд (в
пределах одного мешка). Только через полный цикл рандомного выпадения всех
блоков.

Зона ответственности модуля:
Модуль отвечает только за рандомную выдачу тетромино. Этот модуль не определяет
действия с тетромино и уж тем более никуда их не размещает.
"""
import random

from src.tetris.models.tetromino import Tetromino, TetrominoType


TETROMINO_TYPES: list[TetrominoType] = ["I", "O", "T", "S", "Z", "J", "L"]


class TetrominoBag:
    """
    Класс, представляющий мешок с тетромино, из которого можно вытащить
    рандомный тетромино без повторов до тех пор, пока мешок не будет опустошен
    (после этого мешок создается заново)ю
    """

    def __init__(self) -> None:
        """Метод, создающий новый перемешанный мешок тетромино."""
        self.bag: list[TetrominoType] = self._create_bag()

    def get_next(self) -> Tetromino:
        """
        Метод, возвращающий рандомный из оставшихся в мешке тетромино.

        Returns:
            Tetromino: рандомный тетромино.
        """
        if not self.bag:
            self.bag = self._create_bag()

        return Tetromino(self.bag.pop())

    def reset(self) -> None:
        """
        Метод, сбрасывающий мешок тетромино до нового перемешанного
        состояния.
        """
        self.bag = self._create_bag()

    def _create_bag(self) -> list[TetrominoType]:
        """
        Служебный метод, создающий новый мешок тетромино (с перемешкой).

        Returns:
            list[TetrominoType]: перемешанный список вариантов тетромино.
        """
        bag = TETROMINO_TYPES.copy()
        random.shuffle(bag)
        return bag
