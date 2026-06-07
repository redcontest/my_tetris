"""
Модуль, отвечающий за перемещения тетромино.
"""
from src.tetris.controllers.game_session import GameSession
from src.tetris.controllers.state import StateType, WrapMode
from src.tetris.models.tetromino import Tetromino


type RotationTransition = tuple[int, int]
type WallKickOffset = tuple[int, int]
type WallKickTable = dict[RotationTransition, tuple[WallKickOffset, ...]]


DEFAULT_WALL_KICKS: WallKickTable = {
    (0, 1): ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
    (1, 0): ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
    (1, 2): ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2)),
    (2, 1): ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)),
    (2, 3): ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
    (3, 2): ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
    (3, 0): ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
    (0, 3): ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2)),
}

I_WALL_KICKS: WallKickTable = {
    (0, 1): ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
    (1, 0): ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
    (1, 2): ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
    (2, 1): ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
    (2, 3): ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)),
    (3, 2): ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)),
    (3, 0): ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)),
    (0, 3): ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)),
}


class MoveController:
    """Контроллер, управляющий текущим тетромино."""

    def __init__(self, session: GameSession) -> None:
        """
        Метод, создающий контроллер движения тетромино.

        Args:
            session (GameSession): объект текущей игровой сессии.
        """
        self.session = session

    def move_current_tetromino(self, dx: int, dy: int) -> bool:
        """
        Служебный метод, сдвигающий текущее тетромино, если это возможно.

        Args:
            dx (int): сдвиг по X.
            dy (int): сдвиг по Y.

        Returns:
            bool: True, если тетромино было сдвинуто, False в противном случае.
        """
        next_x = self.session.current_tetromino.x + dx
        next_y = self.session.current_tetromino.y + dy

        if self._can_place_current_tetromino(next_x, next_y):
            self.session.current_tetromino.move(dx, dy)
            self.update_ghost_tetromino()
            self.session.sync_state_models()
            return True

        return False

    def move_current_tetromino_down(self) -> bool:
        """
        Служебный метод, сдвигающий текущее тетромино вниз или фиксирующий его.

        Returns:
            bool: True, если тетромино было сдвинуто вниз; False, если оно было
                зафиксировано на доске.
        """
        if self.move_current_tetromino(0, 1):
            return True

        self.lock_current_tetromino()
        return False

    def soft_drop_current_tetromino(self) -> None:
        """Служебный метод, реализующий быстрый сдвиг тетромино вниз."""
        if self.move_current_tetromino_down():
            self.session.score.add_soft_drop_points()
            self.session.fall_timer = 0.0
            self.update_ghost_tetromino()
            self.session.sync_state_models()

    def hard_drop_current_tetromino(self) -> None:
        """Служебный метод, мгновенно бросающий тетромино максимально вниз."""
        cells_count = 0

        while self.move_current_tetromino_down():
            cells_count += 1

        self.session.score.add_hard_drop_points(cells_count)
        self.update_ghost_tetromino()
        self.session.sync_state_models()

    def lock_current_tetromino(self) -> None:
        """
        Служебный метод, фиксирующий текущее тетромино на доске и выполняющий
        сопутствующие действия.
        """
        if self.session.wrap_mode == WrapMode.ON:
            for x, y in self.session.current_tetromino.get_cells():
                self.session.board.fill_cell(
                    x % self.session.board.width,
                    y,
                    self.session.current_tetromino.type
                )
        else:
            self.session.board.put_tetromino(self.session.current_tetromino)

        cleared_lines_count = self.session.board.clear_full_lines()
        self.session.score.add_cleared_lines(cleared_lines_count)
        self.session.current_tetromino = self.session.spawn_tetromino()
        self.session.fall_timer = 0.0
        self.session.sand_gravity_timer = 0.0
        self.update_ghost_tetromino()
        self.session.sync_state_models()

        if not self._can_place_current_tetromino(
            self.session.current_tetromino.x,
            self.session.current_tetromino.y
                ):
            self.session.state.set_state(StateType.GAME_OVER)

    def rotate_current_tetromino(self) -> None:
        """Служебный метод, поворачивающий текущее тетромино."""
        old_x = self.session.current_tetromino.x
        old_y = self.session.current_tetromino.y
        old_rotation = self.session.current_tetromino.rotation
        self.session.current_tetromino.rotate()
        new_rotation = self.session.current_tetromino.rotation

        for offset_x, offset_y in self._get_wall_kick_offsets(
            old_rotation,
            new_rotation
                ):
            next_x = old_x + offset_x
            next_y = old_y - offset_y

            if self._can_place_current_tetromino(next_x, next_y):
                self.session.current_tetromino.x = next_x
                self.session.current_tetromino.y = next_y
                self.update_ghost_tetromino()
                self.session.sync_state_models()
                return

        self.session.current_tetromino.rotation = old_rotation

    def _get_wall_kick_offsets(
            self,
            old_rotation: int,
            new_rotation: int
            ) -> tuple[WallKickOffset, ...]:
        """
        Служебный метод, возвращающий SRS-сдвиги для попытки поворота.

        Args:
            old_rotation (int): индекс поворота до попытки.
            new_rotation (int): индекс поворота после попытки.

        Returns:
            tuple[WallKickOffset, ...]: набор сдвигов, которые нужно проверить.
        """
        if self.session.current_tetromino.type == "O":
            return ((0, 0),)

        if self.session.current_tetromino.type == "I":
            return I_WALL_KICKS.get((old_rotation, new_rotation), ((0, 0),))

        return DEFAULT_WALL_KICKS.get((old_rotation, new_rotation), ((0, 0),))

    def update_ghost_tetromino(self) -> None:
        """Метод, вычисляющий ghost piece для текущего тетромино."""
        landing_y = self.session.current_tetromino.y

        while self._can_place_current_tetromino(
            self.session.current_tetromino.x,
            landing_y + 1
        ):
            landing_y += 1

        if landing_y == self.session.current_tetromino.y:
            self.session.ghost_tetromino = None
            return

        ghost_tetromino = Tetromino(
            self.session.current_tetromino.type,
            self.session.current_tetromino.x,
            landing_y
        )

        ghost_tetromino.rotation = self.session.current_tetromino.rotation
        self.session.ghost_tetromino = ghost_tetromino

    def _can_place_current_tetromino(self, x: int, y: int) -> bool:
        """
        Служебный метод, проверяющий возможность размещения текущего тетромино.

        Args:
            x (int): координата X.
            y (int): координата Y.

        Returns:
            bool: True, если тетромино можно разместить, False в противном
                случае.
        """
        try:
            if self.session.wrap_mode == WrapMode.ON:
                return self._can_place_wrapped_current_tetromino(x, y)

            return self.session.board.can_place(
                self.session.current_tetromino,
                x,
                y
            )

        except IndexError:
            return False

    def _can_place_wrapped_current_tetromino(self, x: int, y: int) -> bool:
        """
        Служебный метод, проверяющий размещение тетромино в режиме Wrap.

        Args:
            x (int): координата X.
            y (int): координата Y.

        Returns:
            bool: True, если тетромино можно разместить, False в противном
                случае.
        """
        for cell_x, cell_y in self.session.current_tetromino.get_cells(x, y):
            wrapped_x = cell_x % self.session.board.width

            if not self.session.board.is_inside(wrapped_x, cell_y):
                return False

            if not self.session.board.cell_is_empty(wrapped_x, cell_y):
                return False

        return True
