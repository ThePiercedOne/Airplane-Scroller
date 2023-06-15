import pygame   # Importiert das Modul pygame

pygame.init()   # Startet pygame

start_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
dt = 0

player_pos = (0, 0)

lifePoints = 100
running = True
whats_running = 'Start'
test = True

screen_width = 1280
screen_height = 720

font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((screen_width, screen_height))

start_bg_image = pygame.image.load("png/Background/Start.png") 
victory_bg_image = pygame.image.load("png/Background/Victory.png")
gameover_bg_image = pygame.image.load("png/Background/Game Over.png")
lvl1_bg_image = pygame.image.load("png/Background/Lvl1.png")
lvl1run_bg_image = pygame.image.load("png/Background/Lvl1Run.png")

enemy_spawn_timer = 0
enemy_spawn_intervall = 1
last_enemy2_score = 0
last_enemy3_score = 0

player_shots = []


seen_start = False
seen_lvl1 = False
seen_sieg = False
seen_gameover = False

background_y = 0
score = 0

player_plane = 'Plane-1-'

class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('png/Plane1Sheets/shot.png')
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = 500  # Geschwindigkeit des Schusses
        

    def update(self, dt):
        self.rect.y -= self.speed * dt  # Bewege den Schuss nach oben basierend auf der Zeit

class Player:
    global player_sheet, test
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 120
        self.move_speed = 10
        self.current_frame = 0
        self.animations = {
            'FD0F0': self.load_spritesheet(player_plane + 'F-Damage-0-Fire-0-Sheet.png', self.width, self.height, animation_speed=100),
            'FD0F1': self.load_spritesheet(player_plane + 'F-Damage-0-Fire-1-Sheet.png', self.width, self.height, animation_speed=100),
            'FD1F0': self.load_spritesheet(player_plane + 'F-Damage-1-Fire-0-Sheet.png', self.width, self.height, animation_speed=100),
            'FD1F1': self.load_spritesheet(player_plane + 'F-Damage-1-Fire-1-Sheet.png', self.width, self.height, animation_speed=100),
            'FD2F0': self.load_spritesheet(player_plane + 'F-Damage-2-Fire-0-Sheet.png', self.width, self.height, animation_speed=100),
            'FD2F1': self.load_spritesheet(player_plane + 'F-Damage-2-Fire-1-Sheet.png', self.width, self.height, animation_speed=100),
            'FD3F0': self.load_spritesheet(player_plane + 'F-Damage-3-Fire-0-Sheet.png', self.width, self.height, animation_speed=100),
            'FD3F1': self.load_spritesheet(player_plane + 'F-Damage-3-Fire-1-Sheet.png', self.width, self.height, animation_speed=100),
            'LD0F0': self.load_spritesheet(player_plane + 'L-Damage-0-Fire-0-Sheet.png', self.width, self.height, animation_speed=100),
            'LD0F1': self.load_spritesheet(player_plane + 'L-Damage-0-Fire-1-Sheet.png', self.width, self.height, animation_speed=100),
            'RD0F0': self.load_spritesheet(player_plane + 'R-Damage-0-Fire-0-Sheet.png', self.width, self.height, animation_speed=100),
            'RD0F1': self.load_spritesheet(player_plane + 'R-Damage-0-Fire-1-Sheet.png', self.width, self.height, animation_speed=100),
        }
        self.current_animation = 'FD0F0'
        self.keys = {
            pygame.K_LEFT: 'left',
            pygame.K_RIGHT: 'right',
            pygame.K_UP: 'up',
            pygame.K_DOWN: 'down',
            pygame.K_SPACE: 'fire',
            pygame.K_w: 'up',
            pygame.K_a: 'left',
            pygame.K_s: 'down',
            pygame.K_d: 'right',
        }
        self.frame_counter = 0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def load_spritesheet(self, filename, frame_width, frame_height, animation_speed):
        sheet = pygame.image.load(filename).convert_alpha()
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))
                frames.append(frame)
        return frames, animation_speed

    def handle_input(self):
        keys_pressed = pygame.key.get_pressed()
        fire = False

        if not any(keys_pressed[key] for key in self.keys):


            fire = False
            if lifePoints > 75:
                self.change_animation('FD0F0')
            if lifePoints > 50 and lifePoints < 76:
                self.change_animation('FD1F0')
            if lifePoints > 25 and lifePoints < 51:
                self.change_animation('FD2F0')
            if lifePoints > 0 and lifePoints < 26:
                self.change_animation('FD3F0')
            if lifePoints == 0:
                pass

        for key, direction in self.keys.items():
            
            if keys_pressed[key]:
                
                if direction == 'fire':
                    fire = True
                    sounds('PlayerShot')
                    new_shot = PlayerShot(player_pos + pygame.Vector2(40, 10))
                    player_shots.append(new_shot)
                    new_shot = PlayerShot(player_pos + pygame.Vector2(80, 10))
                    player_shots.append(new_shot)
                    
                    if lifePoints > 75:
                        self.change_animation('FD0F1')
                    if lifePoints > 50 and lifePoints < 76:
                        self.change_animation('FD1F1')
                    if lifePoints > 25 and lifePoints < 51:
                        self.change_animation('FD2F1')
                    if lifePoints > 0 and lifePoints < 26:
                        self.change_animation('FD3F1')
                
                if direction == 'left':
                    if lifePoints > 75:
                        if fire == False:
                            self.change_animation('LD0F0')
                        if fire == True:
                            self.change_animation('LD0F1')
                    if lifePoints > 50 and lifePoints < 76:
                        if fire == False:
                            self.change_animation('LD1F0')
                        if fire == True:
                            self.change_animation('LD1F1')
                    if lifePoints > 25 and lifePoints < 51:
                        if fire == False:
                            self.change_animation('LD2F0')
                        if fire == True:
                            self.change_animation('LD2F1')
                    if lifePoints > 0 and lifePoints < 26:
                        if fire == False:
                            self.change_animation('LD3F0')
                        if fire == True:
                            self.change_animation('LD3F1')
                    
                if direction == 'right':
                    if lifePoints > 75:
                        if fire == False:
                            self.change_animation('RD0F0')
                        if fire == True:
                            self.change_animation('RD0F1')
                    if lifePoints > 50 and lifePoints < 76:
                        if fire == False:
                            self.change_animation('RD1F0')
                        if fire == True:
                            self.change_animation('RD1F1')
                    if lifePoints > 25 and lifePoints < 51:
                        if fire == False:
                            self.change_animation('RD2F0')
                        if fire == True:
                            self.change_animation('RD2F1')
                    if lifePoints > 0 and lifePoints < 26:
                        if fire == False:
                            self.change_animation('RD3F0')
                        if fire == True:
                            self.change_animation('RD3F1')
            else:
                self.move(direction)
        

    def change_animation(self, animation_name):
        if animation_name in self.animations:
            if self.current_animation != animation_name:
                self.current_animation = animation_name
                self.animation_frames = self.animations[animation_name]
                self.current_frame = 0

    def move(self, direction):
        if direction == 'left':
            if self.x + self.move_speed + self.width <= screen_width:  # Check if moving right exceeds window width
                self.x += self.move_speed
        elif direction == 'right':
            if self.x - self.move_speed >= 0:  # Check if moving left exceeds window boundaries
                self.x -= self.move_speed
        elif direction == 'up':
            if self.y + self.move_speed + self.height <= screen_height:  # Check if moving down exceeds window height
                self.y += self.move_speed
        elif direction == 'down':
            if self.y - self.move_speed >= 0:  # Check if moving up exceeds window boundaries
                self.y -= self.move_speed
        self.rect.topleft = (self.x, self.y)

        global player_pos
        player_pos = (self.x, self.y)

    def draw(self, window):
        frames, animation_speed = self.animations[self.current_animation]
        window.blit(frames[self.current_frame], (self.x, self.y))
        self.frame_counter += 10
        if self.frame_counter >= animation_speed:
            self.frame_counter = 0
        self.current_frame = (self.current_frame + 1) % len(frames)

    def check_collision(self, other_rect):
        if self.rect.colliderect(other_rect):
            return True
        else:
            return False    

def buttons():  # Definiert die Buttons

    global button_rect1, button_rect2, button_rect3, button_rect4, text1_rect,text2_rect,text3_rect, text4_rect, text1, text2, text3, text4

    button_rect1 = pygame.Rect(540, 450, 200, 50)  # Startfenster
    text1 = font.render('Lets Go', True, (255, 255, 255))
    text1_rect = text1.get_rect(center=button_rect1.center)

    button_rect2 = pygame.Rect(540, 550, 200, 50)  # Startfenster
    text2 = font.render('Test: AUS', True, (255, 255, 255))
    text2_rect = text2.get_rect(center=button_rect2.center)

    button_rect3 = pygame.Rect(540, 550, 200, 50)  # Startfenster
    text3 = font.render('Test: AN', True, (255, 255, 255))
    text3_rect = text3.get_rect(center=button_rect3.center)

    button_rect4 = pygame.Rect(540, 450, 200, 50)  # Lvlfenster
    text4 = font.render('Lets Go', True, (255, 255, 255))
    text4_rect = text4.get_rect(center=button_rect4.center)

def sounds(sound):
    if sound == 'PlayerShot':
        sound_data = [128] * 100 + [0] * 50 + [128] * 100
        sound_bytes = bytes(sound_data)
        shot_sound = pygame.mixer.Sound(buffer=sound_bytes)
        shot_sound.play()

# Hier beginnt das Spiel

buttons()

player = Player(screen_width // 2, screen_height // 2)

while running:
    
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
         
        if event.type == pygame.QUIT:

             running = False

        elif event.type == pygame.MOUSEBUTTONUP:

            if whats_running == 'Start':

                if button_rect1.collidepoint(event.pos):

                    whats_running = 'Lvl1'

            elif whats_running == 'Lvl1':

                if button_rect4.collidepoint(event.pos):

                    whats_running = 'Lvl1Run'

            if button_rect2.collidepoint(event.pos):

                if not test:

                    test = True
                    print('Test: ' + str(test))

                elif test:

                    test = False
                    print('Test: '+ str(test))


    if  whats_running == 'Start':

        if not seen_start:

            screen.blit(start_bg_image, (0, 0))
            seen_start = True

        pygame.draw.rect(screen, (255, 0, 0), button_rect1)
        screen.blit(text1, text1_rect)
        
        if not test:
        
            pygame.draw.rect(screen, (255, 0, 0), button_rect2)
            screen.blit(text2, text2_rect)

        if test:

            pygame.draw.rect(screen, (0, 255, 0), button_rect3)
            screen.blit(text3, text3_rect)



            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_1]:

                whats_running = 'Start'
                seen_start = False

            elif keys[pygame.K_2]:

                whats_running = 'Victory'
                seen_victory = False

            elif keys[pygame.K_3]:

                whats_running = 'Game Over'
                seen_gameover = False

            elif keys[pygame.K_4]:

                whats_running = 'Lvl1'
                seen_lvl1 = False

            elif keys[pygame.K_5]:

                whats_running = 'Lvl1Run'

    if  whats_running == 'Victory':

        if not seen_victory:

            screen.blit(victory_bg_image, (0, 0))
            seen_victory = True

        if test:

            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_1]:

                whats_running = 'Start'
                seen_start = False

            elif keys[pygame.K_2]:

                whats_running = 'Victory'
                seen_victory = False

            elif keys[pygame.K_3]:

                whats_running = 'Game Over'
                seen_gameover = False

            elif keys[pygame.K_4]:

                whats_running = 'Lvl1'
                seen_lvl1 = False

            elif keys[pygame.K_5]:

                whats_running = 'Lvl1Run'


    if  whats_running == 'Game Over':
        if not seen_gameover:

            screen.blit(gameover_bg_image, (0, 0))
            seen_gameover = True

        if test:
            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_1]:

                whats_running = 'Start'
                seen_start = False

            elif keys[pygame.K_2]:

                whats_running = 'Victory'
                seen_victory = False

            elif keys[pygame.K_3]:

                whats_running = 'Game Over'
                seen_gameover = False

            elif keys[pygame.K_4]:

                whats_running = 'Lvl1'
                seen_lvl1 = False

            elif keys[pygame.K_5]:

                whats_running = 'Lvl1Run'

    if  whats_running == 'Lvl1':

        if not seen_lvl1:

            screen.blit(lvl1_bg_image, (0, 0))
            seen_lvl1 = True

        pygame.draw.rect(screen, (255, 0, 0), button_rect4)
        screen.blit(text4, text4_rect)
        
        if test:

            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_1]:

                whats_running = 'Start'
                seen_start = False

            elif keys[pygame.K_2]:

                whats_running = 'Victory'
                seen_victory = False

            elif keys[pygame.K_3]:

                whats_running = 'Game Over'
                seen_gameover = False

            elif keys[pygame.K_4]:

                whats_running = 'Lvl1'
                seen_lvl1 = False

            elif keys[pygame.K_5]:

                whats_running = 'Lvl1Run'

            


    if whats_running == 'Lvl1Run':

        lvl1run_rect = lvl1run_bg_image.get_rect()
        screen.blit(lvl1run_bg_image, (0, background_y))
        screen.blit(lvl1run_bg_image, (0, background_y - screen_height))

        background_y += 0.5

        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.bottomright = (screen.get_width() - 1170, screen.get_height() - 10)
        screen.blit(score_text, score_rect)

        #highscore_text = font.render("Highscore: " + str(highscore), True, (0, 0, 0))
        #highscore_rect = highscore_text.get_rect()
        #highscore_rect.bottomright = (screen.get_width() - 1170, screen.get_height() - 50)
        #screen.blit(highscore_text, highscore_rect)

        lifePoints_text = font.render("LP: " + str(lifePoints), True, (0, 0, 0))
        text_rect = lifePoints_text.get_rect()
        text_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)
        screen.blit(lifePoints_text, text_rect)

        fps = int(clock.get_fps())
        fps_text = font.render ('FPS: ' + str(fps), True, (0, 0, 0))
        fps_rect = fps_text.get_rect()
        fps_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 50)
        screen.blit(fps_text, fps_rect)

        

       

        if background_y >= screen_height:
            background_y = 0
        
        if test:

            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_1]:

                whats_running = 'Start'
                seen_start = False

            elif keys[pygame.K_2]:

                whats_running = 'Victory'
                seen_victory = False

            elif keys[pygame.K_3]:

                whats_running = 'Game Over'
                seen_gameover = False

            elif keys[pygame.K_4]:

                whats_running = 'Lvl1'
                seen_lvl1 = False

            elif keys[pygame.K_5]:

                whats_running = 'Lvl1Run'

            elif keys[pygame.K_z]:

                if lifePoints >= 1:
                    lifePoints = lifePoints - 1
                    print(lifePoints)

        for shot in player_shots:
            shot.update(dt)
            screen.blit(shot.image, shot.rect)
            #for enemy in enemies:
             #   if shot.rect.colliderect(enemy.rect):
              #      player_shots.remove(shot)
               #     enemy.hitPointsRest -= 1
                #    if enemy.hitPointsRest <= 0.75 * enemy.hitPoints and enemy.hitPointsRest >= 0.50 * enemy.hitPoints:
                 #       enemy.image = pygame.image.load('png/' + enemy.name + '/'+ enemy.name + 'damage1.png')
                  #  elif enemy.hitPointsRest <= 0.50 * enemy.hitPoints and enemy.hitPointsRest >= 0.25 * enemy.hitPoints:
                   #     enemy.image = pygame.image.load('png/' + enemy.name + '/'+ enemy.name + 'damage2.png')
                    #elif enemy.hitPointsRest <= 0.25 * enemy.hitPoints and enemy.hitPointsRest >= 0: 
            #            enemy.image = pygame.image.load('png/' + enemy.name + '/'+ enemy.name + 'damage3.png')
             #       elif enemy.hitPointsRest <= 0:
              #          enemy.image = pygame.image.load('png/' + enemy.name + '/'+ enemy.name + 'damage3.png') 
               #         enemy.rect.topleft = (1000, 1000)
                #        score += enemy.hitPoints   

        player.handle_input()

        
        player.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

    pygame.display.flip()

pygame.quit()
