# Buenas Prácticas — Clean Code para Space Invaders

## 1. Naming
- Clases: `PascalCase` (`EnemyFormation`, `CollisionManager`).
- Funciones/variables: `snake_case` descriptivo (`check_player_bullets_vs_enemies`, no `check1`).
- Constantes: `UPPER_SNAKE_CASE`, todas en `settings.py` — **cero magic numbers** en el código (ni `5`, ni `0.3`, ni `800`).
- Sin abreviaciones crípticas (`enm` → `enemy`).

## 2. Single Responsibility
- 1 clase = 1 responsabilidad. `Player` no dibuja HUD. `GameView` no calcula colisiones (delega a `CollisionManager`).
- Si un método supera ~20 líneas, probablemente hace más de una cosa → dividir.

## 3. Funciones pequeñas y predecibles
- Máx ~15-20 líneas por método.
- Sin efectos secundarios ocultos: si una función se llama `check_collision`, no debe también sumar puntos o reproducir sonido — eso lo hace quien la llama.

## 4. DRY (Don't Repeat Yourself)
- Lógica de movimiento/animación repetida entre `Enemy` y `Player` → extraer a clase base o mixin si aplica.
- Spawneo de balas jugador/enemigo: una sola función parametrizada, no dos copias.

## 5. Composición sobre herencia
- Prefiere `EnemyFormation` conteniendo lista de `Enemy`, no una jerarquía profunda de subclases de enemigos. Usa atributos (`enemy_type`, `points_value`) en vez de subclases por tipo si solo cambian datos.

## 6. Manejo de errores
- Carga de assets (`arcade.load_texture`, `arcade.Sound`) envuelta en `try/except` con mensaje claro — si falta un archivo, debe fallar con log entendible, no traceback genérico.
- Validar límites de pantalla, índices de listas (`enemy_formation` vacía, etc.).

## 7. Type hints
- Todo método con type hints en parámetros y retorno: `def add_points(self, points: int) -> None:`. Ayuda en informe ("buenas prácticas de código") y autocompletado.

## 8. Docstrings consistentes
- Formato corto por método (1-3 líneas): qué hace, no cómo. Ejemplo:
```python
def can_shoot(self) -> bool:
    """Retorna True si el cooldown de disparo terminó."""
```

## 9. Separación de concerns (arquitectura ya definida)
- `entities/` = datos + comportamiento propio del sprite.
- `managers/` = lógica de coordinación entre entidades (colisión, score, oleadas).
- `ui/` = solo presentación (Views, HUD).
- Nunca mezclar: un manager no debe dibujar, una entidad no debe decidir reglas de juego globales (eso es del manager/GameView).

## 10. Evitar "God Class" en `GameView`
- `GameView.on_update` debe **orquestar**, no implementar. Si crece mucho, delega bloques a métodos privados (`_update_entities`, `_handle_collisions`, `_check_game_state`).

## 11. Control de versiones limpio
- Commits atómicos por funcionalidad (ya definidos por fase). Mensajes en imperativo: "agrega FSM de enemigos", no "cambios".
- No commitear código comentado/muerto ni prints de debug.

## 12. Consistencia de estilo
- Un solo formateador (`black` o `ruff format`) corriendo antes de cada commit. Evita discusiones de estilo (aplica aunque sea solo, para README/evaluador).
