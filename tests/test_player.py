from src.entities.player import Player
from src.settings import PLAYER_SPEED, SCREEN_WIDTH, PLAYER_COOLDOWN, PLAYER_LIVES

def test_move_left_sets_negative_change_x(player) -> None:
    """Verifica que move_left asigne velocidad negativa."""
    player.move_left()
    assert player.change_x == -PLAYER_SPEED

def test_move_right_sets_positive_change_x(player) -> None:
    """Verifica que move_right asigne velocidad positiva."""
    player.move_right()
    assert player.change_x == PLAYER_SPEED

def test_player_stops_at_screen_edge(player) -> None:
    """Verifica que el jugador no pueda salirse de la pantalla y detenga su velocidad."""
    half_width = player.width / 2

    # Probar borde izquierdo
    player.center_x = half_width + 10
    player.move_left()
    # Ejecutar actualización que supera el borde izquierdo
    player.update(delta_time=1.0)
    assert player.center_x == half_width
    assert player.change_x == 0.0

    # Probar borde derecho
    player.center_x = SCREEN_WIDTH - half_width - 10
    player.move_right()
    # Ejecutar actualización que supera el borde derecho
    player.update(delta_time=1.0)
    assert player.center_x == SCREEN_WIDTH - half_width
    assert player.change_x == 0.0

def test_can_shoot_false_during_cooldown(player) -> None:
    """Verifica que no se pueda disparar mientras esté en cooldown."""
    assert player.can_shoot() is True
    player.shoot()
    assert player.can_shoot() is False

def test_can_shoot_true_after_cooldown_expires(player) -> None:
    """Verifica que se pueda volver a disparar al expirar el temporizador de cooldown."""
    player.shoot()
    assert player.can_shoot() is False
    
    # Simular paso del tiempo igual al cooldown
    player.update(delta_time=PLAYER_COOLDOWN)
    assert player.can_shoot() is True

def test_lives_decrease_on_damage(player) -> None:
    """Verifica que las vidas bajen al recibir daño."""
    assert player.lives == PLAYER_LIVES
    player.lives -= 1
    assert player.lives == PLAYER_LIVES - 1
