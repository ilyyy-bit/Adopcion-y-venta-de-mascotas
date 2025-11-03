
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PERSONAS_FILE = DATA_DIR / "personas.txt"
MASCOTAS_FILE = DATA_DIR / "mascotas.txt"
REGISTROS_FILE = DATA_DIR / "registros.txt"
ALIANZAS_FILE = DATA_DIR / "alianzas.txt"
BANNERS_FILE = DATA_DIR / "banners.txt"
def ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for p in [PERSONAS_FILE, MASCOTAS_FILE, REGISTROS_FILE, ALIANZAS_FILE, BANNERS_FILE]:
        if not p.exists():
            p.write_text("", encoding="utf-8")
