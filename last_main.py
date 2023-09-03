import math
import time
import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Evowars')
pygame.display.flip()

ligne = pygame.Surface([1000, 1])
ligne.set_colorkey((0, 0, 0))
ligne.fill((80, 80, 150))

epee = pygame.Surface([100, 10])
epee.set_colorkey((0, 0, 0))
epee.fill((186, 196, 200))


gun = pygame.Surface([80, 10])
gun.set_colorkey((0, 0, 0))
gun.fill((47, 79, 79))


def normalize_angle(angle):
    """
    Convertit un angle en un angle compris entre -180 et 180 degrés.

    Arguments :
    angle -- L'angle en degrés.

    Retourne :
    L'angle normalisé en degrés.
    """

    normalized_angle = angle % 360  # Calcul de l'angle modulo 360
    if normalized_angle > 180:  # Si l'angle est supérieur à 180 degrés
        normalized_angle -= 360  # Soustraire 360 degrés pour obtenir un angle négatif
    return normalized_angle


class TerrainTennis:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (222, 144, 144)
        self.largeur = 400
        self.longueur = 500
        self.largeur_bande = 10
        self.color_bande = (255, 255, 255)

    def affiche_terrain(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.largeur, self.longueur))
        pygame.draw.rect(window, self.color_bande, (self.x, self.y, self.largeur_bande, 500))
        pygame.draw.rect(window, self.color_bande, (self.x + self.largeur - self.largeur_bande, self.y, self.largeur_bande, 500))
        pygame.draw.rect(window, self.color_bande, (self.x, self.y, 400, self.largeur_bande))
        pygame.draw.rect(window, self.color_bande, (self.x, self.y + self.longueur - self.largeur_bande, 400, self.largeur_bande))
        pygame.draw.rect(window, self.color_bande, (self.x, self.y + self.longueur/2 - self.largeur_bande/2, 400, self.largeur_bande))


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (200, 200, 0)
        self.vitesse = 5
        self.radius = 10

    def affiche_skin(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.radius, 0)
        pygame.draw.circle(window, (0, 0, 0), [self.x, self.y], self.radius, 1)


class Arbre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tronc_radius = 15
        self.feuille_radius = 50

    def affiche_skin_feuille(self):
        return pygame.draw.circle(window, (50, 200, 90), [self.x, self.y], self.feuille_radius, 0)

    def affiche_skin_tronc(self):
        return pygame.draw.circle(window, (88, 41, 0), [self.x, self.y], self.tronc_radius, 0)

    def comportement(self):
        self.affiche_skin_feuille()
        self.affiche_skin_tronc()


class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.radius = 20
        self.color = (50, 50, 90)
        self.ligne = ligne
        self.arme = epee
        self.arme_degree = 0
        self.arme_degainee = True
        self.gun = gun
        self.gun_degree = 0
        self.gun_degainee = True
        self.coup = ""
        self.anim_charge = False
        self.etat_attaque = "repos"
        self.direction_charge = [0, 0]
        self.direction_attaque = [0, 0]
        self.vit_modif = 0
        self.solide = True
        self.obstacle = [Arbre(800, 60)]
        self.projectile = [Projectile(500, 500)]

    @property
    def curseur(self):
        return list(pygame.mouse.get_pos())

    def angle_vers(self, cible: list):
        return math.atan2(cible[1] - self.y, cible[0] - self.x)

    def arme_degree_r(self, curseur):
        """
        :param curseur:
        :return: angle de l'arme + angle de la direction du curseur
        """
        return -self.angle_vers(curseur) * 180 / math.pi + self.arme_degree

    def move_to(self, cible: list):
        self.x += math.cos(self.angle_vers(cible)) * self.vel(cible)
        self.y += math.sin(self.angle_vers(cible)) * self.vel(cible)

    def touche(self, objet):
        distance = math.sqrt((objet.x - self.x) ** 2 + (objet.y - self.y) ** 2)
        if distance <= self.radius + objet.tronc_radius:
            # self.color = (255, 0, 0)
            # print("truuuue")
            return True
        else:
            self.color = (50, 90, 90)
            # print("faaaalse")
            return False

    def bouge(self):
        old_x, old_y = self.x, self.y
        self.move_to(self.direction)
        if not self.solide:
            return

        for obstacle in self.obstacle:
            if self.touche(obstacle):
                new_x = self.x
                self.x = old_x
                if self.touche(obstacle):
                    self.x = new_x
                    self.y = old_y

                if self.touche(obstacle):
                    self.x = old_x

    def inside_circle(self, objet: list):
        if (objet[0] - self.x) ** 2 + (objet[1] - self.y) ** 2 <= 20 ** 2:
            return True
        return False

    def distance_to(self, objet: list):
        return math.sqrt((objet[1] - self.y) ** 2 + (objet[0] - self.x) ** 2)

    def vel(self, curseur):
        vel = self.distance_to(curseur) / 20
        if vel > 2:
            return 2 + self.vit_modif
        return vel

    def affiche_skin(self):
        return pygame.draw.circle(window, self.color, [self.x, self.y], self.radius, 0), \
               pygame.draw.circle(window, (0, 30, 55), [self.x, self.y], 100, 1), \
               pygame.draw.circle(window, (0, 30, 55), [self.x, self.y], 110, 1)

    @staticmethod
    def blit_rotate(surf, image, pos, origin_pos, angle):

        # calculate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        sin_a, cos_a = math.sin(math.radians(angle)), math.cos(math.radians(angle))
        min_x, min_y = min([0, sin_a * h, cos_a * w, sin_a * h + cos_a * w]), max(
            [0, sin_a * w, -cos_a * h, sin_a * w - cos_a * h])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (pos[0] - origin_pos[0] + min_x - pivot_move[0], pos[1] - origin_pos[1] - min_y + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)

        # rotate and blit the image
        surf.blit(rotated_image, origin)

    # Fanatique
    def bouton_fanatique(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_focused() and pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.etat_attaque != "fanatique":
                    self.etat_attaque = "fanatique"
                else:
                    self.etat_attaque = "repos"

    def fanatique(self):
        if self.coup == "coup droit":
            self.arme_degree += 12
        if self.coup == "revert":
            self.arme_degree -= 12

    # Coup
    def bouton_coup_epee(self, event):
        if self.arme_degree == -120 or self.arme_degree == 120:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.etat_attaque = "coup"
                self.direction_attaque = self.curseur

    def coup_epee(self):
        if self.coup == "coup droit":
            self.arme_degree += 12
            if normalize_angle(self.arme_degree) >= 120:
                self.etat_attaque = "repos"

        elif self.coup == "revert":
            self.arme_degree -= 12
            if normalize_angle(self.arme_degree) <= -120:
                self.etat_attaque = "repos"

    def bouton_charge(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.anim_charge = True
                self.direction_charge = self.curseur
                self.vit_modif += 8

    def charge(self):
        if abs(self.x - self.direction_charge[0]) < 20 and abs(
                self.y - self.direction_charge[1] < 20) or self.touche(self.obstacle[0]):
            self.anim_charge = False
            self.vit_modif -= 8

    def ligne_vision(self, degree):
        angle = -self.angle_vers(self.curseur) * 180 / math.pi - degree
        self.blit_rotate(window, self.ligne, (self.x, self.y), (0, 0.5), angle)

    def angle_mort(self, window, curseur):
        # Calculer les angles des deux bords du cône
        angle_g = self.angle_vers(curseur) - math.pi / 3
        angle_d = self.angle_vers(curseur) + math.pi / 3

        # Calculer les coordonnées des coins du rectangle gauche
        x1_g = self.x - 1000 * math.cos(angle_g)
        y1_g = self.y - 1000 * math.sin(angle_g)
        x2_g = self.x + 1000 * math.cos(angle_g)
        y2_g = self.y + 1000 * math.sin(angle_g)
        x3_g = x2_g + 1000 * math.sin(angle_g)
        y3_g = y2_g - 1000 * math.cos(angle_g)
        x4_g = x1_g + 1000 * math.sin(angle_g)
        y4_g = y1_g - 1000 * math.cos(angle_g)

        # Calculer les co0données des coins du rectangle droit
        x1_d = self.x - 1000 * math.cos(angle_d)
        y1_d = self.y - 1000 * math.sin(angle_d)
        x2_d = self.x + 1000 * math.cos(angle_d)
        y2_d = self.y + 1000 * math.sin(angle_d)
        x3_d = x2_d - 1000 * math.sin(angle_d)
        y3_d = y2_d + 1000 * math.cos(angle_d)
        x4_d = x1_d - 1000 * math.sin(angle_d)
        y4_d = y1_d + 1000 * math.cos(angle_d)

        # Dessiner les rectangles
        pygame.draw.polygon(window, (0, 0, 0), [(x1_g, y1_g), (x2_g, y2_g), (x3_g, y3_g), (x4_g, y4_g)])
        pygame.draw.polygon(window, (0, 0, 0), [(x1_d, y1_d), (x2_d, y2_d), (x3_d, y3_d), (x4_d, y4_d)])

    # Repos
    def repositionnement(self):
        if 120 > normalize_angle(self.arme_degree) > 0:
            self.arme_degree += 3
        elif -120 < normalize_angle(self.arme_degree) <= 0:
            self.arme_degree -= 3
        elif -180 < normalize_angle(self.arme_degree) < -125:
            self.arme_degree += 3
        elif 180 >= normalize_angle(self.arme_degree) > 125:
            self.arme_degree -= 3
        elif 125 >= normalize_angle(self.arme_degree) >= 120:
            self.arme_degree = 120
        elif -125 <= normalize_angle(self.arme_degree) <= -120:
            self.arme_degree = -120

    def change_hand(self):
        if self.arme_degree == -120:
            self.coup = "coup droit"
        elif self.arme_degree == 120:
            self.coup = "revert"

    def bouton_change_hand(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if self.arme_degree == -120:
                    self.arme_degree = 120
            if event.key == pygame.K_e:
                if self.arme_degree == 120:
                    self.arme_degree = -120

    @property
    def direction(self):
        if self.anim_charge:
            return self.direction_charge
        elif self.etat_attaque == "coup":
            return self.direction_attaque
        else:
            return self.curseur

    def affiche_arme(self):
        if self.etat_attaque == "fanatique":
            if self.coup == "coup droit":
                self.blit_rotate(window, self.arme, (self.x, self.y), (0, 20), self.arme_degree)
            elif self.coup == "revert":
                self.blit_rotate(window, self.arme, (self.x, self.y), (0, -10), self.arme_degree)
            else:
                self.blit_rotate(window, self.arme, (self.x, self.y), (0, 5), self.arme_degree)
        else:
            if self.coup == "coup droit":
                self.blit_rotate(window, self.arme, (self.x, self.y), (0, 20), self.arme_degree_r(self.direction))
            elif self.coup == "revert":
                self.blit_rotate(window, self.arme, (self.x, self.y), (0, -10), self.arme_degree_r(self.direction))
            else:
                self.blit_rotate(window, self.arme, (self.x, self.y), (0, 5), self.arme_degree_r(self.direction))

    # def detect_ball(self):
    #     arme
    #     if arme.collidepoint(self.projectile[0].x, self.projectile[0].y)

    def detection_collision_arme(self):
        print(self.check_collision(self.arme.get_rect(), self.projectile[0]), [self.x, self.y], end=' ')

    def check_collision(self, rect, circle):
        rect_center_x = rect.x + rect.width / 2
        rect_center_y = rect.y + rect.height / 2

        circle_distance_x = abs(circle.x - rect_center_x)
        circle_distance_y = abs(circle.y - rect_center_y)
        # print(circle_distance_x, circle_distance_y, rect.width / 2 + circle.radius)

        if circle_distance_x > (rect.width / 2 + circle.radius):
            return False
        if circle_distance_y > (rect.height / 2 + circle.radius):
            return False

        if circle_distance_x <= (rect.width / 2):
            return True
        if circle_distance_y <= (rect.height / 2):
            return True

        corner_distance_sq = (circle_distance_x - rect.width / 2) ** 2 + (circle_distance_y - rect.height / 2) ** 2

        return corner_distance_sq <= (circle.radius ** 2)

    def bouton_degainage(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if self.arme_degainee:
                    self.arme_degainee = False
                elif self.arme_degainee is False:
                    self.arme_degainee = True

    def bouton(self, event):
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

        # self.angle_mort(window, self.direction)
        self.ligne_vision(60)
        self.ligne_vision(-60)

        if self.arme_degainee:
            self.affiche_arme()

        self.bouge()
        self.affiche_skin()
        self.detection_collision_arme()


FPS = 60  # Définition du nombre de FPS souhaité
FRAME_DURATION = 1 / FPS  # Calcul de la durée en secondes entre chaque frame
arbre = Arbre(200, 500)
arbre2 = Arbre(80, 600)
arbre3 = Arbre(90, 400)
player = Player()
# projectile = Projectile(500, 500)
terrain = TerrainTennis(300, 100)
running = True
while running:
    start_time = time.monotonic()  # Mesure du temps de début de boucle

    window.fill((255, 240, 190))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.bouton(event)

    # print(logique.touche(logique.obstacle[0]), logique.color)

    arbre.comportement()
    player.obstacle[0].affiche_skin_feuille()
    arbre2.comportement()
    arbre3.comportement()
    player.obstacle[0].affiche_skin_tronc()

    # print(logique.etat_attaque, " ", logique.coup)

    terrain.affiche_terrain()
    player.projectile[0].affiche_skin()
    player.comportement()

    # print(logique.touche(logique.obstacle[0]), logique.color)
    pygame.display.flip()
    # print(logique.touche(logique.obstacle[0]), logique.color)

    # Mesure FPS
    end_time = time.monotonic()  # Mesure du temps de fin de boucle
    elapsed_time = end_time - start_time  # Calcul du temps écoulé depuis le début de la boucle
    time_to_wait = FRAME_DURATION - elapsed_time  # Calcul du temps d'attente avant la prochaine frame
    # print(time_to_wait)
    if time_to_wait > 0:  # Si le temps d'attente est positif, on attend ce temps
        time.sleep(time_to_wait)
