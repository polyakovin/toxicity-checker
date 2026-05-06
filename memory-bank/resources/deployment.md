---
updated: 2026-05-07
---
# Deployment

## Production Server
| Property | Value |
|---|---|
| Provider | Timeweb Cloud |
| Type | VPS (Cloud Server) |
| Server ID | 7825384 |
| IP | 188.225.39.70 |
| Region | ru-1 (Saint Petersburg) |
| OS | Ubuntu 24.04 |
| Preset | 2573 (1 CPU / 1GB RAM / 15GB SSD / 149₽/mo) |
| SSH | `ssh root@188.225.39.70` (key: ~/.ssh/id_ed25519) |

## Project on server
| Property | Value |
|---|---|
| Path | `/opt/check-toxicity` |
| Run | Docker Compose (service: `bot`) |
| Env | `.env` at project root (BOT_TOKEN, ADMIN_IDS) |
| DB | Volume-mounted `./telegram_bot/db:/app/db` |
| Restart | `unless-stopped` |

## Common commands
```bash
# Check bot logs
ssh root@188.225.39.70 "cd /opt/check-toxicity && docker compose logs -f"

# Restart bot
ssh root@188.225.39.70 "cd /opt/check-toxicity && docker compose restart"

# Rebuild and redeploy
ssh root@188.225.39.70 "cd /opt/check-toxicity && docker compose down && docker compose up -d --build"

# Check status
ssh root@188.225.39.70 "cd /opt/check-toxicity && docker compose ps"
```

## twc CLI quick reference
```bash
# Install
pip install twc-cli

# Configure (API token from https://timeweb.cloud/my/api-keys)
twc config

# List servers
twc server list

# Get server info
twc server get 7825384

# Server status (exit 0 if on)
twc server get --status 7825384

# List presets (cheapest in ru-1)
twc server list-presets -f location:ru-1

# Create server
twc server create --name NAME --image ubuntu-24.04 --preset-id PRESET --ssh-key KEY_ID

# Upload SSH key
twc ssh-key new --name NAME ~/.ssh/id_ed25519.pub
```

## Deployment workflow
1. Push changes to git
2. `ssh root@188.225.39.70 "cd /opt/check-toxicity && git pull && docker compose up -d --build"`
3. Or rsync directly: `rsync -avz --exclude='.git' --exclude='__pycache__' . root@188.225.39.70:/opt/check-toxicity/`
4. Check logs to confirm
