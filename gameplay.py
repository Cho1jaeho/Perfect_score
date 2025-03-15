import pygame
import librosa
import sys
import dlib
import cv2
import pyaudio
import numpy as np
import setting as s
import data_analyze
import db

# 게임 메뉴
def game_menu():
    
    menu_items = ["Start Game", "Options", "Exit"]
    while True:
        text_main1 = s.font_main.render("PERFECT SCORE", True, s.settings.font_color)
        s.screen.blit(s.background_image, (0, 0))
        s.screen.blit(text_main1, (s.SCREEN_WIDTH // 2 - 200, 100))
        
        for i, item in enumerate(menu_items):
            text = s.font.render(item, True, s.settings.font_color)
            text_rect = text.get_rect(center=(s.SCREEN_WIDTH // 2, 300 + i * 50))
            s.screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, item in enumerate(menu_items):
                    text_rect = s.font.render(item, True, s.settings.font_color).get_rect(center=(s.SCREEN_WIDTH // 2, 300 + i * 50))
                    if text_rect.collidepoint(mouse_pos):
                        if i == 0:
                            select_song()
                        elif i == 1:
                            options_menu()
                        elif i == 2:
                            pygame.quit()
                            sys.exit()

# 노래 선택 메뉴
def select_song():
    s.screen.blit(s.background_image, (0, 0))
    text_main = s.font_main.render("Select a Song", True, s.settings.font_color)
    s.screen.blit(text_main, (s.SCREEN_WIDTH // 2 - 180, 100))
    
    song_rects = []
    for i, song in enumerate(s.songs.keys()):
        text = s.font.render(song, True, s.settings.font_color)
        rect = text.get_rect(center=(s.SCREEN_WIDTH // 2, 300 + i * 50))
        song_rects.append((rect, song))
        s.screen.blit(text, rect)
        
    # 'Back to Menu' 버튼 추가
    back_text = s.font.render("Back to Menu", True, s.settings.font_color)
    back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
    s.screen.blit(back_text, back_rect)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 'Back to Menu' 버튼 클릭 검사
                if back_rect.collidepoint(mouse_pos):
                    game_menu()  # 메인 메뉴로 돌아가기
                    return
                for rect, song_name in song_rects:
                    if rect.collidepoint(mouse_pos):
                        start_game(s.songs[song_name][0], s.songs[song_name][1], s.songs[song_name][2], song_name)
                        return  # 노래 선택 후 게임 메뉴로 돌아가지 않도록

# 옵션 메뉴
def options_menu():
    while True:
        s.screen.blit(s.background_image, (0, 0))
        option_text = s.font_main.render("Option", True, s.settings.font_color)
        s.screen.blit(option_text, (s.SCREEN_WIDTH // 2 - 80, 100))

        change_color_text = s.font.render("Change Font Color", True, s.settings.font_color)
        change_color_rect = change_color_text.get_rect(center=(s.SCREEN_WIDTH // 2, 300))
        s.screen.blit(change_color_text, change_color_rect)
        
        friends_text = s.font.render("Friends", True, s.settings.font_color)
        friends_rect = friends_text.get_rect(center=(s.SCREEN_WIDTH // 2, 350))
        s.screen.blit(friends_text, friends_rect)
        
        join_text = s.font.render("Join", True, s.settings.font_color)
        join_rect = join_text.get_rect(center=(s.SCREEN_WIDTH // 2, 400))
        s.screen.blit(join_text, join_rect)
        
        back_text = s.font.render("Back to Menu", True, s.settings.font_color)
        back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
        s.screen.blit(back_text, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if change_color_rect.collidepoint(mouse_pos):
                    # 색상 변경
                    s.settings.toggle_font_color()
                if friends_rect.collidepoint(mouse_pos):
                    friends()
                if join_rect.collidepoint(mouse_pos):
                    join()
                if back_rect.collidepoint(mouse_pos):
                    return  # 옵션 메뉴에서 메인 메뉴로 돌아가기
def friends():
    s.screen.blit(s.background_image, (0, 0))
    friends_text = s.font_main.render("Friends", True, s.settings.font_color)
    s.screen.blit(friends_text, (s.SCREEN_WIDTH // 2 - 80, 100))
    
    back_text = s.font.render("Back to Menu", True, s.settings.font_color)
    back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
    s.screen.blit(back_text, back_rect)
    
    request_text = s.font.render("Request", True, s.settings.font_color)
    request_rect = request_text.get_rect(center=(50, 50))
    s.screen.blit(request_text, request_rect)
    
    friends2_text = s.font.render("Friends", True, s.settings.font_color)
    friends2_rect = friends2_text.get_rect(center=(50, 300))
    s.screen.blit(friends2_text, friends2_rect)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            conn = db.connect_to_database()
            cursor = conn.cursor()
            query = """
            SELECT u.username
            FROM users u
            JOIN friends f ON (u.id = f.user_id)
            WHERE f.status = 'pending'
            """
            cursor.execute(query, ())
            result = cursor.fetchall()
            
            rects = []
            for idx, nickname in enumerate(result):
                text = s.font.render(f"{nickname}", True, s.settings.font_color)
                rect = text.get_rect(center=(50, 80 + idx * 30))
                rects.append((rect, nickname))
                s.screen.blit(text, rect)
                
            query = """
            SELECT u.username
            FROM users u
            JOIN friends f ON (u.id = f.user_id)
            WHERE f.status = 'accepted'
            """
            cursor.execute(query, ())
            result = cursor.fetchall()
            
            for idx, nickname in enumerate(result):
                text2 = s.font.render(f"{nickname}", True, s.settings.font_color)
                rect2 = text2.get_rect(center=(50, 330 + idx * 30))
                s.screen.blit(text2, rect2)
            
            cursor.close()
            conn.close()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for req, nickname in rects:
                    if req.collidepoint(mouse_pos):   # 친구 수락
                        conn = db.connect_to_database()
                        cursor = conn.cursor()
                        query = """
                        UPDATE friends
                        SET status = 'accepted'
                        WHERE (user_id = (SELECT id FROM users WHERE username = %s))
                        """
                        cursor.execute(query, (nickname,))
                        conn.commit()
                        query = """
                        insert into friends(user_id, friend_user_id, status)
                        values (%s, (select id from users where username = %s), %s)
                        """
                        cursor.execute(query, (s.current_player.user_id, nickname, "accepted"))
                        conn.commit()
                        cursor.close()
                        conn.close()
                if back_rect.collidepoint(mouse_pos):
                    return
        pygame.display.flip()
    
def join():
    s.screen.blit(s.background_image, (0, 0))
    join_text = s.font_main.render("Join", True, s.settings.font_color)
    s.screen.blit(join_text, (s.SCREEN_WIDTH // 2 - 80, 100))
    
    back_text = s.font.render("Back to Menu", True, s.settings.font_color)
    back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
    s.screen.blit(back_text, back_rect)
    
    request_text = s.font.render("Request", True, s.settings.font_color)
    request_rect = request_text.get_rect(center=(s.SCREEN_WIDTH // 2, 600))
    s.screen.blit(request_text, request_rect)
    
    id_input = s.InputField(s.SCREEN_WIDTH // 2 - 70, 300 - 16, 140, 32)
    
    id_text = s.font.render("Id", True, s.settings.font_color)
    id_rect = id_text.get_rect(center=(s.SCREEN_WIDTH // 2 - 150, 300))
    s.screen.blit(id_text, id_rect)
    id_input.draw(s.screen)
    
    feedback_text = ''  # 피드백 메시지 초기화

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            id_input.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return  # 메뉴로 돌아가기

                if request_rect.collidepoint(event.pos):
                    try:
                        conn = db.connect_to_database()
                        cursor = conn.cursor()
                        # 입력한 id가 실제로 users 테이블에 존재하는지 확인
                        query = "SELECT id FROM users WHERE id = %s"
                        cursor.execute(query, (id_input.text,))
                        result = cursor.fetchone()
                        
                        if result:
                            # 이미 친구 상태인지 확인
                            query = "SELECT * FROM friends WHERE user_id = %s AND friend_user_id = %s AND status = 'accepted'"
                            cursor.execute(query, (s.current_player.user_id, id_input.text))
                            result = cursor.fetchone()
                            if result:
                                feedback_text = 'Already friends.'
                            else:
                                query = "INSERT INTO friends (user_id, friend_user_id, status) VALUES (%s, %s, 'pending')"
                                cursor.execute(query, (s.current_player.user_id, id_input.text))
                                conn.commit()
                                feedback_text = 'Friend request sent.'
                        else:
                            feedback_text = 'User not found.'
                    except Exception as e:
                        feedback_text = str(e)
                    finally:
                        cursor.close()
                        conn.close()

        # 상태 메시지 업데이트
        feedback_surface = s.font.render(feedback_text, True, s.settings.font_color)
        s.screen.blit(feedback_surface, (s.SCREEN_WIDTH // 2 - 150, 400))
        
        pygame.display.flip()


def detect_singing_intervals(y, sr, top_db=60):
    #노래에서 유의미한 소리 구간 감지
    intervals = librosa.effects.split(y, top_db=top_db)
    return librosa.samples_to_time(intervals, sr=sr)

#게임 시작
def start_game(selected_song, accompaniment_path, song, song_title):
    
    pygame.mixer.init()
    s.screen.fill(s.BLACK)
    
    # 부정행위 및 오류 확인
    bad_thing = False
    
    # 웹캠 설정
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not detected.")
        return

    # dlib 얼굴 검출기와 특징점 예측기 로드
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    # 녹음 설정
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050
    CHUNK = 1024
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # 원곡 불러오기
    original_data, sr = librosa.load(selected_song, sr=RATE)
    singing_intervals = detect_singing_intervals(original_data, sr)

    pygame.mixer.music.load(accompaniment_path)
    pygame.mixer.music.play(-1)  # 무한 반복으로 재생
    pygame.time.delay(100)
    
    frames = []
    start_time = pygame.time.get_ticks()
    last_mouth_open_time = start_time
    stream.start_stream()

    while pygame.time.get_ticks() - start_time < len(original_data)/sr * 1000:
        ret, frame = cap.read()
        if not ret:
            bad_thing = True
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        current_time = (pygame.time.get_ticks() - start_time) / 1000
        is_singing_time = any(start <= current_time <= end for start, end in singing_intervals)
        mouth_open_detected = False
        
        
        for face in faces:
            landmarks = predictor(gray, face)
            lip_distance = landmarks.part(66).y - landmarks.part(62).y  # 아랫입술과 윗입술 사이 거리
            if lip_distance > 5:
                last_mouth_open_time = pygame.time.get_ticks()
                mouth_open_detected = True
                break
            
        if is_singing_time and not mouth_open_detected:
            if pygame.time.get_ticks() - last_mouth_open_time > 5000:
                bad_thing = True
                break

        # Convert from OpenCV to Pygame surface
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame_surface = pygame.surfarray.make_surface(frame)
        s.screen.blit(frame_surface, (0, 0))

        # Record audio
        data = stream.read(CHUNK)
        
        # Convert data from int16 to float32
        float_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        frames.append(float_data)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

    # 스트림 종료
    pygame.mixer.music.stop()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    cap.release()
    
    
    # numpy 배열로 변환
    recorded_data = np.hstack(frames)

    # 녹음 데이터의 음정 추출
    recorded_pitches, _ = librosa.core.piptrack(y=recorded_data, sr=RATE)
    original_pitches, _ = librosa.core.piptrack(y=original_data, sr=RATE)
    
    recorded_pitches = extract_pitches(recorded_pitches)
    original_pitches = extract_pitches(original_pitches)
    
    score = calculate_score(recorded_pitches, original_pitches, recorded_data, original_data, sr, song)
    print(score)
    if(bad_thing):
        game_over()
    else:
        show_game_result(score, song_title)
    
# 음정 데이터 정리
def extract_pitches(pitches):
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = pitches[:, t].argmax()
        if pitches[index, t] > 0:
            pitch_values.append(pitches[index, t])
    return np.array(pitch_values)

def calculate_score(recorded_pitches, original_pitches, recorded_data, original_data, sr, song):
    # 피치 정확성 점수 계산
    if len(recorded_pitches) > 0 and len(original_pitches) > 0:
        min_length = min(len(recorded_pitches), len(original_pitches))
        recorded_pitches = recorded_pitches[:min_length]
        original_pitches = original_pitches[:min_length]
        pitch_accuracy = np.mean(np.abs(recorded_pitches - original_pitches))
        max_difference = np.max(np.abs(recorded_pitches - original_pitches))
        normalized_accuracy = 1 - (pitch_accuracy / max_difference) # 0~1 사이의 값(평균이 최대값보다 클 수 없기 때문에)
        pitch = max(20, normalized_accuracy * 100)  # 0에서 100 사이의 점수

    # 박자 정확성 점수 계산
    tempo = calculate_tempo_accuracy(recorded_data, original_data, sr)
    
    # 가중치 적용하여 최종 점수 계산
    pitch_weight, tempo_weight = data_analyze.song_analyze(song)
    score = pitch_weight * pitch + tempo_weight * tempo
    
    return score  # 점수 범위를 50점에서 95점 사이로 조정

def calculate_tempo_accuracy(recorded_data, original_data, sr):
    # 박자 추출
    onset_env = librosa.onset.onset_strength(y=original_data, sr=sr)
    tempo_original, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    onset_env_rec = librosa.onset.onset_strength(y=recorded_data, sr=sr)
    tempo_recorded, _ = librosa.beat.beat_track(onset_envelope=onset_env_rec, sr=sr)

    # 박자 정확성 평가 (예: 템포 차이를 퍼센트로 변환하여 점수로 활용)
    tempo_diff = abs(tempo_original - tempo_recorded) / tempo_original
    tempo_accuracy = 100 * (1 - tempo_diff)  # 박자가 완벽하게 일치하면 100점
    return min(100, max(20, tempo_accuracy))  # 점수 범위 조정


def game_over():
    s.screen.blit(s.background_image, (0, 0))
    
    game_over_text = s.font_main.render("Game Over", True, s.settings.font_color)
    text_rect = game_over_text.get_rect(center=(s.SCREEN_WIDTH // 2, 100))
    s.screen.blit(game_over_text, text_rect)
    
    why_text = s.font.render("bad thing detected: don't open your mouth while singing", True, s.settings.font_color)
    why_rect = why_text.get_rect(center=(s.SCREEN_WIDTH // 2, 350))
    s.screen.blit(why_text, why_rect)
    
    # 'Back to Menu' 버튼 추가
    back_text = s.font.render("Back to Menu", True, s.settings.font_color)
    back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
    s.screen.blit(back_text, back_rect)
    
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # 마우스 클릭 위치 가져오기
                if back_rect.collidepoint(mouse_pos):
                    running = False
                    game_menu()  # 메인 메뉴로 돌아가기
                    
# 게임 결과 화면
def show_game_result(score, song_title):
    s.screen.blit(s.background_image, (0, 0))
    
    score_text = s.font_main.render(f'Your Score: {score:.2f}', True, s.settings.font_color)
    text_rect = score_text.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2))
    s.screen.blit(score_text, text_rect)
    
    # 점수 저장 버튼 추가
    save_text = s.font.render("Save", True, s.settings.font_color)
    save_rect = save_text.get_rect(center=(s.SCREEN_WIDTH // 2, 550))
    s.screen.blit(save_text, save_rect)

    # 리더보드 버튼 추가
    board_text = s.font.render("Leaderboard", True, s.settings.font_color)
    board_rect = board_text.get_rect(center=(s.SCREEN_WIDTH // 2, 600))
    s.screen.blit(board_text, board_rect)

    # 'Back to Menu' 버튼 추가
    back_text = s.font.render("Back to Menu", True, s.settings.font_color)
    back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
    s.screen.blit(back_text, back_rect)
    
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # 마우스 클릭 위치 가져오기
                if save_rect.collidepoint(mouse_pos):
                    # scores 테이블에 점수 저장
                    conn = db.connect_to_database()
                    cursor = conn.cursor()
                    query = "DELETE FROM scores WHERE username = %s AND song_title = %s"
                    cursor.execute(query, (s.current_player.username, song_title))
                    conn.commit()
                    query = "insert into scores (user_id, score, song_title, username) values (%s, %s, %s, %s)"
                    cursor.execute(query, (s.current_player.user_id, score, song_title, s.current_player.username))
                    conn.commit()
                    cursor.close()
                    conn.close()
                if board_rect.collidepoint(mouse_pos):
                    leaderboard(song_title)
                if back_rect.collidepoint(mouse_pos):
                    running = False
                    game_menu()  # 메인 메뉴로 돌아가기
                    
def leaderboard(song_title):
    s.screen.blit(s.background_image, (0, 0))
    
    leaderboard_text = s.font_main.render("Leaderboard", True, s.settings.font_color)
    leaderboard_rect = leaderboard_text.get_rect(center=(s.SCREEN_WIDTH // 2, 100))
    s.screen.blit(leaderboard_text, leaderboard_rect)
    
    # 'Back to Menu' 버튼 추가
    back_text = s.font.render("Back to Menu", True, s.settings.font_color)
    back_rect = back_text.get_rect(center=(s.SCREEN_WIDTH // 2, 650))
    s.screen.blit(back_text, back_rect)
    
    conn = db.connect_to_database()
    cursor = conn.cursor()
    query = """
            SELECT u.username, MAX(s.score) AS max_score
            FROM scores s
            JOIN users u ON s.user_id = u.id
            WHERE s.song_title = %s
            GROUP BY u.username
            LIMIT 10;
            ORDER BY max_score DESC
            """
    cursor.execute(query, (song_title,))
    result = cursor.fetchall()
    
    for idx, (username, score) in enumerate(result):
        text = s.font.render(f"{idx + 1}. {username} - {score:.2f}", True, s.settings.font_color)
        s.screen.blit(text, (s.SCREEN_WIDTH // 2 - 100, 150 + idx * 30))
    
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # 리더보드 데이터를 화면에 표시
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # 마우스 클릭 위치 가져오기
                if back_rect.collidepoint(mouse_pos):
                    running = False
                    game_menu()  # 메인 메뉴로 돌아가기