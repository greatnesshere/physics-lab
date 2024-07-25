import pygame
import math

# Pygame initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elastic Collision Simulator")

# Clock for controlling FPS
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, radius, mass, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.velocity = velocity

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def bounce(self):
        if self.x > WIDTH - self.radius:
            self.velocity[0] = -self.velocity[0]
            self.x = WIDTH - self.radius
        elif self.x < self.radius:
            self.velocity[0] = -self.velocity[0]
            self.x = self.radius
        
        if self.y > HEIGHT - self.radius:
            self.velocity[1] = -self.velocity[1]
            self.y = HEIGHT - self.radius
        elif self.y < self.radius:
            self.velocity[1] = -self.velocity[1]
            self.y = self.radius

    def check_collision(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.radius + other.radius:
            # Elastic collision: calculate new velocities
            dvx = other.velocity[0] - self.velocity[0]
            dvy = other.velocity[1] - self.velocity[1]
            dvdotdr = dx * dvx + dy * dvy
            distance_square = dx**2 + dy**2
            
            # Update velocities based on elastic collision equations
            self.velocity[0] += (2 * other.mass / (self.mass + other.mass)) * (dvdotdr * dx / distance_square)
            self.velocity[1] += (2 * other.mass / (self.mass + other.mass)) * (dvdotdr * dy / distance_square)
            
            other.velocity[0] -= (2 * self.mass / (self.mass + other.mass)) * (dvdotdr * dx / distance_square)
            other.velocity[1] -= (2 * self.mass / (self.mass + other.mass)) * (dvdotdr * dy / distance_square)

# Initialize two balls
ball1 = Ball(100, 300, 20, 1, (255, 0, 0), [2, 0])
ball2 = Ball(700, 300, 30, 2, (0, 0, 255), [-2, 0])

# Main simulation loop
running = True
while running:
    screen.fill(BLACK)  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update balls
    ball1.move()
    ball1.bounce()
    ball2.move()
    ball2.bounce()

    # Check for collision
    ball1.check_collision(ball2)

    # Draw balls
    ball1.draw()
    ball2.draw()

    pygame.display.flip()  # Update display
    clock.tick(60)  # Cap FPS

pygame.quit()  # Quit Pygame
