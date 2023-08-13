import pygame
import time
from game_instance import GameInstance
from projectile import Projectile


pygame.init()

game = GameInstance()
game.window.set_up()
projectile_move = False
direction = 0

running = True

compteur = 0
while running:
    start_time = time.monotonic()  # Mesure du temps de début de boucle
    compteur += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for spirit in game.player.spirit:
            spirit.bouton(event)
        for physique in game.player.physique:
            physique.bouton(event)

    game.couleur_fond, game.assombrir = game.luminosite_tournante(couleur_fond=game.couleur_fond, vitesse_changement=1, assombrir=game.assombrir)

    for spirit in game.player.spirit:
        spirit.color = game.couleur_fond

    game.window.window.fill(game.couleur_fond)

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
    game.projectile.affiche_skin()

    # x, y = 500, 500
    # pygame.draw.circle(game.window.window, (255, 0, 0), (x, y), 7, 1)

    if game.player.physique[0].point_dans_rectangle_incline(game.projectile.x, game.projectile.y, game.player.physique[0].rotated_rect.centerx, game.player.physique[0].rotated_rect.centery, 30, 100, -game.player.physique[0].arme_degree_r(game.player.physique[0].direction) + 90):
        # print(game.player.physique[0].arme_degree_r(game.player.physique[0].curseur))
        game.player.physique[0].color = (255, 0, 0)
        projectile_move = True
        direction = game.player.physique[0].arme_degree_r(game.player.physique[0].curseur)

    else:
        game.player.physique[0].color = (50, 50, 90)

    if projectile_move:
        game.projectile.move_to(direction)

    pygame.display.flip()

    # Mesure FPS
    end_time = time.monotonic()  # Mesure du temps de fin de boucle
    elapsed_time = end_time - start_time  # Calcul du temps écoulé depuis le début de la boucle
    time_to_wait = game.FRAME_DURATION - elapsed_time  # Calcul du temps d'attente avant la prochaine frame
    # print(time_to_wait)
    if time_to_wait > 0:  # Si le temps d'attente est positif, on attend ce temps
        time.sleep(time_to_wait)
