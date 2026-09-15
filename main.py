import os
import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

# ---------- CONFIG ----------
load_dotenv()  # legge TOKEN da un file .env nella stessa cartella

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")  # prefisso per i comandi testuali (i comandi hybrid funzionano anche come /slash)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("main")

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.members = True          # necessario per member.add_roles, kick, ban, ecc.
intents.message_content = True  # necessario per i comandi prefix e il conteggio messaggi


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=intents, help_command=None)
        # help_command=None disabilita l'help di default: lo gestiamo noi in cogs/help.py

    async def setup_hook(self):
        # Carica automaticamente tutti i cog presenti nella cartella "cogs"
        cogs_dir = os.path.join(os.path.dirname(__file__), "cogs")
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                extension = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(extension)
                    log.info(f"✅ Cog caricato: {extension}")
                except Exception as e:
                    log.error(f"❌ Errore caricando {extension}: {e}")

        # Sincronizza gli slash command con Discord
        try:
            synced = await self.tree.sync()
            log.info(f"🔄 Sincronizzati {len(synced)} slash command")
        except Exception as e:
            log.error(f"❌ Errore durante la sync dei comandi: {e}")

    async def on_ready(self):
        log.info(f"🤖 Bot connesso come {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
        )


bot = MyBot()


# ---------- GESTIONE ERRORI GLOBALE (comandi prefix/hybrid) ----------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Non hai i permessi necessari per usare questo comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Manca un parametro obbligatorio. Controlla la sintassi del comando.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Utente non trovato.")
    elif isinstance(error, commands.CommandNotFound):
        return  # ignora comandi inesistenti
    else:
        log.error(f"Errore non gestito: {error}")
        await ctx.send(f"⚠️ Si è verificato un errore: {error}")


def main():
    if not TOKEN:
        raise RuntimeError(
            "Token non trovato. Crea un file .env con dentro DISCORD_TOKEN=il_tuo_token"
        )
    asyncio.run(bot.start(TOKEN))


if __name__ == "__main__":
    main()
