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
