import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH , HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("FOXY")

fox_width , fox_height = 60,70
ship_width , ship_height = 80,90
slide_width , slide_height = 100 , 50

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

isjump = False
jump_count = 7

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
BORDER = pygame.Rect(0 , HEIGHT//2 -5, WIDTH , 10)

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'gunshot.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'hitsound.mp3'))


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT =  pygame.font.SysFont('comicsans' ,100)

FOX_HIT = pygame.USEREVENT + 1
ship_HIT = pygame.USEREVENT +2

fox_image = pygame.image.load(os.path.join('assets','FOXY.png'))
fox = pygame.transform.scale(fox_image, (fox_width , fox_height))

slide_image = pygame.image.load(os.path.join('assets','slide.png' ))
Slide = pygame.transform.scale(slide_image ,(slide_width , slide_height))

YELLOW_SPACE_S = pygame.image.load(os.path.join('assets','yellow spaceS.png'))
yellow_spaceS = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACE_S, (ship_width, ship_height)), 180)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.jpg')), (WIDTH, HEIGHT))


def draw_window(ship, FOX , SLIDE, ship_bullets , fox_bullets, fox_health , ship_health):
    WIN.blit(SPACE, (0,0))
    WIN.blit(fox,(FOX.x , FOX.y))

    fox_health_text = HEALTH_FONT.render("SCORE: " + str(fox_health), 1 , WHITE)
    ship_health_text  = HEALTH_FONT.render("SCORE: " + str(ship_health), 1, WHITE)
    WIN.blit(fox_health_text, (10, HEIGHT - fox_health_text.get_height()- 200))
    WIN.blit( ship_health_text, (10,10))

    WIN.blit(yellow_spaceS , (ship.x, ship.y))
    WIN.blit(Slide , (SLIDE.x , SLIDE.y))


    for bullet in fox_bullets:
        pygame.draw.rect(WIN , RED , bullet)
    for bullet in ship_bullets:
        pygame.draw.rect(WIN , BLUE , bullet)

    pygame.display.update()

def FOX_handle_movement(keys_pressed , FOX):
    global isjump
    global jump_count

    if keys_pressed[pygame.K_a] and FOX.x -VEL >0:  # LEFT MOVEMENT
        FOX.x -= VEL
    if keys_pressed[pygame.K_d] and FOX.x +VEL + fox_width < WIDTH:  # RIGHT MOVEMENT
        FOX.x += VEL
    if not(isjump):

        if isjump is False and keys_pressed[pygame.K_SPACE]:

            isjump = True
    else:
        if jump_count >= -7:
            neg = 1
            if jump_count < 0:
                neg = -1
            FOX.y -= (jump_count ** 2) * 1 * neg
            jump_count -= 1
        else:
            isjump = False
            jump_count = 7


def ship_handle_movement(keys_pressed , ship):
    if keys_pressed[pygame.K_LEFT] and ship.x - VEL > 0:  # LEFT MOVEMENT
        ship.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and ship.x + VEL + ship_width < WIDTH:  # RIGHT MOVEMENT
        ship.x += VEL

def slide_handle_movement(SLIDE):
    if SLIDE.x -VEL > 0:
        SLIDE.x -= VEL

    elif SLIDE.x + VEL + slide_width < WIDTH:
        SLIDE.x += VEL

def handle_bullet(fox_bullets , ship_bullets , FOX , ship):
    for bullet in fox_bullets:
        bullet.y -= BULLET_VEL
        if ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ship_HIT))
            fox_bullets.remove(bullet)
        elif bullet.y < 0:
            fox_bullets.remove(bullet)


    for bullet in ship_bullets:
        bullet.y += BULLET_VEL
        if FOX.colliderect(bullet):
            pygame.event.post(pygame.event.Event(FOX_HIT))
            ship_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            ship_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2 , HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
def main():

    ship = pygame.Rect(430 ,50 , ship_width , ship_height)
    FOX = pygame.Rect(10 , 430 , fox_width ,fox_height)
    SLIDE = pygame.Rect(600, 440 , slide_width , slide_height)

    ship_bullets= []
    fox_bullets= []

    fox_health = 10
    ship_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(fox_bullets)< MAX_BULLETS:
                    bullet = pygame.Rect(FOX.x + fox_width//2 - 2, FOX.y  , 10 , 5)
                    fox_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(ship_bullets)< MAX_BULLETS:
                    bullet = pygame.Rect(ship.x + ship_width//2 - 2,ship.y+ ship_height, 10, 5)
                    ship_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == FOX_HIT:
                fox_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == ship_HIT:
                ship_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if fox_health <= 0:
            winner_text = "SHIP WINS!!!"

        if ship_health <= 0:
            winner_text = "FOX WINS!!!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        FOX_handle_movement(keys_pressed,FOX)
        ship_handle_movement(keys_pressed , ship)
        handle_bullet(fox_bullets, ship_bullets, FOX, ship)
        draw_window(ship , FOX , SLIDE, fox_bullets , ship_bullets, fox_health , ship_health)

    main()

if __name__ == "__main__":
    main()
