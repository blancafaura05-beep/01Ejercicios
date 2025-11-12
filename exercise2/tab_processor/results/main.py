import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "files")
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
VALIDATION_OK = os.path.join(BASE_DIR, "validations", "ok")
VALIDATION_KO = os.path.join(BASE_DIR, "validations", "ko")

def count_files(path):
    """Cuenta los archivos en un directorio."""
    if not os.path.exists(path):
        return 0
    return sum(1 for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))

def main():
    """Muestra el número de archivos por cada tipo de salida."""
    cleaned = count_files(CLEANED_DIR)
    ok = count_files(VALIDATION_OK)
    ko = count_files(VALIDATION_KO)

    print("RESULTS SUMMARY")
    print(f"Cleaned files: {cleaned}")
    print(f"Validated OK: {ok}")
    print(f"Validated KO: {ko}")
    print(f"Total validated: {ok + ko}")

if __name__ == "__main__":
    main()