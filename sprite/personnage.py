import pygame


class AffichePlayer:
    def __init__(self, window, position, posture='cote'):
        self.w = window
        self.position = position
        self.posture = posture
        self.largeur, self.longueur = 250, 125
        self.image_path_origin = "picture/personnage/origin.png"
        self.image_path = "picture/personnage/personnage.png"
        self.postures = {
            "face": pygame.Rect(self.largeur/25, 0, self.largeur*55/250, self.longueur),
            "face-cote": pygame.Rect(self.largeur*70/250, 0, self.largeur*55/250, self.longueur),
            "cote": pygame.Rect(self.largeur/2, 0, self.largeur*55/250, self.longueur),
            "dos": pygame.Rect(self.largeur*183/250, 0, self.largeur*55/250, self.longueur)
            }
        self.image = self.load_image()

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.longueur))
        cropped_rect = self.postures[self.posture]
        cropped_image = image.subsurface(cropped_rect)
        # flipped_image = pygame.transform.flip(image, random.choice([True, False]), random.choice([True, False]))
        return cropped_image

    def affiche_png(self):
        self.w.window.blit(self.image, (self.position['x'], self.position['y']))

    def affiche_zone_png(self):
        pygame.draw.rect(self.w.window, (0, 150, 0), (self.position['x'], self.position['y'], 55, 125))

    def affiche_all(self):
        self.affiche_zone_png()
        self.affiche_png()

    def affiche(self):
        self.affiche_png()
