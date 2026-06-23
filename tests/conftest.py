import pytest
from src.entities.player import Player
from src.entities.bullet import Bullet

@pytest.fixture
def player() -> Player:
    """Fixture que retorna una instancia limpia de Player."""
    return Player()

@pytest.fixture
def bullet_factory():
    """Fixture que retorna una función fábrica para crear proyectiles."""
    def _make_bullet(owner: str = "player", direction: int = 1) -> Bullet:
        return Bullet(owner=owner, direction=direction)
    return _make_bullet

@pytest.fixture
def enemy_formation() -> EnemyFormation:
    """Fixture que retorna una EnemyFormation de tamaño reducido (2x2) para pruebas rápidas."""
    from src.entities.enemy import EnemyFormation
    return EnemyFormation(rows=2, cols=2, speed=100.0)
