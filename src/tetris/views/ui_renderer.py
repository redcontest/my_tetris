"""
Модуль, отвечающий за отрисовку интерфейсов и UI-элементов.
"""
import pygame

from src.tetris.config import (
    GAME_OVER_MENU_Y,
    GAME_OVER_LEVEL_Y,
    GAME_OVER_LINES_Y,
    GAME_OVER_RETRY_Y,
    GAME_OVER_SCORE_Y,
    GAME_OVER_TITLE_Y,
    GAME_INFO_GRAVITY_LABEL_Y,
    GAME_INFO_GRAVITY_VALUE_Y,
    GAME_INFO_LEVEL_LABEL_Y,
    GAME_INFO_LEVEL_VALUE_Y,
    GAME_INFO_LINES_LABEL_Y,
    GAME_INFO_LINES_VALUE_Y,
    GAME_INFO_SCORE_LABEL_Y,
    GAME_INFO_SCORE_VALUE_Y,
    GAME_INFO_WRAP_LABEL_Y,
    GAME_INFO_WRAP_VALUE_Y,
    MENU_TITLE_Y,
    MENU_PLAY_Y,
    MENU_QUIT_Y,
    MENU_SETTINGS_Y,
    MUTED_TEXT_COLOR,
    OVERLAY_COLOR,
    PAUSE_CONTINUE_Y,
    PAUSE_MENU_Y,
    PAUSE_TITLE_Y,
    SCREEN_CENTER_X,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    BOARD_CELL_SIZE,
    BOARD_WIDTH,
    SETTINGS_BACK_Y,
    SETTINGS_SAND_Y,
    SETTINGS_STANDARD_Y,
    SETTINGS_SUBTITLE_Y,
    SETTINGS_TOGGLE_BUTTON_WIDTH,
    SETTINGS_TITLE_Y,
    SETTINGS_WRAP_Y,
    TEXT_COLOR,
    WRAP_BUTTON_GAP,
)
from src.tetris.controllers.state import GameState, GravityMode, WrapMode
from src.tetris.views.ui_details import UiDetails


GRAVITY_MODE_NAMES: dict[GravityMode, str] = {
    GravityMode.STANDARD: "STANDARD",
    GravityMode.SAND: "SAND",
}
WRAP_MODE_NAMES: dict[WrapMode, str] = {
    WrapMode.OFF: "OFF",
    WrapMode.ON: "ON",
}


class UiRenderer:
    """Класс, отрисовывающий меню, кнопки, текст и служебные экраны."""

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Метод, создающий рендерер интерфейсов.

        Args:
            screen (pygame.Surface): поверхность окна для отрисовки.
        """
        self.screen = screen
        self.ui_details = UiDetails(screen)

    def render_menu(self) -> None:
        """
        Метод, отрисовывающий главное меню.
        """
        self.ui_details.render_text(
            "Gravity Tetris",
            self.ui_details.title_font,
            TEXT_COLOR,
            (SCREEN_CENTER_X, MENU_TITLE_Y)
        )

        self.ui_details.render_button("ИГРАТЬ", MENU_PLAY_Y)
        self.ui_details.render_button("НАСТРОЙКИ", MENU_SETTINGS_Y)
        self.ui_details.render_button("ВЫХОД", MENU_QUIT_Y)

    def render_settings(self, state: GameState) -> None:
        """
        Метод, отрисовывающий экран настроек игры.

        Args:
            state (GameState): текущее состояние игры.
        """
        self.ui_details.render_text(
            "НАСТРОЙКИ",
            self.ui_details.title_font,
            TEXT_COLOR,
            (SCREEN_CENTER_X, SETTINGS_TITLE_Y)
        )
        self.ui_details.render_text(
            "РЕЖИМ ГРАВИТАЦИИ",
            self.ui_details.subtitle_font,
            TEXT_COLOR,
            (SCREEN_CENTER_X, SETTINGS_SUBTITLE_Y)
        )

        self.ui_details.render_button(
            "СТАНДАРТНАЯ",
            SETTINGS_STANDARD_Y,
            is_selected=state.gravity_mode == GravityMode.STANDARD
        )
        self.ui_details.render_button(
            "ПЕСОЧНАЯ",
            SETTINGS_SAND_Y,
            is_selected=state.gravity_mode == GravityMode.SAND
        )

        self.ui_details.render_button(
            "WRAP OFF",
            SETTINGS_WRAP_Y,
            is_selected=state.wrap_mode == WrapMode.OFF,
            width=SETTINGS_TOGGLE_BUTTON_WIDTH,
            center_x=(
                SCREEN_CENTER_X
                - SETTINGS_TOGGLE_BUTTON_WIDTH // 2
                - WRAP_BUTTON_GAP // 2
            )
        )
        self.ui_details.render_button(
            "WRAP ON",
            SETTINGS_WRAP_Y,
            is_selected=state.wrap_mode == WrapMode.ON,
            width=SETTINGS_TOGGLE_BUTTON_WIDTH,
            center_x=(
                SCREEN_CENTER_X
                + SETTINGS_TOGGLE_BUTTON_WIDTH // 2
                + WRAP_BUTTON_GAP // 2
            )
        )

        self.ui_details.render_button("НАЗАД", SETTINGS_BACK_Y)

    def render_pause_overlay(self) -> None:
        """
        Метод, отрисовывающий затемнение и кнопки паузы поверх игры.
        """
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )
        overlay.fill(OVERLAY_COLOR)
        self.screen.blit(overlay, (0, 0))

        self.ui_details.render_text(
            "ПАУЗА",
            self.ui_details.title_font,
            TEXT_COLOR,
            (SCREEN_CENTER_X, PAUSE_TITLE_Y)
        )

        self.ui_details.render_button("ПРОДОЛЖИТЬ", PAUSE_CONTINUE_Y)
        self.ui_details.render_button("В МЕНЮ", PAUSE_MENU_Y)

    def render_game_over(self, state: GameState) -> None:
        """
        Метод, отрисовывающий экран завершенной партии.

        Args:
            state (GameState): текущее состояние игры.
        """
        score = state.score
        points = 0 if score is None else score.points
        level = 1 if score is None else score.level
        lines = 0 if score is None else score.lines

        self.ui_details.render_text(
            "ИГРА ОКОНЧЕНА",
            self.ui_details.title_font,
            TEXT_COLOR,
            (SCREEN_CENTER_X, GAME_OVER_TITLE_Y)
        )
        self.ui_details.render_text(
            f"СЧЕТ: {points}",
            self.ui_details.subtitle_font,
            TEXT_COLOR,
            (SCREEN_CENTER_X, GAME_OVER_SCORE_Y)
        )
        self.ui_details.render_text(
            f"УРОВЕНЬ: {level}",
            self.ui_details.text_font,
            MUTED_TEXT_COLOR,
            (SCREEN_CENTER_X, GAME_OVER_LEVEL_Y)
        )
        self.ui_details.render_text(
            f"ЛИНИИ: {lines}",
            self.ui_details.text_font,
            MUTED_TEXT_COLOR,
            (SCREEN_CENTER_X, GAME_OVER_LINES_Y)
        )

        self.ui_details.render_button("ИГРАТЬ СНОВА", GAME_OVER_RETRY_Y)
        self.ui_details.render_button("МЕНЮ", GAME_OVER_MENU_Y)

    def render_game_info(self, state: GameState) -> None:
        """
        Метод, отрисовывающий игровую информацию.

        Args:
            state (GameState): текущее состояние игры.
        """
        score = state.score
        points = 0 if score is None else score.points
        level = 1 if score is None else score.level
        lines = 0 if score is None else score.lines

        board_width = BOARD_WIDTH * BOARD_CELL_SIZE
        board_left = (SCREEN_WIDTH - board_width) // 2
        board_right = board_left + board_width
        modes_x = board_left // 2
        stats_x = (board_right + SCREEN_WIDTH) // 2

        self.ui_details.render_text(
            "GRAVITY",
            self.ui_details.subtitle_font,
            TEXT_COLOR,
            (modes_x, GAME_INFO_GRAVITY_LABEL_Y)
        )
        self.ui_details.render_text(
            GRAVITY_MODE_NAMES[state.gravity_mode],
            self.ui_details.text_font,
            MUTED_TEXT_COLOR,
            (modes_x, GAME_INFO_GRAVITY_VALUE_Y)
        )
        self.ui_details.render_text(
            "WRAP",
            self.ui_details.subtitle_font,
            TEXT_COLOR,
            (modes_x, GAME_INFO_WRAP_LABEL_Y)
        )
        self.ui_details.render_text(
            WRAP_MODE_NAMES[state.wrap_mode],
            self.ui_details.text_font,
            MUTED_TEXT_COLOR,
            (modes_x, GAME_INFO_WRAP_VALUE_Y)
        )

        self.ui_details.render_text(
            "СЧЕТ",
            self.ui_details.subtitle_font,
            TEXT_COLOR,
            (stats_x, GAME_INFO_SCORE_LABEL_Y)
        )
        self.ui_details.render_text(
            str(points),
            self.ui_details.text_font,
            MUTED_TEXT_COLOR,
            (stats_x, GAME_INFO_SCORE_VALUE_Y)
        )
        self.ui_details.render_text(
            "УРОВЕНЬ",
            self.ui_details.subtitle_font,
            TEXT_COLOR,
            (stats_x, GAME_INFO_LEVEL_LABEL_Y)
        )
        self.ui_details.render_text(
            str(level),
            self.ui_details.text_font,
            MUTED_TEXT_COLOR,
            (stats_x, GAME_INFO_LEVEL_VALUE_Y)
        )
        self.ui_details.render_text(
            "ЛИНИИ",
            self.ui_details.subtitle_font,
            TEXT_COLOR,
            (stats_x, GAME_INFO_LINES_LABEL_Y)
        )
        self.ui_details.render_text(
            str(lines),
            self.ui_details.text_font,
            MUTED_TEXT_COLOR,
            (stats_x, GAME_INFO_LINES_VALUE_Y)
        )
