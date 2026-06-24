import arcade
from src.entities.bullet import Bullet
from src.settings import BULLET_SPEED, SCREEN_HEIGHT

def test_bullet_moves_up_when_owner_is_player(bullet_factory) -> None:
    """Verifica que las balas del jugador tengan velocidad vertical positiva."""
    bullet = bullet_factory(owner="player", direction=1)
    assert bullet.change_y > 0
    assert bullet.change_y == BULLET_SPEED

def test_bullet_moves_down_when_owner_is_enemy(bullet_factory) -> None:
    """Verifica que las balas de enemigos tengan velocidad vertical negativa."""
    bullet = bullet_factory(owner="enemy", direction=-1)
    assert bullet.change_y < 0
    assert bullet.change_y == -BULLET_SPEED

def test_bullet_removed_when_offscreen(bullet_factory) -> None:
    """Verifica que las balas se eliminen del SpriteList cuando salen de la pantalla."""
    sprite_list = arcade.SpriteList()
    
    # Proyectil subiendo que sale por arriba
    bullet_up = bullet_factory(owner="player", direction=1)
    sprite_list.append(bullet_up)
    bullet_up.center_y = SCREEN_HEIGHT + 100
    bullet_up.update()
    assert bullet_up not in sprite_list

    # Proyectil bajando que sale por abajo
    bullet_down = bullet_factory(owner="enemy", direction=-1)
    sprite_list.append(bullet_down)
    bullet_down.center_y = -100
    bullet_down.update()
    assert bullet_down not in sprite_list

def test_bullet_reset_repositions_correctly(bullet_factory) -> None:
    """Verifica que el método reset reposicione y cambie la velocidad de la bala."""
    bullet = bullet_factory(owner="player", direction=1)
    bullet.reset(100.0, 200.0, -1)
    assert bullet.center_x == 100.0
    assert bullet.center_y == 200.0
    assert bullet.change_y == -BULLET_SPEED
