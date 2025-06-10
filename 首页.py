import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="AIE直通车",
    page_icon="🚀",
    layout="wide"
)

# 添加CSS样式
st.markdown("""
<style>
    .main > div {
        padding: 2rem;
    }
    .stTitle {
        font-size: 3rem !important;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .project-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .feature-icon {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 标题和简介
st.title("🚀 AIE直通车")
st.markdown("""
<div class='project-card'>
    <h2>项目简介</h2>
    <p>AIE直通车是一个综合性AI应用平台，集成了多种前沿AI技术，为用户提供便捷、高效的人工智能服务。
    通过整合大语言模型、计算机视觉等技术，我们致力于为用户提供全方位的AI解决方案。</p>
</div>
""", unsafe_allow_html=True)

# 功能特点
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class='project-card'>
        <h3>📊 机器学习</h3>
        <p>经典机器学习算法与应用：</p>
        <ul>
            <li>监督学习算法</li>
            <li>无监督学习算法</li>
            <li>特征工程</li>
            <li>模型评估与优化</li>
        </ul>
        <a href='机器学习（ML）'>点击进入 →</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='project-card'>
        <h3>🧠 深度学习</h3>
        <p>深度神经网络与应用：</p>
        <ul>
            <li>神经网络基础</li>
            <li>CNN/RNN/Transformer</li>
            <li>模型训练与调优</li>
            <li>实战项目案例</li>
        </ul>
        <a href='深度学习（DL）'>点击进入 →</a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='project-card'>
        <h3>👁️ 机器视觉</h3>
        <p>计算机视觉技术与应用：</p>
        <ul>
            <li>图像分类</li>
            <li>目标检测</li>
            <li>图像分割</li>
            <li>视频分析</li>
        </ul>
        <a href='机器视觉（CV）'>点击进入 →</a>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='project-card'>
        <h3>💬 自然语言</h3>
        <p>自然语言处理技术：</p>
        <ul>
            <li>文本分类</li>
            <li>命名实体识别</li>
            <li>机器翻译</li>
            <li>情感分析</li>
        </ul>
        <a href='自然语言（NLP）'>点击进入 →</a>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class='project-card'>
        <h3>🤖 大模型</h3>
        <p>大语言模型与AIGC应用：</p>
        <ul>
            <li>智能对话系统</li>
            <li>文本生成与创作</li>
            <li>知识问答</li>
            <li>多模态交互</li>
        </ul>
        <a href='大模型（AIGC）'>点击进入 →</a>
    </div>
    """, unsafe_allow_html=True)

# 使用说明
st.markdown("""
<div class='project-card'>
    <h2>📖 使用指南</h2>
    <ol>
        <li>在左侧边栏选择需要使用的功能模块</li>
        <li>根据每个模块的具体说明进行操作</li>
        <li>如遇到问题，请查看相关文档或联系支持团队</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# 项目信息
st.markdown("""
<div class='project-card' style='text-align: center;'>
    <p>© 2025 AIE直通车 | Powered by AIE-52 G5</p>
</div>
""", unsafe_allow_html=True)