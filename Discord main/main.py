import asyncio
import os
import traceback
import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN, PREFIX


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# FFMPEG Options
FFMPEG_OPTIONS = {
    "options": "-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

@bot.event
async def on_ready():
    try:
        await bot.load_extension("comandos.comando_musica")  
        await bot.tree.sync()
        print(f"Bot pronto! {len(bot.tree.get_commands())} comandos carregados!")
    except Exception as e:
        print(f"Erro em on_ready: {str(e)}")
        traceback.print_exc()


@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clean(ctx, amount: int):
    if not 1 <= amount <= 100:
        await ctx.send("Por favor, forneça um número de 1 a 100.")
        return

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Removido(s) {len(deleted)} mensagem(s).", delete_after=5)


@bot.command()
@commands.guild_only()
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def expulsar(ctx, member: discord.Member, *, reason=None):
    if not ctx.guild.me.guild_permissions.kick_members:
        await ctx.send("Não possui permissão para expulsar esse usúario!")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(
            f"{member.name} foi expulso do servidor! Razão: {reason if reason else 'Nenhuma razão fornecida.'}"
        )
    except discord.Forbidden:
        await ctx.send("Eu não tenho permissão para expulsar esse usuário!")
    except discord.HTTPException:
        await ctx.send("Houve um erro ao tentar expulsar o usuário.")


@bot.command()
@commands.guild_only()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def banir(ctx, member: discord.Member, *, reason=None):
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.send("Eu não tenho permissão para banir membros!")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.name} foi banido do servidor!")
    except discord.Forbidden:
        await ctx.send("Eu não tenho permissão para banir esse usuário!")
    except discord.HTTPException:
        await ctx.send("Houve um erro ao tentar banir o usuário.")


@bot.command()
@commands.guild_only()
@commands.has_permissions(mute_members=True)
@commands.bot_has_permissions(mute_members=True)
async def mute(ctx, member: discord.Member, time: int = 60):
    if not 1 <= time <= 600:
        await ctx.send("Informe um tempo entre 1 e 600 segundos.")
        return
    if ctx.author.top_role <= member.top_role:
        await ctx.send("Você não tem permissão para mutar esse usuário.")
        return
    try:
        await member.edit(mute=True)
        await ctx.send(f"{member.mention} foi mutado por {time} segundos.")
        await asyncio.sleep(time)
        await member.edit(mute=False)
        await ctx.send(f"{member.mention} foi desmutado.")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")
@bot.command()
@commands.guild_only()
@commands.has_permissions(mute_members=True)
@commands.bot_has_permissions(mute_members=True)
async def unmute(ctx, member: discord.Member):
    if ctx.author.top_role <= member.top_role:
        await ctx.send("Você não tem permissão para desmutar esse usuário.")
        return
    await member.edit(mute=False)
    await ctx.send(f"{member.mention} foi desmutado.")    
    

if not TOKEN:
    raise SystemExit("Configure DISCORD_TOKEN antes de executar.")
bot.run(TOKEN)
