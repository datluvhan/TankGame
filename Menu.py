import pygame
class Menu:
    def __init__(self, screen):
        #Planet
        self.baren = pygame.image.load('assets/Tank/Baren.png')
        self.terran = pygame.image.load('assets/Tank/Terran.png')
        self.ice = pygame.image.load('assets/Tank/Ice.png')
        self.back_hole = pygame.image.load('assets/Tank/Black_hole.png')
        self.lava = pygame.image.load('assets/Tank/Lava.png')

        self.baren = pygame.transform.scale(self.baren, (96, 96))
        self.terran = pygame.transform.scale(self.terran, (96, 96))
        self.ice = pygame.transform.scale(self.ice, (96, 96))
        self.back_hole = pygame.transform.scale(self.back_hole, (96, 96))
        self.lava = pygame.transform.scale(self.lava, (96, 96))

        self.background_sprites = pygame.image.load('assets/Tank/background.png')
        self.background_sprites = pygame.transform.scale(self.background_sprites, (800, 600))
        self.screen = screen

        self.title_font = pygame.font.Font('assets/fonts/arcade.ttf', 64)
        self.option_font = pygame.font.Font('assets/fonts/arcade.ttf', 32)

        #Title
        self.title = self.title_font.render('Space Invaders', True, (255, 255, 255))
        self.options = ['Start', 'Exit']

        self.is_active = True
        self.is_playing = False

        self.planet_positions = [
            (40, 45),
            (100, 500),
            (320, 380),
            (610, 55),
            (690, 430),
        ]


    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, option in enumerate(self.options):
                    text = self.option_font.render(option, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 50))
                    if text_rect.collidepoint(mouse_pos):
                        if option == 'Start':
                            self.is_active = False
                            self.is_playing = True
                        elif option == 'Exit':
                            pygame.quit()
                            exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def draw(self):
        if self.is_active:
            self.screen.blit(self.background_sprites, (0, 0))
            self.screen.blit(self.baren, self.planet_positions[0])
            self.screen.blit(self.terran, self.planet_positions[1])
            self.screen.blit(self.ice, self.planet_positions[2])
            self.screen.blit(self.back_hole, self.planet_positions[3])
            self.screen.blit(self.lava, self.planet_positions[4])


            self.screen.blit(self.title, (self.screen.get_width() // 2 - self.title.get_width() // 2, 100))
            for i, option in enumerate(self.options):
                text = self.option_font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 50))
                self.screen.blit(text, text_rect)