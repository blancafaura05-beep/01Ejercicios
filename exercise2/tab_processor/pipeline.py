import os
import sys
import logging
import subprocess

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def path(*parts):
    return os.path.join(BASE_DIR, *parts)

def run_step(name, command):
    logging.info(f"Starting: {name}")
    try:
        subprocess.check_call(command)
        logging.info(f"Completed: {name}")
    except Exception as e:
        logging.error(f"FAILED: {name} - {str(e)}")
        print(f"ERROR in {name}. Check pipeline.log")
        raise

def main():
    logging.info("Pipeline execution started")

    run_step("SCRAPPER",  [sys.executable, path("scrapper", "main.py")])
    run_step("CLEANER",   [sys.executable, path("tab_cleaner", "main.py")])
    run_step("VALIDATOR", [sys.executable, path("tab_validator", "main.py")])
    run_step("RESULTS",   [sys.executable, path("results", "main.py")])
    run_step("LYRICS",    [sys.executable, path("lyrics", "main.py")])
    run_step("INSIGHTS",  [sys.executable, path("insights", "main.py")])

    logging.info("Pipeline execution finished successfully")
    print("Pipeline terminado correctamente.")

if __name__ == "__main__":
    main()
