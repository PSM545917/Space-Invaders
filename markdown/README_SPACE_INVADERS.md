# Space Invaders

Proyecto final — Aplicaciones de la Infografía. Clon de Space Invaders en Python + Arcade.

## Requisitos

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (gestor de dependencias)

## Instalación

```bash
git clone https://github.com/PSM545917/Space-Invaders.git
cd Space-Invaders
uv sync
```

## Ejecución

```bash
uv run main.py
```

## Controles

| Tecla | Acción |
|---|---|
| ← / → | Mover nave |
| ESPACIO | Disparar |
| ENTER | Iniciar / confirmar en menú |
| R | Reiniciar (pantalla Game Over) |
| ESC | Salir |

## Estructura del proyecto

```
src/
├── settings.py        # constantes globales
├── game.py             # GameView, loop principal
├── entities/            # Player, Enemy, Bullet, Barrier
├── managers/             # Collision, Wave, Score
└── ui/                    # MenuView, GameOverView, HUD
assets/                     # sprites, sonidos, fuentes
tests/                       # tests unitarios (pytest)
```

Detalle de archivos y métodos: ver `ESQUELETO_PROYECTO.md`.

## Mecánica

Formación de enemigos avanza y desciende hasta el jugador. El jugador dispara para eliminarlos antes de que la formación llegue al fondo o se acaben sus 3 vidas. Dificultad sube por oleada.

## Tests

```bash
uv run pytest
```

Ver `TESTS.md` para detalle de cobertura.

## Autor

Pablo Schmidt — Computer Systems Engineering, UPB.
