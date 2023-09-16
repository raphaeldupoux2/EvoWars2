import pygame
from game_instance import GameInstance

pygame.init()

game = GameInstance()
game.w.set_up()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.bouton(event)

    game.ordre_affiche()

    pygame.display.flip()
    clock.tick(60)
