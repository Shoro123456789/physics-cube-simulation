import math
import pygame
import sys

gravity_force = -9.81
mass = 1
acceleration = gravity_force
fps = 200

print(acceleration)

pygame.init()
screen_width = 1080
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

square_color = (255, 0, 0)
square_position = [200, 100]
square_size = 50

pygame.display.flip()

square_force = [0, -9.81]
square_acceleration = [(square_force[0]/mass), (square_force[1]/mass)]
square_velocity = [0, 0]
square_Ek = 0
metre = 100
friction_coefficient = 0
normal_force = 0

paused = False
debug_hidden = False
dragging = False
font = pygame.font.Font(None, 36)
last_frame_time = pygame.time.get_ticks()
last_mouse_time = pygame.time.get_ticks()
last_mouse_pos = pygame.mouse.get_pos()
mouse_strength = 0.5

while True:

    current_frame_time = pygame.time.get_ticks()
    delta_time = (current_frame_time - last_frame_time) / 1000.0  # convert to seconds
    last_frame_time = current_frame_time
    current_time = pygame.time.get_ticks()
    current_mouse_pos = pygame.mouse.get_pos()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_f:
                debug_hidden = not debug_hidden
            if event.key == pygame.K_w:
                square_force[1] += 1
                square_acceleration = [(square_force[0]/mass), (square_force[1]/mass)]
            if event.key == pygame.K_s:
                square_force[1] -= 1
                square_acceleration = [(square_force[0]/mass), (square_force[1]/mass)]
            if event.key == pygame.K_a:
                square_force[0] -= 1
                square_acceleration = [(square_force[0]/mass), (square_force[1]/mass)]
            if event.key == pygame.K_d:
                square_force[0] += 1
                square_acceleration = [(square_force[0]/mass), (square_force[1]/mass)]
            if event.key == pygame.K_r:
                square_force[0] = 0
                square_force[1] = 0
                square_acceleration = [(square_force[0]/mass), (square_force[1]/mass)]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(square_position[0], square_position[1], square_size, square_size).collidepoint(event.pos):
                dragging = True
                previous_pos = pygame.mouse.get_pos()
                previous_time = pygame.time.get_ticks()

                curr_time = pygame.time.get_ticks()
                curr_pos = pygame.mouse.get_pos()
                square_position = [max(0, min(curr_pos[0], screen_width - square_size)), max(0, min(curr_pos[1], screen_height - square_size))]


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False




    if not paused:
        if square_position[0] + square_size > screen_width:
            square_position[0] = screen_width - square_size
            square_velocity[0] = -0.5*square_velocity[0]
        if square_position[1] + square_size > screen_height:
            square_velocity[1] = -0.5*square_velocity[1]
            square_position[1] = screen_height - square_size

        if square_position[0] < 0:
            square_position[0] = 0
            square_velocity[0] = -0.5 * square_velocity[0]
        if square_position[1] < 0:
            square_position[1] = 0
            square_velocity[1] = -0.5 * square_velocity[1]

        screen.fill((0, 0, 0))

        square_Ek= (math.sqrt(square_velocity[0]*square_velocity[0] + square_velocity[1]*square_velocity[1])**2)*0.5*mass
        square_acceleration = [(square_force[0]/mass), (square_force[1]/mass)]

    square_velocity[0] += square_acceleration[0] * delta_time
    square_velocity[1] -= square_acceleration[1] * delta_time
    square_position[0] += square_velocity[0] * delta_time * metre
    square_position[1] += square_velocity[1] * delta_time * metre


    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        square_position = [max(0, min(mouse_x, screen_width - square_size)), max(0, min(mouse_y, screen_height - square_size))]

        if current_time - last_mouse_time >= delta_time:
            mouse_velocity = (current_mouse_pos[0] - last_mouse_pos[0], current_mouse_pos[1] - last_mouse_pos[1])
            last_mouse_time = current_time
            last_mouse_pos = current_mouse_pos
            square_velocity[0] = mouse_velocity[0]
            square_velocity[1] = mouse_velocity[1]


    # Draw the square
    pygame.draw.rect(screen, square_color, (square_position[0], square_position[1], square_size, square_size))
    square_rect = pygame.Rect(square_position[0], square_position[1], square_size, square_size)



    if not debug_hidden:
        velocity_text = font.render(f"Vx: {square_velocity[0]:.2f}, Vy: {square_velocity[1]:.2f}", True, (255, 255, 255))
        acceleration_text = font.render(f"ax: {square_acceleration[0]:.2f}, ay: {square_acceleration[1]:.2f}", True, (255, 255, 255))
        force_text = font.render(f"Fx: {square_force[0]:.2f}, Fy: {square_force[1]:.2f}", True, (255, 255, 255))
        Ek_text = font.render(f"Ek: {square_Ek:.2f}", True, (255, 255, 255))

        screen.blit(velocity_text, (10, 70))
        screen.blit(acceleration_text, (10, 40))
        screen.blit(force_text, (10, 10))
        screen.blit(Ek_text, (10, 100))


    pygame.display.flip()
    pygame.time.Clock().tick(fps)