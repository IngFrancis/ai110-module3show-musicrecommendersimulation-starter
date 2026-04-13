"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def run_profile(profile_name: str, user_prefs: dict, songs: list, k: int = 5):
    """Run and display recommendations for a single user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    line = "=" * 72
    subline = "-" * 72
    print()
    print(line)
    print(f"PROFILE: {profile_name}")
    print(line)
    print("User Preferences:")
    for key, value in user_prefs.items():
        print(f"  {key}: {value}")
    print(line)
    for idx, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [r.strip() for r in explanation.split("|") if r.strip()]
        print(f"Rank #{idx}")
        print(f"Song: {song['title']} — {song['artist']}")
        print(f"Final Score: {score:.2f}/100")
        print("Reasons:")
        for reason in reasons:
            print(f"  - {reason}")
        print(subline)
    print(f"Summary: evaluated {len(songs)} songs, returned top {len(recommendations)}.")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Profile 1: High-Energy Pop ---
    run_profile("High-Energy Pop", {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "preferred_tempo_bpm": 130,
        "preferred_valence": 0.85,
        "preferred_danceability": 0.88
    }, songs)

    # --- Profile 2: Chill Lofi ---
    run_profile("Chill Lofi", {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.38,
        "likes_acoustic": True,
        "preferred_tempo_bpm": 75,
        "preferred_valence": 0.58,
        "preferred_danceability": 0.60
    }, songs)

    # --- Profile 3: Deep Intense Rock ---
    run_profile("Deep Intense Rock", {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False,
        "preferred_tempo_bpm": 155,
        "preferred_valence": 0.45,
        "preferred_danceability": 0.65
    }, songs)

    # --- Edge Case 1: Conflicting energy vs mood ---
    run_profile("Edge Case: Conflicting Energy vs Mood", {
        "favorite_genre": "classical",
        "favorite_mood": "melancholic",
        "target_energy": 0.95,
        "likes_acoustic": True,
        "preferred_valence": 0.10
    }, songs)

    # --- Edge Case 2: Rare genre (only 1 metal song exists) ---
    run_profile("Edge Case: Rare Genre (Metal)", {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.96,
        "likes_acoustic": False,
        "preferred_tempo_bpm": 168,
        "preferred_valence": 0.31,
        "preferred_danceability": 0.61
    }, songs)

    # --- Edge Case 3: Middle-of-the-road profile ---
    run_profile("Edge Case: Middle-of-the-Road", {
        "favorite_genre": "jazz",
        "favorite_mood": "focused",
        "target_energy": 0.50,
        "likes_acoustic": True,
        "preferred_tempo_bpm": 100,
        "preferred_valence": 0.50,
        "preferred_danceability": 0.50
    }, songs)


if __name__ == "__main__":
    main()