from player._player_base import PlayerBase


class PlayerSpirit(PlayerBase):
    def __init__(self, window):
        super().__init__(window, liste_obstacle=[], color=(255, 255, 255), is_in_control=True)

    def bouton(self, event):
        if self.is_in_control:
            if self.etat_attaque == "repos":
                self.bouton_change_hand(event)
                self.bouton_coup_epee(event)

            if self.anim_charge is False:
                self.bouton_charge(event)

            self.bouton_fanatique(event)
            self.bouton_degainage(event)

    def comportement(self):
        if self.etat_attaque == "repos":
            self.repositionnement()
            self.change_hand()

        elif self.etat_attaque == "coup":
            self.coup_epee()

        elif self.etat_attaque == "fanatique":
            self.fanatique()

        if self.anim_charge:
            self.charge()

        # if self.is_in_control:
        #     self.angle_mort(self.w.window, self.direction)
        self.ligne_vision(60)
        self.ligne_vision(-60)

        if self.arme_degainee:
            self.affiche_arme()

        self.bouge()
        self.affiche_skin()
        self.affiche_curseur()
        self.detection_collision_arme()
