import arcade
import os
from PIL import Image, ImageDraw
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_COOLDOWN,
    HIGH_SCORE_FILE,
    ASSET_PATHS,
)
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.barrier import Barrier
from src.managers.collision_manager import CollisionManager
from src.managers.wave_manager import WaveManager
from src.managers.score_manager import ScoreManager
from src.ui.hud import HUD
from src.ui.game_over_view import GameOverView

def load_sound_safe(path: str) -> arcade.Sound | None:
    """Intenta cargar un sonido de forma segura; retorna None si no existe o falla."""
    if os.path.exists(path):
        try:
            return arcade.Sound(path)
        except Exception:
            pass
    return None

class Explosion(arcade.Sprite):
    """Representa un efecto visual de explosión temporal al destruir un invasor."""

    def __init__(self, x: float, y: float) -> None:
        """Dibuja una pequeña estrella de explosión pixelada usando PIL."""
        img = Image.new("RGBA", (30, 30), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Dibujar estrella amarilla y naranja
        draw.polygon([(15, 0), (12, 12), (0, 15), (12, 18), (15, 30), (18, 18), (30, 15), (18, 12)], fill=(255, 215, 0, 255))
        draw.ellipse([8, 8, 22, 22], fill=(255, 69, 0, 255))
        
        texture = arcade.Texture(img)
        super().__init__(texture)
        self.center_x = x
        self.center_y = y
        self.timer: float = 0.25  # Duración de la explosión en segundos

    def update(self, delta_time: float = 1/60) -> None:
        """Reduce el tiempo de vida y remueve la explosión de la pantalla."""
        self.timer -= delta_time
        if self.timer <= 0:
            self.remove_from_sprite_lists()

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
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.player)
        self.bullets: arcade.SpriteList = arcade.SpriteList()
        self.barriers: arcade.SpriteList = arcade.SpriteList()
        self.explosions: arcade.SpriteList = arcade.SpriteList()

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

        # Carga de Audio y Música
        self.sound_shoot = load_sound_safe(ASSET_PATHS["sounds"]["shoot"])
        self.sound_explosion = load_sound_safe(ASSET_PATHS["sounds"]["explosion"])
        self.sound_gameover = load_sound_safe(ASSET_PATHS["sounds"]["gameover"])
        self.sound_music = load_sound_safe(ASSET_PATHS["sounds"]["music"])
        
        # Iniciar reproducción de la música de fondo en bucle
        self.bg_player = None
        if self.sound_music:
            try:
                self.bg_player = self.sound_music.play(volume=0.2, loop=True)
            except Exception:
                pass

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
            # Reasignar el dueño
            bullet.owner = owner
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
        """Dibuja todos los elementos en pantalla: entidades, grillas, explosiones y HUD."""
        self.clear()

        # Dibujar todos los Sprites activos
        self.player_list.draw()
        self.bullets.draw()
        if self.wave_manager.formation and self.wave_manager.formation.enemies:
            self.wave_manager.formation.enemies.draw()
        self.barriers.draw()
        self.explosions.draw()

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
        """Actualiza las posiciones y comportamientos de las entidades, explosiones y disparadores."""
        # Jugador y proyectiles
        self.player.update(delta_time)
        self.bullets.update(delta_time)
        self.explosions.update(delta_time)

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
                    if self.sound_shoot:
                        try:
                            # Tono más grave para el disparo enemigo
                            self.sound_shoot.play(volume=0.15, speed=0.8)
                        except Exception:
                            pass

    def _handle_collisions(self) -> None:
        """Resuelve los impactos ocurridos en la partida delegando al CollisionManager."""
        # Proyectiles jugador vs invasores
        if self.wave_manager.formation:
            enemies_list = self.wave_manager.formation.enemies
            
            # Detectar colisiones individuales para disparar las explosiones y sonidos
            for bullet in list(self.bullets):
                if bullet.owner == "player":
                    hit_list = arcade.check_for_collision_with_list(bullet, enemies_list)
                    if hit_list:
                        bullet.remove_from_sprite_lists()
                        for enemy in hit_list:
                            if enemy in enemies_list:
                                # Sumar puntaje
                                self.score_manager.add_points(enemy.points_value)
                                
                                # Instanciar animación de explosión
                                explosion = Explosion(enemy.center_x, enemy.center_y)
                                self.explosions.append(explosion)
                                
                                # Eliminar invasor
                                enemy.remove_from_sprite_lists()
                                
                                # Reproducir audio de explosión
                                if self.sound_explosion:
                                    try:
                                        self.sound_explosion.play(volume=0.3, speed=1.2)
                                    except Exception:
                                        pass

        # Proyectiles enemigos vs jugador
        hit = self.collision_manager.check_enemy_bullets_vs_player(self.bullets, self.player)
        if hit:
            # Efecto acústico al perder una vida
            if self.sound_explosion:
                try:
                    self.sound_explosion.play(volume=0.4, speed=0.6)
                except Exception:
                    pass

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
                # Reproducir sonido de disparo
                if self.sound_shoot:
                    try:
                        self.sound_shoot.play(volume=0.25)
                    except Exception:
                        pass
        elif key == arcade.key.ESCAPE:
            self.check_game_over(force=True)

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Detiene la aceleración del jugador al soltar las teclas direccionales."""
        if key in (arcade.key.LEFT, arcade.key.A) and self.player.change_x < 0:
            self.player.stop_moving()
        elif key in (arcade.key.RIGHT, arcade.key.D) and self.player.change_x > 0:
            self.player.stop_moving()

    def check_game_over(self, force: bool = False) -> None:
        """Detiene la música, guarda la puntuación y cambia la vista activa hacia GameOverView."""
        # Detener la música de fondo en loop
        if self.bg_player:
            try:
                self.bg_player.pause()
                self.bg_player.delete()
            except Exception:
                pass

        # Tocar jingle de fin de juego
        if self.sound_gameover:
            try:
                self.sound_gameover.play(volume=0.4)
            except Exception:
                pass

        self.score_manager.save_high_score()
        game_over_view = GameOverView(self.score_manager.score, self.score_manager.high_score)
        self.window.show_view(game_over_view)
