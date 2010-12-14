#!/usr/bin/env python
import pygame
import random

class Paddle(pygame.sprite.Sprite):
    def __init__(self, xpos, ai=False):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ai = ai
        self.image =  pygame.Surface((10, 70))
        self.rect = self.image.get_rect()
        self.rect.topright = (xpos, 240)
        self.image.fill(pygame.Color("white"))

    def update(self):
        if not self.ai:
            pos = pygame.mouse.get_pos()
            self.rect.topright = (self.xpos, pos[1])
        else:
            global ai_speed
            dy = (1 if self.rect.center[1] < ball.rect.center[1] else -1)*ai_speed
            self.rect.center = (self.xpos-5, self.rect.center[1]+dy)

class Ball(pygame.sprite.Sprite):
    def __init__(self, paddles):
        pygame.sprite.Sprite.__init__(self)
        global ball_speed
        self.speed = ball_speed
        self.paddles = paddles
        self.pos_d = (random.choice([-1,1]), random.choice([-1,1]))
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.image.fill(pygame.Color("white"))

    def get_new_dy(self, paddle):
        new_dy = -(paddle.rect.center[1] - ball.rect.center[1])/15.0
        return new_dy

    def update(self):
        new_dx = self.pos_d[0]
        new_dy = self.pos_d[1]
        if self.rect.topright[1] >= 480:
            new_dy = -new_dy
        elif self.rect.topright[1] <= 0:
            new_dy = -new_dy
        elif self.rect.topright[0] <= 0:
            ai_score()
            new_round()
        elif self.rect.topright[0] >= 640:
            player_score()
            new_round()
        
            
        for paddle in self.paddles:
            if self.collision(paddle.rect):
                new_dx = -new_dx
                new_dy = self.get_new_dy(paddle)
                break

        self.pos_d = (new_dx, new_dy)
        self.rect.move_ip(new_dx*self.speed, new_dy*self.speed)
        
    def collision(self, target):
        return self.rect.colliderect(target)

def update_caption():
    global player_wins, ai_wins
    pygame.display.set_caption("Pong - Player: " + str(player_wins) + "  -  Computer: " + str(ai_wins))

def player_score():
    global player_wins
    player_wins += 1
    update_caption()

def ai_score():
    global ai_wins
    ai_wins += 1
    update_caption()

def new_round():
    global player, computer, ball, allsprites, ai_speed
    player = Paddle(10)
    computer = Paddle(630, True)
    ball = Ball([player, computer])
    ai_speed += 1
    allsprites = pygame.sprite.RenderPlain((player, computer, ball))
  



pygame.init()

ball_speed = 5
ai_speed = 3
player = Paddle(10)
computer = Paddle(630, True)
ball = Ball([player, computer])

player_wins = 0
ai_wins = 0

allsprites = pygame.sprite.RenderPlain((player, computer, ball))

screen = pygame.display.set_mode((640,480))

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(pygame.Color("black"))

screen.blit(background, (0,0))
pygame.display.flip()
pygame.display.set_caption("Pong - Player: 0  -  Computer: 0")
clock = pygame.time.Clock()

while 1:
    clock.tick(30)
    pygame.event.pump()
    allsprites.update()
    screen.blit(background,(0,0))
    allsprites.draw(screen)
    pygame.display.flip()
