import pygame
from Menu import Menu
from GameOver import GameOver
from Spaceshift import Spaceshift
from random import randrange
pygame.init()
w = 800
h = 600
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
#Spaceshift
spaceshift = Spaceshift(None, [w // 2, h // 2])
#Bullet
bullet = pygame.image.load('assets/Tank/bullet.png')
bullet = pygame.transform.scale(bullet, (6, 6))
#road
road = pygame.image.load('assets/Tank/space.png')
road = pygame.transform.scale(road, (w, h))
#Score
score = 0
font = pygame.font.Font('assets/fonts/arcade.ttf', 24)
#sound
shoot_sound = pygame.mixer.Sound('assets/Tank/shoot.mp3')
explosion_sound = pygame.mixer.Sound('assets/Tank/Explosion.wav')
ship_speed = 3

shooting_cooldown = 500
last_shot_time = 0
#Time
time_limit = 60
start_time = pygame.time.get_ticks()  # Store the actual start time once

#Game over

max_score = 0;
#Alien
alien_speed = 1
#Di chuyển xuống dưới
alien_direction = [0, 1]


#Trạng thái trò chơi
is_playing = True
is_game_over = False
def create_bullet():
    bullet_img = pygame.image.load('assets/Tank/bullet.png')
    bullet_img = pygame.transform.scale(bullet_img, (5, 5))
    bullet_pos = [spaceshift.pos[0] + spaceshift.frame_width // 2 - 2.5, spaceshift.pos[1]]
    bullet_direction = [0, -7]  # Di chuyển lên trên
    return {'img': bullet_img, 'pos': bullet_pos, 'dir': bullet_direction}

is_movable = True
#Read file to create movable road on background
def read_road():
    
    with open('assets/Tank/road.txt', 'r') as f:
        road_data = f.read().splitlines()
    return road_data

#Khai báo danh sách đạn
bullet_list = []

#Danh sách alien
alien_list = []

road_data = read_road()
def can_move(x, y, width, height):
    left = x // 40
    right = (x + width - 1) // 40
    top = y // 40
    bottom = (y + height - 1) // 40
    
    # Kiểm tra bounds chặt chẽ trước khi truy cập
    if top < 0 or bottom >= len(road_data):
        return False
    if left < 0:
        return False
    
    # Kiểm tra độ dài từng hàng
    for row_idx in [top, bottom]:
        if right >= len(road_data[row_idx]) or left >= len(road_data[row_idx]):
            return False
    
    if road_data[top][left] == '0' and road_data[top][right] == '0' and road_data[bottom][left] == '0' and road_data[bottom][right] == '0':
        return True
    return False

# Read road data once at start
road_data = read_road()
menu = Menu(screen)
gameover = GameOver(screen)


#Hàm reset Game
def reset_game():
    global score, bullet_list, alien_list, start_time, max_score, is_playing, last_shot_time
    score = 0
    bullet_list = []
    alien_list = []
    start_time = pygame.time.get_ticks()
    max_score = 0
    last_shot_time = 0
    spaceshift.pos[0] = w // 2
    spaceshift.pos[1] = h // 2
    spaceshift.set_state('idle')
    gameover.is_active = False
    menu.is_active = False
    menu.is_playing = True
    is_playing = True


gameover.on_play_again = reset_game

while is_playing:
    clock.tick(60)
    events = pygame.event.get()
    menu.handle_events(events)
    menu.draw()

    # Calculate remaining time
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_limit = 60 - elapsed_time
    if menu.is_playing and not is_game_over:
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_playing = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gameover.is_active:
                #Lấy thời gian hiện tại
                
                current_time = pygame.time.get_ticks()
                if current_time - last_shot_time >= shooting_cooldown:
                    new_bullet = create_bullet()
                    shoot_sound.play()
                    bullet_list.append(new_bullet)
                    spaceshift.trigger_attack()
                    #Cập nhật thời gian cuối cùng bắn
                    last_shot_time = current_time

        screen.blit(road, (0, 0))
        # Only process game logic if not game over
        if not gameover.is_active:
            # Xử lý di chuyển
            new_pos_x = spaceshift.pos[0]
            new_pos_y = spaceshift.pos[1]
            key = pygame.key.get_pressed()
            is_moving = False
            if key[pygame.K_a] and is_movable:
                new_pos_x -= ship_speed
                is_moving = True
            if key[pygame.K_d] and is_movable:
                new_pos_x += ship_speed
                is_moving = True
            if key[pygame.K_w] and is_movable:
                new_pos_y -= ship_speed
                is_moving = True
            if key[pygame.K_s] and is_movable:
                new_pos_y += ship_speed
                is_moving = True

            if can_move(new_pos_x, new_pos_y, spaceshift.frame_width, spaceshift.frame_height):
                spaceshift.pos[0] = new_pos_x
                spaceshift.pos[1] = new_pos_y
                spaceshift.set_state('move' if is_moving else 'idle')
            else:
                spaceshift.set_state('move' if is_moving else 'idle')

        #Draw Spaceshift
        spaceshift.draw(screen)
        if not gameover.is_active:
            # Bullet processing
            bullets_to_remove = []
            for bullet_data in bullet_list:
                bullet_data['pos'][0] += bullet_data['dir'][0]
                bullet_data['pos'][1] += bullet_data['dir'][1]
                
                # Xóa đạn nếu ra khỏi màn hình
                if bullet_data['pos'][1] < 0 or bullet_data['pos'][1] > h:
                    bullets_to_remove.append(bullet_data)
            
            for bullet_data in bullets_to_remove:
                bullet_list.remove(bullet_data)

            # Tạo alien mới với tốc độ hợp lý (không phải mỗi frame)
            if randrange(0, 60) == 0:  # Tạo alien ngẫu nhiên (khoảng 1 lần/giây)
                alien = pygame.image.load('assets/Tank/Alien1.png')
                alien = pygame.transform.scale(alien, (50, 50))
                alien_pos = [randrange(60, w - 82, alien.get_width()), -1]  # Vị trí ngẫu nhiên ở trên cùng
                alien_list.append({'img': alien, 'pos': alien_pos, 'dir': [0, 1]})
            
            # Kiểm tra va chạm giữa đạn và alien
            aliens_to_remove = []
            bullets_to_remove = []
            for alien_data in alien_list:
                for bullet_data in bullet_list:
                    alien_rect = alien_data['img'].get_rect(topleft=alien_data['pos'])
                    bullet_rect = bullet_data['img'].get_rect(topleft=bullet_data['pos'])
                    
                    if alien_rect.colliderect(bullet_rect):
                        explosion_sound.play()
                        if alien_data not in aliens_to_remove:
                            aliens_to_remove.append(alien_data)
                        if bullet_data not in bullets_to_remove:
                            bullets_to_remove.append(bullet_data)
                        score += 1
                        break
            
            for alien_data in aliens_to_remove:
                if alien_data in alien_list:
                    alien_list.remove(alien_data)
            for bullet_data in bullets_to_remove:
                if bullet_data in bullet_list:
                    bullet_list.remove(bullet_data)
            
            max_score = max(score, max_score)

            # Vẽ tất cả đạn
            for bullet_data in bullet_list:
                screen.blit(bullet_data['img'], bullet_data['pos'])

            # Di chuyển và vẽ aliens
            aliens_to_remove = []
            for alien_data in alien_list:
                alien_data['pos'][0] += alien_direction[0] * alien_speed
                alien_data['pos'][1] += alien_direction[1] * alien_speed

                if alien_data['pos'][1] > h:
                    aliens_to_remove.append(alien_data)
                else:
                    screen.blit(alien_data['img'], alien_data['pos'])
            
            for alien_data in aliens_to_remove:
                alien_list.remove(alien_data)

            if time_limit <= 0:
                gameover.is_active = True
        
        # Draw game elements
        score_text = font.render(f'Score {score}', True, (255, 255, 255))
        time_text = font.render(f'Time {max(0, time_limit)}s', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 40))
    
    # Show game over screen
    if gameover.is_active:
        gameover.draw(max_score)
        gameover.handle_events(events, is_playing)


    pygame.display.flip()

pygame.quit()
