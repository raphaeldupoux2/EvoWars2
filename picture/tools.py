import pygame


class Tools:
    @staticmethod
    def changer_couleur_image_and_save_it(image, r=0, g=0, b=0):
        """

        :param image: pygame.image.load("image.png")
        :param r:
        :param g:
        :param b:
        :return:
        """
        # Créer une copie modifiable de l'image
        modified_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)  # Utiliser SRCALPHA pour la transparence
        # Parcourir tous les pixels de l'image et ajuster les couleurs
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                pixel_color = image.get_at((x, y))

                # Saturer le rouge et ajuster le vert pour obtenir une teinte de marron
                new_r = max(0, min(255, pixel_color.r + r))  # Augmenter la valeur rouge
                new_g = max(0, min(255, pixel_color.g + g))  # Diminuer la valeur verte
                new_b = max(0, min(255, pixel_color.b + b))  # Diminuer la valeur bleue

                new_color = (new_r, new_g, new_b, pixel_color.a)
                modified_image.set_at((x, y), new_color)

        pygame.image.save(modified_image, "picture/new.png")

        return modified_image
