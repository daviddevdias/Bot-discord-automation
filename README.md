# Bot de música e moderação para Discord

Bot Python com comandos para reprodução de áudio e moderação de servidores.

## 📌 Funcionalidades

- Música: `/join`, `/leave`, `/tocar`, `/pause`, `/retomar` e `/parar`.
- Moderação por mensagens com prefixo: `/clean`, `/expulsar`, `/banir`, `/mute` e `/unmute`.

## Tecnologias

Python 3, discord.py, yt-dlp, PyNaCl e FFmpeg.

## 🚀 Como executar

```bash
git clone https://github.com/daviddevdias/Bot-discord-automation.git
cd Bot-discord-automation
python -m venv .venv
```

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r "Discord main/requirements.txt"
$env:DISCORD_TOKEN = "seu-token"
cd "Discord main"
python main.py
```

## Configuração do Discord

Crie um aplicativo no Discord Developer Portal e adicione o bot ao servidor com os escopos `bot` e `applications.commands`. Ative Message Content Intent para os comandos por prefixo e conceda as permissões correspondentes aos comandos utilizados.

O FFmpeg deve estar disponível no PATH. O token é lido da variável `DISCORD_TOKEN`; arquivos .env não são carregados automaticamente. Os comandos de música usam a interface de comandos de aplicação, enquanto os de moderação são enviados como mensagens de texto.
