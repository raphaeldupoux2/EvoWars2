import pygame
import threading

from anew.set_up import PygameSetUp
from anew.world import World


class GameInstance:
    def __init__(self):
        self.running = True

        pygame.init()
        # Récupérer la taille de l'écran
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h

        self.conf = PygameSetUp("FullStratFightTactic", self.screen_width, self.screen_height-50, 60)
        self.world = World(self.conf)

    def exit(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def change_control_joueur(self, event):
        if event.type == pygame.KEYDOWN:  # Vérifie si une touche a été enfoncée
            if event.key == pygame.K_SPACE:
                self.world.indice_personnage_control = (self.world.indice_personnage_control + 1) % len(self.world.liste_personnage_control)

    def joueur_deplacement(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # souris clic gauche
                self.world.personnage_control.position_affectee.x_abs = event.pos[0] + self.world.camera.x_abs
                self.world.personnage_control.position_affectee.y_abs = event.pos[1] + self.world.camera.y_abs

    def event(self):
        for event in pygame.event.get():
            self.exit(event)
            self.joueur_deplacement(event)
            self.change_control_joueur(event)

    def game(self):
        f1 = self.conf.fenetres.add_sous_fenetre(self.conf.main_window, (0, 0), self.screen_width, self.screen_height*0.85 - 1, "campagne")
        f2 = self.conf.fenetres.add_sous_fenetre(self.conf.main_window, (0, self.screen_height*0.85), self.screen_width, self.screen_height*0.25, "stats")

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
