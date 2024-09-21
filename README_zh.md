# 智能语音助手系统

## 项目概述

这是一个基于关键词检测、语音识别、语音合成和对话生成的智能语音助手系统。该系统能够通过特定的唤醒词（如"hey bro"）启动与用户的语音对话，并利用先进的自然语言处理技术提供智能回复。

## 主要功能

1. **关键词检测**：使用Porcupine实时监听唤醒词，启动对话。
2. **语音录制和检测**：采用WebRTC VAD进行语音活动检测，录制有效语音片段。
3. **语音识别（ASR）**：使用SenseVoice Small模型将录制的语音转换为文本。
4. **对话生成**：调用Ollama API（兼容OpenAI API），根据上下文生成助手的文本回复。
5. **语音合成（TTS）**：将助手的回复通过语音合成输出，模拟人声对话。
6. **对话历史保存**：定期将对话内容保存为JSON文件，便于后续分析。

## 技术栈

- Python
- Porcupine（关键词检测）
- WebRTC VAD（语音活动检测）
- SenseVoice Small（语音识别）
- Ollama API（对话生成）
- GPT-SoVITS（语音合成）
- PyAudio, NumPy, SciPy（音频处理）

### TTS部分

- 本项目基于GPT-Sovits-v2，感谢开源社区工作者的贡献！

#### GPT-SoVITS TTS 项目

这是一个基于GPT-SoVITS API的文本到语音（TTS）项目。该项目允许用户根据不同的情感生成和播放语音，使用预定义的参考音频来影响输出的语音风格。

##### 功能特点

- 支持多种情感的语音生成（高兴、抑郁、激动、平静、纠结）
- 使用参考音频来控制语音风格
- 实时生成并播放WAV格式的音频文件
- 可自定义文本输入和输出文件名
- 提供TTS处理时间统计
- 可以添加一个情感识别模型来决定参考音频，从而控制音频合成情感(to do)

## 使用指南

1. 克隆仓库：
- git clone https://github.com/HaxxorCialtion/ASR_LLM_TTS_py.git

- cd intelligent-voice-assistant


2. 安装依赖：
- pip install -r requirements.txt


3. 准备必要的API密钥和模型：
- 获取Porcupine API密钥
- 下载SenseVoice Small模型文件
- 确保Ollama API服务已经运行
- 开启GPT-Sovits API服务

4. 配置系统：
- 在脚本中填入Porcupine API密钥
- 设置ASR模型路径
- 配置Ollama API端点（默认为本地）
- 配置GPT-sovits 模型和参考音频

## 使用方法

1. 运行主脚本：
python main.py

2. 等待系统提示"Listening for wake word..."

3. 说出唤醒词（默认为"hey bro"）开始对话

4. 与语音助手进行自然语言交互

5. 超时则需再次触发

6. 结束本轮对话即自动保存对话记录 

## 主要特性

- 实时语音交互
- 智能对话生成
- 自然语音合成
- 长时间无语音自动休眠
- 对话历史记录

## 自定义设置

- 修改`settings`变量来自定义助手的角色和背景
- 调整`max_silence_duration`和`min_speech_duration`等参数来优化语音检测
- 更换唤醒词和对应的模型文件

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

项目维护者：HaxxorCialtion - cialtion@outlook.com
Bilibili视频地址：https://www.bilibili.com/video/BV1pftreQEbu

## 致谢

- [Porcupine](https://github.com/Picovoice/porcupine) - 用于唤醒词检测
- [SenseVoice](https://github.com/FunAudioLLM/SenseVoice) - 提供ASR模型
- [Ollama](https://github.com/ollama/ollama) - 本地大语言模型服务
- [LLM](https://github.com/QwenLM/Qwen2.5) - LLLM服务
- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) - 用于语音合成