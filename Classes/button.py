import pygame

screen = pygame.display.set_mode()

class Button():
    def __init__(self, rect, image, anim, text, text_size, func, parameter = None):
        self.rect = rect
        self.image = image
        self.anim = anim
        self.text = text
        self.text_size = text_size
        self.func = func
        self.parameter = parameter
        self.hovered = False

    def render_text(self):
        if self.text != "":
            police = pygame.font.Font('prstart.ttf', self.text_size)
            text = police.render(self.text,1,(255,255,255))
            text_shadow = police.render(self.text,1,(50,50,50))
            pos = (self.rect.center[0] - text.get_rect()[2] / 2, self.rect.center[1] - text.get_rect()[3] / 2)
            screen.blit(text_shadow, (pos[0] + 5, pos[1] + 5))
            screen.blit(text, pos)

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_click(event)
        self.is_hovered()
        self.update()

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            if self.parameter is None:
                self.func()
            else:
                self.func(self.parameter)

    def is_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
        else:
            self.hovered = False

    def update(self):
        if not self.hovered:
            screen.blit(self.image, self.rect)
        if self.hovered:
            screen.blit(self.anim, self.rect)
        self.render_text()
