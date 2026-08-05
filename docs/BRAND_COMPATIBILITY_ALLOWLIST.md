# 品牌兼容性允许清单（BRAND_COMPATIBILITY_ALLOWLIST）

本文件登记代码库中**被允许保留**的 `AutoGLM` / `autoglm` 字符串。
这些字符串全部是**第三方模型服务的真实标识符**或**上游开源项目名称**，
不属于本产品（ZHIKE-PhoneAgent）的品牌内容，因此不在品牌替换范围内。

> 本文件不得用于保留旧产品品牌。任何新的 `AutoGLM` / `autoglm` 字符串
> 若不属于下表所列类别，必须先修改或登记后才能合入。

## 一、允许保留的标识符

| 标识符 | 性质 | 不能修改的原因 |
| --- | --- | --- |
| `autoglm-phone` | 智谱 BigModel 平台的真实模型 ID | 服务端按此 ID 路由模型，修改会导致 API 调用失败 |
| `autoglm-phone-9b` | 自部署 / 自定义端点的常用模型 ID | 服务端按此 ID 路由模型，修改会导致 API 调用失败 |
| `AutoGLM-Phone-9B` | Hugging Face 模型名称 | 第三方模型仓库标识，非本项目资产 |
| `AutoGLM-Phone-9B-Multilingual` | Hugging Face 模型名称（多语言版） | 第三方模型仓库标识，非本项目资产 |
| `ZhipuAI/AutoGLM-Phone-9B` | ModelScope 模型仓库 ID | 第三方平台仓库路径，修改会导致下载/调用失败 |
| `zai-org/AutoGLM-Phone-9B` | Hugging Face 模型仓库 ID | 第三方平台仓库路径，修改会导致下载/调用失败 |
| `Open-AutoGLM` / `Open AutoGLM` | 上游开源项目名称（zai-org/Open-AutoGLM） | 合法的上游归属与兼容性说明，非本产品品牌 |

## 二、UI 展示约定

1. 普通模式下，UI 只显示「ZHIKE 手机执行模型」「手机视觉执行模型」或服务商名称
   （如「智谱 BigModel」「ModelScope」），不展示上述模型 ID。
2. 真实模型 ID 仅出现在：高级配置项（模型名称输入框）、服务商适配层
   （`frontend/src/routes/chat.tsx` 的 `VISION_PRESETS`）、后端默认配置
   （`zhike_phoneagent/config.py`、`schemas.py`、`config_manager.py`、`__main__.py`）。
3. README 与文档中引用上述 ID 时，均作为「第三方模型服务 ID」说明，
   不得称为 ZHIKE 自研模型。
4. 不得向任何服务端发送虚构的 `zhike-phoneagent` 模型 ID。

## 三、逐条登记（文件、行号、用途）

### 后端默认配置（默认模型 ID，服务商适配层）

| 文件 | 行号 | 内容 | 用途 |
| --- | --- | --- | --- |
| `zhike_phoneagent/__main__.py` | 14 | `DEFAULT_MODEL_NAME = "autoglm-phone-9b"` | CLI 默认模型 ID |
| `zhike_phoneagent/config.py` | 24, 35 | `model_name` 文档与默认值 `autoglm-phone-9b` | 配置模型默认值 |
| `zhike_phoneagent/config_manager.py` | 72, 246 | 默认配置 `autoglm-phone-9b` | 配置管理器默认值 |
| `zhike_phoneagent/schemas.py` | 303 | `model_name: str = "autoglm-phone-9b"` | API Schema 默认值 |
| `docker-compose.yml` | 18 | 注释示例 `ZHIKE_MODEL_NAME=autoglm-phone` | 部署示例中的第三方模型 ID |

### 上游项目引用（兼容性说明注释）

| 文件 | 行号 | 内容 | 用途 |
| --- | --- | --- | --- |
| `zhike_phoneagent/model/message_builder.py` | 41, 83 | `Open-AutoGLM` | 说明输入布局与上游官方实现一致 |
| `zhike_phoneagent/agents/glm/async_agent.py` | 61 | `Open-AutoGLM` | 同上 |
| `zhike_phoneagent/agents/qwen/async_agent.py` | 70 | `Open-AutoGLM` | 同上 |

### 前端服务商适配层与高级配置

| 文件 | 行号 | 内容 | 用途 |
| --- | --- | --- | --- |
| `frontend/src/routes/chat.tsx` | 59, 67, 75 | `VISION_PRESETS` 中 `autoglm-phone` / `ZhipuAI/AutoGLM-Phone-9B` / `autoglm-phone-9b` | 服务商预设的真实模型 ID |
| `frontend/src/routes/chat.tsx` | 349, 655 | 高级配置回退值与输入框占位符 `autoglm-phone-9b` | 高级模型名称配置项 |

### 测试（与默认配置一致的测试夹具）

| 文件 | 行号 | 内容 | 用途 |
| --- | --- | --- | --- |
| `tests/test_devices_api.py` | 198, 208 | `autoglm-phone-9b` | 断言默认模型 ID 透传 |
| `tests/test_agents_chat_config_api.py` | 138, 298, 530, 557 | `autoglm-phone-9b` | 配置 API 测试夹具 |
| `tests/test_layered_max_turns_config.py` | 59, 103, 117 | `autoglm-phone-9b` | 分层代理配置测试夹具 |
| `tests/test_manager_device_coverage.py` | 241 | `autoglm-phone-9b` | 设备配置覆盖测试 |
| `tests/test_glm_async_agent.py` | 5 | 注释中引用 `autoglm-phone` | 历史行为说明注释 |

### 文档（第三方模型服务 ID 说明）

| 文件 | 说明 |
| --- | --- |
| `README.md` / `README_EN.md` | 模型配置章节引用第三方模型服务 ID，已明确标注为第三方服务 |
| `AI_USAGE.md` | AI 使用说明中的第三方模型 ID 示例 |
| `docs/docs/guide/configure-model.md`、`docs/docs/guide/troubleshooting.md` | 配置与排障文档中的第三方模型 ID |
| `docs/docs/reference/cli.md`、`docs/docs/reference/env-vars.md`、`docs/docs/reference/docker.md` | 参考文档中的默认值与示例 |
| `docs/docs/explanation/modes.md`、`layered-agent.md`、`layered-agent-analysis.md`、`agent-types.md` | 架构说明中引用上游 Open-AutoGLM 项目 |

## 四、品牌扫描排除项

执行最终品牌扫描时，以下文件按任务规定排除，原因如下：

| 排除文件 | 排除原因 |
| --- | --- |
| `LICENSE` | Apache-2.0 许可证正文，依法不得修改 |
| `NOTICE` | 归属声明文件，记录上游版权，必须保留原始归属 |
| `CHANGES_FROM_UPSTREAM.md` | 衍生版本修改说明，按许可证要求记录修改事实，需提及原项目名 |
| `docs/BRAND_COMPATIBILITY_ALLOWLIST.md` | 本文件，登记合法保留的第三方标识符 |
