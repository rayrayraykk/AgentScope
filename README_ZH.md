[English](./README.md) | 中文

# AgentScope

更简单地构建基于LLM的多智能体应用。

[![](https://img.shields.io/badge/cs.MA-2402.14034-B31C1C?logo=arxiv&logoColor=B31C1C)](https://arxiv.org/abs/2402.14034)
[![](https://img.shields.io/badge/python-3.9+-blue)](https://pypi.org/project/agentscope/)
[![](https://img.shields.io/badge/pypi-v0.0.3-blue?logo=pypi)](https://pypi.org/project/agentscope/)
[![](https://img.shields.io/badge/Docs-English%7C%E4%B8%AD%E6%96%87-blue?logo=markdown)](https://modelscope.github.io/agentscope/#welcome-to-agentscope-tutorial-hub)
[![](https://img.shields.io/badge/Docs-API_Reference-blue?logo=markdown)](https://modelscope.github.io/agentscope/)
[![](https://img.shields.io/badge/ModelScope-Demos-4e29ff.svg?logo=data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjI0IDEyMS4zMyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KCTxwYXRoIGQ9Im0wIDQ3Ljg0aDI1LjY1djI1LjY1aC0yNS42NXoiIGZpbGw9IiM2MjRhZmYiIC8+Cgk8cGF0aCBkPSJtOTkuMTQgNzMuNDloMjUuNjV2MjUuNjVoLTI1LjY1eiIgZmlsbD0iIzYyNGFmZiIgLz4KCTxwYXRoIGQ9Im0xNzYuMDkgOTkuMTRoLTI1LjY1djIyLjE5aDQ3Ljg0di00Ny44NGgtMjIuMTl6IiBmaWxsPSIjNjI0YWZmIiAvPgoJPHBhdGggZD0ibTEyNC43OSA0Ny44NGgyNS42NXYyNS42NWgtMjUuNjV6IiBmaWxsPSIjMzZjZmQxIiAvPgoJPHBhdGggZD0ibTAgMjIuMTloMjUuNjV2MjUuNjVoLTI1LjY1eiIgZmlsbD0iIzM2Y2ZkMSIgLz4KCTxwYXRoIGQ9Im0xOTguMjggNDcuODRoMjUuNjV2MjUuNjVoLTI1LjY1eiIgZmlsbD0iIzYyNGFmZiIgLz4KCTxwYXRoIGQ9Im0xOTguMjggMjIuMTloMjUuNjV2MjUuNjVoLTI1LjY1eiIgZmlsbD0iIzM2Y2ZkMSIgLz4KCTxwYXRoIGQ9Im0xNTAuNDQgMHYyMi4xOWgyNS42NXYyNS42NWgyMi4xOXYtNDcuODR6IiBmaWxsPSIjNjI0YWZmIiAvPgoJPHBhdGggZD0ibTczLjQ5IDQ3Ljg0aDI1LjY1djI1LjY1aC0yNS42NXoiIGZpbGw9IiMzNmNmZDEiIC8+Cgk8cGF0aCBkPSJtNDcuODQgMjIuMTloMjUuNjV2LTIyLjE5aC00Ny44NHY0Ny44NGgyMi4xOXoiIGZpbGw9IiM2MjRhZmYiIC8+Cgk8cGF0aCBkPSJtNDcuODQgNzMuNDloLTIyLjE5djQ3Ljg0aDQ3Ljg0di0yMi4xOWgtMjUuNjV6IiBmaWxsPSIjNjI0YWZmIiAvPgo8L3N2Zz4K)](https://modelscope.cn/studios?name=agentscope&page=1&sort=latest)

[![](https://img.shields.io/badge/license-Apache--2.0-black)](./LICENSE)
[![](https://img.shields.io/badge/Contribute-Welcome-green)](https://modelscope.github.io/agentscope/tutorial/contribute.html)

如果您觉得我们的工作对您有帮助，请引用我们的[论文](https://arxiv.org/abs/2402.14034)。

欢迎加入我们的社区

| [Discord](https://discord.gg/eYMpfnkG8h) | 钉钉群 |
|---------|----------|
| <img src="https://gw.alicdn.com/imgextra/i1/O1CN01hhD1mu1Dd3BWVUvxN_!!6000000000238-2-tps-400-400.png" width="100" height="100"> | <img src="https://img.alicdn.com/imgextra/i2/O1CN01tuJ5971OmAqNg9cOw_!!6000000001747-0-tps-444-460.jpg" width="100" height="100"> |

## 新闻

- <img src="https://img.alicdn.com/imgextra/i3/O1CN01SFL0Gu26nrQBFKXFR_!!6000000007707-2-tps-500-500.png" alt="new" width="30" height="30"/>**[2024-04-19]** AgentScope现已经支持Llama3！我们提供了面向CPU推理和GPU推理的[脚本](./examples/model_llama3)和[模型配置](./examples/model_llama3)，一键式开启Llama3的探索，在我们的样例中尝试Llama3吧！

- <img src="https://img.alicdn.com/imgextra/i3/O1CN01SFL0Gu26nrQBFKXFR_!!6000000007707-2-tps-500-500.png" alt="new" width="30" height="30"/>**[2024-04-06]** 我们现在发布了**AgentScope** v0.0.3版本！

- <img src="https://img.alicdn.com/imgextra/i3/O1CN01SFL0Gu26nrQBFKXFR_!!6000000007707-2-tps-500-500.png" alt="new" width="30" height="30"/>**[2024-04-06]** 新的样例“[五子棋](./examples/game_gomoku)”，“[与ReAct智能体对话](./examples/conversation_with_react_agent)”，“[与RAG智能体对话](./examples/conversation_with_RAG_agents)”，“[分布式并行搜索](./examples/distributed_search)”上线了！

- <img src="https://img.alicdn.com/imgextra/i3/O1CN01SFL0Gu26nrQBFKXFR_!!6000000007707-2-tps-500-500.png" alt="new" width="30" height="30"/>**[2024-03-19]** 我们现在发布了**AgentScope** v0.0.2版本！在这个新版本中，AgentScope支持了[ollama](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#supported-models)（本地CPU推理引擎），[DashScope](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#supported-models)和[Gemini](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#supported-models) APIs。

- <img src="https://img.alicdn.com/imgextra/i3/O1CN01SFL0Gu26nrQBFKXFR_!!6000000007707-2-tps-500-500.png" alt="new" width="30" height="30"/>**[2024-03-19]** 新的样例“[带有@功能的自主对话](./examples/conversation_with_mentions)”和“[兼容LangChain的基础对话](./examples/conversation_with_langchain)”上线了！

- <img src="https://img.alicdn.com/imgextra/i3/O1CN01SFL0Gu26nrQBFKXFR_!!6000000007707-2-tps-500-500.png" alt="new" width="30" height="30"/>**[2024-03-19]** AgentScope的[中文教程](https://modelscope.github.io/agentscope/zh_CN/index.html)上线了！

- **[2024-02-27]** 我们现在发布了**AgentScope** v0.0.1版本！现在，AgentScope也可以在[PyPI](https://pypi.org/project/agentscope/)上下载

- **[2024-02-14]** 我们在arXiv上发布了论文“[AgentScope: A Flexible yet Robust Multi-Agent Platform](https://arxiv.org/abs/2402.14034)”!

---

## 什么是AgentScope？

AgentScope是一个创新的多智能体开发平台，旨在赋予开发人员使用大模型轻松构建多智能体应用的能力。

- 🤝 **高易用**： AgentScope专为开发人员设计，提供了[丰富的组件](https://modelscope.github.io/agentscope/en/tutorial/204-service.html#), [全面的文档](https://modelscope.github.io/agentscope/zh_CN/index.html)和广泛的兼容性。

- ✅ **高鲁棒**：支持自定义的容错控制和重试机制，以提高应用程序的稳定性。

- 🚀 **分布式**：支持以中心化的方式构建分布式多智能体应用程序。

**支持的模型API**

AgentScope提供了一系列`ModelWrapper`来支持本地模型服务和第三方模型API。

| API                    | Task            | Model Wrapper                                                                                                                   | Configuration                                                                      | Some Supported Models                         |
|------------------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------|
| OpenAI API             | Chat            | [`OpenAIChatWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/openai_model.py)                 |[guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#openai-api)  <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/openai_chat_template.json)       | gpt-4, gpt-3.5-turbo, ...                     |
|                        | Embedding       | [`OpenAIEmbeddingWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/openai_model.py)            | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#openai-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/openai_embedding_template.json)       | text-embedding-ada-002, ...                   |
|                        | DALL·E          | [`OpenAIDALLEWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/openai_model.py)                | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#openai-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/openai_dall_e_template.json)       | dall-e-2, dall-e-3                            |
| DashScope API          | Chat            | [`DashScopeChatWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/dashscope_model.py)           | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#dashscope-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/dashscope_chat_template.json)    | qwen-plus, qwen-max, ...                      |
|                        | Image Synthesis | [`DashScopeImageSynthesisWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/dashscope_model.py) | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#dashscope-api)  <br>[template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/dashscope_image_synthesis_template.json)    | wanx-v1                                       |
|                        | Text Embedding  | [`DashScopeTextEmbeddingWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/dashscope_model.py)  | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#dashscope-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/dashscope_text_embedding_template.json)    | text-embedding-v1, text-embedding-v2, ...     |
|                        | Multimodal      | [`DashScopeMultiModalWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/dashscope_model.py)     | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#dashscope-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/dashscope_multimodal_template.json)    | qwen-vl-max, qwen-vl-chat-v1, qwen-audio-chat |
| Gemini API             | Chat            | [`GeminiChatWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/gemini_model.py)                 | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#gemini-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/gemini_chat_template.json)       | gemini-pro, ...                               |
|                        | Embedding       | [`GeminiEmbeddingWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/gemini_model.py)            | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#gemini-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/gemini_embedding_template.json)       | models/embedding-001, ...                     |
| ollama                 | Chat            | [`OllamaChatWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/ollama_model.py)                 | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#ollama-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/ollama_chat_template.json)       | llama3, llama2, Mistral, ...                  |
|                        | Embedding       | [`OllamaEmbeddingWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/ollama_model.py)            | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#ollama-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/ollama_embedding_template.json)       | llama2, Mistral, ...                          |
|                        | Generation      | [`OllamaGenerationWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/ollama_model.py)           | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#ollama-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/ollama_generate_template.json)       | llama2, Mistral, ...                          |
| Post Request based API | -               | [`PostAPIModelWrapper`](https://github.com/modelscope/agentscope/blob/main/src/agentscope/models/post_model.py)                 | [guidance](https://modelscope.github.io/agentscope/en/tutorial/203-model.html#post-request-api) <br> [template](https://github.com/modelscope/agentscope/blob/main/examples/model_configs_template/postapi_model_config_template.json) | -                                             |

**支持的本地模型部署**

AgentScope支持使用以下库快速部署本地模型服务。

- [ollama (CPU inference)](https://github.com/modelscope/agentscope/blob/main/scripts/README.md#ollama)
- [Flask + Transformers](https://github.com/modelscope/agentscope/blob/main/scripts/README.md#with-transformers-library)
- [Flask + ModelScope](https://github.com/modelscope/agentscope/blob/main/scripts/README.md#with-modelscope-library)
- [FastChat](https://github.com/modelscope/agentscope/blob/main/scripts/README.md#fastchat)
- [vllm](https://github.com/modelscope/agentscope/blob/main/scripts/README.md#vllm)

**支持的服务**

- 网络搜索
- 数据查询
- 数据检索
- 代码执行
- 文件操作
- 文本处理

**样例应用**

- 模型
  - <img src="https://img.alicdn.com/imgextra/i3/O1CN01SFL0Gu26nrQBFKXFR_!!6000000007707-2-tps-500-500.png" alt="new" width="30" height="30"/>[在AgentScope中使用Llama3](./examples/model_llama3)

- 对话
  - [基础对话](./examples/conversation_basic)
  - [带有@功能的自主对话](./examples/conversation_with_mentions)
  - [智能体自组织的对话](./examples/conversation_self_organizing)
  - [兼容LangChain的基础对话](./examples/conversation_with_langchain)
  - [与ReAct智能体对话](./examples/conversation_with_react_agent)
  - [通过对话查询SQL信息](./examples/conversation_nl2sql/)
  - [与RAG智能体对话](./examples/conversation_with_RAG_agents)

- 游戏
  - [五子棋](./examples/game_gomoku)
  - [狼人杀](./examples/game_werewolf)

- 分布式
  - [分布式对话](./examples/distributed_basic)
  - [分布式辩论](./examples/distributed_debate)
  - [分布式并行搜索](./examples/distributed_search)

更多模型API、服务和示例即将推出！

## 安装

AgentScope需要Python 3.9或更高版本。

**_注意：该项目目前正在积极开发中，建议从源码安装AgentScope。_**

### 从源码安装

- 以编辑模式安装AgentScope：

```bash
# 从github拉取源代码
git clone https://github.com/modelscope/agentscope.git
# 以编辑模式安装包
cd agentscope
pip install -e .
```

- 构建分布式多智能体应用需要按照以下方式安装：

```bash
# 在windows上
pip install -e .[distribute]
# 在mac上
pip install -e .\[distribute\]
```

### 使用pip

- 从pip安装的AgentScope

```bash
pip install agentscope
```

## 快速开始

### 配置

AgentScope中，模型的部署和调用是通过`ModelWrapper`实现解耦的。

为了使用这些`ModelWrapper`, 您需要准备如下的模型配置文件：

```python
model_config = {
    # 模型配置的名称，以及使用的模型wrapper
    "config_name": "{your_config_name}",          # 模型配置的名称
    "model_type": "{model_type}",                 # 模型wrapper的类型

    # 用以初始化模型wrapper的详细参数
    # ...
}
```

以OpenAI Chat API为例，模型配置如下：

```python
openai_model_config = {
    "config_name": "my_openai_config",             # 模型配置的名称
    "model_type": "openai_chat",                   # 模型wrapper的类型

    # 用以初始化模型wrapper的详细参数
    "model_name": "gpt-4",                         # OpenAI API中的模型名
    "api_key": "xxx",                              # OpenAI API的API密钥。如果未设置，将使用环境变量OPENAI_API_KEY。
    "organization": "xxx",                         # OpenAI API的组织。如果未设置，将使用环境变量OPENAI_ORGANIZATION。
}
```

关于部署本地模型服务和准备模型配置的更多细节，请参阅我们的[教程](https://modelscope.github.io/agentscope/index.html#welcome-to-agentscope-tutorial-hub)。

### 创建Agent

创建AgentScope内置的`DialogAgent`和`UserAgent`对象.

```python
from agentscope.agents import DialogAgent, UserAgent
import agentscope

# 加载模型配置
agentscope.init(model_configs="./model_configs.json")

# 创建对话Agent和用户Agent
dialog_agent = DialogAgent(name="assistant",
                           model_config_name="my_openai_config")
user_agent = UserAgent()
```

#### 构造对话

在AgentScope中，**Message**是Agent之间的桥梁，它是一个python**字典**（dict），包含两个必要字段`name`和`content`，以及一个可选字段`url`用于本地文件（图片、视频或音频）或网络链接。

```python
from agentscope.message import Msg

x = Msg(name="Alice", content="Hi!")
x = Msg("Bob", "What about this picture I took?", url="/path/to/picture.jpg")
```

使用以下代码开始两个Agent（dialog_agent和user_agent）之间的对话：

```python
x = None
while True:
  x = dialog_agent(x)
  x = user_agent(x)
  if x.content == "exit": # 用户输入"exit"退出对话
    break
```

### AgentScope前端

AgentScope
提供了一个易于使用的运行时用户界面，能够在前端显示多模态输出，包括文本、图像、音频和视频。要启动前端，需要先安装AgentScope完整版本。

```
# On windows
pip install -e .[full]
# On mac
pip install -e .\[full\]
```

然后运行

```
as_studio  path/to/your/script.py
```

前端就会在端口 `localhost:xxxx`上启动，打开后就能看到类似下图的界面：
![](https://gw.alicdn.com/imgextra/i3/O1CN01X673v81WaHV1oCxEN_!!6000000002804-0-tps-2992-1498.jpg)
为了能使用该前端功能，你需要在代码中实现`main`函数。更多详情请参见 [src/agentscope/web/README.md](src/agentscope/web/README.md)。

## 教程

- [快速上手](https://modelscope.github.io/agentscope/zh_CN/tutorial/quick_start.html)
  - [关于AgentScope](https://modelscope.github.io/agentscope/zh_CN/tutorial/101-agentscope.html)
  - [安装](https://modelscope.github.io/agentscope/zh_CN/tutorial/102-installation.html)
  - [快速开始](https://modelscope.github.io/agentscope/zh_CN/tutorial/103-example.html)
  - [创建您的第一个应用](https://modelscope.github.io/agentscope/zh_CN/tutorial/104-usecase.html)
  - [日志和WebUI](https://modelscope.github.io/agentscope/zh_CN/tutorial/105-logging.html#)
- [进阶使用](https://modelscope.github.io/agentscope/zh_CN/tutorial/advance.html)
  - [定制你自己的Agent](https://modelscope.github.io/agentscope/zh_CN/tutorial/201-agent.html)
  - [Pipeline和MsgHub](https://modelscope.github.io/agentscope/zh_CN/tutorial/202-pipeline.html)
  - [模型](https://modelscope.github.io/agentscope/zh_CN/tutorial/203-model.html)
  - [服务函数](https://modelscope.github.io/agentscope/zh_CN/tutorial/204-service.html)
  - [记忆](https://modelscope.github.io/agentscope/zh_CN/tutorial/205-memory.html)
  - [提示工程](https://modelscope.github.io/agentscope/zh_CN/tutorial/206-prompt.html)
  - [监控器](https://modelscope.github.io/agentscope/zh_CN/tutorial/207-monitor.html)
  - [分布式](https://modelscope.github.io/agentscope/zh_CN/tutorial/208-distribute.html)
- [参与贡献](https://modelscope.github.io/agentscope/zh_CN/tutorial/contribute.html)
  - [加入AgentScope社区](https://modelscope.github.io/agentscope/zh_CN/tutorial/301-community.html)
  - [贡献到AgentScope](https://modelscope.github.io/agentscope/zh_CN/tutorial/302-contribute.html)

## License

AgentScope根据Apache License 2.0发布。

## 贡献

欢迎参与到AgentScope的构建中！

我们提供了一个带有额外 pre-commit 钩子以执行检查的开发者版本，与官方版本相比：

```bash
# 对于windows
pip install -e .[dev]
# 对于mac
pip install -e .\[dev\]
# 安装pre-commit钩子
pre-commit install
```

请参阅我们的[贡献指南](https://modelscope.github.io/agentscope/zh_CN/tutorial/302-contribute.html)了解更多细节。

## 引用

如果您觉得我们的工作对您的研究或应用有帮助，请引用[我们的论文](https://arxiv.org/abs/2402.14034)。

```
@article{agentscope,
  author  = {Dawei Gao and
             Zitao Li and
             Weirui Kuang and
             Xuchen Pan and
             Daoyuan Chen and
             Zhijian Ma and
             Bingchen Qian and
             Liuyi Yao and
             Lin Zhu and
             Chen Cheng and
             Hongzhu Shi and
             Yaliang Li and
             Bolin Ding and
             Jingren Zhou},
  title   = {AgentScope: A Flexible yet Robust Multi-Agent Platform},
  journal = {CoRR},
  volume  = {abs/2402.14034},
  year    = {2024},
}
```





## 贡献者 ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/qbc2016"><img src="https://avatars.githubusercontent.com/u/22984042?v=4?s=100" width="100px;" alt="qbc"/><br /><sub><b>qbc</b></sub></a><br /><a href="#infra-qbc2016" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/rayrayraykk/AgentScope/commits?author=qbc2016" title="Tests">⚠️</a> <a href="https://github.com/rayrayraykk/AgentScope/commits?author=qbc2016" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
