import pygame

pygame.init()

class Button():
    def __init__(self, image, hovering_image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.hovering_image = hovering_image
        self.width = image.get_width() if image else 0
        self.height = image.get_height() if image else 0
        self.hovering = False
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        
        if self.image is not None and self.hovering_image is not None:
             self.hover_rect = pygame.Rect(self.x - self.width//2, (self.y - self.height//2) + 1, self.width, self.height)
        else:
            self.hover_rect = self.text.get_rect(center=(self.x, self.y))
        
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def update(self, screen):
        if self.image is not None and self.hovering != True:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        if self.hovering_image is not None and self.hovering == True:
                screen.blit(self.hovering_image, self.hover_rect)
    
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position, screen):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.hovering = True
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.hovering = False
            screen.blit(self.image, self.rect)
            

