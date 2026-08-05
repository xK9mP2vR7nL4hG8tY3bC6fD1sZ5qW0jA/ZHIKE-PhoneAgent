---
title: Docker 配置
sidebar_label: Docker 配置
sidebar_position: 5
---

# Docker 配置参考

本页是 Docker 部署的速查；操作步骤见[Docker 部署](../guide/deploy-docker.md)。

## 镜像

| 镜像 | 说明 |
| --- | --- |
| `ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent:main` | 跟随 main 分支最新代码，推荐 |
| `ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent:<commit-sha>` | 锁定到特定 commit（如 `abc1234`） |

支持架构：`linux/amd64`、`linux/arm64`。

## 端口

默认监听 `8000`。

- **host 网络模式**（推荐，便于 ADB 发现与二维码配对）：用 `--port` 改端口
  ```bash
  docker run -d --network host \
    ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent:main \
    zhike-phoneagent --host 0.0.0.0 --port 9000 --no-browser
  ```
- **bridge 网络模式**：用 `-p` 映射端口
  ```bash
  docker run -d -p 9000:8000 ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent:main
  ```

## 数据卷

| 容器内路径 | 用途 |
| --- | --- |
| `/root/.config/zhike-phoneagent` | 配置与对话历史（`history/` 下每台设备一个 JSON 文件），**务必持久化** |
| `/app/logs` | 日志与追踪文件 |

```bash
docker run -d --network host \
  -v zhike_phoneagent_config:/root/.config/zhike-phoneagent \
  -v zhike_phoneagent_logs:/app/logs \
  ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent:main
```

## 环境变量

可在启动时预配置模型，免去进界面填写。完整清单见[环境变量](./env-vars.md)。

| 变量 | 说明 |
| --- | --- |
| `ZHIKE_BASE_URL` | 模型 API 地址 |
| `ZHIKE_MODEL_NAME` | 模型名称（默认 `autoglm-phone-9b`） |
| `ZHIKE_API_KEY` | API 密钥 |

> 预构建镜像的 `Dockerfile` 中默认将 `ZHIKE_CORS_ORIGINS` 设为 `"*"`，比源码默认的 `http://localhost:3000` 更宽松。如需限制来源，请在启动时显式覆盖该变量。

## 健康检查

```bash
curl http://localhost:8000/api/health
```

## docker-compose 示例

```yaml
services:
  zhike-phoneagent:
    image: ghcr.io/xk9mp2vr7nl4hg8ty3bc6fd1sz5qw0ja/zhike-phoneagent:main
    network_mode: host
    volumes:
      - zhike_phoneagent_config:/root/.config/zhike-phoneagent
      - zhike_phoneagent_logs:/app/logs
    # environment:
    #   ZHIKE_BASE_URL: https://open.bigmodel.cn/api/paas/v4
    #   ZHIKE_MODEL_NAME: autoglm-phone
    #   ZHIKE_API_KEY: sk-xxxxx
volumes:
  zhike_phoneagent_config:
  zhike_phoneagent_logs:
```

> ⚠️ 二维码配对依赖 mDNS 多播，在 bridge 网络下可能受限，建议用 `--network host`。
