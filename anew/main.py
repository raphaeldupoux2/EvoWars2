import pygame

from anew.player import Player
from pygame_setup import PygameSetUp


class Monde:
    def __init__(self):
        self.all_objects = []
        self.player = []

    def refresh_all_objects(self):
        self.all_objects = self.player

    def comportement(self, fenetre):
        for o in self.all_objects:
            o.comportement(fenetre)


class GameInstance:
    def __init__(self):
        self.running = True
        self.conf = PygameSetUp()
        self.monde = Monde()

    def exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def event(self):
        for event in pygame.event.get():
            self.exit(event)

    def game(self):
        self.conf.horloge.fps = 60
        main = self.conf.main_window.add_main_fenetre("FullStratFightTactic", 1000, 720)
        f1 = self.conf.fenetres.add_sous_fenetre(main, (10, 10), 980, 700, "campagne")
        f2 = self.conf.fenetres.add_sous_fenetre(main, (1020, 10), 200, 200, "monde parallèle")
        self.monde.player.append(Player((50, 50), (55, 125)))

        while self.running:
            self.event()

            f1.window.fill((0, 255, 0))
            f2.window.fill((255, 0, 0))

            self.monde.refresh_all_objects()
            self.monde.comportement(f1)

            for f in self.conf.fenetres.all:
                f.comportement()

            self.conf.curseur.refresh_curseur()
            main.window_refresh()
            self.conf.horloge.fps_control()


g = GameInstance()
g.game()
