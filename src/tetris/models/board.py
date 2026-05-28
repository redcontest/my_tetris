"""
Модуль, отвечающий за игровую доску.

Описание зоны ответственности модуля:
Все действия, связанные с взаимодействием с доской. Проверка координат,
валидация, размещение, очистка, удаление линий.

Игровая доска НЕ ОТВЕЧАЕТ за рендеринг тетромино, вычисление позиции тетромино,
поворот тетромино и прочие действия. Только ИГРОВОЕ ПОЛЕ.
"""
# NOTE: координатный отсчет доски считается сверху слева.

from src.tetris.config import BOARD_HEIGHT, BOARD_WIDTH
from src.tetris.models.tetromino import TetrominoType, Tetromino


type CellValue = TetrominoType | None
type BoardLine = list[CellValue]
type BoardGrid = list[BoardLine]


class Board:
    """Главное поле игры, в котором падают тетромино."""

    def __init__(
            self,
            width: int = BOARD_WIDTH,
            height: int = BOARD_HEIGHT
            ) -> None:
        """
        Метод, создающий игровую доску указанного размера.

        Args:
            width (int): ширина доски в клетках.
            height (int): высота доски в клетках.
        """
        self.width: int = width
        self.height: int = height
        self.grid: BoardGrid = self._create_grid()

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

    def clear_full_lines(self) -> int:
        """
        Метод, очищающий заполненные линии поля и сдвигающий максимально вниз
        все верхние непустые линии.

        Returns:
            int: количество очищенных линий.
        """
        remaining_lines: BoardGrid = [
            line for line in self.grid if not self._line_is_full(line)
        ]
        cleared_lines_count = self.height - len(remaining_lines)

        if cleared_lines_count == 0:
            return 0

        empty_lines: BoardGrid = [
            [None for _ in range(self.width)]
            for _ in range(cleared_lines_count)
        ]
        self.grid = empty_lines + remaining_lines

        return cleared_lines_count

    def cell_is_empty(self, x: int, y: int) -> bool:
        """
        Метод, проверяющий, является ли ячейка пустой.

        Args:
            x (int): координата X.
            y (int): координата Y.

        Returns:
            bool: True, если ячейка пустая, False в противном случае.

        Raises:
            IndexError: выбрасывается, если запрошенная ячейка находится за
                пределами игрового поля.

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
            tetromino_type (TetrominoType): тип фигурки тетромино.

        Raises:
            IndexError: выбрасывается, если была попытка поставить тетромино за
            пределы доски.
        """
        if not self.is_inside(x, y):
            raise IndexError("Ячейка находится за пределами доски.")
        self.grid[y][x] = tetromino_type

    def can_place(self, tetromino: Tetromino, x: int, y: int) -> bool:
        """
        Метод, проверяющий, можно ли разместить тетромино в указанной позиции.

        Args:
            x (int): координата X.
            y (int): координата Y.
            tetromino (Tetromino): тетромино, которое нужно разместить.

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

    def put_tetromino(self, tetromino: Tetromino) -> None:
        """
        Метод, устанавливающий в определённую ячейку значения тетромино.

        Args:
            tetromino (Tetromino): тетромино, которое нужно разместить.

        Raises:
            ValueError: если была попытка разместить тетромино в недопустимое
                место.
        """
        if not self.can_place(tetromino, tetromino.x, tetromino.y):
            raise ValueError("Некорректная позиция для размещения.")

        for x, y in tetromino.get_cells():
            self.fill_cell(x, y, tetromino.type)

    def apply_sand_gravity_step(
            self,
            blocked_cells: set[tuple[int, int]] | None = None
            ) -> bool:
        """
        Метод, заставляющий заполненные (чем?, ох уж эти несклоняемые слова)
        тетромино ячейки падать как песок на ОДИН шаг.

        Args:
            blocked_cells (set[tuple[int, int]] | None): клетки, в которые
                нельзя сдвигать блоки.

        Returns:
            bool: True, если хотя бы одна клетка была сдвинута вниз, False в
                противном случае.
        """
        blocked_cells = blocked_cells or set()
        moved = False

        for y in range(self.height - 2, -1, -1):
            for x in range(self.width):
                if (
                    self.grid[y][x] is not None
                    and self.grid[y + 1][x] is None
                    and (x, y + 1) not in blocked_cells
                ):
                    self.grid[y + 1][x] = self.grid[y][x]
                    self.grid[y][x] = None
                    moved = True

        return moved

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
        grid: BoardGrid = [
            [None for _ in range(self.width)]
            for _ in range(self.height)
        ]
        return grid

    def _line_is_full(self, line: BoardLine) -> bool:
        """
        Служебный метод, отвечающий, является ли линия заполненной.

        Args:
            line (BoardLine): линия в игровом поле.

        Returns:
            bool: True, если линия заполнена, False в противном случае.
        """
        return all(cell is not None for cell in line)
