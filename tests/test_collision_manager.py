import arcade
from src.managers.collision_manager import CollisionManager
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy
from src.entities.barrier import Barrier
from src.settings import BARRIER_HP

def test_player_bullet_hits_enemy_removes_both() -> None:
    """Verifica que una bala del jugador destruya al enemigo, se destruya a sí misma y sume puntos."""
    manager = CollisionManager()
    bullets = arcade.SpriteList()
    enemies = arcade.SpriteList()

    bullet = Bullet("player", 1)
    bullet.center_x = 100
    bullet.center_y = 100
    bullets.append(bullet)

    enemy = Enemy(row=0, col=0)
    enemy.center_x = 100
    enemy.center_y = 100
    enemies.append(enemy)

    points = manager.check_player_bullets_vs_enemies(bullets, enemies)
    
    assert points == enemy.points_value
    assert bullet not in bullets
    assert enemy not in enemies

def test_no_collision_returns_zero_points() -> None:
    """Verifica que si no hay contacto, no se sumen puntos ni se eliminen los sprites."""
    manager = CollisionManager()
    bullets = arcade.SpriteList()
    enemies = arcade.SpriteList()

    bullet = Bullet("player", 1)
    bullet.center_x = 100
    bullet.center_y = 100
    bullets.append(bullet)

    enemy = Enemy(row=0, col=0)
    enemy.center_x = 300  # Lejos del proyectil
    enemy.center_y = 300
    enemies.append(enemy)

    points = manager.check_player_bullets_vs_enemies(bullets, enemies)
    
    assert points == 0
    assert bullet in bullets
    assert enemy in enemies

def test_enemy_bullet_hits_player_reduces_lives() -> None:
    """Verifica que el impacto de una bala enemiga reste vidas al jugador."""
    manager = CollisionManager()
    bullets = arcade.SpriteList()
    player = Player()
    player.center_x = 100
    player.center_y = 50

    bullet = Bullet("enemy", -1)
    bullet.center_x = 100
    bullet.center_y = 50
    bullets.append(bullet)

    initial_lives = player.lives
    hit = manager.check_enemy_bullets_vs_player(bullets, player)
    
    assert hit is True
    assert player.lives == initial_lives - 1
    assert bullet not in bullets

def test_enemies_reaching_player_triggers_game_over_flag() -> None:
    """Verifica que se detecte cuando los enemigos llegan a la línea del jugador."""
    manager = CollisionManager()
    enemies = arcade.SpriteList()
    player = Player()
    player.center_x = 100
    player.center_y = 50

    enemy = Enemy(row=0, col=0)
    enemy.center_x = 100
    enemy.center_y = player.top - 1  # Rebasó la parte superior del jugador
    enemies.append(enemy)

    assert manager.check_enemies_vs_player(enemies, player) is True

def test_bullet_vs_barrier_reduces_hp() -> None:
    """Verifica que las balas impactando contra las barreras reduzcan su HP."""
    manager = CollisionManager()
    bullets = arcade.SpriteList()
    barriers = arcade.SpriteList()

    bullet = Bullet("player", 1)
    bullet.center_x = 100
    bullet.center_y = 100
    bullets.append(bullet)

    barrier = Barrier(100, 100)
    barriers.append(barrier)

    manager.check_bullets_vs_barriers(bullets, barriers)
    
    assert barrier.hp == BARRIER_HP - 1
    assert bullet not in bullets

def test_double_bullet_hit_no_double_points() -> None:
    """Verifica que múltiples balas impactando un mismo enemigo en el mismo frame no den doble puntaje."""
    manager = CollisionManager()
    bullets = arcade.SpriteList()
    enemies = arcade.SpriteList()

    # Dos balas en la misma coordenada
    bullet1 = Bullet("player", 1)
    bullet1.center_x = 150
    bullet1.center_y = 150
    bullets.append(bullet1)

    bullet2 = Bullet("player", 1)
    bullet2.center_x = 150
    bullet2.center_y = 150
    bullets.append(bullet2)

    enemy = Enemy(row=0, col=0)
    enemy.center_x = 150
    enemy.center_y = 150
    enemies.append(enemy)

    points = manager.check_player_bullets_vs_enemies(bullets, enemies)
    
    # Se obtienen puntos una única vez y la primera bala es removida. La segunda continúa viaje.
    assert points == enemy.points_value
    assert enemy not in enemies
    assert len(bullets) == 1
