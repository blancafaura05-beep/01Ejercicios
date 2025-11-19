import subprocess
import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_step(name, command):
    """
    Ejecuta un módulo y registra si falla.
    """
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

    run_step("SCRAPPER", ["python", "scrapper/main.py"])
    run_step("CLEANER", ["python", "tab_cleaner/main.py"])
    run_step("VALIDATOR", ["python", "tab_validator/main.py"])
    run_step("RESULTS", ["python", "results/main.py"])
    run_step("LYRICS", ["python", "lyrics/main.py"])
    run_step("INSIGHTS", ["python", "insights/main.py"])

    logging.info("Pipeline execution finished successfully")

if __name__ == "__main__":
    main()