import os
import re

# Directorios
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "files")
OK_DIR = os.path.join(BASE_DIR, "validations", "ok")
OUTPUT_DIR = os.path.join(BASE_DIR, "lyrics")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def remove_chords(text):
    """Elimina acordes de guitarra"""
    # Quita acordes 
    return re.sub(r'\b[A-G][#b]?(maj|min|dim|aug|sus|add)?\d*\b', '', text)

def main():
    """Procesa los archivos OK y guarda la letra sin acordes."""
    for filename in os.listdir(OK_DIR):
        filepath = os.path.join(OK_DIR, filename)

        if not os.path.isfile(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        lyrics_only = remove_chords(text)

        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(lyrics_only)

        print(f"Processed: {filename}")

if __name__ == "__main__":
    main()