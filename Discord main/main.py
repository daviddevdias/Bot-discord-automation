import asyncio
import os
import traceback
import discord
from discord.ext import commands
from discord import app_commands
from comandos.comando_musica import ComandoMusica


permissoes = discord.Intents.all()
permissoes.message_content = True
permissoes.members = True


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

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
async def clean(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Por favor, forneça um número de 1 a 1000.")
        return

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"Removido(s) {len(deleted)} mensagem(s).", delete_after=5)


@bot.command()
@commands.has_permissions(kick_members=True)
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
@commands.has_permissions(ban_members=True)
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
async def mute(ctx, member: discord.Member, time: int = 60):
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
async def unmute(ctx, member: discord.Member):
    await member.editable(mute=False)
    await ctx.send(f"{member.mention} foi desmutado.")    
    

bot.run("MTMzNDQ2OTI5MTU5NjMyMDg1MQ.G7HNjb.mXuM6uwTK2Z6AE3QWJrzyuVkK7NM9NCNnTaaVQ")