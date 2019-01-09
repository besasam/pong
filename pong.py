import sys
import pygame as pg
pg.init()
pg.font.init()

clock = pg.time.Clock()

size = width, height = 800, 600
black = 0, 0, 0
white = 255, 255, 255
speed = 10
lost = False

screen = pg.display.set_mode(size)
text = pg.font.Font(None, 50)

score = 0
scoredisp = text.render(str(score), False, white)
scorerect = scoredisp.get_rect()
scorerect = scorerect.move([width/2 - scorerect.width/2, 10])

paddle = pg.Surface((10, 100))
paddlerect = paddle.get_rect()
paddlerect = paddlerect.move([760, 250])

opp = pg.Surface((10, 100))
opprect = opp.get_rect()
opprect = opprect.move([30,250])
oppspeed = [0, speed]

ball = pg.Surface((10, 10))
ballrect = ball.get_rect()
ballrect = ballrect.move([395, 295])
ballspeed = [speed, speed]

while 1:
    clock.tick(20)

    pg.event.pump()
    keyinput = pg.key.get_pressed()
    if keyinput[pg.K_ESCAPE]: sys.exit()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    if keyinput[pg.K_UP] and paddlerect.top >= 10:
        paddlerect = paddlerect.move([0, -speed])
    if keyinput[pg.K_DOWN] and paddlerect.bottom <= height - 10:
        paddlerect = paddlerect.move([0, speed])

    if 10 < opprect.top < height - 110:
        if opprect.top < ballrect.top:
            oppspeed[1] = speed
            opprect = opprect.move(oppspeed)
        else:
            oppspeed[1] = -speed
            opprect = opprect.move(oppspeed)


    ballrect = ballrect.move(ballspeed)
    if ballrect.top < 10 or ballrect.bottom > height - 10:
        ballspeed[1] = -ballspeed[1]
    if ballrect.colliderect(paddlerect) or ballrect.colliderect(opprect):
        ballspeed[0] = -ballspeed[0]
        ballspeed[1] = -ballspeed[1]
    if ballrect.left < 0:
        score += 1
        scoredisp = text.render(str(score), False, white)
        ballrect = pg.Rect(395, 295, 10, 10)
        ballspeed = [speed, speed]
    if ballrect.right > width:
        lost = True

    screen.fill(black)

    if lost:
        msg = text.render("You lost! Score: " + str(score), False, white)
        msgrect = msg.get_rect()
        msgrect = msgrect.move([width/2 - msgrect.width/2, height/2 - msgrect.height/2])
        screen.blit(msg, msgrect)
    else:
        paddle.fill(white)
        opp.fill(white)
        ball.fill(white)
        screen.blit(paddle, paddlerect)
        screen.blit(opp, opprect)
        screen.blit(ball, ballrect)
        screen.blit(scoredisp, scorerect)

    pg.display.flip()