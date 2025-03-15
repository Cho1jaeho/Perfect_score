import pygame

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
screen = None
font = None
font_main = None
background_image = None
current_player = None
songs = {}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class InputField:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 사용자가 입력 필드 내부를 클릭하면 활성화 상태 토글
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WHITE if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # 텍스트 다시 렌더링
                self.txt_surface = font.render(self.text, True, self.color)

    def draw(self, screen):
        # 입력 필드 텍스트 렌더링 및 배경 그리기
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class GameSettings:
    def __init__(self):
        self.font_color = WHITE  # 초기 색상은 흰색

    def toggle_font_color(self):
        # 색상 변경
        self.font_color = BLACK if self.font_color == WHITE else WHITE

class Player:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.email = None
        # 추가적으로 필요한 속성을 여기에 선언할 수 있습니다.
    def put(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

settings = GameSettings()
current_player = Player()