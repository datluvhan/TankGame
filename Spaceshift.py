import pygame


class Spaceshift:
    def __init__(self, img, pos, scale=1.0):
        self.img = img
        self.pos = pos

        self.sheet = pygame.image.load('assets/Tank/tinyShip.png').convert_alpha()
        self.sheet = pygame.transform.scale(
            self.sheet,
            (
                int(self.sheet.get_width() * scale),
                int(self.sheet.get_height() * scale),
            ),
        )

        self.columns = 5
        self.rows = 3
        self.frame_width = self.sheet.get_width() // self.columns
        self.frame_height = self.sheet.get_height() // self.rows

        self.state_rows = {
            'move': 0,
            'attack': 1,
            'idle': 0,
        }
        self.state_speed = {
            'move': 0.1,
            'attack': 0.08,
            'idle': 0.1,
        }

        self.state = 'idle'
        self.base_state = 'idle'
        self.attack_until = 0
        self.current_frame = 0
        self.frame_time = 0.0
        self._last_time = pygame.time.get_ticks()

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy

    def set_state(self, state):
        if state in ('idle', 'move'):
            self.base_state = state
            if self.state != 'attack':
                self.state = state

    def trigger_attack(self, duration=150):
        self.state = 'attack'
        self.attack_until = pygame.time.get_ticks() + duration
        self.current_frame = 0
        self.frame_time = 0.0

    def animation(self):
        current_time = pygame.time.get_ticks()

        if self.state == 'attack' and current_time >= self.attack_until:
            self.state = self.base_state
            self.current_frame = 0
            self.frame_time = 0.0

        dt = (current_time - self._last_time) / 1000.0
        self._last_time = current_time
        dt = min(dt, 0.05)

        self.frame_time += dt
        frame_delay = self.state_speed[self.state]
        while self.frame_time >= frame_delay:
            self.frame_time -= frame_delay
            self.current_frame = (self.current_frame + 1) % self.columns

    def draw(self, screen):
        self.animation()
        frame_x = self.current_frame * self.frame_width
        frame_y = self.state_rows[self.state] * self.frame_height
        screen.blit(self.sheet, self.pos, (frame_x, frame_y, self.frame_width, self.frame_height))