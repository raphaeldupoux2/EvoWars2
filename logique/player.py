from ._player_base import PlayerBase
import pygame

from EvoWars2.utils import Utils


class Player:
    def __init__(self, window, liste_obstacle):
        self.physique = [PlayerPhysique(window, liste_obstacle)]
        self.spirit = []  # [PlayerSpirit(window)]


class PlayerPhysique(PlayerBase):
    def __init__(self, window, liste_obstacle):
        super().__init__(window, liste_obstacle, color=(50, 50, 90))
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
        # self.affiche_skin()
        for m in self.maitrise.values():
            m.comportement(self.position)

        self.player.comportement(self.position, Utils.angle_degree_entre(self.position, self.direction))
        # self.item["couronne"].affiche_png()

        # if self.is_in_control:
        #     self.angle_mort(self.w.window)
        # self.ligne_vision(60)
        # self.ligne_vision(-60)

        if self.is_in_control:
            self.bouge()
        Utils.affiche_curseur(self.w.window)


# Pour Plus Tard
# class PlayerSpirit(PlayerBase):
#     def __init__(self, window):
#         super().__init__(window, liste_obstacle=[], color=(255, 255, 255), is_in_control=True)
#
#     def bouton(self, event):
#         if self.is_in_control:
#             if self.etat_attaque == "repos":
#                 self.bouton_change_hand(event)
#                 self.bouton_coup_epee(event)
#
#             if self.anim_charge is False:
#                 self.bouton_charge(event)
#
#             self.bouton_fanatique(event)
#             self.bouton_degainage(event)
#
#     def comportement(self):
#         if self.etat_attaque == "repos":
#             self.repositionnement()
#             self.change_hand()
#
#         elif self.etat_attaque == "coup":
#             self.coup_epee()
#
#         elif self.etat_attaque == "fanatique":
#             self.fanatique()
#
#         if self.anim_charge:
#             self.charge()
#
#         # if self.is_in_control:
#         #     self.angle_mort(self.w.window)
#         # self.ligne_vision(60)
#         # self.ligne_vision(-60)
#
#         if self.arme_degainee:
#             self.affiche_arme()
#
#         self.bouge()
#         self.affiche_skin()
#         Utils.affiche_curseur(self.w.window)
#         # self.detection_collision_arme()
