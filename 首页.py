# SQLite版本兼容性修复 - 必须在导入任何依赖之前
try:
    import pysqlite3
    import sys
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="医脉通智能诊疗系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 添加CSS样式
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* 自定义按钮样式 */
    .stButton > button {
        background: white !important;
        color: #667eea !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        padding: 1rem 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="%23ffffff" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    .feature-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        grid-template-rows: repeat(2, 1fr) !important;
        gap: 1.5rem !important;
        margin: 2rem 0;
        width: 100%;
        max-width: none;
    }
    
    @media (max-width: 768px) {
        .feature-grid {
            grid-template-columns: 1fr;
            grid-template-rows: auto;
        }
    }
    
    @media (max-width: 1024px) and (min-width: 769px) {
        .feature-grid {
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(3, 1fr);
        }
    }
    
    .feature-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #5a6c7d;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .info-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        border-left: 5px solid #667eea;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        color: #2c3e50;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 3rem 0;
    }
    
    .cta-button {
        background: white;
        color: #667eea;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #5a6c7d;
        border-top: 1px solid #e9ecef;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# 英雄区域
st.markdown("""
<div class='hero-section'>
    <div class='hero-content'>
        <h1 class='hero-title'>🏥 医脉通智能诊疗系统</h1>
        <p class='hero-subtitle'>基于人工智能的专业医疗咨询平台，集成多模型AI引擎，为您提供精准的医疗咨询服务</p>
        <div class='stats-container'>
            <div class='stat-card'>
                <span class='stat-number'>7</span>
                <span class='stat-label'>专业科室</span>
            </div>
            <div class='stat-card'>
                <span class='stat-number'>5+</span>
                <span class='stat-label'>AI模型</span>
            </div>
            <div class='stat-card'>
                <span class='stat-number'>RAG</span>
                <span class='stat-label'>知识增强</span>
            </div>
            <div class='stat-card'>
                <span class='stat-number'>🔍</span>
                <span class='stat-label'>症状自检</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 行动号召区域
st.markdown("""
<div class='cta-section'>
    <h2 style='margin-bottom: 1rem; font-size: 2rem;'>🚀 开始您的智能医疗咨询之旅</h2>
    <p style='font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.9;'>专业AI助手随时为您提供医疗咨询服务，让健康管理更简单</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button('🔍 症状自检工具', key='symptom_checker', use_container_width=True, type='secondary'):
        st.switch_page('pages/2_症状自检工具.py')
with col2:
    if st.button('立即开始咨询 →', key='top_cta', use_container_width=True, type='primary'):
        st.switch_page('pages/1_医脉通.py')

# 项目简介
st.markdown("""
<div class='info-card'>
    <h2>🎯 项目简介</h2>
    <p>医脉通智能诊疗系统是一个基于人工智能的医疗咨询平台，提供多科室智能助手服务。系统集成了DeepSeek、Qwen、Hunyuan、Doubao等多种先进AI模型，结合RAG（检索增强生成）技术，从专业医学知识库中检索相关信息，为用户提供准确、专业的医疗咨询服务。同时提供症状自检工具，帮助用户更好地描述症状。</p>
</div>
""", unsafe_allow_html=True)

# 功能特点（更新版）
st.markdown("<h2 class='section-title'>✨ 核心功能</h2>", unsafe_allow_html=True)

# 使用Streamlit原生组件创建卡片布局
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border-left: 4px solid #667eea; text-align: center;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🏥</div>
        <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem;'>七科室专业咨询</h3>
        <p style='color: #5a6c7d; line-height: 1.6; font-size: 0.95rem; margin: 0;'>内科、外科、妇产科、儿科、肿瘤科、男科、导诊台</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border-left: 4px solid #667eea; text-align: center; margin-top: 1.5rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🔍</div>
        <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem;'>症状自检工具</h3>
        <p style='color: #5a6c7d; line-height: 1.6; font-size: 0.95rem; margin: 0;'>结构化问答，帮助准确描述症状</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border-left: 4px solid #667eea; text-align: center;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
        <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem;'>多模型AI引擎</h3>
        <p style='color: #5a6c7d; line-height: 1.6; font-size: 0.95rem; margin: 0;'>DeepSeek、Qwen、Hunyuan、Doubao等多种模型</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border-left: 4px solid #667eea; text-align: center; margin-top: 1.5rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>💬</div>
        <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem;'>实时流式对话</h3>
        <p style='color: #5a6c7d; line-height: 1.6; font-size: 0.95rem; margin: 0;'>实时显示AI思考过程，提供自然对话体验</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border-left: 4px solid #667eea; text-align: center;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>📚</div>
        <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem;'>RAG知识增强</h3>
        <p style='color: #5a6c7d; line-height: 1.6; font-size: 0.95rem; margin: 0;'>检索专业医学知识库，提供权威可靠信息</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border-left: 4px solid #667eea; text-align: center; margin-top: 1.5rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>⚙️</div>
        <h3 style='font-size: 1.3rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem;'>灵活参数配置</h3>
        <p style='color: #5a6c7d; line-height: 1.6; font-size: 0.95rem; margin: 0;'>温度、Token数等参数可调，满足个性化需求</p>
    </div>
    """, unsafe_allow_html=True)

# 科室介绍
st.markdown("<h2 class='section-title'>🏥 专业科室</h2>", unsafe_allow_html=True)

st.markdown("""
<div class='info-card'>
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 1rem;'>
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; border-left: 4px solid #667eea;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>👩🏻‍⚕</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.1rem;'>导诊台</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>症状初步评估，科室推荐</p>
        </div>
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; border-left: 4px solid #667eea;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🫀</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.1rem;'>内科</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>心血管、呼吸、消化等内科疾病</p>
        </div>
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; border-left: 4px solid #667eea;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🔬</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.1rem;'>外科</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>普外科、骨科、泌尿外科等</p>
        </div>
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; border-left: 4px solid #667eea;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>👶</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.1rem;'>妇产科</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>妇科疾病、产科、计划生育</p>
        </div>
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; border-left: 4px solid #667eea;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🧸</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.1rem;'>儿科</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>儿童疾病、生长发育</p>
        </div>
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; border-left: 4px solid #667eea;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🎗️</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.1rem;'>肿瘤科</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>肿瘤诊断、治疗、康复</p>
        </div>
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; border-left: 4px solid #667eea;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>👨‍⚕️</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem; font-size: 1.1rem;'>男科</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>男性生殖健康、泌尿系统</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 使用说明
st.markdown("<h2 class='section-title'>📖 使用指南</h2>", unsafe_allow_html=True)

st.markdown("""
<div class='info-card'>
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1rem;'>
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🔍</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem;'>症状自检</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>使用结构化工具准确描述症状</p>
        </div>
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🏥</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem;'>选择科室</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>根据症状选择相应的专业科室</p>
        </div>
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>💬</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem;'>AI咨询</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>与AI助手对话获得专业建议</p>
        </div>
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>⚙️</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.5rem;'>参数调节</h3>
            <p style='color: #5a6c7d; font-size: 0.9rem;'>根据需要调整AI模型参数</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 使用指南（可展开）
with st.expander("📖 详细使用指南", expanded=False):
    # 快速开始部分
    st.markdown("<h2 style='color: #2c3e50; margin-bottom: 1.5rem;'>🚀 快速开始</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #5a6c7d; margin-bottom: 2rem;'>按照以下步骤开始使用医脉通智能诊疗系统</p>", unsafe_allow_html=True)
    
    # 使用4列布局显示步骤（横向单行排列）
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    
    with step_col1:
        # 步骤1
        st.markdown("""
        <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0; border-left: 4px solid #667eea; position: relative;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 25px; height: 25px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.8rem;'>1</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.8rem; font-size: 1.1rem;'>选择服务类型</h3>
            <p style='color: #5a6c7d; margin-bottom: 0.8rem; font-size: 0.9rem;'>在首页选择您需要的服务</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        # 步骤2
        st.markdown("""
        <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0; border-left: 4px solid #667eea; position: relative;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 25px; height: 25px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.8rem;'>2</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.8rem; font-size: 1.1rem;'>选择专业科室</h3>
            <p style='color: #5a6c7d; margin-bottom: 0.8rem; font-size: 0.9rem;'>根据您的症状选择相应的专业科室</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        # 步骤3
        st.markdown("""
        <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0; border-left: 4px solid #667eea; position: relative;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 25px; height: 25px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.8rem;'>3</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.8rem; font-size: 1.1rem;'>描述症状</h3>
            <p style='color: #5a6c7d; margin-bottom: 0.8rem; font-size: 0.9rem;'>详细描述您的症状和病史</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col4:
        # 步骤4
        st.markdown("""
        <div style='background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; padding: 1.2rem; margin: 1rem 0; border-left: 4px solid #667eea; position: relative;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 25px; height: 25px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; margin-bottom: 0.8rem;'>4</div>
            <h3 style='color: #2c3e50; margin-bottom: 0.8rem; font-size: 1.1rem;'>获得专业建议</h3>
            <p style='color: #5a6c7d; margin-bottom: 0.8rem; font-size: 0.9rem;'>AI助手提供专业医疗建议</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 症状自检工具说明
    st.markdown("<h2 style='color: #2c3e50; margin-bottom: 1.5rem; margin-top: 2rem;'>🔍 症状自检工具</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #5a6c7d; margin-bottom: 2rem;'>通过结构化的问答方式，帮助您更准确地描述症状</p>", unsafe_allow_html=True)
    
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
            <h3 style='margin: 0 0 1rem 0;'>✨ 工具特点</h3>
            <ul style='margin: 0; padding-left: 1.5rem;'>
                <li>按身体部位分类，便于快速定位</li>
                <li>结构化问答，确保信息完整</li>
                <li>严重程度评估，帮助判断紧急程度</li>
                <li>生成详细报告，可直接用于AI咨询</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tool_col2:
        st.markdown("""
        <div style='background: #e8f4fd; border: 1px solid #b3d9ff; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; border-left: 4px solid #2196F3;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #1976D2;'>💡 使用建议</h4>
            <p style='margin: 0; color: #424242;'>建议先使用症状自检工具生成详细描述，然后点击"开始AI咨询"按钮，系统会自动跳转到AI咨询页面并开始分析您的症状，这样可以获得更准确的医疗建议。</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 注意事项
    st.markdown("<h2 style='color: #2c3e50; margin-bottom: 1.5rem; margin-top: 2rem;'>⚠️ 重要注意事项</h2>", unsafe_allow_html=True)
    
    notice_col1, notice_col2 = st.columns(2)
    
    with notice_col1:
        st.markdown("""
        <div style='background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; border-left: 4px solid #f39c12;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #856404;'>🚨 紧急情况</h4>
            <p style='margin: 0; color: #856404;'>如果您出现以下症状，请立即就医或拨打120：</p>
            <ul style='margin: 0.5rem 0 0 0; color: #856404; padding-left: 1.5rem;'>
                <li>剧烈胸痛、呼吸困难</li>
                <li>意识丧失、严重外伤</li>
                <li>大量出血、休克症状</li>
                <li>急性腹痛、高热不退</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with notice_col2:
        st.markdown("""
        <div style='background: #e8f4fd; border: 1px solid #b3d9ff; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; border-left: 4px solid #2196F3;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #1976D2;'>📋 使用限制</h4>
            <ul style='margin: 0; color: #424242; padding-left: 1.5rem;'>
                <li>本系统提供的建议仅供参考，不能替代专业医生诊断</li>
                <li>不提供具体的药物处方，只能给出用药建议</li>
                <li>不处理紧急医疗情况，紧急情况请立即就医</li>
                <li>不提供手术建议，手术相关问题请咨询外科医生</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# 行动号召区域
st.markdown("""
<div class='cta-section'>
    <h2 style='margin-bottom: 1rem; font-size: 2rem;'>🚀 开始您的智能医疗咨询之旅</h2>
    <p style='font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.9;'>专业AI助手随时为您提供医疗咨询服务，让健康管理更简单</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button('🔍 症状自检工具', key='symptom_checker_bottom', use_container_width=True, type='secondary'):
        st.switch_page('pages/2_症状自检工具.py')
with col2:
    if st.button('立即开始咨询 →', key='bottom_cta', use_container_width=True, type='primary'):
        st.switch_page('pages/1_医脉通.py')

# 免责声明
st.markdown("""
<div class='info-card' style='background: #fff3cd; border-left: 5px solid #ffc107;'>
    <h3 style='color: #856404; margin-bottom: 1rem;'>⚠️ 重要提示</h3>
    <p style='color: #856404; font-size: 0.9rem; line-height: 1.6;'>
        本系统提供的医疗建议仅供参考，不能替代专业医生的诊断和治疗。如有严重症状或紧急情况，请立即就医。
        使用本系统即表示您同意我们的服务条款和隐私政策。
    </p>
</div>
""", unsafe_allow_html=True)

# 项目信息
st.markdown("""
<div class='footer'>
    <p>© 2025 AIE直通车 | Powered by LChuck</p>
    <p style='font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;'>致力于让AI技术服务于人类健康事业</p>
</div>
""", unsafe_allow_html=True)
