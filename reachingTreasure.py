#Setting up the display.

import pygame

#Size of the screen
SCREEN_TITLE = "Test Scenario"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#Colors of the screen
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
clock = pygame.time.Clock() # generar el reloj del juego
pygame.font.init()
font = pygame.font.SysFont('comicsans',75)

class Game:
    TICK_RATE = 60 #Setear los fps con lo que va a correr el game.
    

    def __init__(self, title, image_path, width, height):
        self.title = title
        self.width = width
        self.height = height
        
        #Creating the window game screen, it uses a tuple of width and height
        self.game_screen = pygame.display.set_mode((width, height))
        #Setting the color of the screen
        self.game_screen.fill(WHITE_COLOR)
        #Setea el titulo de la ventana.
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image,(width,height))
        
    def run_game_loop(self):
        
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        enemy_0 = EnemyCharacter('enemy.png', 20, 400, 50 , 50)
        treasure = GameObject('treasure.png',375,50,50,50)
        while not is_game_over:
            
            for event in pygame.event.get(): #todos los eventos son KEYPRESS, MOUSECLICK, MOUSEMOVEMENT
                
                if event.type == pygame.QUIT: #LOS QUIT EVENTS SON UNA CONSTANTE DE PYGAME
                    is_game_over = True
                #Detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    #Move up if up key pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    #Move down if down key pressed    
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                    elif event.key == pygame.K_LEFT:
                        direction = 2
                    elif event.key == pygame.K_RIGHT:
                        direction = -2
                #detect when key is released
                elif event.type == pygame.KEYUP:
                    #Stop movement when key no longer pressed.
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or pygame.K_RIGHT or pygame.K_LEFT:
                        direction = 0
                    
                print(event)
                
            #Dibuja un rectangulo en la gamescreen del color que quiero en la pos que quiero con el width and height que quiero.
            #del x.0/y.0 se va a crear abajo derecha, por ender hay que retarle mitad de w y de h a la pos para que quede centrado.     
            ##pygame.draw.rect(game_screen, BLACK_COLOR,[350,350,100,100])
            ##pygame.draw.circle(game_screen, BLACK_COLOR,(400,300),50)

            #se comporta como el rectangulo, se pone aca porq tiene que refreshear su pos.
            #game_screen.blit(player_image,(375,375))

            #Redraw the screen to white.
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image,(0,0))
            treasure.draw(self.game_screen)
            
            #Update player position
            player_character.move(direction, self.height, self.width)
            #Draw the player at the new position
            player_character.draw(self.game_screen)

            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)
            
            if player_character.detectCollision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render("You lost...",True,BLACK_COLOR)
                self.game_screen.blit(text,(275,350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detectCollision(treasure):
                is_game_over = True
                did_win = True
                text = font.render("YOU WIN!!",True,BLACK_COLOR)
                self.game_screen.blit(text,(275,350))
                pygame.display.update()
                clock.tick(1)
                break
            
            pygame.display.update() #updatea el render del juego
            clock.tick(self.TICK_RATE) #Renderea el next frame

        if did_win:
            self.run_game_loop()
        else:
            return
        

#Generic game object class to be subclassed by other objects
class GameObject:


    def __init__(self, image_path, x, y, width, height):

        #importa la imagen al proyecto
        object_image = pygame.image.load(image_path)
        #le cambia el tamanio a la imagen. Escala la imagen 
        self.image = pygame.transform.scale(object_image,(width, height))
        
        self.xPos = x
        self.yPos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.xPos, self.yPos))

#Class to represent the character controlled by the player        
class PlayerCharacter(GameObject):
    #how many tiles the character moves per second
    SPEED = 6

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
    #Move function will move character up if direction > 0 and down if direction < 0
    def move(self, direction, max_height, max_width):

        if direction == 1:
            self.yPos -= self.SPEED
        elif direction == -1:
            self.yPos += self.SPEED
        elif direction == 2:
            self.xPos -= self.SPEED
        elif direction == -2:
            self.xPos += self.SPEED

        if self.yPos >= max_height - 55:
            self.yPos = max_height - 55
        elif self.yPos <= 0:
            self.yPos = 0

        if self.xPos >= max_width - 50:
            self.xPos = max_width - 50
        elif self.xPos <= 0:
            self.xPos = 0
    def detectCollision(self, otherBody):
       if self.yPos > otherBody.yPos + otherBody.height:
           return False
       elif self.yPos + self.height < otherBody.yPos:
            return False

       if self.xPos > otherBody.xPos + otherBody.width:
            return False
       elif self.xPos + self.width < otherBody.xPos:
            return False

       return True            

class EnemyCharacter(GameObject):
   
    SPEED = 6

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
        
    def move(self, max_width):
        if self.xPos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.xPos >= max_width - 70:
            self.SPEED = -abs(self.SPEED)
        self.xPos += self.SPEED



pygame.init() #inicializa el pygame.

new_game = Game(SCREEN_TITLE,'background.png',SCREEN_WIDTH,SCREEN_HEIGHT)
new_game.run_game_loop()
 
#Game loops, while loop that contains all of the game logic.
pygame.quit() #exit del programa
quit() #exit del programa
