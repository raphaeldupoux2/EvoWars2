import pygame


class PygameSetUp:
    _instance = None  # Instance partagée

    def __new__(cls, width, height, title):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            pygame.init()

            cls._instance.width = width
            cls._instance.height = height
            cls._instance.title = title

            cls._instance.window = cls._instance.window_dimension(width, height)
            cls._instance.window_title(title)

            cls._instance.surface_fenetre1 = pygame.Surface((800, 720))
            cls._instance.surface_fenetre2 = pygame.Surface((200, 720))

            cls._instance.clock = pygame.time.Clock()
            cls._instance.fps = 60

        return cls._instance

    def window_title(self, title):
        return pygame.display.set_caption(title)

    def window_dimension(self, width, height):
        return pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def window_refresh(self):
        return pygame.display.flip()

    def fps_control(self):
        self.clock.tick(self.fps)


pygame_params = PygameSetUp(1000, 720, "FullStratFightTactic")
