# Tests — Contexto y Esqueleto

Framework: `pytest`. Carpeta `tests/` en raíz, espejo de `src/`.

```
tests/
├── conftest.py
├── test_player.py
├── test_bullet.py
├── test_enemy.py
├── test_collision_manager.py
├── test_score_manager.py
└── test_wave_manager.py
```

**Perspectiva:** tests unitarios sobre lógica pura (no dependen de ventana/render de Arcade). Se prueban estados y transiciones, no gráficos. Evita abrir `arcade.Window` real en tests — usar mocks/stubs para `arcade.Sprite` cuando haga falta textura.

---

## `conftest.py`
Fixtures compartidas para evitar repetir setup en cada test.

- `player()`: fixture que retorna instancia limpia de `Player` con posición inicial conocida.
- `enemy_formation()`: fixture que retorna `EnemyFormation` chica (ej. 2x2) para tests rápidos.
- `bullet_factory()`: fixture que retorna función para crear `Bullet` con parámetros default.

---

## `test_player.py`
Verifica movimiento, límites de pantalla y cooldown de disparo.

- `test_move_left_sets_negative_change_x`: confirma que `move_left()` deja `change_x < 0`.
- `test_move_right_sets_positive_change_x`: confirma que `move_right()` deja `change_x > 0`.
- `test_player_stops_at_screen_edge`: mueve jugador hasta borde, confirma que `update()` no lo deja salir.
- `test_can_shoot_false_during_cooldown`: dispara, confirma que `can_shoot()` retorna `False` inmediatamente después.
- `test_can_shoot_true_after_cooldown_expires`: avanza `cooldown_timer` a 0, confirma `can_shoot()` retorna `True`.
- `test_lives_decrease_on_damage`: aplica daño, confirma que `lives` baja en 1.

---

## `test_bullet.py`
Verifica movimiento y despawn de balas.

- `test_bullet_moves_up_when_owner_is_player`: confirma `change_y > 0` para balas de jugador.
- `test_bullet_moves_down_when_owner_is_enemy`: confirma `change_y < 0` para balas enemigas.
- `test_bullet_removed_when_offscreen`: simula posición fuera de pantalla, confirma que se elimina de `SpriteList`.
- `test_bullet_reset_repositions_correctly`: llama `reset()`, confirma nueva posición/dirección (valida object pooling).

---

## `test_enemy.py`
Verifica formación y FSM de movimiento.

- `test_formation_creates_correct_grid_size`: confirma cantidad de enemigos = `rows * cols`.
- `test_formation_moves_right_then_left_on_edge`: simula enemigo llegando a borde derecho, confirma cambio de estado a `MOVING_LEFT`.
- `test_formation_descends_on_direction_change`: confirma que `y` de todos los enemigos baja al cambiar de dirección.
- `test_is_empty_true_when_all_enemies_removed`: elimina todos los enemigos, confirma `is_empty()` retorna `True`.
- `test_random_shooter_returns_alive_enemy_position`: confirma que la posición retornada corresponde a un enemigo vivo.

---

## `test_collision_manager.py`
Verifica detección y resolución de colisiones (sin render).

- `test_player_bullet_hits_enemy_removes_both`: posiciona bala sobre enemigo, confirma que ambos sprites se eliminan y se retornan puntos > 0.
- `test_no_collision_returns_zero_points`: bala lejos de cualquier enemigo, confirma retorno de 0 puntos.
- `test_enemy_bullet_hits_player_reduces_lives`: posiciona bala enemiga sobre jugador, confirma `lives -= 1`.
- `test_enemies_reaching_player_triggers_game_over_flag`: posiciona formación en y del jugador, confirma flag de derrota.
- `test_bullet_vs_barrier_reduces_hp`: bala impacta barrera, confirma reducción de `hp`.

---

## `test_score_manager.py`
Verifica acumulación y persistencia de puntaje.

- `test_add_points_increases_score`: suma puntos, confirma `score` actualizado.
- `test_high_score_updates_when_exceeded`: score supera high score guardado, confirma actualización.
- `test_high_score_not_updated_when_lower`: score menor a high score, confirma que no cambia.

---

## `test_wave_manager.py`
Verifica progresión de oleadas y dificultad.

- `test_next_wave_increments_counter`: llama `next_wave()`, confirma `current_wave += 1`.
- `test_enemy_speed_increases_per_wave`: confirma que velocidad de nueva oleada > velocidad de oleada anterior.
- `test_start_wave_creates_new_formation`: confirma que se genera nueva `EnemyFormation` con enemigos vivos.

---

## Cobertura esperada

Prioridad: `collision_manager` (núcleo de la mecánica) > `enemy` (FSM) > `player`/`bullet` > `score`/`wave`. No es necesario testear `ui/` (views) ni dibujo — bajo retorno de inversión para este alcance.
