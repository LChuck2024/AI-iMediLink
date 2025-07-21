# SQLite版本兼容性修复 - 必须在导入任何依赖之前
try:
    import pysqlite3
    import sys
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

import streamlit as st
import os

from utils.tools import load_info
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.tools import read_prompt_file, get_context_from_db
from operator import itemgetter
from langchain_core.runnables import RunnableLambda
from time import time

# LangChain 配置
os.environ["LANGCHAIN_TRACING"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "AI-iMediLink"
os.environ["LANGCHAIN_API_KEY"] = load_info("keys")["LANGCHAIN_API_KEY"]
os.environ["DASHSCOPE_API_KEY"] = load_info("keys")["DASHSCOPE_API_KEY"]

# 设置页面标题和图标
st.set_page_config(
    page_title="医脉通智能助手", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 侧边栏配置
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-bottom: 1rem; color: white;'>
        <h2 style='margin: 0; font-size: 1.5rem;'>🤖 AI医疗助手</h2>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;'>专业智能医疗咨询</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏥 科室选择")
    dept_options = {
        "导诊台": "👩🏻‍⚕ 导诊台",
        "内科": "🫀 内科",
        "外科": "🔬 外科", 
        "妇产科": "👶 妇产科",
        "儿科": "🧸 儿科",
        "肿瘤科": "🎗️ 肿瘤科",
        "男科": "👨‍⚕️ 男科"
    }
    
    dept_display = st.selectbox(
        "请选择咨询科室",
        options=list(dept_options.values()),
        index=0
    )
    
    # 获取实际的科室名称
    dept = [k for k, v in dept_options.items() if v == dept_display][0]
    
    # 读取prompt
    system_prompt = read_prompt_file(dept)
    
    st.markdown("---")
    
    # 模型配置
    st.markdown("### 🤖 模型配置")
    models = load_info("models").keys()
    selected_model = st.selectbox("AI模型", models, help="选择不同的AI模型以获得不同的回答风格")
    
    rag_flag = st.toggle("🔍 启用知识库检索", value=True, help="开启后将从专业医学知识库中检索相关信息")
    
    st.markdown("### ⚙️ 高级设置")
    with st.expander("模型参数调节", expanded=False):
        temperature = st.slider(
            "创造性温度", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.3, 
            step=0.1,
            help="较低值使回答更保守准确，较高值使回答更有创造性"
        )
        max_tokens = st.slider(
            "最大回答长度", 
            min_value=100, 
            max_value=2048, 
            value=800, 
            step=50,
            help="控制AI回答的最大字数"
        )
    
    st.markdown("---")
    
    # 症状自检工具入口
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
        <h4 style='margin: 0 0 0.5rem 0; color: white;'>🔍 症状自检工具</h4>
        <p style='margin: 0; color: rgba(255,255,255,0.9); font-size: 0.85rem;'>
            不确定如何描述症状？使用症状自检工具获得结构化帮助
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 使用症状自检工具", key="symptom_checker_btn", use_container_width=True):
        st.switch_page('pages/2_症状自检工具.py')
    
    st.markdown("---")
    
    # 使用提示
    st.markdown("""
    <div style='background: #e8f4fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3;'>
        <h4 style='margin: 0 0 0.5rem 0; color: #1976D2;'>💡 使用提示</h4>
        <ul style='margin: 0; padding-left: 1rem; font-size: 0.85rem; color: #424242;'>
            <li>详细描述症状和病史</li>
            <li>提供准确的个人信息</li>
            <li>如有紧急情况请立即就医</li>
            <li>AI建议仅供参考</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 自定义CSS，美化界面
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* 聊天容器样式 */
    .stChatInputContainer {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e8ed;
    }
    
    .stChatInputContainer > div {
        background: white;
        border-radius: 15px;
    }
    
    /* 用户消息样式 */
    [data-testid="stChatMessageContent"][data-testid*="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 18px 18px 5px 18px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        border: none;
    }
    
    /* AI助手消息样式 */
    [data-testid="stChatMessageContent"]:not([data-testid*="user"]) {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e1e8ed;
        border-radius: 18px 18px 18px 5px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        position: relative;
    }
    
    /* 移除自定义头像图标，使用Streamlit默认头像 */
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 标题样式 */
    h1 {
        color: #2c3e50;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* 副标题样式 */
    .stCaption {
        text-align: center;
        color: #5a6c7d;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* 加载动画 */
    .stSpinner {
        text-align: center;
    }
    
    /* 展开器样式 */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* 聊天区域容器 */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e8ed;
    }
    
    /* 状态指示器 */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: #e8f5e8;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #2e7d32;
        margin-bottom: 1rem;
    }
    
    /* 思考内容样式 */
    .streamlit-expanderContent {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# 主要内容区域
st.markdown(f"""
<div class='chat-container'>
    <div style='text-align: center; margin-bottom: 1.5rem;'>
        <h1 style='margin: 0; color: #2c3e50; font-size: 2.2rem;'>🏥 医脉通智能助手</h1>
        <p style='margin: 0.5rem 0 0 0; color: #5a6c7d; font-size: 1rem;'>{dept_display} 专业咨询服务</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 状态指示器
status_color = "#e8f5e8" if rag_flag else "#fff3cd"
status_text_color = "#2e7d32" if rag_flag else "#856404"
rag_status = "🔍 知识库检索已启用" if rag_flag else "🤖 仅使用AI模型"

st.markdown(f"""
<div style='display: flex; justify-content: center; margin-bottom: 1rem;'>
    <div style='display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; 
                background: {status_color}; border-radius: 20px; font-size: 0.85rem; color: {status_text_color};'>
        <span>{rag_status}</span>
        <span>•</span>
        <span>🤖 {selected_model}</span>
        <span>•</span>
        <span>🌡️ 温度: {temperature}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 初始化聊天记录 (使用 session_state)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"您好！我是医脉通{dept}智能助手 🏥\n\n我可以为您提供专业的{dept}医疗咨询服务。请详细描述您的症状或问题，我会根据专业知识为您提供建议。\n\n⚠️ 请注意：我的建议仅供参考，如有紧急情况请立即就医。"}
    ]

# 显示聊天记录
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.chat_message(msg["role"], avatar="🩺").write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

# 获取模型配置
model_info = load_info("models")[selected_model]
# print(f"模型配置: {model_info}")
model_name = model_info["model_name"]
base_url = model_info["base_url"]
api_key = model_info["api_key"]

if selected_model == "DeepSeek-Chat":
    Model = ChatDeepSeek
else:
    Model = ChatOpenAI

# 定义模型
llm = Model(
    model=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=temperature,
    max_tokens=max_tokens,
    streaming=True
)

# 定义提示模板
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt + """\n已知内容：{RAG}，
                                如果找到相关内容，请优先从“{RAG}”中提取内容，整合加工后回答，并标明知识来自检索库。
                                如果找不到相关内容，请用你的专业知识进行回答，并标明知识来自大模型。
                                注意：如果用户问你关于开发者、公司或者相关问题，请回答开发者是"LChuck"。
                             """),
    ("human", "{user_input}")
])

if rag_flag:

    chain = ({
                 "RAG": RunnableLambda(itemgetter("user_input")) | get_context_from_db,
                 "user_input": itemgetter("user_input")
             }
             | prompt_template
             | llm
             | StrOutputParser()
             )
else:
    chain = ({
                 "RAG": itemgetter("user_input"),
                 "user_input": itemgetter("user_input")
              }
             | prompt_template
             | llm
             | StrOutputParser()
             )
# print(f'chain{chain}')

# 检查是否有来自症状自检工具的自动咨询请求
if hasattr(st.session_state, 'auto_consultation') and st.session_state.auto_consultation:
    if hasattr(st.session_state, 'auto_symptom_description') and st.session_state.auto_symptom_description:
        # 自动添加症状描述到聊天记录
        symptom_description = st.session_state.auto_symptom_description
        st.session_state.messages.append({"role": "user", "content": symptom_description})
        
        # 清除自动咨询标志
        del st.session_state.auto_consultation
        del st.session_state.auto_symptom_description
        
        # 显示自动输入的症状描述
        st.chat_message("user").write(symptom_description)
        
        # 自动处理AI回复
        with st.chat_message("assistant", avatar="🩺"):
            try:
                start_time = time()
                print(f"自动处理症状描述: {symptom_description}")
                
                # 显示思考状态
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown("""
                <div style='display: flex; align-items: center; gap: 0.5rem; padding: 1rem; 
                            background: #f0f8ff; border-radius: 10px; border-left: 4px solid #667eea;'>
                    <div style='font-size: 1.2rem;'>🤔</div>
                    <div style='color: #667eea; font-weight: 500;'>AI助手正在分析您的症状...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 创建空白占位符用于流式输出
                response_placeholder = st.empty()
                response_content = ""
                
                # 使用LangChain处理消息并实现流式输出
                for chunk in chain.stream({"user_input": symptom_description}):
                    response_content += chunk
                    thinking_placeholder.empty()  # 清除思考状态
                    response_placeholder.markdown(response_content + "▌")  # 添加光标效果

                # 完成后显示最终内容
                import re

                think_content_match = re.search(r'<think>(.*?)</think>', response_content, re.DOTALL)
                if think_content_match:
                    think_text = think_content_match.group(1).strip()
                    # 移除原始response_content中的think标签内容
                    response_content_without_think = re.sub(r'<think>.*?</think>', '', response_content,
                                                            flags=re.DOTALL)
                    with st.expander("🧠 查看AI思考过程", expanded=False):
                        st.markdown(f"""
                        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; 
                                    border-left: 4px solid #667eea; font-size: 0.9rem;'>
                            {think_text}
                        </div>
                        """, unsafe_allow_html=True)
                    response_placeholder.markdown(response_content_without_think)
                else:
                    response_placeholder.markdown(response_content)
                    
                end_time = time()
                duration = (end_time - start_time).__trunc__()
                print(f"自动症状分析完成，耗时: {duration}秒")
                
                # 显示处理时间和来源信息
                source_info = "知识库 + AI模型" if rag_flag else "AI模型"
                st.markdown(f"""
                <div style='margin-top: 1rem; padding: 0.5rem; background: #f8f9fa; 
                            border-radius: 8px; font-size: 0.8rem; color: #5a6c7d; text-align: center;'>
                    📊 处理耗时: {duration}秒 | 🔍 信息来源: {source_info} | 🤖 模型: {selected_model}
                    <br>💡 此分析基于症状自检工具生成的详细描述
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                print(f"自动症状分析错误: {e}")
                thinking_placeholder.empty()
                response_placeholder.markdown(f"""
                <div style='background: #ffebee; padding: 1rem; border-radius: 8px; 
                            border-left: 4px solid #f44336; color: #c62828;'>
                    ❌ 抱歉，自动分析症状时出现了错误：{str(e)}
                    
                    请尝试：
                    - 手动重新描述症状
                    - 切换其它模型
                    - 检查网络连接
                </div>
                """)
                response_content = f"抱歉，我无法分析您的症状。错误信息：{str(e)}"

        # 将AI回复添加到聊天记录
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
        # 显示成功提示
        st.success("✅ 症状自检工具已自动为您生成AI分析！")

# 处理用户输入
if question := st.chat_input("💬 请详细描述您的症状或医疗问题..."):
    # 将用户消息添加到聊天记录
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # 获取机器人回复 (显示加载状态)
    with st.chat_message("assistant", avatar="🩺"):
        try:
            start_time = time()
            print(f"开始处理消息: {question}")
            
            # 显示思考状态
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("""
            <div style='display: flex; align-items: center; gap: 0.5rem; padding: 1rem; 
                        background: #f0f8ff; border-radius: 10px; border-left: 4px solid #667eea;'>
                <div style='font-size: 1.2rem;'>🤔</div>
                <div style='color: #667eea; font-weight: 500;'>AI助手正在分析您的问题...</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 创建空白占位符用于流式输出
            response_placeholder = st.empty()
            response_content = ""
            
            # 使用LangChain处理消息并实现流式输出
            for chunk in chain.stream({"user_input": question}):
                response_content += chunk
                thinking_placeholder.empty()  # 清除思考状态
                response_placeholder.markdown(response_content + "▌")  # 添加光标效果

            # 完成后显示最终内容
            import re

            think_content_match = re.search(r'<think>(.*?)</think>', response_content, re.DOTALL)
            if think_content_match:
                think_text = think_content_match.group(1).strip()
                # 移除原始response_content中的think标签内容
                response_content_without_think = re.sub(r'<think>.*?</think>', '', response_content,
                                                        flags=re.DOTALL)
                with st.expander("🧠 查看AI思考过程", expanded=False):
                    st.markdown(f"""
                    <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px; 
                                border-left: 4px solid #667eea; font-size: 0.9rem;'>
                        {think_text}
                    </div>
                    """, unsafe_allow_html=True)
                response_placeholder.markdown(response_content_without_think)
            else:
                response_placeholder.markdown(response_content)
                
            end_time = time()
            duration = (end_time - start_time).__trunc__()
            print(f"消息处理完成: {question}, 耗时: {duration}秒")
            
            # 显示处理时间和来源信息
            source_info = "知识库 + AI模型" if rag_flag else "AI模型"
            st.markdown(f"""
            <div style='margin-top: 1rem; padding: 0.5rem; background: #f8f9fa; 
                        border-radius: 8px; font-size: 0.8rem; color: #5a6c7d; text-align: center;'>
                📊 处理耗时: {duration}秒 | 🔍 信息来源: {source_info} | 🤖 模型: {selected_model}
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            print(f"Error: {e}")
            thinking_placeholder.empty()
            response_placeholder.markdown(f"""
            <div style='background: #ffebee; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid #f44336; color: #c62828;'>
                ❌ 抱歉，处理您的问题时出现了错误：{str(e)}
                
                请尝试：
                - 重新描述您的问题
                - 切换其它模型
                - 检查网络连接
                - 稍后再试
            </div>
            """)
            response_content = f"抱歉，我无法回答您的问题。错误信息：{str(e)}"

    # 将机器人回复添加到聊天记录
    st.session_state.messages.append({"role": "assistant", "content": response_content})

# 底部操作区域
st.markdown("<br>", unsafe_allow_html=True)

# 聊天记录导出功能
def export_chat_history():
    """导出聊天记录为文本文件"""
    if len(st.session_state.messages) <= 1:
        return None
    
    # 生成文件名
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"医脉通_{dept}_咨询记录_{timestamp}.txt"
    
    # 构建聊天记录内容
    chat_content = f"""医脉通智能诊疗系统 - 聊天记录导出
{'='*50}
科室: {dept}
模型: {selected_model}
导出时间: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
{'='*50}

"""
    
    for i, msg in enumerate(st.session_state.messages, 1):
        role_emoji = "👤" if msg["role"] == "user" else "🤖"
        role_name = "用户" if msg["role"] == "user" else "AI助手"
        chat_content += f"\n【第{i}轮对话】\n"
        chat_content += f"{role_emoji} {role_name}:\n"
        chat_content += f"{msg['content']}\n"
        chat_content += "-" * 30 + "\n"
    
    chat_content += f"""
{'='*50}
⚠️ 重要提醒：
- 本记录仅供个人参考使用
- AI建议不能替代专业医生诊断
- 如有严重症状请及时就医
- 请妥善保管个人健康信息
{'='*50}
"""
    
    return chat_content, filename

# 操作按钮区域
if len(st.session_state.messages) > 1:
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🗑️ 清空对话", use_container_width=True, help="清空所有聊天记录"):
            st.session_state.messages = [
                {"role": "assistant", "content": f"您好！我是医脉通{dept}智能助手 🏥\n\n我可以为您提供专业的{dept}医疗咨询服务。请详细描述您的症状或问题，我会根据专业知识为您提供建议。\n\n⚠️ 请注意：我的建议仅供参考，如有紧急情况请立即就医。"}
            ]
            st.rerun()
    
    with col2:
        chat_data = export_chat_history()
        if chat_data:
            chat_content, filename = chat_data
            st.download_button(
                label="📄 导出记录",
                data=chat_content,
                file_name=filename,
                mime="text/plain",
                use_container_width=True,
                help="直接下载聊天记录为文本文件"
            )
    
    with col3:
        if chat_data:
            if st.button("📋 复制记录", use_container_width=True, help="点击后显示聊天记录，可手动复制"):
                # 显示聊天记录
                st.markdown("### 📋 聊天记录内容")
                st.markdown("---")
                
                # 使用st.text_area显示内容，便于复制
                st.text_area(
                    "聊天记录",
                    value=chat_content,
                    height=400,
                    help="选中全部内容后按 Ctrl+C (Mac: Cmd+C) 复制"
                )
                
                # 提供复制按钮和说明
                col_copy1, col_copy2 = st.columns([1, 1])
                with col_copy1:
                    st.success("✅ 聊天记录已显示")
                with col_copy2:
                    st.info("💡 选中上方文本后复制")
                
                # 添加复制提示
                st.markdown("""
                <div style='background: #e8f4fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3; margin-top: 1rem;'>
                    <h4 style='margin: 0 0 0.5rem 0; color: #1976D2;'>📋 复制操作步骤：</h4>
                    <ol style='margin: 0; color: #424242; padding-left: 1.5rem;'>
                        <li>点击上方文本框，按 <strong>Ctrl+A</strong> (Mac: <strong>Cmd+A</strong>) 全选内容</li>
                        <li>按 <strong>Ctrl+C</strong> (Mac: <strong>Cmd+C</strong>) 复制到剪贴板</li>
                        <li>粘贴到您需要的地方</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
    
    with col4:
        if st.button("🔄 刷新页面", use_container_width=True, help="刷新页面重新开始"):
            st.rerun()
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("💡 开始对话后，您可以导出聊天记录")

# 页面底部信息
st.markdown("""
<div style='margin-top: 2rem; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; text-align: center; color: white;'>
    <p style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>
        🏥 医脉通智能诊疗系统 | 🤖 Powered by LChuck | ⚠️ 仅供医疗参考，不替代专业诊断
    </p>
</div>
""", unsafe_allow_html=True)
