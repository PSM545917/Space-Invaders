import arcade

class CollisionManager:
    """Centraliza toda la detección de colisiones físicas usando AABB del motor Arcade."""

    def check_player_bullets_vs_enemies(self, bullets: arcade.SpriteList, enemies: arcade.SpriteList) -> int:
        """Comprueba colisiones entre balas del jugador e invasores. Elimina ambos y retorna puntos ganados."""
        total_points = 0
        for bullet in list(bullets):
            hit_enemies = arcade.check_for_collision_with_list(bullet, enemies)
            if hit_enemies:
                bullet.remove_from_sprite_lists()
                for enemy in hit_enemies:
                    # Prevenir doble puntuación si el enemigo ya fue eliminado por otra bala en este frame
                    if enemy in enemies:
                        total_points += getattr(enemy, "points_value", 10)
                        enemy.remove_from_sprite_lists()
        return total_points

    def check_enemy_bullets_vs_player(self, bullets: arcade.SpriteList, player: arcade.Sprite) -> bool:
        """Comprueba si el jugador fue impactado por proyectiles enemigos. Resta una vida y retorna True."""
        hit_bullets = arcade.check_for_collision_with_list(player, bullets)
        if hit_bullets:
            for bullet in hit_bullets:
                bullet.remove_from_sprite_lists()
            player.lives -= 1
            return True
        return False

    def check_enemies_vs_player(self, enemies: arcade.SpriteList, player: arcade.Sprite) -> bool:
        """Comprueba si la formación enemiga descendió hasta la línea de defensa del jugador."""
        for enemy in enemies:
            if enemy.bottom <= player.top:
                return True
        return False

    def check_bullets_vs_barriers(self, bullets: arcade.SpriteList, barriers: arcade.SpriteList) -> None:
        """Comprueba colisiones entre cualquier bala y los escudos, restando vida a la barrera."""
        for bullet in list(bullets):
            hit_barriers = arcade.check_for_collision_with_list(bullet, barriers)
            if hit_barriers:
                bullet.remove_from_sprite_lists()
                for barrier in hit_barriers:
                    if barrier in barriers:
                        # Cada impacto resta 1 HP
                        barrier.take_damage(1)
                
