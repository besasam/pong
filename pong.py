import sys
import random
import pygame as pg

# Initialize PyGame
pg.init()
pg.font.init()
clock = pg.time.Clock()
text = pg.font.Font(None, 50)

# Game variables
size = width, height = 800, 600
black = 0, 0, 0
white = 255, 255, 255
speed = 10
playing = False
lost = False

screen = pg.display.set_mode(size)

# Declare menu items
title = text.render("Pong", False, white)
titlerect = title.get_rect()
titlerect = titlerect.move([width/2 - titlerect.width/2, 10])

playtext = text.render(">Play", False, white)
playrect = playtext.get_rect()
playrect = playrect.move([width/2 - playrect.width/2, titlerect.height + 40])

exittext = text.render("Exit", False, white)
exitrect = exittext.get_rect()
exitrect = exitrect.move(
    [width/2 - exitrect.width/2, titlerect.height + playrect.height + 50])

selected = 0

# Initialize score & score display
score = 0
scoredisp = text.render(str(score), False, white)
scorerect = scoredisp.get_rect()
scorerect = scorerect.move([width/2 - scorerect.width/2, 10])

highscore = 0

# Player paddle
paddle = pg.Surface((10, 100))
paddlerect = paddle.get_rect()
paddlerect = paddlerect.move([760, 250])

# Opponent paddle
opp = pg.Surface((10, 100))
opprect = opp.get_rect()
opprect = opprect.move([30, 250])
oppspeed = [0, speed]

# Ball
ballrect = pg.Surface((10, 10)).get_rect()
ballrect = ballrect.move([395, 295])
ballspeed = [speed, speed]
ballimg = pg.transform.scale(pg.image.load('assets/green-pepper.png'), ballrect.size).convert_alpha()

# Game code
while 1:
    if not playing:
        pg.event.pump()
        keyinput = pg.key.get_pressed()
        if keyinput[pg.K_ESCAPE]:
            sys.exit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if keyinput[pg.K_UP] and selected == 1:
            playtext = text.render(">Play", False, white)
            exittext = text.render("Exit", False, white)
            selected = 0
        if keyinput[pg.K_DOWN] and selected == 0:
            playtext = text.render("Play", False, white)
            exittext = text.render(">Exit", False, white)
            selected = 1
        if keyinput[pg.K_RETURN]:
            if selected == 0:
                playing = True
            else:
                sys.exit()

        # Menu screen
        screen.fill(black)
        screen.blit(title, titlerect)
        screen.blit(playtext, playrect)
        screen.blit(exittext, exitrect)
        pg.display.flip()

    if playing:
        clock.tick(20)

        # Catch keystrokes (esc to exit, arrow up/down to move paddle)
        pg.event.pump()
        keyinput = pg.key.get_pressed()
        if keyinput[pg.K_ESCAPE]:
            sys.exit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if keyinput[pg.K_UP] and paddlerect.top >= 10 and not lost:
            paddlerect = paddlerect.move([0, -speed])
        if keyinput[pg.K_DOWN] and paddlerect.bottom <= height - 10 and not lost:
            paddlerect = paddlerect.move([0, speed])
        if keyinput[pg.K_RETURN] and lost:
            lost = False

        if not lost:
            # Opponent movement
            oppcenter = opprect.top + 50
            ballcenter = ballrect.top + 5
            offset = random.randint(100, 150)
            if oppcenter < ballcenter - offset and opprect.bottom < height:
                oppspeed[1] = speed
                opprect = opprect.move(oppspeed)
            elif oppcenter > ballcenter + offset and opprect.top > 0:
                oppspeed[1] = -speed
                opprect = opprect.move(oppspeed)

            # Ball movement
            ballrect = ballrect.move(ballspeed)
            # Bounce off upper/lower edge of screen
            if ballrect.top < 10 or ballrect.bottom > height - 10:
                ballspeed[1] = -ballspeed[1]
            # Bounce off paddles
            if ballrect.colliderect(paddlerect) or ballrect.colliderect(opprect):
                ballspeed[0] = -ballspeed[0]
                ballspeed[1] = -ballspeed[1]
            # Opponent misses ball -> score increase, respawn ball at center
            if ballrect.left < 0:
                score += 1
                scoredisp = text.render(str(score), False, white)
                ballrect = pg.Rect(395, 295, 10, 10)
                ballspeed = [speed, speed]
            # Player misses ball -> game lost
            if ballrect.right > width:
                lost = True
                ballrect = pg.Rect(395, 295, 10, 10)

            # Render graphics
            screen.fill(black)
            paddle.fill(white)
            opp.fill(white)
            screen.blit(paddle, paddlerect)
            screen.blit(opp, opprect)
            screen.blit(ballimg, ballrect)
            screen.blit(scoredisp, scorerect)
            pg.display.flip()

        while lost:
            pg.event.pump()
            keyinput = pg.key.get_pressed()
            if keyinput[pg.K_ESCAPE]:
                sys.exit()
            if keyinput[pg.K_RETURN]:
                lost = False
                break

            if score > highscore:
                highscore = score

            msg = text.render("You lost! Score: " + str(score), False, white)
            msgrect = msg.get_rect()
            msgrect = msgrect.move(
                [width/2 - msgrect.width/2, height/2 - msgrect.height/2])

            hsmsg = text.render("Highscore: " + str(highscore), False, white)
            hsrect = hsmsg.get_rect()
            hsrect = hsrect.move(
                [width/2 - hsrect.width/2, height/2 - msgrect.height/2 + hsrect.height + 20])

            playagain = text.render("Play again? (Enter)", False, white)
            parect = playagain.get_rect()
            parect = parect.move([width/2 - parect.width/2, height/2 -
                                  msgrect.height/2 + hsrect.height + parect.height + 60])
            screen.fill(black)
            screen.blit(msg, msgrect)
            screen.blit(hsmsg,hsrect)
            screen.blit(playagain,parect)
            pg.display.flip()
