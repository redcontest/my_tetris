"""
Модуль, содержащий настройки игры.

Описание зоны ответственности модуля:
Модуль хранит константы окна, доски, скорости падения, цветов и расположения
элементов интерфейса.

Модуль НЕ ОТВЕЧАЕТ за игровую логику, отрисовку и обработку пользовательского
ввода. Только общие настройки проекта.
"""
# Настройки окна и главного цикла.
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
SCREEN_CENTER_X = SCREEN_WIDTH // 2

FPS = 60

# Настройки игрового поля.
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_CELL_SIZE = 28
BOARD_BORDER_WIDTH = 2
BOARD_GRID_LINE_WIDTH = 1
BOARD_CELL_PADDING = 4
BOARD_CELL_BORDER_RADIUS = 4

# Баланс скорости падения.
MIN_FALL_DELAY = 0.05
TETRIS_GRAVITY_BASE = 0.8
TETRIS_GRAVITY_STEP = 0.01
SOFT_FALL_DELAY = 0.05
SAND_GRAVITY_DELAY = 0.08

# Баланс счета и уровней.
LINES_PER_LEVEL = 10
LINE_SCORES = {
    1: 100,
    2: 300,
    3: 600,
    4: 1200,
}

# Шрифты интерфейса.
TITLE_FONT_SIZE = 72
SUBTITLE_FONT_SIZE = 36
TEXT_FONT_SIZE = 28

# Размеры кнопок.
MENU_BUTTON_WIDTH = 360
MENU_BUTTON_HEIGHT = 64
BUTTON_BORDER_WIDTH = 2
BUTTON_BORDER_RADIUS = 12
SETTINGS_TOGGLE_BUTTON_WIDTH = 170
WRAP_BUTTON_GAP = 20

# Координаты главного меню.
MENU_TITLE_Y = 150
MENU_PLAY_Y = 260
MENU_SETTINGS_Y = 340
MENU_QUIT_Y = 420

# Координаты паузы.
PAUSE_TITLE_Y = 220
PAUSE_CONTINUE_Y = 320
PAUSE_MENU_Y = 400

# Координаты экрана завершенной игры.
GAME_OVER_TITLE_Y = 110
GAME_OVER_SCORE_Y = 190
GAME_OVER_LEVEL_Y = 235
GAME_OVER_LINES_Y = 270
GAME_OVER_RETRY_Y = 380
GAME_OVER_MENU_Y = 460

# Координаты экрана настроек.
SETTINGS_TITLE_Y = 70
SETTINGS_SUBTITLE_Y = 130
SETTINGS_STANDARD_Y = 200
SETTINGS_SAND_Y = 290
SETTINGS_WRAP_Y = 400
SETTINGS_BACK_Y = 550

# Координаты игровой информации.
GAME_INFO_GRAVITY_LABEL_Y = 235
GAME_INFO_GRAVITY_VALUE_Y = 270
GAME_INFO_WRAP_LABEL_Y = 335
GAME_INFO_WRAP_VALUE_Y = 370
GAME_INFO_SCORE_LABEL_Y = 180
GAME_INFO_SCORE_VALUE_Y = 215
GAME_INFO_LEVEL_LABEL_Y = 300
GAME_INFO_LEVEL_VALUE_Y = 335
GAME_INFO_LINES_LABEL_Y = 420
GAME_INFO_LINES_VALUE_Y = 455

# Типы цветов.
type Color = tuple[int, int, int]
type AlphaColor = tuple[int, int, int, int]

# Цветовая тема игры.
BACKGROUND_COLOR: Color = (250, 242, 246)
BOARD_BACKGROUND_COLOR: Color = (255, 249, 251)
BOARD_BORDER_COLOR: Color = (225, 184, 202)
GRID_COLOR: Color = (246, 232, 238)
TEXT_COLOR: Color = (88, 49, 72)
MUTED_TEXT_COLOR: Color = (214, 174, 194)
BUTTON_COLOR: Color = (229, 166, 190)
BUTTON_BORDER_COLOR: Color = (197, 115, 151)
SELECTED_BUTTON_COLOR: Color = (144, 184, 166)
SELECTED_BUTTON_BORDER_COLOR: Color = (100, 145, 124)
OVERLAY_COLOR: AlphaColor = (0, 0, 0, 140)
GHOST_ALPHA = 80

# Цвета тетромино.
TETROMINO_COLORS: dict[str, Color] = {
    "I": (158, 207, 224),
    "O": (241, 216, 137),
    "T": (196, 164, 222),
    "S": (166, 211, 172),
    "Z": (230, 143, 153),
    "J": (151, 174, 221),
    "L": (235, 180, 132),
}
