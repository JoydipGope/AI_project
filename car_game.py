import pygame
from pygame.locals import *
import random
import time

pygame.init()

WIDTH, HEIGHT = 500, 500
FPS = 120
ROAD_WIDTH = 300
MARKER_WIDTH = 10
LANE_WIDTH = 100
SPEED_INCREMENT = 1
INITIAL_SPEED = 2
MAX_VEHICLES = 5
GAME_DURATION = 60  

COLORS = {
    'gray': (100, 100, 100),
    'green': (76, 208, 56),
    'red': (200, 0, 0),
    'white': (255, 255, 255),
    'yellow': (255, 232, 0)
}


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Car Game')


LANES = [150, 250, 350]


def load_image(filename):
    try:
        return pygame.image.load(f'images/{filename}')
    except pygame.error as e:
        print(f"Error loading image: {filename} - {e}")
        return None


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (45, 45 * image.get_height() // image.get_width()))
        self.rect = self.image.get_rect(center=(x, y))

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = load_image('car.png')
        super().__init__(image, x, y)

class AICar(PlayerVehicle):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, vehicle_group):
       
        for vehicle in vehicle_group:
            if vehicle.rect.colliderect(self.rect):
                
                if self.rect.x == LANES[0]:  
                    if self.rect.x < LANES[1] and not any(v.rect.x == LANES[1] and v.rect.y > self.rect.y for v in vehicle_group):
                        self.rect.x = LANES[1]  
                elif self.rect.x == LANES[2]:  
                    if self.rect.x > LANES[1] and not any(v.rect.x == LANES[1] and v.rect.y > self.rect.y for v in vehicle_group):
                        self.rect.x = LANES[1]  
                else:  
                    if not any(v.rect.x == LANES[0] and v.rect.y > self.rect.y for v in vehicle_group):
                        self.rect.x = LANES[0]  
                    elif not any(v.rect.x == LANES[2] and v.rect.y > self.rect.y for v in vehicle_group):
                        self.rect.x = LANES[2]  

def main():
    clock = pygame.time.Clock()
    player = AICar(WIDTH // 2, HEIGHT - 100)
    player_group = pygame.sprite.Group(player)
    vehicle_group = pygame.sprite.Group()
    
    speed = INITIAL_SPEED
    score = 0
    gameover = False
    start_time = time.time()

    while True:
        clock.tick(FPS)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        if not gameover:
            
            if len(vehicle_group) < MAX_VEHICLES:
                lane = random.choice(LANES)
                vehicle_image = random.choice(['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png'])
                vehicle = Vehicle(load_image(vehicle_image), lane, -50)
                vehicle_group.add(vehicle)

            
            for vehicle in vehicle_group:
                vehicle.rect.y += speed
                if vehicle.rect.top > HEIGHT:
                    vehicle.kill()
                    score += 1
                    if score % 5 == 0:
                        speed += SPEED_INCREMENT

            
            player.move(vehicle_group)

            
            if pygame.sprite.spritecollideany(player, vehicle_group):
                gameover = True

        
        screen.fill(COLORS['green'])
        pygame.draw.rect(screen, COLORS['gray'], (100, 0, ROAD_WIDTH, HEIGHT))  # Draw the road
        vehicle_group.draw(screen)  
        player_group.draw(screen)  

        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, COLORS['white'])
        screen.blit(score_text, (10, 10))

        
        if gameover:
            game_over_text = font.render('Game Over!', True, COLORS['red'])
            screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
            pygame.display.flip()
            time.sleep(2)
            break

        pygame.display.flip()

        
        if elapsed_time > GAME_DURATION:
            break

    pygame.quit()
