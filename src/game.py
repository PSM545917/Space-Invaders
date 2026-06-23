import arcade
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_COOLDOWN,
    HIGH_SCORE_FILE,
)
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.barrier import Barrier
from src.managers.collision_manager import CollisionManager
from src.managers.wave_manager import WaveManager
from src.managers.score_manager import ScoreManager
from src.ui.hud import HUD
from src.ui.game_over_view import GameOverView

class GameView(arcade.View):
    """Loop principal del gameplay — orquesta todas las entidades y managers del juego."""

    def __init__(self) -> None:
        """Inicializa los componentes de la partida actual, grillas de sprites y pool de balas."""
        super().__init__()
        # Inicialización de Entidades y Managers
        self.player: Player = Player()
        self.wave_manager: WaveManager = WaveManager()
        self.collision_manager: CollisionManager = CollisionManager()
        self.score_manager: ScoreManager = ScoreManager()
        self.hud: HUD = HUD()

        # Listas de Sprites de Arcade
        self.bullets: arcade.SpriteList = arcade.SpriteList()
        self.barriers: arcade.SpriteList = arcade.SpriteList()

        # Iniciar la primera oleada y referenciar sus enemigos
        self.wave_manager.start_wave(1)

        # Generar las barreras
        self._setup_barriers()

        # Estructuras para el Object Pooling de Proyectiles
        self.bullet_pool: list[Bullet] = []
        self.active_bullets_tracking: list[Bullet] = []

        # Temporizadores para disparo enemigo
        self.enemy_shoot_timer: float = 0.0
        self.enemy_shoot_cooldown: float = 1.5

    def _setup_barriers(self) -> None:
        """Instancia 4 barreras distribuidas simétricamente a lo ancho de la pantalla."""
        x_positions = [160, 320, 480, 640]
        y_position = 150.0
        for x in x_positions:
            barrier = Barrier(x, y_position)
            self.barriers.append(barrier)

    def _spawn_bullet(self, x: float, y: float, owner: str, direction: int) -> None:
        """Obtiene una bala inactiva del pool (o crea una nueva) y la coloca en la grilla activa."""
        if self.bullet_pool:
            bullet = self.bullet_pool.pop()
            bullet.reset(x, y, direction)
            # Reasignar el dueño y color del proyectil
            bullet.owner = owner
            bullet.color = arcade.color.YELLOW if owner == "player" else arcade.color.RED
        else:
            bullet = Bullet(owner, direction)
            bullet.center_x = x
            bullet.center_y = y

        self.bullets.append(bullet)
        self.active_bullets_tracking.append(bullet)

    def _reclaim_bullets(self) -> None:
        """Detecta proyectiles inactivos (removidos de self.bullets) y los devuelve al pool."""
        reclaimed = []
        for bullet in self.active_bullets_tracking:
            if bullet not in self.bullets:
                reclaimed.append(bullet)
                self.bullet_pool.append(bullet)
        
        for bullet in reclaimed:
            self.active_bullets_tracking.remove(bullet)

    def on_show_view(self) -> None:
        """Se ejecuta cuando la vista se activa. Establece el color de fondo."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self) -> None:
        """Dibuja todos los elementos en pantalla: entidades, grillas y HUD."""
        self.clear()

        # Dibujar todos los Sprites activos
        self.player.draw()
        self.bullets.draw()
        if self.wave_manager.formation and self.wave_manager.formation.enemies:
            self.wave_manager.formation.enemies.draw()
        self.barriers.draw()

        # Dibujar HUD
        self.hud.draw(
            score=self.score_manager.score,
            lives=self.player.lives,
            wave=self.wave_manager.current_wave
        )

    def on_update(self, delta_time: float) -> None:
        """Actualiza el estado de las entidades, maneja colisiones y vigila el estado de juego."""
        self._update_entities(delta_time)
        self._handle_collisions()
        self._check_game_state()
        self._reclaim_bullets()

    def _update_entities(self, delta_time: float) -> None:
        """Actualiza las posiciones y comportamientos de las entidades y disparadores."""
        # Jugador y proyectiles
        self.player.update(delta_time)
        self.bullets.update(delta_time)

        # Formación de enemigos
        if self.wave_manager.formation:
            self.wave_manager.formation.update(delta_time)

            # Disparo aleatorio de enemigos
            self.enemy_shoot_timer += delta_time
            if self.enemy_shoot_timer >= self.enemy_shoot_cooldown:
                self.enemy_shoot_timer = 0.0
                shoot_pos = self.wave_manager.formation.random_shooter()
                if shoot_pos:
                    self._spawn_bullet(shoot_pos[0], shoot_pos[1], "enemy", -1)

    def _handle_collisions(self) -> None:
        """Resuelve los impactos ocurridos en la partida delegando al CollisionManager."""
        # Proyectiles jugador vs invasores
        if self.wave_manager.formation:
            enemies_list = self.wave_manager.formation.enemies
            points = self.collision_manager.check_player_bullets_vs_enemies(self.bullets, enemies_list)
            if points > 0:
                self.score_manager.add_points(points)

        # Proyectiles enemigos vs jugador
        self.collision_manager.check_enemy_bullets_vs_player(self.bullets, self.player)

        # Proyectiles vs escudos protectores
        self.collision_manager.check_bullets_vs_barriers(self.bullets, self.barriers)

    def _check_game_state(self) -> None:
        """Inspecciona condiciones de fin de partida (derrota/victoria) o avance de nivel."""
        # Condición de Derrota: 0 vidas o invasores llegan abajo
        reached_defense_line = False
        if self.wave_manager.formation:
            reached_defense_line = self.collision_manager.check_enemies_vs_player(
                self.wave_manager.formation.enemies, self.player
            )

        if self.player.lives <= 0 or reached_defense_line:
            self.check_game_over(force=True)
            return

        # Condición de Victoria parcial: todos los enemigos destruidos -> Siguiente oleada
        if self.wave_manager.formation and self.wave_manager.formation.is_empty():
            self.wave_manager.next_wave()
            # Escalar dificultad de disparo enemigo: cooldown menor
            self.enemy_shoot_cooldown = max(0.4, 1.5 - (self.wave_manager.current_wave - 1) * 0.15)
            self.enemy_shoot_timer = 0.0

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Gestiona el input del teclado para mover el jugador, disparar o salir."""
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.move_left()
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.move_right()
        elif key == arcade.key.SPACE:
            if self.player.can_shoot():
                # Llama a shoot() para disparar e iniciar cooldown interno del jugador
                self.player.shoot()
                # Generamos la bala desde el pool en vez de instanciar de cero
                self._spawn_bullet(self.player.center_x, self.player.top, "player", 1)
        elif key == arcade.key.ESCAPE:
            self.window.close()

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Detiene la aceleración del jugador al soltar las teclas direccionales."""
        if key in (arcade.key.LEFT, arcade.key.A) and self.player.change_x < 0:
            self.player.stop_moving()
        elif key in (arcade.key.RIGHT, arcade.key.D) and self.player.change_x > 0:
            self.player.stop_moving()

    def check_game_over(self, force: bool = False) -> None:
        """Guarda la puntuación y cambia la vista activa hacia GameOverView."""
        self.score_manager.save_high_score()
        game_over_view = GameOverView(self.score_manager.score, self.score_manager.high_score)
        self.window.show_view(game_over_view)
