
import pygame
from enum import Enum


class CEnemyState:
    def __init__(self, start_pos: pygame.Vector2) -> None:
        self.state = EnemyState.IDLE
        self.start_pos = pygame.Vector2(start_pos.x, start_pos.y)



class EnemyState(Enum):
    IDLE = 0
    MOVE = 1
    RETURN = 2