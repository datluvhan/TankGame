import pygame


class GameOver:
    def __init__(self, screen):
        self.screen = screen
        self.game_over_font = pygame.font.Font('assets/fonts/arcade.ttf', 64)
        self.font = pygame.font.Font('assets/fonts/arcade.ttf', 32)

        self.options = ['Play Again', 'Exit']
        self.is_active = False
        self.on_play_again = None
    #Hàm xử lý sự kiện
    def handle_events(self, events, is_playing):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, option in enumerate(self.options):
                    text = self.font.render(option, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 50))
                    if text_rect.collidepoint(mouse_pos):
                        if option == 'Play Again':
                            self.is_active = False
                            if self.on_play_again:
                                self.on_play_again()

                        elif option == 'Exit':
                            pygame.quit()
                            exit()

    def draw(self, score):
        if self.is_active:
            game_over_text = self.game_over_font.render('Game Over', True, (255, 0, 0))
            final_score_text = self.font.render(f'Final Score {score}', True, (255, 255, 255))
            
            self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 100))
            self.screen.blit(final_score_text, (self.screen.get_width() // 2 - final_score_text.get_width() // 2, 150))
            for i, option in enumerate(self.options):
                text = self.font.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 50))
                self.screen.blit(text, text_rect)