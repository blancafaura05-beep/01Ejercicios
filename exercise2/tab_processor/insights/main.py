import os
import re
from collections import Counter

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "files")
LYRICS_DIR = os.path.join(BASE_DIR, "lyrics")
INSIGHTS_DIR = os.path.join(BASE_DIR, "insights")

os.makedirs(INSIGHTS_DIR, exist_ok=True)



def clean_words(text):
    text = text.lower()
    words = re.findall(r"[a-záéíóúñ]+", text)#quita signos de puntuación
    return words


def main():
    artist_lyrics = {}
    global_counter = Counter()

    # Leer archivos de lyrics
    for filename in os.listdir(LYRICS_DIR):
        filepath = os.path.join(LYRICS_DIR, filename)

        if not os.path.isfile(filepath):
            continue

        # Extraer artista por nombre archivo
        if " - " in filename:
            artist = filename.split(" - ")[0]
        else:
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        if artist not in artist_lyrics:
            artist_lyrics[artist] = ""

        artist_lyrics[artist] += "\n" + text

    # Crear archivo por artista y contar palabras
    for artist, text in artist_lyrics.items():
        artist_file = os.path.join(INSIGHTS_DIR, f"{artist}_all.txt")

        with open(artist_file, "w", encoding="utf-8") as f:
            f.write(text)

        words = clean_words(text)
        counter = Counter(words)
        global_counter.update(words)

        top10 = counter.most_common(10)

        print(f"Top 10 palabras de {artist}:")
        for word, count in top10:
            print(f"{word}: {count}")
        print()

    # TOP 20 global
    global_top20 = global_counter.most_common(20)
    global_file = os.path.join(INSIGHTS_DIR, "global_top20.txt")

    with open(global_file, "w", encoding="utf-8") as f:
        for word, count in global_top20:
            f.write(f"{word}: {count}\n")

    print("Análisis global generado")


if __name__ == "__main__":
    main()