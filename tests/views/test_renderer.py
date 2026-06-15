import pygame

from src.tetris.controllers.state import (
    GameState,
    GravityMode,
    StateType,
    WrapMode,
)
from src.tetris.models.board import Board
from src.tetris.models.score import Score
from src.tetris.models.tetromino import Tetromino
from src.tetris.views.main_renderer import MainRenderer


def test_renderer_draws_playing_state_without_real_window():
    screen = pygame.display.set_mode((900, 600))
    state = GameState(StateType.PLAYING)
    state.board = Board()
    state.score = Score()
    state.current_tetromino = Tetromino("T", x=4, y=0)
    state.gravity_mode = GravityMode.STANDARD
    renderer = MainRenderer(screen)

    renderer.draw(state)

    assert renderer.screen is screen


def test_renderer_draws_wrapped_tetromino_without_real_window():
    screen = pygame.display.set_mode((900, 600))
    state = GameState(StateType.PLAYING)
    state.board = Board()
    state.score = Score()
    state.current_tetromino = Tetromino("O", x=9, y=0)
    state.gravity_mode = GravityMode.STANDARD
    state.wrap_mode = WrapMode.ON
    renderer = MainRenderer(screen)

    renderer.draw(state)

    assert renderer.screen is screen


def test_renderer_draws_settings_state_without_real_window():
    screen = pygame.display.set_mode((900, 600))
    state = GameState(StateType.SETTINGS)
    renderer = MainRenderer(screen)

    renderer.draw(state)

    assert renderer.screen is screen


def test_renderer_draws_pause_state_without_real_window():
    screen = pygame.display.set_mode((900, 600))
    state = GameState(StateType.PAUSED)
    state.board = Board()
    state.score = Score()
    state.current_tetromino = Tetromino("T", x=4, y=0)
    state.gravity_mode = GravityMode.STANDARD
    renderer = MainRenderer(screen)

    renderer.draw(state)

    assert renderer.screen is screen


def test_renderer_draws_game_over_state_with_score_without_real_window():
    screen = pygame.display.set_mode((900, 600))
    state = GameState(StateType.GAME_OVER)
    state.score = Score()
    state.score.points = 1200
    state.score.level = 3
    state.score.lines = 12
    renderer = MainRenderer(screen)

    renderer.draw(state)

    assert renderer.screen is screen
