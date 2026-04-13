# Reflection: Music Recommender Evaluation

## Profile Comparisons

### High-Energy Pop vs Chill Lofi

These two profiles are almost complete opposites and the results reflect
that clearly. The High-Energy Pop user prefers loud, fast, danceable songs
and got Sunrise City and Gym Hero at the top — both high-tempo pop tracks
with energy above 0.80. The Chill Lofi user prefers quiet, slow, acoustic
songs and got Library Rain and Midnight Coding — two soft lofi tracks with
energy below 0.45.

What makes sense here is that the numeric features (energy, acousticness,
tempo) did exactly what they were designed to do — they pulled the two
profiles in completely opposite directions. The catalog naturally separates
into high-energy and low-energy clusters, and the scoring rewarded songs
closest to each user's target.

---

### High-Energy Pop vs Deep Intense Rock

Both profiles want high-energy songs, so they share some overlap in the
lower ranks — Gym Hero appeared in both top 5 lists because its energy
(0.93) scores well for any user targeting high intensity. However the top
spots diverged because of genre and mood: the pop user got Sunrise City
(genre match + mood match) while the rock user got Storm Runner (genre
match + mood match). This shows the categorical features doing their job
of separating users who want similar energy but different styles.

---

### Chill Lofi vs Middle-of-the-Road

The Chill Lofi profile produced strong, well-separated results with a
clear #1 scorer at 96.60. The Middle-of-the-Road profile — with all
preferences set near 0.5 — produced a cluster of scores between 50 and
76 with no clear winner. This comparison reveals something important:
the recommender works best when the user has strong, clear preferences.
Vague preferences produce vague recommendations. A real Spotify user
who says "I like everything" is just as hard to recommend to as this
middle-of-the-road profile.

---

### Deep Intense Rock vs Rare Genre Metal

Both profiles want aggressive, high-energy music. The rock user got Storm
Runner at 97.72 — a near-perfect match. The metal user got Iron Pulse at
99.36 — an even better match. But here is where they diverge sharply:
the rock user had reasonable backup options at ranks 2–5 (Gym Hero, Iron
Pulse, etc.) while the metal user had nothing comparable after rank 1 —
ranks 2–5 all dropped to around 50 points. This shows that catalog size
matters as much as scoring logic. The metal user was well served for one
song and completely abandoned after that.

---

### Rare Genre Metal vs Conflicting Energy vs Mood

Both are edge cases but for different reasons. The metal user had clear,
consistent preferences that the catalog simply couldn't fully satisfy due
to limited genre coverage. The conflicting profile (high energy +
melancholic + acoustic) had internally contradictory preferences — songs
that are high energy tend to be low acoustic, and songs that are melancholic
tend to be low energy. No song in any catalog could perfectly satisfy all
three at once. The metal user's problem was a data problem. The conflicting
user's problem was a logic problem. Both produced low scores but for
completely different reasons.

---

## Why Does Gym Hero Keep Showing Up?

Imagine you tell a friend: "I want a happy pop song." Your friend looks
through a stack of 18 CDs and picks Sunrise City — perfect match, great
energy, happy vibe, pop genre. But then you ask for four more suggestions
and your friend keeps pulling out Gym Hero. Why?

Because Gym Hero is extremely loud and extremely non-acoustic. Those two
qualities — high energy and low acousticness — together earn 35+ points
in the scoring system before genre and mood are even checked. With only
18 songs to choose from, very few tracks compete with Gym Hero on those
two dimensions simultaneously.

It is not that the system thinks Gym Hero is a happy pop song. It is that
the system runs out of better options and Gym Hero keeps scoring just
high enough on the numeric features to sneak into the top 5. This is
the catalog size problem in action — with 200 songs instead of 18, there
would be plenty of better alternatives and Gym Hero would never appear
for a rock or metal user.

---

## Key Takeaway

A recommender system is only as good as the data it runs on. The scoring
logic in VibeFinder 1.0 is mathematically sound — it rewards closeness,
penalizes distance, and weights important features more heavily. But when
the catalog has only 1–3 songs per genre, the system has nowhere to go
after the top match. Real recommenders like Spotify work because they
have millions of songs, not because their math is dramatically different.
The algorithm matters, but the data matters more.
