import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_x = random.randint(0, 1100)
    bb_y = random.randint(0, 650)
    bb_rct.center = bb_x, bb_y
    vx , vy = +5 , +5
    clock = pg.time.Clock()
    tmr = 0
    

    DELTA = {
        pg.K_UP:    (0, -5),
        pg.K_DOWN:  (0, +5),
        pg.K_LEFT:  (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    def check_bound(rct: pg.rect) -> tuple[bool, bool]:
        """
        引数で与えられたRectが画面内か画面外か判定する関数
        引数：こうかとんRectかばくだんRect
        戻り値：横方向、縦方向判定結果（True：画面内。False：画面外）
        """
        yoko, tate = True, True
        if rct.left < 0 or WIDTH < rct.right:
            yoko = False
        if rct.top < 0 or HEIGHT < rct.bottom:
            tate = False
        return yoko, tate

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
        if kk_rct.colliderect(bb_rct):
            return
        
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, delta in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)


        bb_rct.move_ip(vx , vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
