"""
Модуль, содержащий класс для управления уровнем и счётом игры.

Зона ответственности модуля:
Уровень игры в тетрисе используется для вычисления скорости падения тетромино,
однако сам этот модуль НЕ МЕНЯЕТ скорость напрямую. Этот модуль отвечает только
за подсчет линий, вычисление счета и уровня.

Этот модуль не отвечает за рендеринг окна с отображением текущего уровня,
очков и прочего.
"""
from src.tetris.config import LINES_PER_LEVEL, LINE_SCORES


class Score:
    """Класс, описывающий счёт игры."""

    def __init__(self) -> None:
        """Метод, создающий счет с начальными значениями партии."""
        self.points: int = 0
        self.level: int = 1
        self.lines: int = 0

    def add_cleared_lines(self, lines_count: int) -> None:
        """
        Метод, начисляющий очки за очищенные линии. Очищенных линий в тетрисе
        может быть максимум 4 - столько может очистить самая длинная фигурка.

        Args:
            lines_count (int): количество очищенных линий.

        Raises:
            ValueError: выбрасывается, если количество линий меньше 0 или
                больше 4.
        """
        if not 0 <= lines_count <= 4:
            raise ValueError(
                "Количество очищенных линий должно быть от 0 до 4."
            )

        if lines_count == 0:
            return

        self.points += LINE_SCORES[lines_count] * self.level
        self.lines += lines_count
        self.level = self._calculate_level()

    def add_soft_drop_points(self, cells_count: int = 1) -> None:
        """
        Метод, начисляющий очки за ускоренное падение тетромино.

        Args:
            cells_count (int): количество клеток, на которое тетромино было
                быстро сдвинуто вниз.

        Raises:
            ValueError: выбрасывается, если количество клеток меньше 0.
        """
        if cells_count < 0:
            raise ValueError("Количество клеток не может быть отрицательным.")

        self.points += cells_count

    def add_hard_drop_points(self, cells_count: int) -> None:
        """
        Метод, начисляющий очки за мгновенное падение тетромино до самого
        конца.

        Args:
            cells_count (int): количество клеток, которые тетромино прошло
                мгновенно.

        Raises:
            ValueError: выбрасывается, если количество клеток меньше 0.
        """
        if cells_count < 0:
            raise ValueError("Количество клеток не может быть отрицательным.")

        self.points += cells_count * 2

    def reset(self) -> None:
        """Метод, сбрасывающий счет до начального состояния."""
        self.points = 0
        self.level = 1
        self.lines = 0

    def _calculate_level(self) -> int:
        """
        Служебный метод, вычисляющий текущий уровень по количеству очищенных за
        раунд линий.

        Returns:
            int: текущий уровень игры.
        """
        return self.lines // LINES_PER_LEVEL + 1
