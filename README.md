
![](https://i.imgur.com/IBrUrab.png)
<div align="center">

![Status](https://img.shields.io/badge/status-v0.5.0-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![discord.py](https://img.shields.io/badge/discord.py-latest-blue.svg)

</div>

A Discord bot built using **discord.py**, created for learning the basics of bot development.

> [!NOTE]
> This project is currently in development and is mainly intended as an initial template/skeleton for a minimal working Discord bot.

# Setup
Bot requires Python 3.8+ to run.
### Install the dependencies
```bash
pip install -r requirements.txt
```
> [!TIP]
> It is recommended to use a virtual environment.

### Setting up the bot properties
Set .env file with the values in `.env.example` You can get your bot token from [discord developer portal](https://discord.com/developers/applications "Discord Developer Portal").

```python
BOT_TOKEN = your_token_here
BOT_STATUS = "Your Status Here"
GUILD_ID = your_test_server_id
OWNER_ID = your_user_id
```

# How to run
```
python main.py
```
### Docker

```bash
# detached mode
docker compose up --build -d

# attached mode
docker compose up --build
```

To stop:

```bash
docker compose down
```
# Project Structure

```
mamon/
├── cogs/           # Command modules loaded at startup
│   ├── github.py
│   ├── help.py
│   ├── info.py
│   └── moderation.py
├── core/
│   └── uptime.py   # Uptime tracking
├── utils/          # Shared helpers
│   ├── embed.py    # Error and success embed builders
│   ├── checks.py   # Permission and hierarchy validation
│   └── __init__.py
├── config.py       # Env variable loading
├── settings.py     # Bot constants (name, version, colors)
├── main.py         # Entry point
├── Dockerfile
└── docker-compose.yml
```

# Commands

## Info
| Command | Description |
|---|---|
| `/info` | Bot info and stats |
| `/serverinfo` | Server details |
| `/userinfo [user]` | User details |
| `/avatar [user]` | Get a user's avatar |
| `/ping` | Bot latency and uptime |

## Moderation
| Command | Description |
|---|---|
| `/kick <user> [reason]` | Kick a member |
| `/ban <user> [reason]` | Ban a member |
| `/unban <user_id> [reason]` | Unban a user by ID |
| `/mute <user> <minutes> [reason]` | Timeout a member (max 40320 min) |
| `/unmute <user> [reason]` | Remove a timeout |
| `/purge <amount>` | Bulk delete messages (max 100) |

## Other
| Command | Description |
|---|---|
| `/help` | List all commands |