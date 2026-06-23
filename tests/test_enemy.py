from src.entities.enemy import EnemyFormation, FormationState
from src.settings import SCREEN_WIDTH, ENEMY_DESCEND_AMOUNT

def test_formation_creates_correct_grid_size(enemy_formation) -> None:
    """Verifica que la formación inicialice el número correcto de enemigos (rows * cols)."""
    # La fixture enemy_formation crea una cuadrícula de 2x2 (4 enemigos)
    assert len(enemy_formation.enemies) == 4

def test_formation_moves_right_then_left_on_edge(enemy_formation) -> None:
    """Verifica que la formación cambie su estado a MOVING_LEFT al chocar con el borde derecho."""
    # Colocar la formación deliberadamente en el extremo derecho
    for enemy in enemy_formation.enemies:
        enemy.center_x = SCREEN_WIDTH + 10.0
    
    assert enemy_formation.state == FormationState.MOVING_RIGHT
    enemy_formation.update(0.016)
    
    # La FSM procesa el descenso y cambia de inmediato a MOVING_LEFT en el mismo frame
    assert enemy_formation.state == FormationState.MOVING_LEFT

def test_formation_descends_on_direction_change(enemy_formation) -> None:
    """Verifica que todas las Y de los enemigos bajen cuando cambia la dirección."""
    # Guardar las Y iniciales
    initial_ys = [enemy.center_y for enemy in enemy_formation.enemies]

    # Forzar el choque con el borde derecho para gatillar el descenso
    for enemy in enemy_formation.enemies:
        enemy.center_x = SCREEN_WIDTH + 10.0
    
    enemy_formation.update(0.016)

    # Confirmar que la altura disminuyó por la constante ENEMY_DESCEND_AMOUNT
    for i, enemy in enumerate(enemy_formation.enemies):
        assert enemy.center_y == initial_ys[i] - ENEMY_DESCEND_AMOUNT

def test_is_empty_true_when_all_enemies_removed(enemy_formation) -> None:
    """Verifica que is_empty sea True cuando no hay enemigos vivos."""
    assert enemy_formation.is_empty() is False
    enemy_formation.enemies.clear()
    assert enemy_formation.is_empty() is True

def test_random_shooter_returns_alive_enemy_position(enemy_formation) -> None:
    """Verifica que random_shooter retorne la posición de un invasor vivo y None si está vacía."""
    pos = enemy_formation.random_shooter()
    assert pos is not None
    assert len(pos) == 2
    
    # Verificar que las coordenadas pertenezcan a algún enemigo de la formación
    x_coords = [e.center_x for e in enemy_formation.enemies]
    y_coords = [e.center_y for e in enemy_formation.enemies]
    assert pos[0] in x_coords
    assert pos[1] in y_coords

    # Probar caso límite de formación vacía
    enemy_formation.enemies.clear()
    assert enemy_formation.random_shooter() is None
