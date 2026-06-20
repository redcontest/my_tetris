"""
Точка входа в игру.

Описание зоны ответственности модуля:
Модуль только создает объект игры и запускает его.
"""
from src.tetris.game import Game


if __name__ == "__main__":
    game = Game()
    game.start()
