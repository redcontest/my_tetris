"""
Модуль, отвечающий за отрисовку базовых UI-элементов.
"""
import pygame

from src.tetris.config import (
    BUTTON_BORDER_COLOR,
    BUTTON_BORDER_RADIUS,
    BUTTON_BORDER_WIDTH,
    BUTTON_COLOR,
    Color,
    MENU_BUTTON_HEIGHT,
    MENU_BUTTON_WIDTH,
    SCREEN_CENTER_X,
    SELECTED_BUTTON_BORDER_COLOR,
    SELECTED_BUTTON_COLOR,
    SUBTITLE_FONT_SIZE,
    TEXT_COLOR,
    TEXT_FONT_SIZE,
    TITLE_FONT_SIZE,
)


class UiDetails:
    """Класс, содержащий методы для рендеринга кнопок и текста интерфейса."""

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Метод, создающий рендерер базовых UI-элементов.

        Args:
            screen (pygame.Surface): поверхность окна для отрисовки.
        """
        self.screen = screen
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.subtitle_font = pygame.font.Font(None, SUBTITLE_FONT_SIZE)
        self.text_font = pygame.font.Font(None, TEXT_FONT_SIZE)

    def render_button(
            self,
            text: str,
            center_y: int,
            is_selected: bool = False,
            width: int = MENU_BUTTON_WIDTH,
            center_x: int | None = None
            ) -> None:
        """
        Метод, отрисовывающий кнопку с текстом.

        Args:
            text (str): текст кнопки.
            center_y (int): координата Y центра кнопки.
            is_selected (bool): True, если кнопка выбрана.
            width (int): ширина кнопки в пикселях.
            center_x (int | None): координата X центра кнопки.
        """
        button_center_x = SCREEN_CENTER_X if center_x is None else center_x
        rect = pygame.Rect(0, 0, width, MENU_BUTTON_HEIGHT)
        rect.center = (button_center_x, center_y)
        color = SELECTED_BUTTON_COLOR if is_selected else BUTTON_COLOR
        border_color = (
            SELECTED_BUTTON_BORDER_COLOR
            if is_selected
            else BUTTON_BORDER_COLOR
        )

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=BUTTON_BORDER_RADIUS
        )
        pygame.draw.rect(
            self.screen,
            border_color,
            rect,
            width=BUTTON_BORDER_WIDTH,
            border_radius=BUTTON_BORDER_RADIUS
        )
        self.render_text(text, self.subtitle_font, TEXT_COLOR, rect.center)

    def render_text(
            self,
            text: str,
            font: pygame.font.Font,
            color: Color,
            center: tuple[int, int]
            ) -> None:
        """
        Метод, отрисовывающий текст с центром в указанной точке.

        Args:
            text (str): текст для отрисовки.
            font (pygame.font.Font): шрифт текста.
            color (Color): цвет текста.
            center (tuple[int, int]): координаты центра текста.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)
