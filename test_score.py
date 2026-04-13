from src.recommender import load_songs, score_song

songs = load_songs("data/songs.csv")

user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,
    "preferred_tempo_bpm": 78,
    "preferred_valence": 0.56,
    "preferred_danceability": 0.62
}

for song in songs[:3]:
    score, reasons = score_song(user_prefs, song)
    print(f"\n{song['title']} — {score:.2f} pts")
    for r in reasons:
        print(f"  {r}")