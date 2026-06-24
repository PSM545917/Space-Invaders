import arcade
import random
import enum
from src.settings import (
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ENEMY_SPACING_X,
    ENEMY_SPACING_Y,
    ENEMY_START_X,
    ENEMY_START_Y,
    ENEMY_DESCEND_AMOUNT,
    ENEMY_POINTS,
    SCREEN_WIDTH,
    ASSET_PATHS,
)

class FormationState(enum.Enum):
    """Estados del movimiento coordinado de la formación de enemigos."""
    MOVING_RIGHT = 1
    MOVING_LEFT = 2
    DESCEND = 3

class Enemy(arcade.Sprite):
    """Representa a un invasor individual en la formación."""

    def __init__(self, row: int, col: int) -> None:
        """Inicializa al enemigo con textura, color según su fila y almacena sus índices."""
        texture = arcade.load_texture(ASSET_PATHS["sprites"]["enemy"])
        super().__init__(texture)
        if row == 0:
            self.color = arcade.color.RED_DEVIL
        elif row in (1, 2):
            self.color = arcade.color.PUMPKIN
        else:
            self.color = arcade.color.MAGENTA
        self.row: int = row
        self.col: int = col
        self.points_value: int = ENEMY_POINTS.get(row, 10)

class EnemyFormation:
    """Administra la cuadrícula de enemigos y su máquina de estados de movimiento."""

    def __init__(self, rows: int, cols: int, speed: float) -> None:
        """Inicializa la formación, instanciando la grilla completa de enemigos."""
        self.enemies: arcade.SpriteList = arcade.SpriteList()
        self.speed: float = speed
        self.state: FormationState = FormationState.MOVING_RIGHT
        self.next_state: FormationState = FormationState.MOVING_LEFT

        # Generación de la grilla de invasores
        for r in range(rows):
            for c in range(cols):
                x = ENEMY_START_X + c * (ENEMY_WIDTH + ENEMY_SPACING_X)
                y = ENEMY_START_Y + r * (ENEMY_HEIGHT + ENEMY_SPACING_Y)
                enemy = Enemy(r, c)
                enemy.center_x = x
                enemy.center_y = y
                self.enemies.append(enemy)

    def update(self, delta_time: float) -> None:
        """Actualiza el movimiento coordinado del grupo aplicando la FSM."""
        if not self.enemies:
            return

        if self.state == FormationState.MOVING_RIGHT:
            # Mover todos los enemigos a la derecha
            displacement = self.speed * delta_time
            for enemy in self.enemies:
                enemy.center_x += displacement

            # Detectar si alguno tocó el borde derecho de la pantalla
            hit_edge = False
            for enemy in self.enemies:
                if enemy.right >= SCREEN_WIDTH:
                    hit_edge = True
                    break

            if hit_edge:
                self.state = FormationState.DESCEND
                self.next_state = FormationState.MOVING_LEFT

        elif self.state == FormationState.MOVING_LEFT:
            # Mover todos los enemigos a la izquierda
            displacement = -self.speed * delta_time
            for enemy in self.enemies:
                enemy.center_x += displacement

            # Detectar si alguno tocó el borde izquierdo de la pantalla
            hit_edge = False
            for enemy in self.enemies:
                if enemy.left <= 0:
                    hit_edge = True
                    break

            if hit_edge:
                self.state = FormationState.DESCEND
                self.next_state = FormationState.MOVING_RIGHT

        # Manejo inmediato de la transición descendente
        if self.state == FormationState.DESCEND:
            # Descender toda la formación verticalmente
            for enemy in self.enemies:
                enemy.center_y -= ENEMY_DESCEND_AMOUNT

            # Cambiar de estado a la nueva dirección horizontal
            self.state = self.next_state

    def random_shooter(self) -> tuple[float, float] | None:
        """Elige un enemigo vivo al azar y retorna su posición (x, y)."""
        if not self.enemies:
            return None
        # Selecciona un enemigo al azar de la lista
        enemy = random.choice(list(self.enemies))
        return enemy.center_x, enemy.center_y

    def is_empty(self) -> bool:
        """Retorna True si no quedan enemigos vivos en la formación."""
        return len(self.enemies) == 0
