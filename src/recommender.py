import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """Represents a song and its audio feature attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """Stores a user's taste preferences for music recommendation matching."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    preferred_tempo_bpm: Optional[float] = None
    preferred_valence: Optional[float] = None
    preferred_danceability: Optional[float] = None

class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of songs and store them for later ranking."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a user profile, ranked by recommendation score."""
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short text explanation of why a song matches the user profile."""
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file and return a list of song dictionaries with converted field types."""
    songs: List[Dict] = []
    try:
        with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                song = {
                    "id":           int(row["id"]),
                    "title":        row["title"],
                    "artist":       row["artist"],
                    "genre":        row["genre"],
                    "mood":         row["mood"],
                    "energy":       float(row["energy"]),
                    "tempo_bpm":    float(row["tempo_bpm"]),
                    "valence":      float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: songs file not found at path: {csv_path}")
        return []
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return the total score with reason strings.

    Scoring Recipe (max = 100 points):
        genre match:         24 pts (exact match)
        energy closeness:    24 pts (proximity formula)
        mood match:          16 pts (exact match)
        acoustic fit:        16 pts (bool → float proximity)
        tempo closeness:      8 pts (optional, normalized /120)
        valence closeness:    6 pts (optional)
        danceability:         6 pts (optional)
    """
    score = 0.0
    reasons = []

    # --- STEP 1: Categorical Scores ---

    # Genre match (24 pts)
    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += 24
        reasons.append(f"Genre match ({song['genre']}): +24 pts")
    else:
        reasons.append(f"No genre match ({song['genre']} vs {user_prefs.get('favorite_genre')}): +0 pts")

    # Mood match (16 pts)
    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += 16
        reasons.append(f"Mood match ({song['mood']}): +16 pts")
    else:
        reasons.append(f"No mood match ({song['mood']} vs {user_prefs.get('favorite_mood')}): +0 pts")

    # --- STEP 2: Numeric Proximity Scores ---

    # Energy closeness (24 pts)
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_proximity = 1 - abs(target_energy - song.get("energy", 0.5))
    energy_points = 24 * max(0.0, energy_proximity)
    score += energy_points
    reasons.append(f"Energy closeness: +{energy_points:.1f} pts")

    # Acoustic fit (16 pts) — bool → float conversion
    acoustic_target = 1.0 if user_prefs.get("likes_acoustic", False) else 0.0
    acoustic_proximity = 1 - abs(acoustic_target - song.get("acousticness", 0.5))
    acoustic_points = 16 * max(0.0, acoustic_proximity)
    score += acoustic_points
    reasons.append(f"Acoustic fit: +{acoustic_points:.1f} pts")

    # --- STEP 3: Optional Numeric Features ---

    # Tempo closeness (8 pts) — normalized over 60–180 range
    if user_prefs.get("preferred_tempo_bpm") is not None:
        tempo_proximity = 1 - abs(user_prefs["preferred_tempo_bpm"] - song.get("tempo_bpm", 120)) / 120
        tempo_points = 8 * max(0.0, tempo_proximity)
        score += tempo_points
        reasons.append(f"Tempo closeness: +{tempo_points:.1f} pts")

    # Valence closeness (6 pts)
    if user_prefs.get("preferred_valence") is not None:
        valence_proximity = 1 - abs(user_prefs["preferred_valence"] - song.get("valence", 0.5))
        valence_points = 6 * max(0.0, valence_proximity)
        score += valence_points
        reasons.append(f"Valence closeness: +{valence_points:.1f} pts")

    # Danceability closeness (6 pts)
    if user_prefs.get("preferred_danceability") is not None:
        dance_proximity = 1 - abs(user_prefs["preferred_danceability"] - song.get("danceability", 0.5))
        dance_points = 6 * max(0.0, dance_proximity)
        score += dance_points
        reasons.append(f"Danceability closeness: +{dance_points:.1f} pts")

    return (round(score, 2), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort results from highest to lowest, and return the top k recommendations."""
    results: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        results.append((song, score, explanation))
    ranked_results = sorted(results, key=lambda item: item[1], reverse=True)
    return ranked_results[:k]