"""
Модуль, описывающий падающие тетромино и их формы.

Зона ответственности модуля:
Модуль отвечает за действия, связанные конкретно с созданием и управлением
тетромино.

Модуль ничего не рендерит и не проставляет на игровую доску.
"""
from typing import Literal


type TetrominoType = Literal["I", "O", "T", "S", "Z", "J", "L"]
type TetrominoRow = list[bool]
type TetrominoShape = list[TetrominoRow]
type TetrominoCells = list[tuple[int, int]]


TETROMINO_SHAPES: dict[TetrominoType, list[TetrominoShape]] = {
    "I": [
        [
            [False, False, False, False],
            [True, True, True, True],
            [False, False, False, False],
            [False, False, False, False],
        ],
        [
            [False, False, True, False],
            [False, False, True, False],
            [False, False, True, False],
            [False, False, True, False],
        ],
        [
            [False, False, False, False],
            [False, False, False, False],
            [True, True, True, True],
            [False, False, False, False],
        ],
        [
            [False, True, False, False],
            [False, True, False, False],
            [False, True, False, False],
            [False, True, False, False],
        ],
    ],
    "O": [
        [[True, True], [True, True]],
    ],
    "T": [
        [[False, True, False], [True, True, True], [False, False, False]],
        [[False, True, False], [False, True, True], [False, True, False]],
        [[False, False, False], [True, True, True], [False, True, False]],
        [[False, True, False], [True, True, False], [False, True, False]],
    ],
    "S": [
        [[False, True, True], [True, True, False], [False, False, False]],
        [[False, True, False], [False, True, True], [False, False, True]],
        [[False, False, False], [False, True, True], [True, True, False]],
        [[True, False, False], [True, True, False], [False, True, False]],
    ],
    "Z": [
        [[True, True, False], [False, True, True], [False, False, False]],
        [[False, False, True], [False, True, True], [False, True, False]],
        [[False, False, False], [True, True, False], [False, True, True]],
        [[False, True, False], [True, True, False], [True, False, False]],
    ],
    "J": [
        [[True, False, False], [True, True, True], [False, False, False]],
        [[False, True, True], [False, True, False], [False, True, False]],
        [[False, False, False], [True, True, True], [False, False, True]],
        [[False, True, False], [False, True, False], [True, True, False]],
    ],
    "L": [
        [[False, False, True], [True, True, True], [False, False, False]],
        [[False, True, False], [False, True, False], [False, True, True]],
        [[False, False, False], [True, True, True], [True, False, False]],
        [[True, True, False], [False, True, False], [False, True, False]],
    ],
}


class Tetromino:
    """Класс, описывающий фигурку тетриса (тетромино), падающую вниз."""

    def __init__(
            self,
            tetromino_type: TetrominoType,
            x: int = 0,
            y: int = 0
            ) -> None:
        """
        Метод, создающий тетромино указанного типа в заданной позиции.

        Args:
            tetromino_type (TetrominoType): тип создаваемого тетромино.
            x (int): начальная координата X.
            y (int): начальная координата Y.
        """
        self.type: TetrominoType = tetromino_type
        self.x: int = x
        self.y: int = y
        self.rotation: int = 0

    @property
    def shape(self) -> TetrominoShape:
        """
        Метод для получения Текущей формы тетромино с учетом поворота.

        Returns:
            TetrominoShape: список, отражающий форму тетромино, где True -
                занятая клетка.
        """
        return TETROMINO_SHAPES[self.type][self.rotation]

    @property
    def width(self) -> int:
        """
        Ширина текущей формы тетромино в клетках.

        Returns:
            int: ширина тетромино.
        """
        return len(self.shape[0])

    # NOTE: метод height пока не используется в игре. Однако я оставлю на
    # всякий случай (к тому же, интерфейс так будет явно более универсальным).
    @property
    def height(self) -> int:
        """
        Высота текущей формы тетромино в клетках.

        Returns:
            int: высота тетромино.
        """
        return len(self.shape)

    def get_cells(
            self,
            x: int | None = None,
            y: int | None = None
            ) -> TetrominoCells:
        """
        Метод, возвращающий координаты занятых тетромино клеток на игровой
        доске.

        Args:
            x (int | None): координата X для проверки. Если None, проверка
                выполняется по текущей координате X.
            y (int | None): координата Y для проверки. Если None, проверка
                выполняется по текущей координате Y.

        Returns:
            TetrominoCells: список координат занятых тетромино клеток.
        """
        base_x = self.x if x is None else x
        base_y = self.y if y is None else y

        cells = []
        for row_y, row in enumerate(self.shape):
            for cell_x, is_filled in enumerate(row):
                if is_filled:
                    cells.append((base_x + cell_x, base_y + row_y))

        return cells

    def move(self, dx: int, dy: int) -> None:
        """
        Метод, сдвигающий тетромино на указанное количество клеток.

        Args:
            dx (int): сдвиг на X клеток.
            dy (int): сдвиг на Y клеток.
        """
        self.x += dx
        self.y += dy

    def move_down(self) -> None:
        """Метод, сдвигающий тетромино на одну клетку вниз."""
        self.move(0, 1)

    def rotate(self) -> None:
        """Метод, поворачивающий тетромино по часовой стрелке."""
        rotations_count = len(TETROMINO_SHAPES[self.type])
        self.rotation = (self.rotation + 1) % rotations_count
