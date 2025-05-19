import discord
from discord.ext import commands
import yt_dlp as youtube_dl

class ComandoMusica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="join", description="Faz o bot entrar no canal de voz."
    )
    async def join(self, interaction: discord.Interaction):
        """Faz o bot entrar no canal de voz."""
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.send_message(
                f"Entrei no canal de voz: {channel.name}! 🎶"
            )
        else:
            await interaction.response.send_message(
                "Você precisa estar em um canal de voz!"
            )

    @discord.app_commands.command(
        name="leave", description="Faz o bot sair do canal de voz."
    )
    async def leave(self, interaction: discord.Interaction):
        """Faz o bot sair do canal de voz."""
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Saí do canal de voz! 🛑")
        else:
            await interaction.response.send_message("Não estou em nenhum canal de voz!")

    @discord.app_commands.command(
        name="tocar", description="Toca uma música a partir de uma URL."
    )
    async def tocar(self, interaction: discord.Interaction, url: str):
        """Toca uma música a partir de uma URL."""
        # Se o bot não estiver no canal de voz, entra no canal
        if not interaction.guild.voice_client:
            await self.join(interaction)

        # Configuração do yt-dlp para pegar a URL de áudio
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["url"]

        # Para qualquer música que esteja tocando
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()

        # Toca a nova música
        interaction.guild.voice_client.play(
            discord.FFmpegPCMAudio(url2),
            after=lambda e: print(f"Erro: {e}" if e else "Tocando..."),
        )

        # Envia a mensagem de confirmação
        await interaction.response.send_message(f"Tocando agora: {info['title']} 🎵")

    @discord.app_commands.command(name="pause", description="Pausa a música.")
    async def pause(self, interaction: discord.Interaction):
        """Pausa a música tocando no canal de voz."""
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("Música pausada! ⏸️")
        else:
            await interaction.response.send_message("Não há música tocando no momento.")

    @discord.app_commands.command(name="retomar", description="Retoma a música.")
    async def retomar(self, interaction: discord.Interaction):
        """Retoma a música pausada."""
        if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("Música retomada! 🎶")
        else:
            await interaction.response.send_message("Não há música pausada no momento.")

    @discord.app_commands.command(name="parar", description="Para a música.")
    async def parar(self, interaction: discord.Interaction):
        """Para a música que está tocando no canal de voz."""
        if interaction.guild.voice_client:
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Música parada! ⏹️")
        else:
            await interaction.response.send_message("Não há música tocando no momento.")


# Função de setup do Cog
async def setup(bot):
    await bot.add_cog(ComandoMusica(bot))
    await bot.tree.sync()  # Sincroniza os comandos Slash com o Discord
