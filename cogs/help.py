import discord
from discord import app_commands
from discord.ext import commands

# Emoji da associare al nome del cog (facoltativo, solo estetica)
CATEGORY_EMOJI = {
    "Moderation": "🛡️",
    "Help": "❓",
}


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Mostra tutti i comandi disponibili o i dettagli di uno specifico")
    @app_commands.describe(comando="Nome del comando di cui vuoi vedere i dettagli (opzionale)")
    async def help(self, ctx, comando: str = None):
        # ---------- HELP SU UN SINGOLO COMANDO ----------
        if comando:
            cmd = self.bot.get_command(comando)
            if cmd is None:
                return await ctx.send(f"❌ Nessun comando chiamato `{comando}` trovato.")

            embed = discord.Embed(
                title=f"Comando: {ctx.prefix}{cmd.name}",
                description=cmd.description or "Nessuna descrizione disponibile.",
                color=discord.Color.blurple(),
            )

            if cmd.clean_params:
                params = " ".join(f"<{p}>" for p in cmd.clean_params)
                embed.add_field(name="Utilizzo", value=f"`{ctx.prefix}{cmd.name} {params}`", inline=False)

            if isinstance(cmd, commands.HybridCommand):
                embed.add_field(name="Slash command", value=f"`/{cmd.name}`", inline=False)

            return await ctx.send(embed=embed)

        # ---------- LISTA COMPLETA DEI COMANDI, RAGGRUPPATI PER COG ----------
        embed = discord.Embed(
            title="📖 Lista comandi",
            description=f"Usa `{ctx.prefix}help <comando>` per i dettagli su un comando specifico.\n"
                        f"Tutti i comandi funzionano sia come `{ctx.prefix}comando` sia come `/comando`.",
            color=discord.Color.blurple(),
        )

        cogs_commands = {}
        for cmd in self.bot.commands:
            if cmd.hidden:
                continue
            cog_name = cmd.cog_name or "Altro"
            cogs_commands.setdefault(cog_name, []).append(cmd)

        for cog_name, cmds in sorted(cogs_commands.items()):
            emoji = CATEGORY_EMOJI.get(cog_name, "📂")
            value = ", ".join(f"`{c.name}`" for c in sorted(cmds, key=lambda c: c.name))
            embed.add_field(name=f"{emoji} {cog_name}", value=value, inline=False)

        embed.set_footer(text=f"Richiesto da {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
