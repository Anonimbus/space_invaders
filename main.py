import pygame
import random
from pygame import mixer

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((1000, 800))   #(width, height)

#Background
background = pygame.image.load("images/background.jpg")

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/ufo_high.png")
pygame.display.set_icon(icon)

#Font and Mixer
if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")
#Fonts
font = pygame.font.Font('freesansbold.ttf', 32)
big_font = pygame.font.Font('freesansbold.ttf', 70)
#Sounds and Music
mixer.music.load("sound_effects/rock_music.mp3")
mixer.music.play(-1)
bullet_sound = mixer.Sound("sound_effects/laser.wav")
explosion_sound = mixer.Sound("sound_effects/explosion.mp3")
game_over_sound = mixer.Sound("sound_effects/game-over-arcade.mp3")
# Set the volume (0.0 to 1.0)
mixer.music.set_volume(0.1)
bullet_sound.set_volume(0.5)
explosion_sound.set_volume(0.5)
game_over_sound.set_volume(1.0)

#Player
playerImg = pygame.image.load("images/spaceship_color.png")
playerX = 470
playerY = 700
player_speed = 1.5
playerX_change = 0;

#Enemy
enemyImg = pygame.image.load("images/alien.png")
enemyX_speed = 1
enemyY_change = 30

no_of_enemies = 6
enemyDir = [1] * no_of_enemies
enemyX = [0] * no_of_enemies
enemyY = [0] * no_of_enemies
enemy_alive = [False] * no_of_enemies

#Bullet
bulletImg = pygame.image.load("images/bullets.png")
bulletX = playerX + 2
bulletY = playerY
bulletY_change = 5
bullet_fired = False

#Functions
def display_score(x, y):
    score_text = font.render("Score: " + str(Score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def pause_screen():
    resume_text = font.render("Press 'p' to pause/resume", True, (255, 255, 255))
    screen.blit(resume_text, (340, 360))

def gameOver():
    global player_out
    game_over_text = big_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over_text, (300, 350))
    player_out = True
    restart_text = font.render("Press 'r/R' to restart", True, (255, 255, 255))
    screen.blit(restart_text, (370, 430))

def player_render(x, y):
    screen.blit(playerImg, (x, y))

def enemy_render(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_fired
    bullet_fired = True
    screen.blit(bulletImg, (x, y))

def destroy_bullet():
    global bullet_fired, bulletY
    bullet_fired = False
    bulletY = 999

def init_enemy(i):
    global enemyX, enemyY, enemyX_speed, enemyY_change, enemy_alive
    # enemyX_speed *= 1.001
    # enemyY_change += 1  #increases the distance the enemy falls
    enemyX[i] = random.randint(1, 934)
    enemyY[i] = random.randint(50, 150)
    enemy_alive[i] = True

#Game Loop
for i in range(no_of_enemies):
    init_enemy(i)
Score = 0
program_running = True
paused = False
player_out = False
while program_running:    
    screen.fill((80, 80, 80))
    screen.blit(background, (0,0))

    display_score(10, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_running = False

        #if keystroke is pressed, perform certain actions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # prompt to quit the program
                quit_prompt = True
                while quit_prompt:
                    for sub_event in pygame.event.get():
                        if sub_event.type == pygame.KEYDOWN:
                            if sub_event.key == pygame.K_y:
                                program_running = False
                                quit_prompt = False
                            if sub_event.key == pygame.K_n:
                                quit_prompt = False
                    screen.fill((0, 0, 0))
                    quit_text = font.render("Are you sure you want to quit? (y/n)", True, (255, 255, 255))
                    screen.blit(quit_text, (250, 360))
                    pygame.display.update()

            if event.key == pygame.K_p:
                # pause/resume the program
                paused = True
                while paused:
                    for sub_event in pygame.event.get():
                        if sub_event.type == pygame.KEYDOWN:
                            if sub_event.key == pygame.K_p:
                                paused = False
                    pause_screen()
                    pygame.display.update()
            
            if event.key == pygame.K_r:
                # Reload or restart the game
                Score = 0
                playerX = 470
                playerY = 700
                playerX_change = 0
                bullet_fired = False
                bulletX = playerX + 2
                bulletY = playerY
                player_out = False
                for i in range(no_of_enemies):
                    init_enemy(i)

            if event.key == pygame.K_m:
                # mute the sounds
                if mixer.music.get_volume() > 0:
                    mixer.music.set_volume(0)
                    bullet_sound.set_volume(0)
                    explosion_sound.set_volume(0)
                else:
                    mixer.music.set_volume(0.1)
                    bullet_sound.set_volume(0.5)
                    explosion_sound.set_volume(0.5)
                    game_over_sound.set_volume(1)


        #if keystroke is released then stop the spaceship
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    #player control by arrow_keys, and shoot by spacebar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerX_change = -player_speed
    if keys[pygame.K_RIGHT]:
        playerX_change = player_speed
    if keys[pygame.K_SPACE]:
        if not bullet_fired:    #this line lets user fire only once
            bulletX = playerX + 2
            bulletY = playerY
            fire_bullet(bulletX, bulletY)
            bullet_sound.play()
    playerX += playerX_change

    #checking player boundary
    if playerX < 0:
        playerX = 0
    elif playerX > 935:
        playerX = 935
    
    #Enemy Movement
    for i in range(no_of_enemies):
        enemyX[i] += enemyDir[i]*enemyX_speed
        #checking if enemy hits the boundary
        if enemyX[i] <= 0:         #left boundary
            enemyDir[i] = 1        #right direction
            enemyY[i] += enemyY_change
        elif enemyX[i] >= 935:     #right boundary
            enemyDir[i] = -1       #left direction
            enemyY[i] += enemyY_change
        
        #check bullet-enemy collision
        if (bulletX > enemyX[i] - 30 and bulletX < enemyX[i] + 30) and (bulletY <= enemyY[i] + 40 and bulletY > enemyY[i] ):
            enemy_alive[i] = False #doesn't play a role now, as the enemy is continuously spawning
            # destroy_bullet()  #uncomment if you want to kill a single enemy with a single bullet
            Score += 1
            explosion_sound.play()
            pygame.time.delay(30)
            init_enemy(i)
            #blast effects

        #Game Over
        if enemyY[i] >= 620:
            if not player_out:  #the player becomes out only in the gameOver() below
                game_over_sound.play()
            gameOver()
            for j in range(no_of_enemies):
                enemyY[j] = 2000
        
        if enemy_alive[i]:
            enemy_render(enemyX[i], enemyY[i])

    #change the bullet Y-position each loop
    if bullet_fired:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #make the bullet disappear on top of the screen
    if bulletY <= 20:
        destroy_bullet()

    player_render(playerX, playerY)
    pygame.display.update()