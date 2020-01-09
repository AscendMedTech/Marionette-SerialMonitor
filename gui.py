from Comm import Comm
import pygame

width, height = 500, 500

# a list of coordinates that are evenly split into quadrants
positions = [[width * .25, height * .25], [width * .75, height * .25],
             [width * .25, height * .75], [width * .75, height * .75]]

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Deflection Results')

font = pygame.font.Font(pygame.font.get_default_font(), 32)

ser = Comm('COM5', 9600)

done = False

# creates texts objects that can be displayed py pygame
def createText(messages, font, positions):
    texts = []
    x = 0
    for msg in messages:
        text = font.render(str(msg), True, (50, 50, 0))
        textRect = text.get_rect()
        textRect.center = (positions[x][0], positions[x][1])
        texts.append([text, textRect])
        x += 1
    return texts

# creates an array of posiitons for the label text
label_positions = []
for pos in positions:
    label_positions.append([pos[0], pos[1] - 50])
# creates text objects that are displayable by pygame for the labels
labels = createText(['X Steps', 'Y Steps', 'X Inches', 'Y Inches'], font,
                    label_positions)

while not done:
    screen.fill((255, 255, 255)) # blank the screen at the beggining of every frame
    msg = ser.recieve_steps()
    if msg != None:
        texts = createText(msg, font, positions)
    else:
        # when the program is first starting up it's
        # sometimes possible for ser.recieve_steps() to return None
        texts = createText(['1', '2', '3', '4'], font, positions)
    
    #display the text arrays
    for text in texts:
        screen.blit(text[0], text[1])
    for label in labels:
        screen.blit(label[0], label[1])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.flip() # show the new frame
