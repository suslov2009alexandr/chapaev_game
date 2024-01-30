import pygame
import os
from math import atan, cos, sin, pi

pygame.init()

size = w, h = 600, 600
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

current = 1


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Board:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.left = 100
        self.top = 100
        self.current1 = 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        colors = [pygame.Color('brown'), pygame.Color('yellow')]
        for y in range(self.height):
            current2 = self.current1
            for x in range(self.width):
                pygame.draw.rect(scr, colors[current2],
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size))
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)
                current2 = (current2 + 1) % 2
            self.current1 = (current2 + 1) % 2

    def reversal(self):
        self.current1 = (self.current1 + 1) % 2


class Checker(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        super().__init__(all_sprites)
        self.diameter = 48
        self.pos = pos
        self.color = color
        self.dx = 0
        self.dy = 0
        self.dx_s = 0
        self.dy_s = 0
        self.v_side = 1
        self.k = 1
        self.image = pygame.Surface((self.diameter, self.diameter),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('white' if color == 1 else 'black'),
                           (self.diameter / 2, self.diameter / 2), self.diameter / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pre_dx = 0
        self.pre_dy = 0

    def update(self, _events, _screen, _board, _mouse_pos):
        # if self.dx < -600:
        #     self.dx = -600
        # if self.dx > 600:
        #     self.dx = 600
        # if self.dy < -600:
        #     self.dy = -600
        # if self.dy > 600:
        #     self.dy = 600

        # self.dx += self.dx_s
        # self.dy += self.dy_s
        # self.dx_s = 0
        # self.dy_s = 0
        pre = []

        # co = self.rect.topleft

        def examination():
            if len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)) > 1:
                for s in pygame.sprite.spritecollide(self, all_sprites, dokill=False):
                    if s == self:
                        continue
                    # co = self.rect.topleft
                    # co2 = s.rect.topleft
                    if len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)) > 1 and not (
                            self.dx == 0) and not (
                            self.dy == 0):
                        if s in pre:
                            continue
                        a1 = atan(self.dy / self.dx)
                        dx = self.rect.topleft[0] - s.rect.topleft[0]
                        dy = self.rect.topleft[1] - s.rect.topleft[1]
                        if not (dx == 0):
                            a2 = atan(dy / dx)
                            a = a1 - a2
                            coefficient = 1 / cos(a)  # 1 / cos(a)
                            c = self.diameter * coefficient
                            x1 = -1 * (s.rect.topleft[0] + (
                                    self.diameter / 2) -
                                       (c ** 2 / ((self.dy / self.dx) ** 2 + 1)) - self.rect.topleft[
                                           0] - self.diameter / 2)
                            y1 = -1 * (s.rect.topleft[1] + (
                                    self.diameter / 2) -
                                       (self.dy / self.dx * x1) - self.rect.topleft[1] - self.diameter / 2)
                            s.side_v(x1, y1)
                        else:
                            a = pi / 2 - a1
                            coefficient = cos(a)
                            side = coefficient * self.diameter
                            x1 = -1 * cos(a1) * side
                            y1 = -1 * self.diameter - sin(a1) * side
                            s.side_v(x1, y1)
                        s.set_v(self.dx / len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)),
                                self.dy / len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)))
                        # self.set_v(-self.dx / 2, -self.dy / 2)
                        shift(self.pre_dx, self.pre_dy, s)
                        pre.append(s)
                    elif len(
                            pygame.sprite.spritecollide(self, all_sprites, dokill=False)) > 1 and self.dx == 0 and not (
                            self.dy == 0):
                        if s in pre:
                            continue
                        x1 = s.rect.topleft[0] - self.rect.topleft[0]
                        y1 = 0
                        s.side_v(x1, y1)
                        s.set_v(self.dx / (len(pygame.sprite.spritecollide(self, all_sprites, dokill=False))),
                                self.dy / len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)))
                        # self.set_v(-self.dx / 2, -self.dy / 2)
                        shift(self.pre_dx, self.pre_dy, s)
                        pre.append(s)
                    elif len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)) > 1 and self.dy == 0 and \
                            not (self.dx == 0):
                        if s in pre:
                            continue
                        y1 = s.rect.topleft[1] - self.rect.topleft[1]
                        x1 = 0
                        s.side_v(x1, y1)
                        s.set_v(self.dx / 2, self.dy / 2)
                        # s.set_v(self.dx / 2, self.dy / 2)
                        # self.set_v(-self.dx / 2, -self.dy / 2)
                        shift(self.pre_dx, self.pre_dy, s)
                        pre.append(s)
                    # self.set_v(-self.dx / 2, -self.dy / 2)
                    self.set_v(-self.dx / len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)),
                               -self.dy / len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)))
                    #
                return True

        def shift(dx, dy, other):
            x_self, y_self = self.rect.topleft
            x_other, y_other = other.rect.topleft
            x1 = x_other - x_self
            y1 = y_other - y_self
            if not (dx == 0 and dy == 0):
                if dx > 0:
                    if dy > 0:
                        if x1 > 0 and y1 > 0:
                            other.move(1, 1)
                    elif dy < 0:
                        if y1 < 0 < x1:
                            other.move(1, -1)
                    else:
                        if x1 > 0:
                            other.move(1, 0)
                elif dx < 0:
                    if dy > 0:
                        if x1 < 0 < y1:
                            other.move(-1, 1)
                    elif dy < 0:
                        if x1 < 0 and y1 < 0:
                            other.move(-1, -1)
                    else:
                        if x1 < 0:
                            other.move(-1, 0)
                else:
                    if dy > 0:
                        if x1 == 0 < y1:
                            other.move(0, 1)
                    elif dy < 0:
                        if x1 == 0 and y1 < 0:
                            other.move(0, -1)
            else:
                if y1 > 0:
                    other.move(0, 1)
                elif y1 < 0:
                    other.move(0, -1)
                if x1 > 0:
                    other.move(1, 0)
                elif x1 < 0:
                    other.move(-1, 0)

        def in_board():
            coords = round(self.rect.x + self.diameter / 2), round(self.rect.y + self.diameter / 2)
            r = round(self.diameter / 2)
            if ((coords[0] + r < 100 or coords[0] - r > 500) or
                    (coords[1] + r < 100 or coords[1] - r > 500)):
                self.kill()
                checkers.remove(self)
                return
            ex = 0
            if coords[0] < 100:
                if coords[1] < 100:
                    a = 100 - coords[0]
                    b = 100 - coords[1]
                    ex = (a ** 2 + b ** 2) ** 2
                if coords[1] > 500:
                    a = 100 - coords[0]
                    b = coords[1] - 500
                    ex = (a ** 2 + b ** 2) ** 2
            if coords[0] > 500:
                if coords[1] < 100:
                    a = coords[0] - 100
                    b = 100 - coords[1]
                    ex = (a ** 2 + b ** 2) ** 2
                if coords[1] > 500:
                    a = coords[0] - 100
                    b = coords[1] - 500
                    ex = (a ** 2 + b ** 2) ** 2
                if ex > r:
                    self.kill()
                    checkers.remove(self)

        # if not (self.dx == self.dy == 0):
        #     print((self.pre_dx, self.pre_dy), (self.dx, self.dy))
        if self.pre_dx == 0 and self.pre_dy == 0:
            # co = self.rect.topleft
            if not (self.dx == 0):
                if not (abs(self.dx) - self.k < 0):
                    self.dx = self.dx - self.k if self.dx > 0 else self.dx + self.k
                else:
                    self.dx = 0
            if not (self.dy == 0):
                if not (abs(self.dy) - self.k < 0):
                    self.dy = self.dy - self.k if self.dy > 0 else self.dy + self.k
                else:
                    self.dy = 0
            if not (self.dx_s == 0):
                if not (abs(self.dx_s) - self.k < 0):
                    self.dx_s = self.dx_s - self.k if self.dx_s > 0 else self.dx_s + self.k
                else:
                    self.dx_s = 0
            if not (self.dy_s == 0):
                if not (abs(self.dy_s) - self.k < 0):
                    self.dy_s = self.dy_s - self.k if self.dy_s > 0 else self.dy_s + self.k
                else:
                    self.dy_s = 0
            self.pre_dx = self.dx + self.dx_s
            self.pre_dy = self.dy + self.dy_s
        if self.pre_dx == self.pre_dy == 0 and \
                len(pygame.sprite.spritecollide(self, all_sprites, dokill=False)) > 1:
            for s in pygame.sprite.spritecollide(self, all_sprites, dokill=False):
                if s == self:
                    continue
                shift(0, 0, s)
        # if not (self.pre_dx == 0 and self.pre_dy == 0):
        #     print((self.pre_dx, self.pre_dy), (self.dx, self.dy))
        d_x = self.pre_dx
        d_y = self.pre_dy
        # if not (self.pre_dx == 0 and self.pre_dy == 0):
        #     print(self.pre_dx, self.pre_dy)
        if abs(d_y) > abs(d_x):
            if not (d_x == 0):
                y = d_y // d_x
                x_limit = abs(d_x)
                for _ in range(abs(d_x)):
                    if self.pre_dx == self.pre_dy == 0:
                        break
                    # if _ == x_limit:
                    #     break
                    self.rect = self.rect.move(1 if d_x > 0 else -1, 0)
                    # if y == 0:
                    #     res = examination()
                    #     if res:
                    #         self.pre_dx -= 1 if self.pre_dx > 0 else -1
                    #         self.pre_dy = round(self.pre_dy / 2)
                    #         y = round(y / 2)
                    #         self.pre_dx = round(self.pre_dx / 2)
                    #         x_limit = round(x_limit / 2)
                    #         break
                    if d_y == 0:
                        res = examination()
                        if res:
                            if not (self.pre_dx == 0):
                                self.pre_dx -= 1 if self.pre_dx > 0 else -1
                            self.pre_dy = round(self.pre_dy / 2)
                            y = round(y / 2)
                            self.pre_dx = round(self.pre_dx / 2)
                            x_limit = round(x_limit / 2)
                            break
                    if not (self.pre_dx == 0):
                        self.pre_dx -= 1 if self.pre_dx > 0 else -1
                    for j in range(abs(y) if not (_ == abs(d_x) - 1) else abs(abs(d_y) % abs(d_x))):
                        if self.pre_dx == self.pre_dy == 0:
                            break
                        self.rect = self.rect.move(0, 1 if d_y > 0 else -1)
                        res = examination()
                        if res:
                            if not (self.pre_dy == 0):
                                self.pre_dy -= 1 if self.pre_dy > 0 else -1
                            self.pre_dy = round(self.pre_dy / 2)
                            y = round(y / 2)
                            self.pre_dx = round(self.pre_dx / 2)
                            x_limit = round(x_limit / 2)
                            break
                        if not (self.pre_dy == 0):
                            self.pre_dy -= 1 if self.pre_dy > 0 else -1
            else:
                y = d_y
                for _ in range(abs(d_y)):
                    if self.pre_dx == self.pre_dy == 0:
                        break
                    # if _ == y:
                    #     break
                    self.rect = self.rect.move(0, 1 if d_y > 0 else -1)
                    res = examination()
                    if res:
                        if not (self.pre_dy == 0):
                            self.pre_dy -= 1 if self.pre_dy > 0 else -1
                        self.pre_dy = round(self.pre_dy / 2)
                        y = round(y / 2)
                        break
                    if not (self.pre_dy == 0):
                        self.pre_dy -= 1 if self.pre_dy > 0 else -1
        elif (abs(d_x) > abs(d_y) or abs(d_x) == abs(d_y)) and not (d_x == 0 and d_y == 0):
            if not (d_y == 0):
                x = d_x
                y_limit = abs(d_y)
                for _ in range(abs(d_y)):
                    if self.pre_dx == self.pre_dy == 0:
                        break
                    # if _ == y_limit:
                    #     break
                    self.rect = self.rect.move(0, 1 if d_y > 0 else -1)
                    # if x == 0:
                    #     res = examination()
                    #     if res:
                    #         self.pre_dy -= 1 if self.pre_dy > 0 else -1
                    #         self.pre_dx = round(self.pre_dx / 2)
                    #         x = round(x / 2)
                    #         self.pre_dy = round(self.pre_dy / 2)
                    #         y_limit = round(y_limit / 2)
                    #         break
                    #     else:
                    #         self.pre_dy -= 1 if self.pre_dy > 0 else -1
                    if d_y == 0:
                        res = examination()
                        if res:
                            if not (self.pre_dy == 0):
                                self.pre_dy -= 1 if self.pre_dy > 0 else -1
                            self.pre_dx = round(self.pre_dx / 2)
                            x = round(x / 2)
                            self.pre_dy = round(self.pre_dy / 2)
                            y_limit = round(y_limit / 2)
                            break
                    if not (self.pre_dy == 0):
                        self.pre_dy -= 1 if self.pre_dy > 0 else -1
                    for j in range(
                            abs(x) if not (_ == abs(d_y) - 1 or (abs(d_x) == abs(d_y))) else abs(abs(d_x) % abs(d_y))):
                        if self.pre_dx == self.pre_dy == 0:
                            break
                        self.rect = self.rect.move(1 if d_x > 0 else -1, 0)
                        res = examination()
                        if res:
                            if not (self.pre_dx == 0):
                                self.pre_dx -= 1 if self.pre_dx > 0 else -1
                            self.pre_dx = round(self.pre_dx / 2)
                            x = round(x / 2)
                            self.pre_dy = round(self.pre_dy / 2)
                            y_limit = round(y_limit / 2)
                            break
                        if not (self.pre_dx == 0):
                            self.pre_dx -= 1 if self.pre_dx > 0 else -1
            else:
                x = d_x
                for _ in range(abs(d_x)):
                    if self.pre_dx == self.pre_dy == 0:
                        break
                    # if _ == x:
                    #     break
                    self.rect = self.rect.move(1 if d_x > 0 else -1, 0)
                    res = examination()
                    if res:
                        if not (self.pre_dx == 0):
                            self.pre_dx -= 1 if self.pre_dx > 0 else -1
                        self.pre_dx = round(self.pre_dx / 2)
                        x = round(x / 2)
                        break
                    if not (self.pre_dx == 0):
                        self.pre_dx -= 1 if self.pre_dx > 0 else -1
                    # if not (self.pre_dx == 0):
                    #     self.pre_dx -= 1 if self.pre_dx > 0 else -1
        # dx_s = self.dx_s
        # dy_s = self.dy_s
        # if abs(dy_s) > abs(dx_s):
        #     if not (dx_s == 0):
        #         y = dy_s // dx_s
        #         x_limit = abs(dx_s)
        #         for _ in range(abs(dx_s)):
        #             if _ == x_limit:
        #                 break
        #             self.rect = self.rect.move(1 if dx_s > 0 else -1, 0)
        #             if y == 0:
        #                 res = examination()
        #                 if res:
        #                     y = round(y / 2)
        #                     x_limit = round(x_limit / 2)
        #             for j in range(abs(y) if not (_ == abs(dx_s) - 1) else abs(dy_s % dx_s)):
        #                 self.rect = self.rect.move(0, 1 if dy_s > 0 else -1)
        #                 res = examination()
        #                 if res:
        #                     y = round(y / 2)
        #                     x_limit = round(x_limit / 2)
        #     else:
        #         y = dy_s
        #         for _ in range(abs(dy_s)):
        #             if _ == y:
        #                 break
        #             self.rect = self.rect.move(0, 1 if dy_s > 0 else -1)
        #             res = examination()
        #             if res:
        #                 y = round(y / 2)
        # elif abs(dx_s) > abs(dy_s):
        #     if not (dy_s == 0):
        #         x = dx_s // dy_s
        #         y_limit = abs(dy_s)
        #         for _ in range(abs(dy_s)):
        #             if _ == y_limit:
        #                 break
        #             self.rect = self.rect.move(0, 1 if dy_s > 0 else -1)
        #             if x == 0:
        #                 res = examination()
        #                 if res:
        #                     x = round(x / 2)
        #                     y_limit = round(y_limit / 2)
        #             for j in range(abs(x) if not (_ == abs(dy_s) - 1) else abs(dx_s % dy_s)):
        #                 self.rect = self.rect.move(1 if dx_s > 0 else -1, 0)
        #                 res = examination()
        #                 if res:
        #                     x = round(x / 2)
        #                     y_limit = round(y_limit / 2)
        #     else:
        #         x = dx_s
        #         for _ in range(abs(dx_s)):
        #             if _ == x:
        #                 break
        #             self.rect = self.rect.move(1 if dx_s > 0 else -1, 0)
        #             res = examination()
        #             if res:
        #                 x = round(x / 2)
        # self.v(_events, _screen, _board, _mouse_pos)
        # if not (self.dx_s == 0):
        #     if not (abs(self.dx_s) - self.k < 0):
        #         self.dx_s = self.dx_s - self.k if self.dx_s > 0 else self.dx_s + self.k
        #     else:
        #         self.dx_s = 0
        # if not (self.dy_s == 0):
        #     if not (abs(self.dy_s) - self.k < 0):
        #         self.dy_s = self.dy_s - self.k if self.dy_s > 0 else self.dy_s + self.k
        #     else:
        #         self.dy_s = 0
        # coords = round(self.rect.x + self.diameter / 2), round(self.rect.y + self.diameter / 2)
        # r = round(self.diameter / 2)
        # if ((coords[0] + r < 100 or coords[0] - r > 500) or
        #         (coords[1] + r < 100 or coords[1] - r > 500)):
        #     self.kill()
        #     checkers.remove(self)
        in_board()
        # if not (self.pre_dx == 0 and self.pre_dy == 0):
        #     print(self.pre_dx, self.pre_dy)

    def side_v(self, dx, dy):
        if not (dx == 0 and dy == 0):
            c = (dx ** 2 + dy ** 2) ** 0.5
            k = self.v_side / c
            x = dx * k
            y = dy * k
            self.dx_s = round(x)
            self.dy_s = round(y)

    def v(self, _events, _screen, _board, _mouse_pos):
        global current, perfect
        if self.rect.collidepoint(*_mouse_pos) and \
                any([_event.type == pygame.MOUSEBUTTONDOWN for _event in _events]):
            if not (self.color == current):
                return
            if not game:
                return
            if not turn:
                return
            _run = True
            p = _mouse_pos
            pre = _mouse_pos
            while _run:
                for _event in pygame.event.get():
                    if _event.type == pygame.MOUSEBUTTONUP:
                        _run = False
                p = pygame.mouse.get_pos()
                if not p == pre:
                    _screen.fill(pygame.Color('orange'))
                    _board.render(_screen)
                    _screen.blit(string_chapaev, string_chapaev_rect)
                    all_sprites.draw(_screen)
                    auxiliary_sprites.draw(_screen)
                    pygame.draw.line(_screen, start_pos=(self.rect.topleft[0] + self.diameter / 2,
                                                         self.rect.topleft[1] + self.diameter / 2),
                                     end_pos=p,
                                     color=pygame.color.Color('red'), width=3)
                pygame.display.flip()
            x = round(-1 * (p[0] - (self.rect.topleft[0] + self.diameter / 2)) * 1)
            y = round(-1 * (p[1] - (self.rect.topleft[1] + self.diameter / 2)) * 1)
            self.dx = x
            self.dy = y
            perfect = True
            # current = (current + 1) % 2

    def set_v(self, dx, dy):
        self.dx += round(dx)
        self.dy += round(dy)

    def reversal(self):
        self.rect.y = self.rect.y - (2 * (self.rect.y - 276))

    def is_stopped(self):
        return self.dx == 0 and self.dy == 0 and self.dx_s == 0 and self.dy_s == 0 and \
               self.pre_dy == 0 and self.pre_dx == 0

    def colour(self):
        return 1 if self.color else 0

    def move(self, x, y):
        self.rect = self.rect.move(x, y)


class StartAgain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(auxiliary_sprites)
        self.image = pygame.Surface((100, 24), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.color.Color('green'), (0, 0, 150, 24))
        self.font = pygame.font.Font(None, 30)
        string = self.font.render('Заново', 1, pygame.color.Color('white'))
        string_rect = string.get_rect()
        string_rect.topleft = (15, 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (498, 2)
        self.image.blit(string, string_rect)

    def update(self):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
                for s in checkers:
                    s.kill()
                checkers.clear()
                for s in auxiliary_sprites:
                    s.kill()
                start_again()


class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(auxiliary_sprites)
        self.image = pygame.Surface((120, 30), pygame.SRCALPHA, 32)
        self.font = pygame.font.Font(None, 30)
        string = self.font.render('Ход белых', 1, pygame.color.Color('white'))
        string_rect = string.get_rect()
        self.rect = self.image.get_rect()
        self.rect.topleft = (250, 30)
        self.image.blit(string, string_rect)

    def update(self):
        if count_white == 0 or count_black == 0:
            if count_black == count_white == 0:
                self.image = pygame.Surface((120, 30), pygame.SRCALPHA, 32)
                self.font = pygame.font.Font(None, 30)
                string = self.font.render('Ничья!', 1, pygame.color.Color('white'))
                string_rect = string.get_rect()
                self.rect = self.image.get_rect()
                self.rect.topleft = (250, 30)
                self.image.blit(string, string_rect)
            elif count_black == 0:
                self.image = pygame.Surface((175, 30), pygame.SRCALPHA, 32)
                self.font = pygame.font.Font(None, 30)
                string = self.font.render('Выиграли белые!', 1, pygame.color.Color('white'))
                string_rect = string.get_rect()
                self.rect = self.image.get_rect()
                self.rect.topleft = (225, 30)
                self.image.blit(string, string_rect)
            elif count_white == 0:
                self.image = pygame.Surface((185, 30), pygame.SRCALPHA, 32)
                self.font = pygame.font.Font(None, 30)
                string = self.font.render('Выиграли чёрные!', 1, pygame.color.Color('white'))
                string_rect = string.get_rect()
                self.rect = self.image.get_rect()
                self.rect.topleft = (225, 30)
                self.image.blit(string, string_rect)
            return
        if current == 1:
            self.image = pygame.Surface((120, 30), pygame.SRCALPHA, 32)
            self.font = pygame.font.Font(None, 30)
            string = self.font.render('Ход белых', 1, pygame.color.Color('white'))
            string_rect = string.get_rect()
            self.rect = self.image.get_rect()
            self.rect.topleft = (250, 30)
            self.image.blit(string, string_rect)
        else:
            self.image = pygame.Surface((120, 30), pygame.SRCALPHA, 32)
            self.font = pygame.font.Font(None, 30)
            string = self.font.render('Ход чёрных', 1, pygame.color.Color('white'))
            string_rect = string.get_rect()
            self.rect = self.image.get_rect()
            self.rect.topleft = (250, 30)
            self.image.blit(string, string_rect)


class Instruction(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(auxiliary_sprites)
        self.image = pygame.Surface((100, 24), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.color.Color('green'), (0, 0, 150, 24))
        self.font = pygame.font.Font(None, 30)
        string = self.font.render('Справка', 1, pygame.color.Color('white'))
        string_rect = string.get_rect()
        string_rect.topleft = (10, 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (498, 32)
        self.image.blit(string, string_rect)

    def update(self):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
                instruction_screen()


def instruction_screen():
    global screen, board, all_sprites, auxiliary_sprites, running
    close_group = pygame.sprite.Group()

    class Close(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(close_group)
            self.image = pygame.Surface((100, 24), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, pygame.color.Color('red'), (0, 0, 150, 24))
            self.font = pygame.font.Font(None, 30)
            string = self.font.render('Закрыть', 1, pygame.color.Color('white'))
            string_rect = string.get_rect()
            string_rect.topleft = (10, 2)
            self.rect = self.image.get_rect()
            self.rect.topleft = (250, 515)
            self.image.blit(string, string_rect)

        def update(self):
            nonlocal run
            for e in events_instruction:
                if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(instruction_mouse_pos):
                    run = False
                    self.kill()

    close = Close()
    run = True
    image = load_image('Chapaev.jpg')
    image_rect = image.get_rect()
    image_rect.topleft = (122, 65)
    font = pygame.font.Font(None, 30)
    goal1 = font.render('Цель: выбить все шашки противника,', 1,
                        pygame.color.Color('white'))
    goal_rect1 = goal1.get_rect()
    goal_rect1.topleft = (111, 310)
    goal2 = font.render('сохранив как можно больше своих.', 1,
                        pygame.color.Color('white'))
    goal_rect2 = goal2.get_rect()
    goal_rect2.topleft = (122, 330)
    turn_description1 = font.render('Ход делается по принципу "рогатки".', 1,
                                    pygame.color.Color('white'))
    turn_description_rect1 = turn_description1.get_rect()
    turn_description_rect1.topleft = (111, 360)
    turn_description2 = font.render('Оттяните мышкой линию от нужной шашки', 1,
                                    pygame.color.Color('white'))
    turn_description_rect2 = turn_description2.get_rect()
    turn_description_rect2.topleft = (83, 380)
    turn_description3 = font.render('эквивалентно силе удара в противоположном', 1,
                                    pygame.color.Color('white'))
    turn_description_rect3 = turn_description3.get_rect()
    turn_description_rect3.topleft = (69, 400)
    turn_description4 = font.render('направлении от желаемого.', 1,
                                    pygame.color.Color('white'))
    turn_description_rect4 = turn_description4.get_rect()
    turn_description_rect4.topleft = (162, 420)
    current_turn_description1 = font.render('Тот, кто сбил чужие шашки, не теряя своих,', 1,
                                           pygame.color.Color('white'))
    current_turn_description_rect1 = current_turn_description1.get_rect()
    current_turn_description_rect1.topleft = (80, 450)
    current_turn_description2 = font.render(
        'ходит снова, в противном случае ходит', 1,
        pygame.color.Color('white'))
    current_turn_description_rect2 = current_turn_description2.get_rect()
    current_turn_description_rect2.topleft = (100, 470)
    current_turn_description3 = font.render(
        'соперник.', 1,
        pygame.color.Color('white'))
    current_turn_description_rect3 = current_turn_description3.get_rect()
    current_turn_description_rect3.topleft = (250, 490)
    while run:
        events_instruction = pygame.event.get()
        instruction_mouse_pos = pygame.mouse.get_pos()
        for ev in events_instruction:
            if ev.type == pygame.QUIT:
                run = False
                running = False
        screen.fill(pygame.Color('orange'))
        screen.blit(string_chapaev, string_chapaev_rect)
        board.render(screen)
        all_sprites.draw(screen)
        auxiliary_sprites.draw(screen)
        pygame.draw.rect(screen, color=pygame.color.Color('orange'),
                         rect=(50, 50, 500, 500))
        pygame.draw.rect(screen, color=pygame.color.Color('white'),
                         rect=(50, 50, 500, 500), width=4)
        screen.blit(image, image_rect)
        screen.blit(goal1, goal_rect1)
        screen.blit(goal2, goal_rect2)
        close_group.draw(screen)
        screen.blit(turn_description1, turn_description_rect1)
        screen.blit(turn_description2, turn_description_rect2)
        screen.blit(turn_description3, turn_description_rect3)
        screen.blit(turn_description4, turn_description_rect4)
        screen.blit(current_turn_description1, current_turn_description_rect1)
        screen.blit(current_turn_description2, current_turn_description_rect2)
        screen.blit(current_turn_description3, current_turn_description_rect3)
        close.update()
        pygame.display.flip()


all_sprites = pygame.sprite.Group()
auxiliary_sprites = pygame.sprite.Group()

start_again_button = StartAgain()
status_bar = StatusBar()
instruction = Instruction()
checkers = []
for i in range(8):
    checkers.append(Checker(1, (100 + 50 * i + 1, 450 + 1)))
for i in range(8):
    checkers.append(Checker(0, (100 + 50 * i + 1, 100 + 1)))

board = Board(8, 8, 50)

game = True

turn = True
pre_current = current

count_white = 8
count_black = 8
pre_count_white = count_white
pre_count_black = count_black
perfect = False


def start_again():
    global current, start_again_button, status_bar, checkers, board, game, count_white, count_black, \
        turn, pre_current, pre_count_white, pre_count_black, perfect, instruction
    current = 1
    start_again_button = StartAgain()
    status_bar = StatusBar()
    instruction = Instruction()
    checkers = []
    for j in range(8):
        checkers.append(Checker(1, (100 + 50 * j + 1, 450 + 1)))
    for j in range(8):
        checkers.append(Checker(0, (100 + 50 * j + 1, 100 + 1)))
    board = Board(8, 8, 50)
    game = True
    count_white = 8
    count_black = 8
    turn = True
    pre_current = current
    pre_count_white = count_white
    pre_count_black = count_black
    perfect = False


def reverse():
    board.reversal()
    for s in all_sprites:
        s.reversal()


def all_stopped():
    return all([checker.is_stopped() for checker in checkers])


running = True
font_chapaev = pygame.font.Font(None, 40)
string_chapaev = font_chapaev.render('"ЧАПАЕВ"', 1, pygame.color.Color('red'))
string_chapaev_rect = string_chapaev.get_rect()
while running:
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color('orange'))
    screen.blit(string_chapaev, string_chapaev_rect)
    board.render(screen)
    all_sprites.draw(screen)
    auxiliary_sprites.draw(screen)
    auxiliary_sprites.update()
    # all_sprites.update(events, screen, board, mouse_pos)
    for c in checkers:
        c.v(events, screen, board, mouse_pos)
    checkers.sort(key=lambda x: (x.dx ** 2 + x.dy ** 2) ** 0.5, reverse=True)
    # for c in checkers:
    #     if not all([(c.dx, c.dy) == (0, 0) for c in checkers]):
    #         print([(c.dx, c.dy) for c in checkers])
    maximal = checkers[0]
    checkers.sort(key=lambda x: ((x.rect.x - maximal.rect.x) ** 2 + (x.rect.y - maximal.rect.y) ** 2) ** 0.5)
    # if not all([i.dx == i.dy == 0 for i in checkers]):
    #     print([c.rect.topleft for c in checkers])
    #     print()
    for c in checkers:
        c.update(events, screen, board, mouse_pos)
        # if not (c.dx == c.dy == 0):
        #     print(c.rect.topleft)
        #     print([(i.dx, i.dy) for i in checkers])
        # if not all([(c.dx, c.dy) == (0, 0) for c in checkers]):
        #     print([(c.dx, c.dy) for c in checkers])
        #     print()
    pygame.display.flip()
    clock.tick(FPS)
    count_white = len([s for s in all_sprites if s.colour() == 1])
    count_black = len([s for s in all_sprites if s.colour() == 0])
    if count_black == 0 or count_white == 0:
        game = False
    # if not (pre_current == current) and all_stopped():
    #     reverse()
    #     pre_current = current
    if ((((pre_count_white == count_white) or (pre_count_black != count_black)) and current == 0) or
        (((pre_count_black == count_black) or (pre_count_white != count_white)) and current == 1)) and \
            all_stopped() and perfect:
        current = (current + 1) % 2
        # pre_current = current
        # pre_count_white = count_white
        # pre_count_black = count_black
        perfect = False
        reverse()
        # print((count_white, count_black), (pre_count_white, pre_count_black))
    if all_stopped():
        if not turn:
            pygame.time.delay(1000)
        turn = True
        perfect = False
    else:
        turn = False
    pre_current = current
    pre_count_white = count_white
    pre_count_black = count_black
    # if not all([(c.dx, c.dy) == (0, 0) for c in checkers]):
    #     print('---------------------------------------------------------')
    #     print()
pygame.quit()
