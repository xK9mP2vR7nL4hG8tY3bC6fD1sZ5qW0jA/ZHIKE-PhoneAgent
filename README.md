# ZHIKE-PhoneAgent

**AI 驱动的 Android 手机自动化与智能体平台** —— 通过视觉模型理解屏幕、规划步骤并自动执行操作，让手机任务实现全自动化。

[English README](README_EN.md)

---

## 核心功能

- **手机智能体**：视觉模型直接理解手机屏幕，完成「理解任务 → 规划步骤 → 观察屏幕 → 执行动作」的完整闭环
- **分层代理模式**：决策模型（规划层）+ 手机视觉执行模型（执行层）协同工作，适合长链路复杂任务
- **多种 Agent 类型**：支持 GLM、Qwen、MAI-UI 等多种 Agent 实现
- **实时屏幕投屏**：基于 scrcpy 的低延迟设备画面串流与远程操控
- **任务调度**：内置定时任务调度器，支持周期性自动化任务
- **桌面应用**：Windows / macOS / Linux 全平台 Electron 客户端，开箱即用
- **Docker 部署**：一条命令完成服务端部署
- **MCP 服务**：内置 MCP Server，可被其他 AI 工具调用

## 下载

| 平台 | 下载 | 说明 |
| --- | --- | --- |
| 🪟 Windows (x64) | [便携版 EXE](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) · [安装版 EXE](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | 适用于 Windows 10/11 |
| 🍎 macOS (Apple Silicon) | [DMG](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | 适用于 M 系列芯片 Mac |
| 🍎 macOS (Intel) | [DMG](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | 适用于 Intel Mac |
| 🐧 Linux (x64) | [AppImage](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) · [tar.gz](https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/releases/latest) | 通用格式，支持主流发行版 |

### Windows 便携版与安装版的区别

| | 便携版（`ZHIKE-PhoneAgent-x.x.x-x64.exe`） | 安装版（`ZHIKE-PhoneAgent-Setup-x.x.x-x64.exe`） |
| --- | --- | --- |
| 安装过程 | 无需安装，双击即用 | 向导式安装，可自定义安装目录 |
| 快捷方式 | 不创建 | 自动创建桌面与开始菜单快捷方式 |
| 卸载 | 直接删除文件 | 通过系统「应用与功能」卸载 |
| 适用场景 | 临时使用、U 盘携带 | 长期使用的推荐方式 |

## Android 设备连接

1. 在手机上开启 **开发者选项** 和 **USB 调试**
2. 通过 USB 连接电脑，或在同一局域网下使用无线 ADB
3. 启动 ZHIKE-PhoneAgent，设备会自动出现在设备列表中
4. 首次连接时在手机上确认 RSA 授权弹窗

> 如果系统未安装 ADB，ZHIKE-PhoneAgent 会自动下载 Android Platform Tools
> 到 `~/.cache/zhike-phoneagent/platform-tools/`，无需手动配置。

## 模型 API 配置

ZHIKE-PhoneAgent 通过 OpenAI 兼容接口调用第三方模型服务。首次启动后在
**设置页** 填写以下三项：

| 配置项 | 说明 | 示例 |
| --- | --- | --- |
| Base URL | 模型服务的 OpenAI 兼容端点 | `https://open.bigmodel.cn/api/paas/v4` |
| Model Name | 第三方模型服务 ID | 见下方「第三方模型说明」 |
| API Key | 模型服务商颁发的密钥 | 在服务商控制台获取 |

常用服务商预设已内置（智谱 BigModel、ModelScope），也可以切换为
**自定义** 并指向自部署的 vLLM/SGLang 服务。

## Docker 部署

```bash
curl -O https://raw.githubusercontent.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent/main/docker-compose.yml
docker compose up -d
```

镜像地址：`ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent`

- 配置持久化卷：`zhike_phoneagent_config`（挂载到 `/root/.config/zhike-phoneagent`）
- 日志持久化卷：`zhike_phoneagent_logs`（挂载到 `/app/logs`）
- 环境变量前缀：`ZHIKE_`（如 `ZHIKE_BASE_URL`、`ZHIKE_MODEL_NAME`、`ZHIKE_API_KEY`）
- Linux 推荐使用 `network_mode: host` 以支持 mDNS 与 USB 设备

## 源码开发

环境要求：Python ≥ 3.11、[uv](https://docs.astral.sh/uv/)、Node.js、pnpm

```bash
git clone https://github.com/xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent.git
cd ZHIKE-PhoneAgent

# 安装 Python 依赖（含开发依赖与 droidrun 可选依赖）
uv sync --dev --extra droidrun

# 启动后端开发服务
uv run zhike-phoneagent

# 前端开发（另一个终端）
cd frontend
pnpm install
pnpm dev
```

## 本地构建

```bash
# 一键构建 Electron 桌面应用（前端 + 后端 + 安装包）
uv run python scripts/build_electron.py --publish never
```

构建产物位于 `electron/dist/`：

- `ZHIKE-PhoneAgent-x.x.x-x64.exe` —— Windows 便携版
- `ZHIKE-PhoneAgent-Setup-x.x.x-x64.exe` —— Windows 安装版

单独打包后端：

```bash
uv run pyinstaller scripts/zhike-phoneagent.spec
# 输出：scripts/dist/zhike-phoneagent/
```

## GitHub Actions 发布

1. 更新版本：`uv run python scripts/release.py --version x.y.z`（支持 `--dry-run` 预演）
2. 推送提交与标签：`git push && git push origin vx.y.z`
3. `Release` 工作流自动完成：Python 包构建 → GitHub Release → Docker 镜像推送 GHCR → Windows/macOS/Linux Electron 产物上传
4. PyPI 发布默认禁用；配置 Trusted Publisher 后，在仓库 Variables 中设置 `ENABLE_PYPI_PUBLISH=true` 启用

## 常见问题

**Q: 设备列表为空？**
确认 USB 调试已开启，执行 `adb devices` 能看到设备；首次连接需在手机上确认授权。

**Q: 后端启动失败？**
查看日志目录中的 `zhike_phoneagent_YYYY-MM-DD.log`；端口被占用时可使用 `--port` 指定其他端口。

**Q: 配置文件在哪里？**
桌面端：`%APPDATA%/ZHIKE-PhoneAgent/`（Windows）；命令行/Docker：`~/.config/zhike-phoneagent/config.json`。

**Q: 如何关闭自动更新？**
自动更新仅检查本仓库 Releases；不访问任何第三方更新服务器。

## 第三方模型说明

ZHIKE-PhoneAgent 是**模型无关**的客户端平台，自身不内置、不研发任何大模型。
界面与文档中出现的 `autoglm-phone`、`AutoGLM-Phone-9B`、`ZhipuAI/AutoGLM-Phone-9B`
等均为**第三方模型服务 ID**，由相应模型服务商（如智谱、ModelScope、Hugging Face
社区）提供和运营。完整清单见
[docs/BRAND_COMPATIBILITY_ALLOWLIST.md](docs/BRAND_COMPATIBILITY_ALLOWLIST.md)。

本项目基于上游开源项目 [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM)
的技术体系构建，感谢 zai-org 团队的开源工作。

## 安全和合规说明

- API Key 仅存储在本机配置目录，不会上传到任何第三方服务器
- 自动化操作仅作用于用户明确连接的自有设备
- 请遵守所用模型服务商的使用条款，以及目标应用/平台的服务条款
- 请勿将本工具用于未经授权的设备控制或任何违法用途

## 开源许可

本项目基于 [Apache-2.0](LICENSE) 开源。本项目是经过修改和重新品牌化的衍生版本，
修改说明见 [CHANGES_FROM_UPSTREAM.md](CHANGES_FROM_UPSTREAM.md)，归属声明见
[NOTICE](NOTICE)。
