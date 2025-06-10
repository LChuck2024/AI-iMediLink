# AIE_Multi_Show

## 项目简介
AIE直通车项目，包含机器学习、深度学习、计算机视觉、自然语言处理和大模型等模块。

## 项目结构
- `/code`: 主要代码目录
- `/data`: 数据目录
  - `/Prompt`: 提示词数据
  - `/RAG`: 检索增强生成数据
- `/pages`: 各模块入口文件
  - `1_机器学习（ML）.py`
  - `2_深度学习（DL）.py`
  - `3_机器视觉（CV）.py`
  - `4_自然语言（NLP）.py`
  - `5_大模型（AIGC）.py`
- `/utils`: 工具模块
  - `config.json`: 配置文件
  - `load_key.py`: 密钥加载
  - `tools.py`: 工具函数
- `首页.py`: 主入口文件

## 安装指南
```bash
pip install -r requirements.txt