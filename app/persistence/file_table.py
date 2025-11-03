
import json, os, tempfile
from pathlib import Path
from typing import List, Dict, Iterable, Union
PathLike = Union[str, Path]
def ensure_file(path: PathLike) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists(): p.write_text("", encoding="utf-8")
def read_all(path: PathLike) -> List[Dict]:
    ensure_file(path)
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s:
                rows.append(json.loads(s))
    return rows
def append_one(path: PathLike, record: Dict) -> None:
    ensure_file(path)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
def overwrite_all_atomic(path: PathLike, records: Iterable[Dict]) -> None:
    ensure_file(path)
    d = str(Path(path).parent)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".swap_", suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, str(path))
    except Exception:
        try: os.remove(tmp)
        except OSError: pass
        raise
