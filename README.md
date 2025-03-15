# 🎵 Perfect Score

**Perfect Score** is a music game that analyzes the accuracy of a user's singing and assigns a score. 🎤🎶  

## 📌 Key Features
- 🎵 **Real-time Pitch Analysis**: Records and analyzes pitch and rhythm in real-time  
- 📊 **Leaderboard**: Tracks high scores and compares them with other players  
- 👫 **Friend System**: Add friends and compare scores  
- 📂 **Data Storage**: Manages user information and score database  

## 🛠️ Installation
1. **Install required libraries**  
    ```bash
    pip install -r requirements.txt
    ```
2. **Set up the database**  
    ```bash
    python setup_db.py
    ```
3. **Run the game**  
    ```bash
    python main.py
    ```

## Project Details

### Start
![Start Screen](https://github.com/user-attachments/assets/212431ea-8350-4c19-8058-9bc8824db41e)
When the program is first launched, the following screen appears. Users can log in to access the game, or sign up if they do not have an account.

### Song Selection
![Song Selection](https://github.com/user-attachments/assets/022e89c6-4dff-4d96-92a1-bd4ddc15a9c4)  
Users can select a song they want to sing.

### Gameplay
![Gameplay Screen](https://github.com/user-attachments/assets/e73a2be7-b6c1-4898-a8c2-7bd9073f01c6)  
During the game, the user's face appears on the screen using the built-in webcam of their laptop. This feature is implemented to prevent cheating.

### Cheating Prevention
![Cheating Detection](https://github.com/user-attachments/assets/66666ecf-38a2-4531-83ec-26ba613b41f9)  
If the user does not open their mouth for more than 5 seconds during the singing parts, it is considered cheating, and the game ends.

### Game Over
![Game Over Screen](https://github.com/user-attachments/assets/4b11e187-6518-4bc8-87f5-a7d90879ca54)  
If the user completes the game without cheating, the following screen appears. Users can save their score and check the leaderboard rankings.


## 🎮 How to Play
1. Sign up or log in after launching the program  
2. Sing a song and check your score  
3. Add friends and compare scores  

## 🤝 Contribution
1. Fork this repository  
2. Add new features or make improvements  
3. Create a Pull Request  

## 📜 License
This project follows the MIT License.  
