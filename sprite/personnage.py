import pygame


class AffichePlayer:
    def __init__(self, window, x, y):
        self.w = window
        self.x = x
        self.y = y
        self.largeur, self.longueur = 250, 125
        self.image_path = "picture/personnage.png"
        self.image = self.load_image()

    def changer_couleur_image(self, image):
        # Créer une copie modifiable de l'image
        modified_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)  # Utiliser SRCALPHA pour la transparence
        # Parcourir tous les pixels de l'image et ajuster les couleurs
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))

                # Saturer le rouge et ajuster le vert pour obtenir une teinte de marron
                new_r = pixel_color.b - 0  # min(255, pixel_color.r + 0)  # Augmenter la valeur rouge
                new_g = pixel_color.g + 0  # max(0, pixel_color.g - 100)  # Diminuer la valeur verte
                new_b = pixel_color.b - 0  # max(0, pixel_color.b - 100)  # Diminuer la valeur bleue

                new_color = (new_r, new_g, new_b, pixel_color.a)
                modified_image.set_at((x, y), new_color)
        return modified_image

    def save_image(self, modified_image):
        # Enregistrer l'image modifiée
        modified_image_path = "picture/personnage_marron.png"
        self.image_path = modified_image_path
        pygame.image.save(modified_image, modified_image_path)

    def load_image(self):
        image_origin = pygame.image.load(self.image_path).convert_alpha()
        image = pygame.transform.scale(image_origin, (self.largeur, self.longueur))
        modified_image = self.changer_couleur_image(image)
        self.save_image(modified_image)
        cropped_rect = pygame.Rect(0, 0, 70, 125)
        cropped_image = modified_image.subsurface(cropped_rect)
        # flipped_image = pygame.transform.flip(image, random.choice([True, False]), random.choice([True, False]))
        return cropped_image

    def affiche_png(self):
        self.w.window.blit(self.image, (self.x, self.y))

    def affiche_zone_png(self):
        pygame.draw.rect(self.w.window, (0, 150, 0), (self.x, self.y, 70, 125))

    def comportement(self):
        self.affiche_png()
