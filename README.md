# AI-iMediLink 🏥

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 项目简介

AI-iMediLink 是一个基于人工智能的医疗咨询系统，提供智能诊疗服务。系统集成了OpenAI GPT和DeepSeek等先进AI模型，结合RAG（检索增强生成）技术，从专业医学知识库中检索相关信息，为用户提供准确、专业的医疗咨询服务。同时提供症状自检工具，帮助用户更好地描述症状。

### 核心特色
- 🤖 **多模型AI引擎**: 集成DeepSeek、Qwen、Hunyuan、Doubao等多种AI模型
- 🏥 **七科室覆盖**: 支持内科、外科、妇产科、儿科、肿瘤科、男科、导诊台
- 📚 **RAG知识增强**: 基于检索增强生成技术的医疗知识检索
- 🔍 **症状自检工具**: 结构化问答帮助准确描述症状
- 💬 **实时流式对话**: 实时显示AI思考过程
- ⚙️ **灵活参数配置**: 支持温度、Token数等参数调节

## 技术栈

- **前端框架**: Streamlit
- **AI模型**: DeepSeek, Qwen, Hunyuan, Doubao等多种模型
- **向量数据库**: ChromaDB
- **知识检索**: LangChain + RAG
- **数据处理**: Pandas, NumPy
- **开发语言**: Python 3.8+

## 项目结构

```
AI-iMediLink/
├── 📁 data/                    # 数据目录
│   ├── 📁 Prompt/              # 各科室提示词模板
│   │   ├── 导诊台.md
│   │   ├── 内科.md
│   │   ├── 外科.md
│   │   ├── 妇产科.md
│   │   ├── 儿科.md
│   │   ├── 肿瘤科.md
│   │   └── 男科.md
│   ├── 📁 RAG/                 # 医疗知识库文档
│   │   ├── 📁 内科/
│   │   ├── 📁 外科/
│   │   ├── 📁 妇产科/
│   │   ├── 📁 儿科/
│   │   ├── 📁 肿瘤科/
│   │   └── 📁 男科/
│   └── 📁 chroma_data/         # ChromaDB向量数据库
├── 📁 pages/                   # 页面模块
│   ├── 1_医脉通.py             # AI医疗咨询页面
│   └── 2_症状自检工具.py       # 症状自检工具页面
├── 📁 utils/                   # 工具模块
│   ├── config.json            # 模型配置文件
│   └── tools.py               # 核心工具函数
├── 📁 code/                    # 开发文档
│   └── 提示词.md              # 提示词开发指南
├── 📄 首页.py                   # 应用主入口
├── 📄 requirements.txt         # 依赖包列表
└── 📄 README.md               # 项目说明文档
```

## 功能特点

### 🏥 专业医疗服务
- **七科室覆盖**: 导诊台、内科、外科、妇产科、儿科、肿瘤科、男科
- **专业知识库**: 基于医疗文献和临床指南的专业知识检索
- **症状分析**: 智能症状识别和初步诊断建议
- **用药指导**: 提供药物信息和用药建议

### 🤖 AI技术特性
- **多模型支持**: 集成DeepSeek、Qwen、Hunyuan、Doubao等多种AI模型
- **RAG增强**: 检索增强生成技术，确保回答的专业性和准确性
- **流式输出**: 实时流式响应，提升交互体验
- **上下文记忆**: 支持多轮对话的上下文理解

### 🔍 症状自检工具
- **结构化问答**: 按身体部位分类的症状选择
- **严重程度评估**: 智能评估症状严重程度
- **详细报告生成**: 生成完整的症状描述报告
- **AI咨询跳转**: 一键跳转到AI咨询页面

### ⚙️ 系统特性
- **灵活配置**: 支持模型切换、温度调节、Token数量控制
- **响应式界面**: 现代化UI设计，支持多设备访问
- **数据安全**: 本地部署，保护用户隐私
- **易于扩展**: 模块化设计，便于功能扩展

## 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python版本**: 3.8 或更高版本
- **内存**: 建议 8GB 以上
- **存储空间**: 至少 2GB 可用空间
- **网络**: 需要互联网连接以访问AI模型API

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/your_username/AI-iMediLink.git
cd AI-iMediLink
```

### 2. 创建虚拟环境（推荐）
```bash
# 使用 conda
conda create -n ai-medilink python=3.8
conda activate ai-medilink

# 或使用 venv
python -m venv ai-medilink
# Windows
ai-medilink\Scripts\activate
# macOS/Linux
source ai-medilink/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置API密钥

#### 方法一：环境变量（推荐）
```bash
# Windows
set OPENAI_API_KEY=your_openai_api_key
set DEEPSEEK_API_KEY=your_deepseek_api_key

# macOS/Linux
export OPENAI_API_KEY=your_openai_api_key
export DEEPSEEK_API_KEY=your_deepseek_api_key
```

#### 方法二：.env文件
在项目根目录创建 `.env` 文件：
```env
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

#### 方法三：修改配置文件
编辑 `utils/config.json` 文件，填入您的API密钥。

### 5. 启动应用
```bash
streamlit run 首页.py
```

应用将在浏览器中自动打开，默认地址：`http://localhost:8501`

## 使用指南

### 基本操作流程

#### 方式一：直接AI咨询
1. **启动应用**: 运行 `streamlit run 首页.py`
2. **选择科室**: 在侧边栏选择相应的医疗科室
3. **配置模型**: 选择AI模型并调整参数（温度、最大Token数等）
4. **开始咨询**: 在输入框中描述症状或医疗问题
5. **获取建议**: 系统将提供专业的医疗咨询建议

#### 方式二：症状自检工具
1. **选择自检工具**: 在首页点击"症状自检工具"
2. **选择身体部位**: 按身体部位分类选择症状
3. **详细描述**: 回答结构化问题，详细描述症状
4. **严重程度评估**: 评估症状的严重程度
5. **生成报告**: 系统生成完整的症状描述报告
6. **跳转咨询**: 点击"开始AI咨询"跳转到AI咨询页面

### 功能说明

#### 科室选择
- **导诊台**: 症状初步评估，科室推荐
- **内科**: 心血管、呼吸、消化等内科疾病
- **外科**: 普外科、骨科、泌尿外科等
- **妇产科**: 妇科疾病、产科、计划生育
- **儿科**: 儿童疾病、生长发育
- **肿瘤科**: 肿瘤诊断、治疗、康复
- **男科**: 男性生殖健康、泌尿系统

#### 模型配置
- **模型选择**: 支持DeepSeek、Qwen、Hunyuan、Doubao等多种AI模型
- **温度**: 控制回答的创造性（0.1-1.0，越高越有创造性）
- **最大Token**: 控制回答长度（建议500-2000）
- **知识库检索**: 系统会自动从相关医疗知识库中检索信息
- **流式输出**: 实时显示AI生成的回答过程

#### 症状自检工具特点
- **按身体部位分类**: 便于快速定位症状
- **结构化问答**: 确保信息完整准确
- **严重程度评估**: 帮助判断紧急程度
- **详细报告生成**: 可直接用于AI咨询

### 注意事项
⚠️ **重要提醒**：
- 本系统仅供医疗咨询参考，不能替代专业医生诊断
- 如有严重症状，请及时就医
- 系统建议仅供参考，具体治疗方案请咨询专业医生
- 不提供具体的药物处方，只能给出用药建议
- 不处理紧急医疗情况，紧急情况请立即就医

## API密钥获取

### OpenAI API
1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册并登录账户
3. 进入 API Keys 页面
4. 创建新的API密钥
5. 复制密钥并妥善保存

### DeepSeek API
1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册并登录账户
3. 进入API管理页面
4. 创建新的API密钥
5. 复制密钥并妥善保存

## 故障排除

### 常见问题

**Q: 启动时提示模块未找到**
```bash
A: 确保已激活虚拟环境并安装所有依赖：
pip install -r requirements.txt
```

**Q: API调用失败**
```bash
A: 检查API密钥是否正确配置：
1. 验证密钥格式是否正确
2. 确认账户余额充足
3. 检查网络连接
```

**Q: 页面无法访问**
```bash
A: 检查端口是否被占用：
streamlit run 首页.py --server.port 8502
```

**Q: 知识库检索失败**
```bash
A: 确保ChromaDB数据已正确初始化：
1. 检查 data/chroma_data 目录是否存在
2. 重新运行应用以初始化向量数据库
```

**Q: ModuleNotFoundError: No module named 'distutils'**
```bash
A: 这是 Python 3.12+ 的兼容性问题，解决方案：
pip install setuptools>=68.0.0 wheel>=0.41.0
```

### 日志查看
应用运行时的详细日志会显示在终端中，包括：
- API调用状态
- 知识库检索结果
- 错误信息和堆栈跟踪

```bash
# 查看详细错误信息
streamlit run 首页.py --logger.level debug
```

## 开发指南

### 项目架构
- `首页.py`: 主应用入口，包含UI布局和核心功能
- `pages/1_医脉通.py`: AI医疗咨询页面的具体实现
- `pages/2_症状自检工具.py`: 症状自检工具的实现
- `utils/tools.py`: 核心工具函数，包含RAG检索和模型调用
- `utils/config.json`: 模型配置文件
- `data/`: 知识库和提示词数据

### 添加新科室
1. 在 `data/Prompt/` 目录下添加新科室的提示词文件
2. 在 `data/RAG/` 目录下添加相应的知识库文档
3. 更新 `pages/1_医脉通.py` 中的科室列表
4. 重新运行应用以更新向量数据库

### 集成新模型
1. 在 `utils/config.json` 中添加新模型配置
2. 在 `pages/1_医脉通.py` 中更新模型选择逻辑
3. 更新UI中的模型选择选项

## 未来规划

### 功能增强
- **语音输入**: 支持语音描述症状
- **图片上传**: 上传症状图片辅助诊断
- **紧急症状识别**: 快速识别需要立即就医的症状
- **药物相互作用检查**: 检查多种药物间的相互作用
- **健康数据可视化**: 图表展示症状变化趋势

### 用户体验优化
- **多语言支持**: 增加英文等其他语言
- **移动端优化**: 更好的移动设备体验
- **离线模式**: 基础功能支持离线使用
- **响应速度优化**: 减少AI响应时间

### 系统性能优化
- **缓存机制**: 智能缓存常用查询结果
- **离线知识库**: 本地存储常用医疗知识
- **智能推荐**: 基于症状推荐相关科室和检查

## 贡献指南

我们欢迎所有形式的贡献！无论是报告bug、提出新功能建议，还是提交代码改进。

### 如何贡献

1. **Fork 项目**
2. **创建功能分支**: `git checkout -b feature/your-feature-name`
3. **提交更改**: `git commit -m "Add: 描述你的更改"`
4. **推送到分支**: `git push origin feature/your-feature-name`
5. **创建 Pull Request**

### 贡献类型
- 🐛 **Bug修复**: 报告或修复系统bug
- ✨ **新功能**: 提出或实现新功能
- 📚 **文档改进**: 完善文档和注释
- 🎨 **UI优化**: 改进用户界面和体验
- 🔧 **代码重构**: 优化代码结构和性能

## 更新日志

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- 🏥 支持7大医疗科室（导诊台、内科、外科、妇产科、儿科、肿瘤科、男科）
- 🤖 集成DeepSeek、Qwen、Hunyuan、Doubao等多种AI模型
- 📚 实现RAG知识检索
- 🔍 新增症状自检工具
- 💬 实时流式对话
- ⚙️ 灵活参数配置
- 🎨 现代化UI界面

## 致谢

感谢以下开源项目和贡献者：
- [Streamlit](https://streamlit.io/) - Web应用框架
- [LangChain](https://langchain.com/) - AI应用开发框架
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [DeepSeek](https://www.deepseek.com/) - 开源大模型
- [Qwen](https://qwen.ai/) - 通义千问大模型
- [Hunyuan](https://hunyuan.cloud.tencent.com/) - 腾讯混元大模型
- [Doubao](https://www.doubao.com/) - 豆包大模型

## 联系我们

- 📧 邮箱: your-email@example.com
- 🐛 问题反馈: [GitHub Issues](https://github.com/your_username/AI-iMediLink/issues)
- 💬 讨论交流: [GitHub Discussions](https://github.com/your_username/AI-iMediLink/discussions)

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

<div align="center">
  <p>⭐ 如果这个项目对你有帮助，请给我们一个星标！</p>
  <p>Made with ❤️ by AI-iMediLink Team</p>
</div>
