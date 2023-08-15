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
        for spirit in game.player.spirit:
            spirit.bouton(event)
        for physique in game.player.physique:
            physique.bouton(event)

    game.comportement()
    for spirit in game.player.spirit:
        spirit.color = game.couleur_fond
    for terrain in game.terrain:
        terrain.affiche_terrain()
    for spirit in game.player.spirit:
        spirit.comportement()
    for physique in game.player.physique:
        physique.comportement()
    for stone in game.stone:
        stone.comportement()
    for arbre in game.arbre:
        arbre.comportement()
    for balle in game.balle:
        balle.comportement()

    pygame.display.flip()

    clock.tick(60)
