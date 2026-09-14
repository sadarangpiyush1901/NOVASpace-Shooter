import pygame
import random
import math

pygame.init()

WIDTH = 550
HEIGHT = 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Strike - Total War")
CLOCK = pygame.time.Clock()
FPS = 60

# Colors
DARK_BG = (10, 14, 26)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 210, 255)
ENGINE_ORANGE = (255, 110, 20)
BULLET_YELLOW = (255, 235, 60)
HEALTH_GREEN = (40, 235, 120)
HEALTH_BAR_BG = (50, 50, 60)
DAMAGE_RED = (255, 55, 75)
ASTEROID_GREY = (115, 125, 135)
ASTEROID_DARK = (70, 78, 86)

# Enemy Planes Color Palette
T1_COLOR = (255, 175, 40)     # Rogue Interceptor
T2_COLOR = (0, 240, 200)     # Stealth Strike Fighter
T3_COLOR = (185, 75, 255)    # Heavy Twin-Wing Bomber
T4_COLOR = (255, 45, 80)     # Dreadnought Flagship

FONT_HUD = pygame.font.SysFont("consolas", 18, bold=True)
FONT_BIG = pygame.font.SysFont("consolas", 40, bold=True)
FONT_POPUP = pygame.font.SysFont("consolas", 13, bold=True)

stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(85)]

class FighterJet:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 7
        self.width = 48
        self.height = 54
        self.cooldown = 0
        self.cooldown_max = 8

    def move(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x - self.width // 2 > 4:
            self.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x + self.width // 2 < WIDTH - 4:
            self.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y - self.height // 2 > 10:
            self.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y + self.height // 2 < HEIGHT - 15:
            self.y += self.speed

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)

        thrust = random.randint(10, 18)
        pygame.draw.polygon(surface, ENGINE_ORANGE, [(cx - 12, cy + 20), (cx - 6, cy + 20), (cx - 9, cy + 20 + thrust)])
        pygame.draw.polygon(surface, ENGINE_ORANGE, [(cx + 6, cy + 20), (cx + 12, cy + 20), (cx + 9, cy + 20 + thrust)])

        main_wings = [
            (cx, cy - 24), (cx - 24, cy + 12), (cx - 20, cy + 20),
            (cx - 8, cy + 18), (cx, cy + 22), (cx + 8, cy + 18),
            (cx + 20, cy + 20), (cx + 24, cy + 12)
        ]
        pygame.draw.polygon(surface, (15, 80, 150), main_wings)
        pygame.draw.polygon(surface, NEON_BLUE, main_wings, 2)

        body = [(cx, cy - 28), (cx - 8, cy + 16), (cx, cy + 21), (cx + 8, cy + 16)]
        pygame.draw.polygon(surface, WHITE, body)

        pygame.draw.rect(surface, (200, 200, 220), (cx - 21, cy - 2, 4, 14))
        pygame.draw.rect(surface, (200, 200, 220), (cx + 17, cy - 2, 4, 14))

        cockpit = [(cx, cy - 15), (cx - 4, cy), (cx, cy + 6), (cx + 4, cy)]
        pygame.draw.polygon(surface, (0, 235, 255), cockpit)

class LaserBolt:
    def __init__(self, x, y, dx=0, dy=-15, color=BULLET_YELLOW, damage=1, length=14):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.damage = damage
        self.length = length

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        pygame.draw.line(surface, self.color, (int(self.x), int(self.y)), (int(self.x - self.dx), int(self.y + self.length)), 4)
        pygame.draw.line(surface, WHITE, (int(self.x), int(self.y)), (int(self.x - self.dx), int(self.y + self.length // 2)), 2)

class EnemyPlane:
    def __init__(self, tier):
        self.tier = tier
        self.x = random.randint(40, WIDTH - 40)
        self.y = -50
        self.anim = random.uniform(0, 10)

        if tier == 1:
            self.hp = 1
            self.max_hp = 1
            self.speed = random.uniform(3.5, 4.5)
            self.radius = 18
            self.color = T1_COLOR
        elif tier == 2:
            self.hp = 2
            self.max_hp = 2
            self.speed = random.uniform(3.8, 4.8)
            self.radius = 22
            self.color = T2_COLOR
        elif tier == 3:
            self.hp = 4
            self.max_hp = 4
            self.speed = random.uniform(2.3, 3.0)
            self.radius = 28
            self.color = T3_COLOR
        else:  # Tier 4
            self.hp = 8
            self.max_hp = 8
            self.speed = random.uniform(1.8, 2.5)
            self.radius = 36
            self.color = T4_COLOR

    def update(self):
        self.y += self.speed
        self.anim += 0.08
        if self.tier == 2:
            self.x += math.sin(self.anim * 1.5) * 3.4
        elif self.tier >= 3:
            self.x += math.sin(self.anim) * 1.8
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius

        # Downward enemy jet thrusters
        pygame.draw.polygon(surface, (255, 100, 50), [(cx - 6, cy - r), (cx + 6, cy - r), (cx, cy - r - random.randint(6, 12))])

        if self.tier == 1:
            # Dart Wing Fighter
            wings = [(cx, cy + r), (cx - r, cy - r // 2), (cx - r // 3, cy - r // 2), (cx, cy - r), (cx + r // 3, cy - r // 2), (cx + r, cy - r // 2)]
            pygame.draw.polygon(surface, self.color, wings)
            pygame.draw.polygon(surface, WHITE, wings, 1)
            pygame.draw.rect(surface, DAMAGE_RED, (cx - 2, cy + 2, 4, 8))

        elif self.tier == 2:
            # Swept Forward Attack Jet
            wings = [
                (cx, cy + r), (cx - r, cy + r // 3), (cx - r * 1.1, cy - r // 2),
                (cx - r // 3, cy - r * 0.8), (cx, cy - r // 2),
                (cx + r // 3, cy - r * 0.8), (cx + r * 1.1, cy - r // 2), (cx + r, cy + r // 3)
            ]
            pygame.draw.polygon(surface, self.color, wings)
            pygame.draw.polygon(surface, WHITE, wings, 1)
            pygame.draw.polygon(surface, DAMAGE_RED, [(cx, cy - 2), (cx - 4, cy + 8), (cx + 4, cy + 8)])

        elif self.tier == 3:
            # Heavy Bomber Plane
            wings = [
                (cx, cy + r), (cx - r * 1.2, cy), (cx - r, cy - r // 2),
                (cx - r // 2, cy - r), (cx + r // 2, cy - r),
                (cx + r, cy - r // 2), (cx + r * 1.2, cy)
            ]
            pygame.draw.polygon(surface, self.color, wings)
            pygame.draw.polygon(surface, WHITE, wings, 2)
            pygame.draw.rect(surface, BULLET_YELLOW, (cx - 8, cy - 2, 16, 6))

        else:
            # Dreadnought Flagship
            wings = [
                (cx, cy + r * 1.1), (cx - r * 1.1, cy + r // 3), (cx - r * 0.9, cy - r // 2),
                (cx - r // 2, cy - r), (cx + r // 2, cy - r),
                (cx + r * 0.9, cy - r // 2), (cx + r * 1.1, cy + r // 3)
            ]
            pygame.draw.polygon(surface, self.color, wings)
            pygame.draw.polygon(surface, (255, 215, 0), wings, 2)
            pygame.draw.circle(surface, DAMAGE_RED, (cx - 12, cy - 2), 4)
            pygame.draw.circle(surface, DAMAGE_RED, (cx + 12, cy - 2), 4)
            pygame.draw.polygon(surface, WHITE, [(cx, cy - 6), (cx - 5, cy + 8), (cx + 5, cy + 8)])

        # HP Bar
        if self.max_hp > 1:
            bar_w = int(r * 1.6)
            hp_w = int((self.hp / self.max_hp) * bar_w)
            pygame.draw.rect(surface, HEALTH_BAR_BG, (cx - bar_w // 2, cy - r - 12, bar_w, 4))
            pygame.draw.rect(surface, HEALTH_GREEN, (cx - bar_w // 2, cy - r - 12, hp_w, 4))

class Asteroid:
    def __init__(self):
        self.radius = random.randint(22, 36)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = -50
        self.speed = random.uniform(2.0, 3.2)
        self.hp = 5
        self.angle = 0
        self.rot_speed = random.uniform(-2, 2)
        # Random jagged polygon shape
        self.num_points = 8
        self.offsets = [random.uniform(0.75, 1.25) for _ in range(self.num_points)]

    def update(self):
        self.y += self.speed
        self.angle += self.rot_speed

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        points = []
        for i in range(self.num_points):
            theta = math.radians(self.angle + i * (360 / self.num_points))
            dist = self.radius * self.offsets[i]
            px = cx + dist * math.cos(theta)
            py = cy + dist * math.sin(theta)
            points.append((px, py))
        pygame.draw.polygon(surface, ASTEROID_GREY, points)
        pygame.draw.polygon(surface, ASTEROID_DARK, points, 3)

class HealthDrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2.2
        self.radius = 15
        self.pulse = 0

    def update(self):
        self.y += self.speed
        self.pulse += 0.1

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        glow_r = int(self.radius + math.sin(self.pulse) * 3)
        pygame.draw.circle(surface, (20, 60, 30), (cx, cy), glow_r)
        pygame.draw.circle(surface, HEALTH_GREEN, (cx, cy), self.radius, 2)
        # Red Cross / Medical Cross
        pygame.draw.rect(surface, HEALTH_GREEN, (cx - 8, cy - 3, 16, 6))
        pygame.draw.rect(surface, HEALTH_GREEN, (cx - 3, cy - 8, 6, 16))

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(1.5, 6.0)
        self.dx = math.cos(ang) * spd
        self.dy = math.sin(ang) * spd
        self.life = random.randint(12, 22)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), max(1, self.life // 5))

class Popup:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 24

    def update(self):
        self.y -= 1.0
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            surf = FONT_POPUP.render(self.text, True, self.color)
            surface.blit(surf, (int(self.x) - surf.get_width() // 2, int(self.y)))

def fire_system(jet, score, bullets):
    cx, cy = jet.x, jet.y

    if score < 500:
        bullets.append(LaserBolt(cx, cy - 26, dx=0, dy=-15, color=BULLET_YELLOW, damage=1, length=12))
    elif score < 1000:
        bullets.append(LaserBolt(cx - 19, cy - 2, dx=0, dy=-16, color=NEON_BLUE, damage=1, length=14))
        bullets.append(LaserBolt(cx + 19, cy - 2, dx=0, dy=-16, color=NEON_BLUE, damage=1, length=14))
    elif score < 1500:
        bullets.append(LaserBolt(cx, cy - 28, dx=0, dy=-16, color=HEALTH_GREEN, damage=2, length=16))
        bullets.append(LaserBolt(cx - 19, cy - 2, dx=-2.4, dy=-15, color=HEALTH_GREEN, damage=1, length=14))
        bullets.append(LaserBolt(cx + 19, cy - 2, dx=2.4, dy=-15, color=HEALTH_GREEN, damage=1, length=14))
    else:
        bullets.append(LaserBolt(cx - 6, cy - 28, dx=0, dy=-17, color=(255, 60, 220), damage=2, length=16))
        bullets.append(LaserBolt(cx + 6, cy - 28, dx=0, dy=-17, color=(255, 60, 220), damage=2, length=16))
        bullets.append(LaserBolt(cx - 20, cy - 2, dx=-3.2, dy=-15, color=BULLET_YELLOW, damage=2, length=14))
        bullets.append(LaserBolt(cx + 20, cy - 2, dx=3.2, dy=-15, color=BULLET_YELLOW, damage=2, length=14))

def main():
    jet = FighterJet()
    bullets = []
    enemies = []
    asteroids = []
    health_drops = []
    particles = []
    popups = []

    score = 0
    shields = 3
    spawn_enemy_timer = 0
    spawn_asteroid_timer = 0
    time_score_counter = 0
    game_over = False

    running = True
    while running:
        CLOCK.tick(FPS)
        WIN.fill(DARK_BG)

        # Starfield
        for s in stars:
            s[1] += s[2]
            if s[1] > HEIGHT:
                s[1] = 0
                s[0] = random.randint(0, WIDTH)
            pygame.draw.circle(WIN, (180, 190, 220), (s[0], s[1]), s[2] // 2 + 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    return main()

        keys = pygame.key.get_pressed()

        if not game_over:
            # Time survival bonus
            time_score_counter += 1
            if time_score_counter >= 10:
                score += 1
                time_score_counter = 0

            jet.move(keys)

            # Auto-fire on Spacebar hold
            if jet.cooldown > 0:
                jet.cooldown -= 1
            if keys[pygame.K_SPACE] and jet.cooldown == 0:
                fire_system(jet, score, bullets)
                jet.cooldown = jet.cooldown_max

            # Tier & Spawn Scaling (Dense Swarms)
            if score < 500:
                curr_tier = 1
                spawn_interval = 22
            elif score < 1000:
                curr_tier = 2
                spawn_interval = 17
            elif score < 1500:
                curr_tier = 3
                spawn_interval = 13
            else:
                curr_tier = 4
                spawn_interval = 10

            # Spawn Enemies
            spawn_enemy_timer += 1
            if spawn_enemy_timer >= spawn_interval:
                enemies.append(EnemyPlane(random.randint(1, curr_tier)))
                spawn_enemy_timer = 0

            # Spawn Asteroid Obstacles
            spawn_asteroid_timer += 1
            if spawn_asteroid_timer >= 95:
                asteroids.append(Asteroid())
                spawn_asteroid_timer = 0

            # Update Bullets
            for b in bullets[:]:
                b.update()
                if b.y < -25 or b.x < -20 or b.x > WIDTH + 20:
                    bullets.remove(b)

            # Update Health Drops
            for h in health_drops[:]:
                h.update()
                dist_h = math.hypot(jet.x - h.x, jet.y - h.y)
                if dist_h < h.radius + 20:
                    shields = min(5, shields + 1)
                    popups.append(Popup(h.x, h.y, "+1 HULL RESTORED!", HEALTH_GREEN))
                    for _ in range(12):
                        particles.append(Particle(h.x, h.y, HEALTH_GREEN))
                    health_drops.remove(h)
                elif h.y > HEIGHT + 20:
                    health_drops.remove(h)

            # Update Asteroids
            for a in asteroids[:]:
                a.update()
                # Bullet vs Asteroid
                for b in bullets[:]:
                    if math.hypot(b.x - a.x, b.y - a.y) < a.radius + 4:
                        a.hp -= b.damage
                        for _ in range(3):
                            particles.append(Particle(b.x, b.y, ASTEROID_GREY))
                        if b in bullets:
                            bullets.remove(b)
                        if a.hp <= 0:
                            score += 40
                            popups.append(Popup(a.x, a.y, "+40 DEBRIS CLEARED", WHITE))
                            for _ in range(16):
                                particles.append(Particle(a.x, a.y, ASTEROID_GREY))
                            asteroids.remove(a)
                            break
                # Jet vs Asteroid
                if a in asteroids and math.hypot(jet.x - a.x, jet.y - a.y) < a.radius + 18:
                    shields -= 1
                    for _ in range(18):
                        particles.append(Particle(jet.x, jet.y, DAMAGE_RED))
                    asteroids.remove(a)
                    if shields <= 0:
                        game_over = True
                elif a in asteroids and a.y - a.radius > HEIGHT + 30:
                    asteroids.remove(a)

            # Update Enemies & Combat
            for e in enemies[:]:
                e.update()

                # Bullet vs Enemy
                for b in bullets[:]:
                    if math.hypot(b.x - e.x, b.y - e.y) < e.radius + 6:
                        e.hp -= b.damage
                        popups.append(Popup(b.x, b.y, f"-{b.damage}", BULLET_YELLOW))
                        for _ in range(3):
                            particles.append(Particle(b.x, b.y, WHITE))
                        if b in bullets:
                            bullets.remove(b)

                        if e.hp <= 0:
                            kill_pts = e.max_hp * 40
                            score += kill_pts
                            popups.append(Popup(e.x, e.y, f"+{kill_pts}", HEALTH_GREEN))
                            for _ in range(15):
                                particles.append(Particle(e.x, e.y, e.color))

                            # 10% chance to drop Health Kit
                            if random.random() < 0.10:
                                health_drops.append(HealthDrop(e.x, e.y))

                            if e in enemies:
                                enemies.remove(e)
                            break

                # Jet vs Enemy Plane
                if e in enemies and math.hypot(jet.x - e.x, jet.y - e.y) < e.radius + 18:
                    shields -= 1
                    for _ in range(20):
                        particles.append(Particle(jet.x, jet.y, DAMAGE_RED))
                    enemies.remove(e)
                    if shields <= 0:
                        game_over = True
                elif e in enemies and e.y - e.radius > HEIGHT + 20:
                    enemies.remove(e)

        # Particles & Popups
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)
        for pop in popups[:]:
            pop.update()
            if pop.life <= 0:
                popups.remove(pop)

        # Draw Entities
        for p in particles:
            p.draw(WIN)
        for a in asteroids:
            a.draw(WIN)
        for h in health_drops:
            h.draw(WIN)
        for b in bullets:
            b.draw(WIN)
        for e in enemies:
            e.draw(WIN)
        for pop in popups:
            pop.draw(WIN)

        if not game_over:
            jet.draw(WIN)

        # HUD
        tier_now = 1 if score < 500 else (2 if score < 1000 else (3 if score < 1500 else 4))
        score_lbl = FONT_HUD.render(f"SCORE: {score}", True, WHITE)
        wpn_lbl = FONT_HUD.render(f"WEAPON LVL: {tier_now}", True, BULLET_YELLOW)
        shield_lbl = FONT_HUD.render(f"LIVES: {shields}/5", True, HEALTH_GREEN if shields > 1 else DAMAGE_RED)

        WIN.blit(score_lbl, (15, 14))
        WIN.blit(wpn_lbl, (15, 38))
        WIN.blit(shield_lbl, (WIDTH - 150, 14))

        # Game Over Screen
        if game_over:
            over_lbl = FONT_BIG.render("WARSHIP DESTROYED", True, DAMAGE_RED)
            final_lbl = FONT_HUD.render(f"Final Score: {score}", True, WHITE)
            retry_lbl = FONT_HUD.render("Press 'R' to Deploy New Jet", True, NEON_BLUE)

            WIN.blit(over_lbl, (WIDTH // 2 - over_lbl.get_width() // 2, HEIGHT // 2 - 50))
            WIN.blit(final_lbl, (WIDTH // 2 - final_lbl.get_width() // 2, HEIGHT // 2 + 5))
            WIN.blit(retry_lbl, (WIDTH // 2 - retry_lbl.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()