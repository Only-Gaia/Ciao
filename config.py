import discord

# ---------- GENERALE ----------
PREFIX = "!"                 # prefisso comandi testuali (i comandi hybrid funzionano anche come /slash)
OWNER_IDS = []                # ID Discord dei proprietari/admin del bot, es: [123456789012345678]

# ---------- MODERAZIONE ----------
MAX_WARNS_BEFORE_ACTION = 3    # esempio: soglia oltre la quale potresti automatizzare un ban/kick
DEFAULT_MUTE_MINUTES = 10      # durata di default se in futuro vuoi un mute senza specificare i minuti

# ---------- ESTETICA ----------
EMBED_COLOR = discord.Color.blurple()
EMBED_COLOR_SUCCESS = discord.Color.green()
EMBED_COLOR_ERROR = discord.Color.red()
EMBED_COLOR_WARN = discord.Color.orange()

CATEGORY_EMOJI = {
    "Moderation": "🛡️",
    "Help": "❓",
}

# ---------- DATI ----------
DATA_DIR_NAME = "data"        # nome della cartella dove data.py salva i file JSON

# NOTA: il token del bot NON va mai messo qui.
# Va sempre nel file .env, come DISCORD_TOKEN=il_tuo_token
# (vedi main.py, che lo legge con load_dotenv() + os.getenv)
