import pygame as pg
import sys
import random as rd

# Konstanter
WIDTH = 400
HEIGHT = 600

# Størrelsen til vinduet
SIZE = (WIDTH, HEIGHT)

# Frames per second (bilder per sekund)
FPS = 60

# Farger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (142, 142, 142)
LIGHTBLUE = (127, 207, 255)

# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()

# Variabel som styrer om spillet skal kjøres
run = True

# Verdier for spilleren
w = 60 # bredde
h = 80 # høyde

# Startposisjon
x = WIDTH/2
y = HEIGHT - h - 20

# Henter bilde til spilleren
player_img = pg.image.load('bucket.png')

# Henter bilde for bakgrunnen
background_img = pg.image.load('background_snow_2-3.png')

# Tilpasser bakgrunnsbilde til vår skjermstørrelse
background_img = pg.transform.scale(background_img, SIZE)

# Henter font
font = pg.font.SysFont("Arial", 26)
    
# Poeng
points = 0

# Liv
lives = 3
# Fart
pace = 5

# Funksjin som viser antall poeng
def display_points():
    text_img = font.render(f"Antall poeng: {points}", True, BLACK)
    surface.blit(text_img, (20, 10))
    
def display_lives():
    text_lives = font.render(f"Antall liv: {lives}", True, BLACK)
    surface.blit(text_lives, (20, 50))
    
class Player:
    def __init__(self, navn):
        self.navn = navn
        self.antall_baller = 0
            
    def __str__(self):
        return f" {self.navn} klarte å fange {self.antall_baller}. "

class Ball:
    def __init__(self):
        self.w = 20
        self.h = 20
        self.r = 20
        self.x = rd.randint(w, WIDTH)
        self.y = -self.w

    def update(self):
        self.y += pace
    
    def draw(self):
        #pg.draw.circle(surface, WHITE, (self.x, self.y), self.r)
        snowball_img = pg.image.load('snowball.png')
        snowball_img = pg.transform.scale(snowball_img, (self.w, self.h))
        surface.blit(snowball_img, (self.x, self.y))
        


# Lager et ball-objekt
ball = Ball()


# Spill-løkken
while run:
    # Sørger for at løkken kjører i korrekt hastighet
    clock.tick(FPS)
    
    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes
    
    
    # Fyller skjermen med en farge
    #surface.fill(LIGHTBLUE)
    surface.blit(background_img, (0, 0))
    
    # Hastigheten til spilleren
    vx = 0
    

    keys = pg.key.get_pressed()
    
    # Sjekker om ulike taster trykkes på

    if keys[pg.K_LEFT]:
        vx = -5
    
    elif keys[pg.K_RIGHT]:
        vx = 5
    
    # Oppdaterer posisjonen til rektangelet
    x += vx
    
    # Ball
    ball.update()
    ball.draw()
    
    # Sjekker kollisjon og hvis TRUE endrer retning
    if x+w > WIDTH:
        #pg.draw.rect(surface, GREY, [WIDTH-w, HEIGHT-h, w, h])
        surface.blit(player_img, (WIDTH-w, HEIGHT-h-20))
    elif x <= 0:
        #pg.draw.rect(surface, GREY, [0, HEIGHT-h, w, h])
        surface.blit(player_img, (0, HEIGHT-h-20))
    else:
        # Spiller
        #pg.draw.rect(surface, GREY, [x, y, w, h])
        surface.blit(player_img, (x, y))
    
    # Sjekker kollisjon med bøtte
    if ball.y > y and x < ball.x < x+w:
        print("kollisjon")
        points+= 1
        pace += 0.1
        ball = Ball()
    
    # Sjekker om vi ikke klarer å fange ballen
    if ball.y + ball.r > HEIGHT:
        lives -= 1
    
        # Sjekker om spilleren fortsatt har liv
        if lives == 0:
            run = False # Game over
            print("Du klarte ikke å fange ballen")
            print(f"Du fikk {points} poeng")
            
            name = str(input("Hva heter du? "))
            
            filename = "scores_2.txt"
            with open(filename, "a") as file:
                file.write(f"{name};{points}\n")

            #run = False # Game over
        else:
            ball = Ball()
    
    
    # Tekst
    display_points()
    display_lives()
    
    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()


# Avslutter pygame
pg.quit()
sys.exit()