import pygame
import threading

from anew.set_up import PygameSetUp
from anew.world import World


class GameInstance:
    def __init__(self):
        self.running = True
        self.conf = PygameSetUp("FullStratFightTactic", 1000, 720, 60)
        self.world = World(self.conf)

    def exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def joueur1_button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.world.player[1].position_affectee = event.pos

    def joueur2_button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.world.player[0].position_affectee = event.pos

    def event(self):
        for event in pygame.event.get():
            self.exit(event)
            self.joueur1_button(event)
            self.joueur2_button(event)

    def game(self):
        f1 = self.conf.fenetres.add_sous_fenetre(self.conf.main_window, (10, 10), 980, 520, "campagne")
        f2 = self.conf.fenetres.add_sous_fenetre(self.conf.main_window, (10, 540), 980, 170, "stats")

        while self.running:
            self.event()

            f1.window.fill((190, 200, 90))
            f2.window.fill((180, 180, 180))

            self.world.run(f1)
            self.world.affiche_stat(f2)

            for f in self.conf.fenetres.all:
                f.comportement()

            self.conf.curseur.refresh_curseur()
            self.conf.main_window.window_refresh()
            self.conf.horloge.fps_control()

            # Ajoutez un délai pour ne pas surcharger la connexion
            # time.sleep(0.1)

    def creer_un_thread(self, cible):
        thread = threading.Thread(target=cible)
        print('thread créé')
        thread.daemon = True
        thread.start()
