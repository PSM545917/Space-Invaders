# Space Invaders — Esqueleto de Proyecto

Repo: https://github.com/PSM545917/Space-Invaders.git
Stack: Python 3.13 + Arcade + uv

---

## Estructura

```
space-invaders/
├── README.md
├── pyproject.toml
├── main.py
├── src/
│   ├── settings.py
│   ├── game.py
│   ├── entities/
│   │   ├── player.py
│   │   ├── enemy.py
│   │   ├── bullet.py
│   │   └── barrier.py
│   ├── managers/
│   │   ├── collision_manager.py
│   │   ├── wave_manager.py
│   │   └── score_manager.py
│   └── ui/
│       ├── menu_view.py
│       ├── game_over_view.py
│       └── hud.py
└── assets/
    ├── sprites/
    ├── sounds/
    └── fonts/
```

---

## FASE 0 — Setup

**Archivos:** `pyproject.toml`, `main.py`, `src/settings.py`, carpetas `assets/`

### `pyproject.toml`
Define dependencias (`arcade`) y metadata del proyecto. Generado/ajustado con `uv init` + `uv add arcade`.

### `main.py`
Punto de entrada. Crea `arcade.Window`, instancia `MenuView`, llama `arcade.run()`.

- `main()`: crea ventana, setea vista inicial (`MenuView`), arranca loop con `arcade.run()`.

### `src/settings.py`
Constantes globales del juego (sin clases, solo valores).

Contiene: `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `SCREEN_TITLE`, `PLAYER_SPEED`, `BULLET_SPEED`, `ENEMY_SPEED_BASE`, `ENEMY_ROWS`, `ENEMY_COLS`, `PLAYER_LIVES`, `ASSET_PATHS` (dict con rutas a sprites/sonidos).

**Commit:**
```bash
git init
git add pyproject.toml main.py src/settings.py
git commit -m "fase0: setup proyecto, dependencias y settings globales"
```

---

## FASE 1 — Jugador y disparo

**Archivos:** `src/entities/player.py`, `src/entities/bullet.py`

### `src/entities/player.py`
Clase `Player(arcade.Sprite)`. Controla movimiento horizontal y disparo del jugador.

- `__init__(self)`: carga textura, posición inicial, setea `lives`, `cooldown_timer`.
- `update(self, delta_time)`: aplica `change_x` según input, limita posición a bordes de pantalla.
- `move_left(self)` / `move_right(self)`: setea `change_x` negativo/positivo.
- `stop_moving(self)`: setea `change_x = 0`.
- `can_shoot(self)`: retorna `True` si `cooldown_timer <= 0`.
- `shoot(self)`: crea y retorna instancia de `Bullet`, resetea `cooldown_timer`.

### `src/entities/bullet.py`
Clase `Bullet(arcade.Sprite)`. Proyectil reusable (jugador o enemigo).

- `__init__(self, owner, direction)`: carga textura según `owner` ("player"/"enemy"), setea velocidad según `direction`.
- `update(self, delta_time)`: mueve bala en `change_y`, marca `self.remove_from_sprite_lists()` si sale de pantalla.
- `reset(self, x, y, direction)`: reposiciona bala para reuso (soporta **object pooling**).

**Commit:**
```bash
git add src/entities/player.py src/entities/bullet.py
git commit -m "fase1: jugador con movimiento y disparo (object pooling balas)"
```

---

## FASE 2 — Enemigos y formación

**Archivos:** `src/entities/enemy.py`, `src/managers/wave_manager.py`

### `src/entities/enemy.py`
Clase `Enemy(arcade.Sprite)` + clase `EnemyFormation`. Maneja grid de enemigos y su FSM de movimiento.

- `Enemy.__init__(self, row, col)`: carga textura según tipo/fila, posición inicial en grid.
- `Enemy.update(self, delta_time)`: aplica movimiento delegado por `EnemyFormation` (no individual).
- `EnemyFormation.__init__(self, rows, cols)`: crea `SpriteList`, instancia enemigos en grid.
- `EnemyFormation.update(self, delta_time)`: implementa **FSM** (`MOVING_RIGHT` → `MOVING_LEFT` → `DESCEND`), detecta bordes de pantalla y desciende toda la formación.
- `EnemyFormation.random_shooter(self)`: elige enemigo random vivo, retorna posición para disparo.
- `EnemyFormation.is_empty(self)`: retorna `True` si no quedan enemigos (condición de victoria).

### `src/managers/wave_manager.py`
Controla oleadas y dificultad progresiva.

- `__init__(self)`: setea `current_wave = 1`, velocidad base.
- `start_wave(self, wave_number)`: crea nueva `EnemyFormation`, incrementa velocidad según `wave_number`.
- `next_wave(self)`: incrementa contador, llama `start_wave`.

**Commit:**
```bash
git add src/entities/enemy.py src/managers/wave_manager.py
git commit -m "fase2: formacion de enemigos con FSM y sistema de oleadas"
```

---

## FASE 3 — Colisiones, vidas y score

**Archivos:** `src/managers/collision_manager.py`, `src/managers/score_manager.py`, `src/entities/barrier.py`

### `src/managers/collision_manager.py`
Centraliza toda la lógica de detección de colisiones (AABB vía Arcade).

- `check_player_bullets_vs_enemies(self, bullets, enemies)`: detecta colisión, elimina ambos sprites, retorna puntos ganados.
- `check_enemy_bullets_vs_player(self, bullets, player)`: detecta colisión, resta vida al jugador.
- `check_enemies_vs_player(self, enemies, player)`: detecta si formación llegó a nivel del jugador (game over).
- `check_bullets_vs_barriers(self, bullets, barriers)`: detecta impacto y reduce HP de la barrera.

### `src/managers/score_manager.py`
Lleva el puntaje y high score.

- `__init__(self)`: setea `score = 0`, carga `high_score` desde archivo local.
- `add_points(self, points)`: suma al score actual.
- `save_high_score(self)`: persiste high score si fue superado (escribe a archivo simple).

### `src/entities/barrier.py`
Clase `Barrier(arcade.Sprite)`. Escudo destructible (opcional pero suma puntos).

- `__init__(self, x, y)`: carga textura, setea `hp`.
- `take_damage(self, amount)`: resta `hp`, cambia textura según daño, se elimina si `hp <= 0`.

**Commit:**
```bash
git add src/managers/collision_manager.py src/managers/score_manager.py src/entities/barrier.py
git commit -m "fase3: sistema de colisiones, score y barreras destructibles"
```

---

## FASE 4 — Vistas (Menu, Game, GameOver) y HUD

**Archivos:** `src/ui/menu_view.py`, `src/game.py`, `src/ui/game_over_view.py`, `src/ui/hud.py`

### `src/ui/menu_view.py`
Clase `MenuView(arcade.View)`. Pantalla inicial.

- `on_draw(self)`: dibuja título, instrucciones, "presiona ENTER".
- `on_key_press(self, key, modifiers)`: si `ENTER`, cambia a `GameView`.

### `src/game.py`
Clase `GameView(arcade.View)`. Loop principal del gameplay — orquesta todos los managers y entidades.

- `__init__(self)`: instancia `Player`, `WaveManager`, `CollisionManager`, `ScoreManager`, `SpriteList`s.
- `on_show_view(self)`: setea color de fondo, reinicia estado si es nueva partida.
- `on_update(self, delta_time)`: actualiza todas las entidades, llama checks de `CollisionManager`, verifica condiciones de victoria/derrota.
- `on_draw(self)`: dibuja todos los `SpriteList`s y el `HUD`.
- `on_key_press(self, key, modifiers)` / `on_key_release(self, key, modifiers)`: delega input a `Player` (mover/disparar).
- `check_game_over(self)`: si `lives <= 0` o enemigos llegan abajo, cambia a `GameOverView`.

### `src/ui/game_over_view.py`
Clase `GameOverView(arcade.View)`. Pantalla de derrota/victoria.

- `__init__(self, score)`: guarda score final a mostrar.
- `on_draw(self)`: dibuja "GAME OVER", score final, high score, "presiona R para reiniciar".
- `on_key_press(self, key, modifiers)`: si `R`, vuelve a `GameView` nuevo.

### `src/ui/hud.py`
Clase `HUD`. Dibuja score, vidas y oleada actual durante el juego (no es una View, es un helper dibujado dentro de `GameView`).

- `__init__(self)`: carga fuente pixel.
- `draw(self, score, lives, wave)`: dibuja texto en esquinas de pantalla con `arcade.draw_text`.

**Commit:**
```bash
git add src/ui/ src/game.py
git commit -m "fase4: vistas menu/game/gameover y HUD"
```

---

## FASE 5 — Pulido y entrega

**Tareas (sin archivos nuevos necesariamente):**
- Sonidos: integrar `arcade.Sound` en disparo/explosión/música fondo (en `player.py`, `enemy.py`, `game.py`).
- Animación explosión: spritesheet en `enemy.py`/`bullet.py` al morir.
- Balance: ajustar velocidades, cooldowns, puntos por tipo de enemigo.
- `README.md`: instrucciones de instalación (`uv sync`), ejecución (`uv run main.py`), controles.
- Testing manual: jugar 10+ partidas buscando bugs/glitches (requisito explícito del enunciado).

**Commit final:**
```bash
git add .
git commit -m "fase5: sonido, animaciones, balance y README final"
git tag v1.0
git push origin main --tags
```

---

## Comandos generales del flujo

```bash
# clonar/iniciar
git clone https://github.com/PSM545917/Space-Invaders.git
cd Space-Invaders
uv sync

# correr juego
uv run main.py

# flujo por fase
git checkout -b fase-X
# ... codear ...
git add <archivos>
git commit -m "fase X: descripcion"
git checkout main
git merge fase-X
git push origin main
```
