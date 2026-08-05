# CHANGES_FROM_UPSTREAM

本项目是经过修改和重新品牌化的衍生版本。
This project is a modified and rebranded derivative version.

- 上游项目 / Upstream: [AutoGLM-GUI](https://github.com/suyiiyii/AutoGLM-GUI)（Apache-2.0）
- 修改时间 / Modification date: 2026
- 修改方 / Modified by: ZHIKE

## 修改范围 / Summary of Modifications

修改包括产品名称、Python 包名、模块路径、前端界面、Electron 桌面程序、
安装资源、Docker 配置和发布流程。具体如下：

### 品牌与命名 / Branding & Naming

- 产品名称：`AutoGLM-GUI` → `ZHIKE-PhoneAgent`（简称 `ZHIKE`）
- Python 模块目录：`AutoGLM_GUI` → `zhike_phoneagent`
- Python 分发包与控制台命令：`autoglm-gui` → `zhike-phoneagent`
- PyInstaller spec：`autoglm.spec` → `zhike-phoneagent.spec`
- Electron npm 包名：→ `zhike-phoneagent-desktop`
- Windows App ID：`com.autoglm.gui` → `com.zhike.phoneagent`
- 环境变量前缀：`AUTOGLM_` → `ZHIKE_`
- 配置目录：`~/.config/autoglm` → `~/.config/zhike-phoneagent`
- 日志文件前缀：`autoglm_` → `zhike_phoneagent_`
- Docker volumes：`autoglm_config` / `autoglm_logs` → `zhike_phoneagent_config` / `zhike_phoneagent_logs`
- 前端 localStorage / sessionStorage 键前缀统一为 `zhike-phoneagent-*`

### 桌面程序与安装资源 / Desktop & Installer

- 替换全部应用图标、favicon、NSIS 安装封面（installerHeader/installerSidebar/uninstallerSidebar）为 ZHIKE 品牌资源
- 新增 Splash 启动页（`electron/splash.html`、`electron/splash-logo.png`）
- Windows 安装包、便携包、快捷方式、卸载程序名称统一为 `ZHIKE-PhoneAgent`
- 版本号统一重置为 `1.0.0`

### 发布与基础设施 / Release & Infrastructure

- GitHub Release、自动更新、Docker 镜像全部指向
  `xK9mP2vR7nL4hG8tY3bC6fD1sZ5qW0jA/ZHIKE-PhoneAgent`
- GHCR 镜像：`ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent`
- PyPI 发布默认禁用（仓库变量 `ENABLE_PYPI_PUBLISH` 控制）
- Linux `deb` 构建暂时移除（待 ZHIKE 官方维护者邮箱配置后恢复）
- 重写 README.md / README_EN.md；新增 NOTICE 与本文件；
  新增 docs/BRAND_COMPATIBILITY_ALLOWLIST.md

### 保留内容 / What Was Preserved

- `LICENSE`（Apache-2.0 正文）未做任何修改
- 源文件中已有的版权、专利、商标和第三方归属声明全部保留
- 第三方模型服务的真实模型 ID（如 `autoglm-phone`、`AutoGLM-Phone-9B`）
  出于服务互操作性保留，详见 docs/BRAND_COMPATIBILITY_ALLOWLIST.md
