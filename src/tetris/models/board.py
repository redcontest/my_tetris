"""
TODO: написать докстринг для этого гениального модуля
"""
from src.tetris.config import BOARD_HEIGHT, BOARD_WIDTH
from src.tetris.models.tetromino import TetrominoType


type CellValue = TetrominoType | None
type BoardLine = list[CellValue]
type BoardGrid = list[BoardLine]


# TODO: на момент написания этого модуля нет класса Tetromino и он не
# импортирован. Это критично для аннотации. После завершения класса Tetromino
# нужно исправить это.


class Board:
    """Главное поле игры, в котором падают тетромино."""
    def __init__(
            self,
            width: int = BOARD_WIDTH,
            height: int = BOARD_HEIGHT
            ) -> None:
        self.width = width
        self.height = height
        self.grid = self._create_grid()

    def is_inside(self, x: int, y: int) -> bool:
        """
        Метод, возвращающий, являются ли координаты x и y ячейкой внутри
        игрового поля или нет.

        Args:
            x (int): координата X.
            y (int): координата Y.
        Returns:
            bool: True, если координаты являются корректной ячейкой, False в
                противном случае.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> CellValue:
        """
        Метод, возвращающий ячейку (то, что она содержит).

        Args:
            x (int): координата X.
            y (int): координата Y.

        Returns:
            CellValue: тип тетромино, если ячейка не пустая, None
                в противном случае.

        Raises:
            IndexError: выбрасывается, если запрошенная ячейка за пределами
                поля.
        """
        if not self.is_inside(x, y):
            raise IndexError("Ячейка находится за пределами доски.")
        return self.grid[y][x]

    def clear_full_lines(self) -> None:
        """
        Метод, очищающий заполненные линии поля и сдвигающий максимально вниз
        все верхние непустые линии.
        """
        for y, line in enumerate(self.grid):
            if self._line_is_full(line):
                self.grid.pop(y)  # Обычное удаление.
                # После удаления верхние линии надо сдвинуть вниз. С pop это
                # произошло само, но в самом верху теперь строки не хватает.
                # Исправляю с помощью вставки новой.
                self.grid.insert(0, [None for _ in range(self.width)])

    def cell_is_empty(self, x: int, y: int) -> bool:
        """
        Метод, проверяющий, является ли ячейка пустой.

        Args:
            x (int): координата X.
            y (int): координата Y.

        Returns:
            bool: True, если ячейка пустая, False в противном случае.

        Raises:
            IndexError: возникает, если запрошенная ячейка за пределами
                игрового поля.

        """
        if not self.is_inside(x, y):
            raise IndexError("Ячейка находится за пределами доски.")
        return self.grid[y][x] is None

    def fill_cell(self, x: int, y: int, tetromino_type: TetrominoType) -> None:
        """
        Заполняет ячейку определенным типом тетромино.

        Args:
            x (int): координата X.
            y (int): координата Y.
            tetromino_type (TetrominoType): тип фигурки.

        Raises:
            IndexError: выбрасывается, если была попытка поставить тетромино за
            пределы доски.
        """
        if not self.is_inside(x, y):
            raise IndexError("Ячейка находится за пределами доски.")
        self.grid[y][x] = tetromino_type

    def can_place(self, tetromino, x: int, y: int) -> bool:
        """
        Метод, проверяющий, можно ли разместить тетромино в указанной позиции.

        Args:
            x (int): координата X.
            y (int): координата Y.
            tetromino: тетромино, которое нужно разместить.

        Returns:
            bool: True, если разместить можно, False в противном случае.
        """
        # NOTE: В этом методе нет проверки на то, находится ли запрошенная
        # ячейка в пределах поля, потому что эту работу уже перехватывает
        # self.cell_is_empty.
        for cell_x, cell_y in tetromino.get_cells(x, y):
            if not self.cell_is_empty(cell_x, cell_y):
                return False
        return True

    def put_tetromino(self, tetromino) -> None:
        """
        Метод, устанавливающий в определённую ячейку значения тетромино.

        Args:
            tetromino: тетромино, которое нужно разместить.

        Raises:
            ValueError: если была попытка разместить тетромино в недопустимое
                место.
        """
        if not self.can_place(tetromino, tetromino.x, tetromino.y):
            raise ValueError("Некорректная позиция для размещения.")

        for x, y in tetromino.get_cells():
            self.fill_cell(x, y, tetromino.type)

    # NOTE: метод возможно придется удалить.
    def clear_cell(self, x: int, y: int) -> None:
        """
        Метод, очищающий ячейку до пустого состояния.

        Args:
            x (int): координата X.
            y (int): координата Y.
        """
        if not self.is_inside(x, y):
            raise IndexError("Ячейка находится за пределами доски.")
        self.grid[y][x] = None

    def reset(self) -> None:
        """
        Метод, сбрасывающий игровую сетку до пустого состояния.
        """
        self.grid = self._create_grid()

    def _create_grid(self) -> BoardGrid:
        """
        Служебный метод, создающий сетку для игрвого поля.

        Returns:
            BoardGrid: сетка игрового поля.
        """
        return [[None for _ in range(self.width)] for _ in range(self.height)]

    def _line_is_full(self, line: BoardLine) -> bool:
        """
        Служебный метод, отвечающий, является ли линия заполненной.

        Args:
            line (BoardLine): линия в игровом поле.

        Returns:
            bool: True, если линия заполнена, False в противном случае.
        """
        return all(cell is not None for cell in line)
