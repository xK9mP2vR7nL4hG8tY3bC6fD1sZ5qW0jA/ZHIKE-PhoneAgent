# ZHIKE-PhoneAgent

**AI-powered Android automation and phone agent platform** — vision models understand the screen, plan steps, and execute actions automatically, turning phone tasks into fully automated flows.

[中文 README](README.md)

---

## Key Features

- **Phone Agent**: a vision model perceives the phone screen and completes the full loop of understanding → planning → observing → acting
- **Layered Agent Mode**: a decision model (planning layer) works with a phone vision execution model (execution layer) for long, complex flows
- **Multiple Agent Types**: GLM, Qwen, MAI-UI and more
- **Realtime Screen Mirroring**: low-latency device streaming and remote control powered by scrcpy
- **Task Scheduler**: built-in scheduler for recurring automation tasks
- **Desktop App**: Electron client for Windows / macOS / Linux, ready out of the box
- **Docker Deployment**: one command to run the server
- **MCP Server**: built-in MCP server callable by other AI tools

## Download

| Platform | Download | Notes |
| --- | --- | --- |
| 🪟 Windows (x64) | [Portable EXE](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) · [Setup EXE](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | Windows 10/11 |
| 🍎 macOS (Apple Silicon) | [DMG](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | M-series Macs |
| 🍎 macOS (Intel) | [DMG](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | Intel Macs |
| 🐧 Linux (x64) | [AppImage](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) · [tar.gz](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | Universal formats |

### Windows Portable vs Setup

| | Portable (`ZHIKE-PhoneAgent-x.x.x-x64.exe`) | Setup (`ZHIKE-PhoneAgent-Setup-x.x.x-x64.exe`) |
| --- | --- | --- |
| Installation | None, double-click to run | Guided wizard, custom install directory |
| Shortcuts | Not created | Desktop and Start Menu shortcuts |
| Uninstall | Delete the file | Via Windows "Apps & Features" |
| Best for | Temporary use, USB carry | Recommended for long-term use |

## Connect an Android Device

1. Enable **Developer options** and **USB debugging** on the phone
2. Connect via USB, or use wireless ADB on the same network
3. Start ZHIKE-PhoneAgent — the device appears in the device list automatically
4. Confirm the RSA authorization prompt on the phone on first connection

> If ADB is not installed, ZHIKE-PhoneAgent automatically downloads Android
> Platform Tools to `~/.cache/zhike-phoneagent/platform-tools/`.

## Model API Configuration

ZHIKE-PhoneAgent talks to third-party model services through OpenAI-compatible
endpoints. On first launch, open the **Settings** page and fill in:

| Field | Description | Example |
| --- | --- | --- |
| Base URL | OpenAI-compatible endpoint of the model service | `https://open.bigmodel.cn/api/paas/v4` |
| Model Name | Third-party model service ID | See "Third-Party Models" below |
| API Key | Key issued by the model provider | From the provider console |

Built-in provider presets (Zhipu BigModel, ModelScope) are available, or switch
to **Custom** and point to a self-hosted vLLM/SGLang service.

## Docker Deployment

```bash
curl -O https://raw.githubusercontent.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/main/docker-compose.yml
docker compose up -d
```

Image: `ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent`

- Config volume: `zhike_phoneagent_config` (mounted at `/root/.config/zhike-phoneagent`)
- Log volume: `zhike_phoneagent_logs` (mounted at `/app/logs`)
- Environment variable prefix: `ZHIKE_` (e.g. `ZHIKE_BASE_URL`, `ZHIKE_MODEL_NAME`, `ZHIKE_API_KEY`)
- On Linux, `network_mode: host` is recommended for mDNS and USB device support

## Development

Requirements: Python ≥ 3.11, [uv](https://docs.astral.sh/uv/), Node.js, pnpm

```bash
git clone https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent.git
cd ZHIKE-PhoneAgent

# Install Python dependencies (dev + droidrun extra)
uv sync --dev --extra droidrun

# Run the backend dev server
uv run zhike-phoneagent

# Frontend dev server (another terminal)
cd frontend
pnpm install
pnpm dev
```

## Local Build

```bash
# One-step Electron desktop build (frontend + backend + installers)
uv run python scripts/build_electron.py --publish never
```

Artifacts land in `electron/dist/`:

- `ZHIKE-PhoneAgent-x.x.x-x64.exe` — Windows portable
- `ZHIKE-PhoneAgent-Setup-x.x.x-x64.exe` — Windows installer

Backend-only packaging:

```bash
uv run pyinstaller scripts/zhike-phoneagent.spec
# Output: scripts/dist/zhike-phoneagent/
```

## GitHub Actions Release

1. Bump version: `uv run python scripts/release.py --version x.y.z` (`--dry-run` supported)
2. Push commit and tag: `git push && git push origin vx.y.z`
3. The `Release` workflow builds the Python package, creates the GitHub Release, pushes the Docker image to GHCR, and uploads Windows/macOS/Linux Electron artifacts
4. PyPI publishing is disabled by default; after configuring a Trusted Publisher, set the repository variable `ENABLE_PYPI_PUBLISH=true` to enable it

## FAQ

**Q: The device list is empty?**
Make sure USB debugging is enabled and `adb devices` shows the device; confirm the authorization prompt on the phone on first connection.

**Q: The backend fails to start?**
Check `zhike_phoneagent_YYYY-MM-DD.log` in the logs directory; use `--port` if the port is occupied.

**Q: Where is the config file?**
Desktop: `%APPDATA%/ZHIKE-PhoneAgent/` (Windows); CLI/Docker: `~/.config/zhike-phoneagent/config.json`.

**Q: How is auto-update handled?**
Auto-update only checks this repository's GitHub Releases; no third-party update servers are contacted.

## Third-Party Models

ZHIKE-PhoneAgent is a **model-agnostic** client platform and does not bundle or
develop any large model itself. IDs such as `autoglm-phone`, `AutoGLM-Phone-9B`
and `ZhipuAI/AutoGLM-Phone-9B` shown in the UI or docs are **third-party model
service IDs**, provided and operated by their respective providers (e.g. Zhipu,
ModelScope, the Hugging Face community). See
[docs/BRAND_COMPATIBILITY_ALLOWLIST.md](docs/BRAND_COMPATIBILITY_ALLOWLIST.md)
for the complete list.

This project builds upon the technology stack of the upstream open-source
project [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM). Thanks to the
zai-org team for their open-source work.

## Security and Compliance

- API keys are stored only in the local config directory and never uploaded to third-party servers
- Automation only runs on your own explicitly connected devices
- Comply with the terms of your model provider and of the target apps/platforms
- Do not use this tool for unauthorized device control or any illegal purpose

## License

Licensed under [Apache-2.0](LICENSE). This is a modified and rebranded
derivative version — see [CHANGES_FROM_UPSTREAM.md](CHANGES_FROM_UPSTREAM.md)
for the change summary and [NOTICE](NOTICE) for attributions.
