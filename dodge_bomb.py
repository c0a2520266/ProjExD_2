import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_x = random.randint(0, 1100)
    bb_y = random.randint(0, 650)
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
    
    def gameover(screen: pg.Surface) -> None:
        """
        画面を暗転させ"Game Over"と泣いているこうかとんを表示する関数
        引数：screen
        戻り値：なし
        """
        bg_gameover = pg.Surface((WIDTH, HEIGHT))
        bg_gameover.set_alpha(200)
        gameover_font = pg.font.Font(None, 120)
        txt = gameover_font.render("GAME OVER", True, (255, 255, 255))
        bg_gameover.blit(txt, [550, 325])
        gameover_img = pg.image.load("fig/8.png")
        bg_gameover.blit(gameover_img, [500, 200])
        screen.blit(bg_gameover, [0, 0])
        pg.display.update()
        time.sleep(5)
     
    def init_bb_imgs(bb_imgs, bb_accs) -> tuple[list[pg.Surface], list[int]]:
        """
        10段階のサイズ・速度のリストを得るための関数
        引数：なし
        戻り値：Surfaceとintのリストのタプル
        """
        for r in range(1, 11):
            bb_img = pg.Surface((20*r, 20*r))
            pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            bb_img.set_colorkey((0, 0, 0))
            bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
        return bb_imgs, bb_accs

    bb_imgs, bb_accs = init_bb_imgs([], [])
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = bb_x, bb_y

    def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
        """
        移動量タプルと対応する画像Surfaceの辞書を返す関数
        戻り値：移動量タプルと対応する画像Surfaceの辞書
        """
        kk_dict = {
            (0, 0): pg.transform.rotozoom(kk_img,0 , 1.0),
            (+5, 0): pg.transform.rotozoom(kk_img, -90, 1.0),
            (0, +5): pg.transform.rotozoom(kk_img, 180, 1.0),
            (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
            (0, -5): pg.transform.rotozoom(kk_img, 0, 1.0),
            (+5, +5): pg.transform.rotozoom(kk_img, -135, 1.0),
            (+5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
            (-5, +5): pg.transform.rotozoom(kk_img, +135, 1.0),
            (-5, -5): pg.transform.rotozoom(kk_img, +45, 1.0),
        }
        return kk_dict
    
    kk_imgs = get_kk_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # こうかとんと爆弾の当たり判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bg_img, [0, 0])

        # こうかとん移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, delta in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        mv_tuple = tuple(sum_mv)
        kk_img_disp = kk_imgs.get(mv_tuple, kk_imgs[(0, 0)])
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img_disp, kk_rct)

        # 爆弾の大きさ・速度を時間で変化させる
        bb_idx = min(tmr//500, 9)
        old_center = bb_rct.center
        bb_img = bb_imgs[bb_idx]
        bb_rct = bb_img.get_rect()
        bb_rct.center = old_center
        avx = vx * bb_accs[bb_idx]
        avy = vy * bb_accs[bb_idx]
        bb_rct.move_ip(avx, avy)
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
