import mysql.connector

def connect_to_database():
    try:
        # 데이터베이스 연결 설정
        conn = mysql.connector.connect(
            host='127.0.0.1',  # MySQL 서버 주소
            user='root',  # MySQL 사용자 이름
            password='630900',  # MySQL 비밀번호
            database='perfect_score'  # 연결할 데이터베이스 이름
        )
        return conn
    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return None