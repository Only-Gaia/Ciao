import json
import os

# Cartella dove vengono salvati i file JSON (uno per "categoria": warns.json, levels.json, ecc.)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def _path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.json")


def load(name: str) -> dict:
    """Carica un file JSON dalla cartella data/. Se non esiste, restituisce un dizionario vuoto."""
    path = _path(name)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except json.JSONDecodeError:
        # File corrotto/vuoto: non facciamo crashare il bot, ripartiamo da zero
        return {}


def save(name: str, content: dict) -> None:
    """Salva un dizionario nel file JSON corrispondente (data/<name>.json)."""
    path = _path(name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)


def get_user_levels(guild_id, user_id):
    """
    Ritorna (levels, user_data) dove:
    - levels è l'intero dizionario dei livelli (tutte le guild/utenti)
    - user_data è il dizionario del singolo utente in quella guild,
      creato con valori di default se non esiste ancora.

    L'oggetto restituito è già "dentro" a levels, quindi modificarlo
    e poi chiamare save("levels", levels) salva correttamente le modifiche.
    """
    levels = load("levels")
    g = levels.setdefault(str(guild_id), {})
    u = g.setdefault(str(user_id), {"messages": 0})
    u.setdefault("messages", 0)  # nel caso l'utente esista già ma senza questa chiave
    return levels, u


def get_user_warns(guild_id, user_id):
    """
    Analogo a get_user_levels ma per i warn: ritorna (warns, user_warns_list).
    user_warns_list è la lista di warn dell'utente, già "dentro" a warns.
    """
    warns = load("warns")
    g = warns.setdefault(str(guild_id), {})
    u = g.setdefault(str(user_id), [])
    return warns, u
