import pygame
from random import randint

class COIN_n_MONSTER_fall:
    def __init__(self) -> None:
        pygame.init()
#        self.starting_menue()
        self.load_images()
        self.to_left = False
        self.to_right = False
        self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode((640, self.height + self.lives.get_height() + 15))
        self.new_game()
        self.font = pygame.font.SysFont("Arial", 24)
        self.font2 = pygame.font.SysFont("Fixedsys Regular", 40)
        self.font3 = pygame.font.SysFont("Terminal", 15) 
        self.font4 = pygame.font.SysFont("Castellar Regular", 60)
        self.x = 0
        self.y = self.height-self.robot.get_height()
        self.clock = pygame.time.Clock()
        self.main_loop()



    def load_images(self):
        self.lives = pygame.image.load("door.png")
        self.robot = pygame.image.load("robot.png")
        self.coin = pygame.image.load("coin.png")
        self.monster = pygame.image.load("monster.png")

    def new_game(self):
        self.points = 0
        self.health = 3
        self.number = 5
        self.x = 0
        self.positions = []
        is_monster = False
        r = randint(1, self.number)
        for i in range(1,self.number+1):
            if r == i:
                is_monster = True
            self.positions.append([randint(0,self.width-self.coin.get_width()),-randint(100,1000), is_monster])
            is_monster = False
        

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.clock.tick(60)


    def draw_window(self):
        if self.health <= 0:
            self.end_panal()
            return

        self.screen.fill((25, 0, 51))
        self.screen.blit(self.robot, (self.x, self.y))


        for i in range(self.number):
            if self.positions[i][2]:
                self.screen.blit(self.monster, (self.positions[i][0], self.positions[i][1]))
                continue
            self.screen.blit(self.coin, (self.positions[i][0], self.positions[i][1]))
    
        text = self.font.render("Points: "+str(self.points), True, (255, 255, 250))
        esc = self.font2.render("ESC to exit", True, (0, 51, 51))
        mons = self.font3.render("MONSTERS take a life but they give 10 points", True,(0, 9,0))

        self.screen.blit(text, (self.width-110, 10))
        pygame.draw.rect(self.screen, (160, 160, 160), (0, self.height, 640, 90))
        for i in range(self.health):
            self.screen.blit(self.lives,(20 * i, self.height + 5))
        pygame.draw.rect(self.screen, (160, 160, 160), (0, self.height, 640, 18))
        self.screen.blit(esc, (200, self.height + 40))
        self.screen.blit(mons, (20, self.height + 70))
        self.screen.blit(mons, (mons.get_width() + 100, self.height + 70))
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: 
                    x,y = pygame.mouse.get_pos()
                    self.starting_menue(x,y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_LSHIFT:
                    self.new_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
    
            if event.type == pygame.QUIT:
                exit()
        
        self.movement(self.to_left, self.to_right)
    
    def end_panal(self):
        text = self.font.render("Points: "+str(self.points), True, (255, 255, 250))
        lost = self.font4.render("GAME OVER!!!", True, (255, 255, 255))
        self.screen.fill((51,0,25))
        width_middle = self.width/2 - lost.get_width()/2
        height_middle = self.height/2 - lost.get_height()/2
        self.screen.blit(lost, (width_middle, height_middle))
        self.screen.blit(self.coin, (width_middle + 120, height_middle + 100))
        self.screen.blit(text, (self.width/2 - text.get_width()/2, height_middle + 200))
        pygame.display.flip()


    def movement(self, to_left, to_right):
        if to_left:
            self.x-= 2
        if to_right:
            self.x+=2

        if self.x + self.robot.get_width() <= 0:
            self.x = 630 
        if self.x >= self.width:
            self.x = -self.robot.get_width()
        
        for i in range(self.number):
            self.positions[i][1] += 1
            if self.health <= 0:
                break
            if self.positions[i][1] >= self.height:
                if self.positions[i][2]:
                    self.positions[i][0] = randint(0,self.width-self.monster.get_width())
                    self.positions[i][1] = -randint(100,1000)
                else:
                    self.positions[i][0] = randint(0,self.width-self.coin.get_width())
                    self.positions[i][1] = -randint(100,1000)
                    self.health -= 1
            if self.positions[i][2]:
                if self.positions[i][1] + self.monster.get_height() >= self.y:
                    robot_middle = self.x+self.robot.get_width()/2
                    monster_middle = self.positions[i][0]+self.monster.get_width()/2
                    if abs(robot_middle-monster_middle) <= (self.robot.get_width()+self.monster.get_width())/2:
                        self.health-= 1
                        self.positions[i][0] = randint(0,self.width-self.monster.get_width())
                        self.positions[i][1] = -randint(100,1000)
                        self.points += 10
            if self.positions[i][1]+self.coin.get_height() >= self.y:
                robot_middle = self.x+self.robot.get_width()/2
                coin_middle = self.positions[i][0]+self.coin.get_width()/2
                if abs(robot_middle-coin_middle) <= (self.robot.get_width()+self.coin.get_width())/2:
                    # the robot caught an asteroid
                    self.positions[i][0] = randint(0,self.width-self.coin.get_width())
                    self.positions[i][1] = -randint(100,1000)
                    self.points += 1



d = COIN_n_MONSTER_fall()
