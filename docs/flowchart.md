# Recommender System Flowchart

This diagram shows the data flow from user input to final recommendations.

```mermaid
flowchart TD
    A[Input user preferences<br/>favorite_genre, favorite_mood, target_energy, likes_acoustic<br/>optional: preferred_tempo_bpm, preferred_valence, preferred_danceability] --> B[Load song catalog CSV]
    B --> C[Initialize empty scored_results list]
    C --> D{{More songs to score?}}
    D -- Yes --> E[Get next song]
    E --> F[Run score_song(user, song)]
    F --> G[Genre match check<br/>0 or +24]
    G --> H[Mood match check<br/>0 or +16]
    H --> I[Energy proximity<br/>+0 to +24]
    I --> J[Acoustic fit from likes_acoustic vs acousticness<br/>+0 to +16]
    J --> K{Optional preferences present?}
    K -- Yes --> L[Tempo proximity +0 to +8<br/>Valence proximity +0 to +6<br/>Danceability proximity +0 to +6]
    K -- No --> M[Skip optional scoring]
    L --> N[Calculate total score and reasons]
    M --> N
    N --> O[Append (song, score, reasons) to scored_results]
    O --> D
    D -- No --> P[Sort scored_results by total score descending]
    P --> Q[Select top K songs]
    Q --> R[Output recommendations<br/>song + score + reasons]
```
