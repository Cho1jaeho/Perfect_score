import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
import librosa
import numpy as np

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def extract_features_from_song(audio_path, scaler, model):
    y, sr = librosa.load(audio_path, sr=None)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    energy = np.sqrt(np.mean(librosa.feature.rms(y=y)**2))
    acousticness = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    features = np.array([energy, acousticness, tempo])
    features_scaled = scaler.transform([features])
    predicted_weights = model.predict(features_scaled)
    normalized_weights = softmax(predicted_weights[0])
    return normalized_weights

def song_analyze(song_path):
    # 데이터 로드 및 확인
    data = pd.read_csv('single_album_track_data.csv')
    features = ['energy', 'acousticness', 'tempo']
    data = data.dropna(subset=['Track_Id'])

    # 데이터 스케일링
    scaler = StandardScaler()
    data_features = scaler.fit_transform(data[features])
    data = pd.DataFrame(data_features, columns=features)

    # 음정, 박자 가중치 계산
    data['pitch_weight'] = data['acousticness']
    data['tempo_weight'] = 0.5 * data['tempo'] + 0.5 * data['energy']
    data['weight_sum'] = data['pitch_weight'] + data['tempo_weight']
    data['pitch_weight'] /= data['weight_sum']
    data['tempo_weight'] /= data['weight_sum']

    X = data[features]
    y = data[['pitch_weight', 'tempo_weight']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = MultiOutputRegressor(GradientBoostingRegressor(n_estimators=100))
    model.fit(X_train, y_train)

    # 가중치 추출
    weights = extract_features_from_song(song_path, scaler, model)
    return weights
