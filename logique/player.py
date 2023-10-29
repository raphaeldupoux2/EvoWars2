from logique._player_base import PlayerBase
import pygame

from utils import Utils


class Player(PlayerBase):
    def __init__(self, window, curseur, position, liste_obstacle):
        super().__init__(window, curseur, position, liste_obstacle, color=(50, 50, 90))
        self.is_in_control = True

    def bouton_change_in_controle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.is_in_control = not self.is_in_control

    def bouton(self, event):
        # if self.is_in_control:
        for b in self.maitrise.values():
            b.bouton(event)
        self.bouton_change_in_controle(event)

    def comportement(self):
        # if self.is_in_control:
        #     self.angle_mort(self.w.window)
        # self.affiche_skin()
        for m in self.maitrise.values():
            m.comportement((self.x_arme, self.y_arme))

        self.player.comportement((self.x_arme, self.y_arme), Utils.angle_degree_entre((self.x_arme, self.y_arme), self.direction))
        # self.item["couronne"].affiche_png()

        # self.ligne_vision(60)
        # self.ligne_vision(-60)

        if self.is_in_control:
            self.bouge()
        Utils.affiche_curseur(self.window.window)
        self.affiche_pied()
