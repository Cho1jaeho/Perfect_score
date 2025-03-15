import pygame
import sys
import setting as s
import db
import hashlib
from gameplay import game_menu

# 로그인, 회원가입
def sign():
    
    menu_items = ["Sign In", "Sign Up"]
    while True:
        text_main = s.font_main.render("PERFECT SCORE", True, s.settings.font_color)
        s.screen.blit(s.background_image, (0, 0))
        s.screen.blit(text_main, (s.SCREEN_WIDTH // 2 - 200, 100))
        
        for i, item in enumerate(menu_items):
            text = s.font.render(item, True, s.settings.font_color)
            text_rect = text.get_rect(center=(s.SCREEN_WIDTH // 2, 300 + i * 100))
            s.screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, item in enumerate(menu_items):
                    text_rect = s.font.render(item, True, s.settings.font_color).get_rect(center=(s.SCREEN_WIDTH // 2, 300 + i * 100))
                    if text_rect.collidepoint(mouse_pos):
                        if i == 0:
                            sign_in()
                        elif i == 1:
                            sign_up()

def sign_in():
    
    menu_items = ["id: ", "pw: "]
    # 입력 필드 생성
    input_boxes = [s.InputField(s.SCREEN_WIDTH // 2 - 70, 300 - 16, 140, 32),
                   s.InputField(s.SCREEN_WIDTH // 2 - 70, 400 - 16, 140, 32)]

    # 게임 루프
    while True:
        text_main = s.font_main.render("PERFECT SCORE", True, s.settings.font_color)
        s.screen.blit(s.background_image, (0, 0))
        s.screen.blit(text_main, (s.SCREEN_WIDTH // 2 - 200, 100))
        
        sign_text = s.font.render("Sign In", True, s.settings.font_color)
        sign_rect = sign_text.get_rect(center=(s.SCREEN_WIDTH // 2, 600))
        s.screen.blit(sign_text, sign_rect)
        
        back_text = s.font.render("Back", True, s.settings.font_color)
        back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
        s.screen.blit(back_text, back_rect)
        
        for i, item in enumerate(menu_items):
            text = s.font.render(item, True, s.settings.font_color)
            text_rect = text.get_rect(center=(s.SCREEN_WIDTH // 2 - 150, 300 + i * 100))
            input_boxes[i].draw(s.screen)
            s.screen.blit(text, text_rect)
    
        signed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_rect.collidepoint(mouse_pos):
                    return
                if sign_rect.collidepoint(mouse_pos):
                    # users 테이블과 비교하는 로직(일치하는 id, pw가 있으면 로그인 성공.)
                    conn = db.connect_to_database()
                    cursor = conn.cursor()
                    hashed = hashlib.sha256(input_boxes[1].text.encode('utf-8')).hexdigest()
                    query = "SELECT id, username, email FROM users WHERE id = %s AND password_hash = %s"
                    cursor.execute(query, (input_boxes[0].text, hashed))
                    result = cursor.fetchone()
                    signed = result is not None
                    if signed:
                        iid, name, email = result
                        
                        s.current_player.put(iid, name, email)
                        
                        cursor.close()
                        conn.close()
                        game_menu()
                    

        pygame.display.flip()

def sign_up():
    menu_items = ["id: ", "pw: ", "name: ", "email: "]
    
    # 입력 필드 생성
    input_boxes = [s.InputField(s.SCREEN_WIDTH // 2 - 70, 300 - 16, 140, 32), #id
                   s.InputField(s.SCREEN_WIDTH // 2 - 70, 350 - 16, 140, 32), #pw
                   s.InputField(s.SCREEN_WIDTH // 2 - 70, 400 - 16, 140, 32), #name
                   s.InputField(s.SCREEN_WIDTH // 2 - 70, 450 - 16, 140, 32)] #email
    
    # 게임 루프
    while True:
        text_main = s.font_main.render("PERFECT SCORE", True, s.settings.font_color)
        s.screen.blit(s.background_image, (0, 0))
        s.screen.blit(text_main, (s.SCREEN_WIDTH // 2 - 200, 100))
        
        sign_text = s.font.render("Sign Up", True, s.settings.font_color)
        sign_rect = sign_text.get_rect(center=(s.SCREEN_WIDTH // 2, 600))
        s.screen.blit(sign_text, sign_rect)
        
        back_text = s.font.render("Back", True, s.settings.font_color)
        back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
        s.screen.blit(back_text, back_rect)
        
        for i, item in enumerate(menu_items):
            text = s.font.render(item, True, s.settings.font_color)
            text_rect = text.get_rect(center=(s.SCREEN_WIDTH // 2 - 150, 300 + i * 50))
            input_boxes[i].draw(s.screen)
            s.screen.blit(text, text_rect)
    
        
        sign_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_rect.collidepoint(mouse_pos):
                    return
                if sign_rect.collidepoint(mouse_pos):   # 회원가입 버튼 클릭 시
                    # 아이디 중복 검사(일치하는 id 정보가 없으면 result는 None이 돼서 회원가입을 할 수 있게 됨)
                    conn = db.connect_to_database()
                    cursor = conn.cursor()
                    query = "SELECT id FROM users WHERE id = %s or username = %s"
                    cursor.execute(query, (input_boxes[0].text, input_boxes[2].text))
                    result = cursor.fetchone()
                    
                    sign_up = result is None
                    if sign_up:
                        # users 테이블에 아이디, 비번, 닉네임, 이메일 저장
                        query = """
                        INSERT INTO users (id, password_hash, username, email)
                        VALUES (%s, %s, %s, %s)
                        """
                        hashed = hashlib.sha256(input_boxes[1].text.encode('utf-8')).hexdigest()
                        cursor.execute(query, (input_boxes[0].text, hashed, input_boxes[2].text, input_boxes[3].text))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        return
        
        pygame.display.flip()

    