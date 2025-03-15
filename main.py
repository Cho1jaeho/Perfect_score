import pygame
from sign import sign
import setting as s

def main():
    
    pygame.init()
    # 화면 크기 설정
    s.SCREEN_WIDTH = 1280
    s.SCREEN_HEIGHT = 720
    s.screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
    pygame.display.set_caption("perfect score")

    # 폰트 설정
    s.font = pygame.font.SysFont(None, 36)
    s.font_main = pygame.font.Font("title_ttf\Giants-inline.ttf", 50)
    
    s.WHITE = (255, 255, 255)
    s.BLACK = (0, 0, 0)
    
    #배경 설정
    s.background_image = pygame.image.load("background.jpg")
    
    # 노래 목록
    s.songs = {
        "humidifier": ['splt/gaseupgi/vocals.wav', 'splt/gaseupgi/accompaniment.wav', 'data/gaseupgi.mp3'],
        "a story of star and dream": ['splt/별과꿈의이야기/vocals.wav', 'splt/별과꿈의이야기/accompaniment.wav', 'data/별과꿈의이야기.mp3'],
        "lamborgini": ['splt/lamborgini/vocals.wav', 'splt/lamborgini/accompaniment.wav', 'data/lamborgini.mp3'],
        "miss you": ['splt/보고싶다/vocals.wav', 'splt/보고싶다/accompaniment.wav', 'data/보고싶다.mp3'],
        #test
        "test": ['data/test_A_piano.mp3', 'data/test_A_piano.mp3', 'data/test_A_piano.mp3']
    }
    # 로그인/회원가입 화면으로 시작
    sign()

if __name__ == '__main__':
    main()