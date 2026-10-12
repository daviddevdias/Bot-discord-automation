# Bot de música e moderação para Discord

Projeto Python com comandos de reprodução de áudio e moderação. Usa `discord.py`, `yt-dlp` e FFmpeg.

## 📁 Recursos

- Comandos de aplicação: `/join`, `/leave`, `/tocar`, `/pause`, `/retomar` e `/parar`.
- Comandos por prefixo: `/clean`, `/expulsar`, `/banir`, `/mute` e `/unmute`.
- Módulo de música em `Discord main/comandos/comando_musica.py`.

Os comandos de moderação por prefixo são mensagens de texto; não estão registrados como comandos de aplicação do Discord.

## 🚀 Executar

Requisitos: Python 3, FFmpeg acessível no PATH, aplicativo de bot no Discord e servidor de teste.

```bash
git clone https://github.com/daviddevdias/Bot-discord-automation.git
cd Bot-discord-automation
python -m venv .venv
```

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r "Discord main/requirements.txt"
$env:DISCORD_TOKEN = "seu-token-novo"
cd "Discord main"
python main.py
```

Ative Message Content Intent no portal do bot para os comandos por prefixo. Convide o aplicativo com os escopos `bot` e `applications.commands` e somente as permissões necessárias. Não é preciso conceder Administrador.

## 🔒 Segurança

O token é lido da variável `DISCORD_TOKEN`; não é carregado automaticamente de um arquivo .env. Tokens anteriormente publicados precisam ser redefinidos no Discord Developer Portal.

Os comandos de moderação verificam permissões do usuário e do bot. `clean` aceita entre 1 e 100 mensagens; `mute` aceita de 1 a 600 segundos e afeta o áudio no servidor.

## Limitações

A reprodução depende do provedor e de FFmpeg. O tratamento de interações e erros ainda precisa de revisão. Os comandos de música recebem URLs externas e ainda não têm lista de destinos permitidos; use o bot em um servidor de teste com acesso restrito até validar esse fluxo.

Não publique caches, logs ou tokens. Remover o token do código atual não o remove dos commits antigos.

