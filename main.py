import math
import pygame 
pygame.init()

WIDTH, HEIGHT = 600,600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100, 149,237)
BLACK = (0,0,0)
RED = (188, 39, 50)
DARK_GREY = (80,78,81)

class Planet:
    AU = 149.6e6 * 1000 # to get into meters
    G = 6.67428e-11
    SCALE = 189/AU # 1Au = 100 pixels in our scale.
    TIMESTEP = 3600*24 # 1DAY in seconds


    def __init__(self,x,y,radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False
        self.distance_to_sun = 0 #for now
        self.orbit = [] 

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x,y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x **2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2 # straight line force
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
        
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:  
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0,0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10**24)
    mercury.y_vel = 47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = 35.02 * 1000

    planets = [sun, mars, earth, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)


        for planet in planets:
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()



main()



