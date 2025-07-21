# SQLite版本兼容性修复 - 必须在导入任何依赖之前
try:
    import pysqlite3
    import sys
    sys.modules['sqlite3'] = pysqlite3
except ImportError:
    pass

import streamlit as st
import json
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="症状自检工具",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
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
    
    .symptom-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e8ed;
        transition: all 0.3s ease;
    }
    
    .symptom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .body-part-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e1e8ed;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .body-part-card:hover {
        border-color: #667eea;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .body-part-card.selected {
        border-color: #667eea;
        background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 8px;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .severity-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .severity-low {
        background: #e8f5e8;
        color: #2e7d32;
    }
    
    .severity-medium {
        background: #fff3cd;
        color: #856404;
    }
    
    .severity-high {
        background: #ffebee;
        color: #c62828;
    }
    
    .severity-emergency {
        background: #ff1744;
        color: white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .result-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 症状数据定义
SYMPTOM_DATA = {
    "头部": {
        "icon": "🧠",
        "symptoms": {
            "头痛": {
                "questions": [
                    "疼痛位置在哪里？",
                    "疼痛性质如何？",
                    "疼痛持续时间？",
                    "是否有其他症状？"
                ],
                "options": {
                    "疼痛位置": ["前额", "后脑勺", "太阳穴", "整个头部", "单侧头部"],
                    "疼痛性质": ["胀痛", "刺痛", "跳痛", "钝痛", "压迫感"],
                    "持续时间": ["几分钟", "几小时", "几天", "持续存在", "间歇性"],
                    "伴随症状": ["恶心呕吐", "头晕", "视力模糊", "发热", "无其他症状"]
                }
            },
            "头晕": {
                "questions": [
                    "头晕类型？",
                    "发作频率？",
                    "持续时间？",
                    "诱发因素？"
                ],
                "options": {
                    "头晕类型": ["旋转性眩晕", "非旋转性头晕", "站立时头晕", "行走不稳"],
                    "发作频率": ["偶尔", "经常", "每天", "持续存在"],
                    "持续时间": ["几秒钟", "几分钟", "几小时", "持续存在"],
                    "诱发因素": ["体位改变", "疲劳", "压力", "无明确诱因"]
                }
            }
        }
    },
    "胸部": {
        "icon": "🫀",
        "symptoms": {
            "胸痛": {
                "questions": [
                    "疼痛位置？",
                    "疼痛性质？",
                    "诱发因素？",
                    "缓解方式？"
                ],
                "options": {
                    "疼痛位置": ["左侧胸部", "右侧胸部", "胸骨后", "整个胸部"],
                    "疼痛性质": ["压迫感", "刺痛", "钝痛", "烧灼感"],
                    "诱发因素": ["运动", "情绪激动", "呼吸", "无明确诱因"],
                    "缓解方式": ["休息", "药物", "体位改变", "无缓解"]
                }
            },
            "呼吸困难": {
                "questions": [
                    "呼吸困难程度？",
                    "发作时间？",
                    "诱发因素？",
                    "伴随症状？"
                ],
                "options": {
                    "呼吸困难程度": ["轻度", "中度", "重度", "无法呼吸"],
                    "发作时间": ["活动时", "休息时", "夜间", "持续存在"],
                    "诱发因素": ["运动", "过敏", "感染", "无明确诱因"],
                    "伴随症状": ["咳嗽", "胸痛", "发热", "无其他症状"]
                }
            }
        }
    },
    "腹部": {
        "icon": "🫃",
        "symptoms": {
            "腹痛": {
                "questions": [
                    "疼痛位置？",
                    "疼痛性质？",
                    "发作时间？",
                    "伴随症状？"
                ],
                "options": {
                    "疼痛位置": ["上腹部", "下腹部", "左侧", "右侧", "整个腹部"],
                    "疼痛性质": ["绞痛", "钝痛", "刺痛", "胀痛"],
                    "发作时间": ["餐后", "空腹", "夜间", "持续存在"],
                    "伴随症状": ["恶心呕吐", "腹泻", "便秘", "发热"]
                }
            },
            "恶心呕吐": {
                "questions": [
                    "呕吐频率？",
                    "呕吐物性质？",
                    "诱发因素？",
                    "缓解方式？"
                ],
                "options": {
                    "呕吐频率": ["偶尔", "频繁", "持续", "间歇性"],
                    "呕吐物性质": ["食物", "胆汁", "血液", "清水"],
                    "诱发因素": ["进食", "运动", "药物", "无明确诱因"],
                    "缓解方式": ["休息", "药物", "禁食", "无缓解"]
                }
            }
        }
    },
    "四肢": {
        "icon": "🦵",
        "symptoms": {
            "关节疼痛": {
                "questions": [
                    "疼痛关节？",
                    "疼痛性质？",
                    "活动影响？",
                    "伴随症状？"
                ],
                "options": {
                    "疼痛关节": ["膝关节", "髋关节", "肩关节", "腕关节", "踝关节"],
                    "疼痛性质": ["酸痛", "刺痛", "僵硬", "肿胀"],
                    "活动影响": ["活动时加重", "休息时加重", "晨僵", "无影响"],
                    "伴随症状": ["肿胀", "发热", "活动受限", "无其他症状"]
                }
            },
            "肢体麻木": {
                "questions": [
                    "麻木部位？",
                    "麻木程度？",
                    "持续时间？",
                    "诱发因素？"
                ],
                "options": {
                    "麻木部位": ["手指", "脚趾", "手臂", "腿部", "面部"],
                    "麻木程度": ["轻微", "明显", "完全", "间歇性"],
                    "持续时间": ["几分钟", "几小时", "几天", "持续存在"],
                    "诱发因素": ["体位", "压力", "温度", "无明确诱因"]
                }
            }
        }
    }
}

# 严重程度评估
SEVERITY_LEVELS = {
    "轻度": {
        "color": "severity-low",
        "icon": "🟢",
        "description": "症状轻微，不影响日常生活"
    },
    "中度": {
        "color": "severity-medium", 
        "icon": "🟡",
        "description": "症状明显，部分影响日常生活"
    },
    "重度": {
        "color": "severity-high",
        "icon": "🔴", 
        "description": "症状严重，严重影响日常生活"
    },
    "紧急": {
        "color": "severity-emergency",
        "icon": "🚨",
        "description": "需要立即就医的紧急情况"
    }
}

def initialize_session_state():
    """初始化会话状态"""
    if 'symptom_checker_step' not in st.session_state:
        st.session_state.symptom_checker_step = 0
    if 'selected_body_part' not in st.session_state:
        st.session_state.selected_body_part = None
    if 'selected_symptom' not in st.session_state:
        st.session_state.selected_symptom = None
    if 'symptom_answers' not in st.session_state:
        st.session_state.symptom_answers = {}
    if 'symptom_severity' not in st.session_state:
        st.session_state.symptom_severity = "轻度"

def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #2c3e50; font-size: 2.5rem; margin-bottom: 0.5rem;'>🔍 症状自检工具</h1>
        <p style='color: #5a6c7d; font-size: 1.1rem;'>通过结构化问答，帮助您更准确地描述症状</p>
    </div>
    """, unsafe_allow_html=True)

def render_progress_bar():
    """渲染进度条"""
    steps = ["选择身体部位", "选择症状", "详细描述", "严重程度", "生成报告"]
    current_step = st.session_state.symptom_checker_step
    
    progress = (current_step + 1) / len(steps)
    
    st.markdown(f"""
    <div style='margin: 2rem 0;'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
            {''.join([f'<span style="color: {"#667eea" if i <= current_step else "#ccc"}; font-weight: {"600" if i <= current_step else "400"};">{step}</span>' for i, step in enumerate(steps)])}
        </div>
        <div class='progress-bar' style='width: {progress * 100}%;'></div>
    </div>
    """, unsafe_allow_html=True)

def step_1_select_body_part():
    """步骤1：选择身体部位"""
    st.markdown("""
    <div class='symptom-card'>
        <h2 style='color: #2c3e50; margin-bottom: 1.5rem;'>📍 请选择症状出现的身体部位</h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, (body_part, data) in enumerate(SYMPTOM_DATA.items()):
        with cols[i % 2]:
            is_selected = st.session_state.selected_body_part == body_part
            st.markdown(f"""
            <div class='body-part-card {"selected" if is_selected else ""}' 
                     onclick='document.querySelector("[data-testid=stButton] button").click()'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>{data['icon']}</div>
                <h3 style='margin: 0; font-size: 1.2rem;'>{body_part}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"选择 {body_part}", key=f"body_part_{body_part}", use_container_width=True):
                st.session_state.selected_body_part = body_part
                st.session_state.symptom_checker_step = 1
                st.rerun()

def step_2_select_symptom():
    """步骤2：选择具体症状"""
    if not st.session_state.selected_body_part:
        st.error("请先选择身体部位")
        return
    
    body_part_data = SYMPTOM_DATA[st.session_state.selected_body_part]
    
    st.markdown(f"""
    <div class='symptom-card'>
        <h2 style='color: #2c3e50; margin-bottom: 1rem;'>
            {body_part_data['icon']} {st.session_state.selected_body_part} - 请选择具体症状
        </h2>
        <p style='color: #5a6c7d; margin-bottom: 1.5rem;'>请选择最符合您情况的症状</p>
    </div>
    """, unsafe_allow_html=True)
    
    symptoms = list(body_part_data['symptoms'].keys())
    
    for symptom in symptoms:
        if st.button(f"📋 {symptom}", key=f"symptom_{symptom}", use_container_width=True):
            st.session_state.selected_symptom = symptom
            st.session_state.symptom_checker_step = 2
            st.rerun()
    
    if st.button("🔙 返回选择身体部位", key="back_to_body_part"):
        st.session_state.symptom_checker_step = 0
        st.session_state.selected_body_part = None
        st.rerun()

def step_3_detailed_description():
    """步骤3：详细描述症状"""
    if not st.session_state.selected_symptom:
        st.error("请先选择症状")
        return
    
    body_part = st.session_state.selected_body_part
    symptom = st.session_state.selected_symptom
    symptom_data = SYMPTOM_DATA[body_part]['symptoms'][symptom]
    
    st.markdown(f"""
    <div class='symptom-card'>
        <h2 style='color: #2c3e50; margin-bottom: 1rem;'>
            📝 详细描述您的 {symptom}
        </h2>
        <p style='color: #5a6c7d; margin-bottom: 1.5rem;'>请回答以下问题，帮助我们更好地了解您的症状</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 收集症状详细信息
    answers = {}
    
    for question in symptom_data['questions']:
        st.markdown(f"**{question}**")
        
        # 获取该问题的选项
        question_key = None
        for key, options in symptom_data['options'].items():
            if question in key or key in question:
                question_key = key
                break
        
        if question_key and question_key in symptom_data['options']:
            options = symptom_data['options'][question_key]
            selected = st.selectbox(
                f"选择答案",
                options,
                key=f"answer_{question_key}",
                label_visibility="collapsed"
            )
            answers[question_key] = selected
        else:
            # 如果没有预设选项，使用文本输入
            text_answer = st.text_input(
                f"请输入答案",
                key=f"text_answer_{question}",
                label_visibility="collapsed"
            )
            answers[question] = text_answer
    
    st.session_state.symptom_answers = answers
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 返回选择症状", key="back_to_symptom"):
            st.session_state.symptom_checker_step = 1
            st.session_state.selected_symptom = None
            st.rerun()
    
    with col2:
        if st.button("➡️ 下一步：评估严重程度", key="next_to_severity"):
            st.session_state.symptom_checker_step = 3
            st.rerun()

def step_4_severity_assessment():
    """步骤4：严重程度评估"""
    st.markdown("""
    <div class='symptom-card'>
        <h2 style='color: #2c3e50; margin-bottom: 1rem;'>⚠️ 症状严重程度评估</h2>
        <p style='color: #5a6c7d; margin-bottom: 1.5rem;'>请评估您症状的严重程度</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示严重程度选项
    for level, data in SEVERITY_LEVELS.items():
        is_selected = st.session_state.symptom_severity == level
        
        st.markdown(f"""
        <div class='symptom-card' style='border-left: 5px solid {"#667eea" if is_selected else "#e1e8ed"};'>
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <span style='font-size: 1.5rem;'>{data['icon']}</span>
                <div style='flex: 1;'>
                    <h3 style='margin: 0 0 0.5rem 0; color: #2c3e50;'>{level}</h3>
                    <p style='margin: 0; color: #5a6c7d; font-size: 0.9rem;'>{data['description']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"选择 {level}", key=f"severity_{level}", use_container_width=True):
            st.session_state.symptom_severity = level
            st.session_state.symptom_checker_step = 4
            st.rerun()
    
    if st.button("🔙 返回详细描述", key="back_to_description"):
        st.session_state.symptom_checker_step = 2
        st.rerun()

def step_5_generate_report():
    """步骤5：生成症状报告"""
    st.markdown("""
    <div class='symptom-card'>
        <h2 style='color: #2c3e50; margin-bottom: 1rem;'>📋 症状自检报告</h2>
        <p style='color: #5a6c7d; margin-bottom: 1.5rem;'>基于您的描述生成的详细症状报告</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 生成症状描述
    body_part = st.session_state.selected_body_part
    symptom = st.session_state.selected_symptom
    severity = st.session_state.symptom_severity
    answers = st.session_state.symptom_answers
    
    # 构建详细描述
    description_parts = []
    description_parts.append(f"【症状自检报告】")
    description_parts.append(f"主要症状：{symptom}")
    description_parts.append(f"症状部位：{body_part}")
    description_parts.append(f"严重程度：{severity}")
    description_parts.append(f"")
    description_parts.append(f"【详细描述】")
    
    for question, answer in answers.items():
        description_parts.append(f"• {question}：{answer}")
    
    description_parts.append(f"")
    description_parts.append(f"请根据以上症状描述，为我提供专业的医疗建议和分析。")
    
    detailed_description = "\n".join(description_parts)
    
    # 显示报告
    st.markdown(f"""
    <div class='result-card'>
        <h3 style='color: #2c3e50; margin-bottom: 1rem;'>📋 症状详细描述</h3>
        <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea;'>
            <pre style='margin: 0; white-space: pre-wrap; font-family: inherit; line-height: 1.6;'>{detailed_description}</pre>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 严重程度提示
    severity_data = SEVERITY_LEVELS[severity]
    st.markdown(f"""
    <div class='result-card'>
        <div class='severity-indicator {severity_data["color"]}'>
            <span>{severity_data['icon']}</span>
            <span>严重程度：{severity}</span>
        </div>
        <p style='margin: 1rem 0 0 0; color: #5a6c7d;'>{severity_data['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 操作按钮
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔙 重新开始", key="restart_checker"):
            st.session_state.symptom_checker_step = 0
            st.session_state.selected_body_part = None
            st.session_state.selected_symptom = None
            st.session_state.symptom_answers = {}
            st.session_state.symptom_severity = "轻度"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center; color: white;'>
            <p style='margin: 0; font-size: 0.9rem;'>💡 点击下方按钮将自动跳转到AI咨询页面并开始分析</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💬 开始AI咨询", key="start_ai_consultation", use_container_width=True):
            # 将症状描述存储到session_state，然后跳转到AI咨询页面
            st.session_state.auto_symptom_description = detailed_description
            st.session_state.auto_consultation = True
            st.switch_page('pages/1_医脉通.py')
    
    with col3:
        # 生成更详细的报告
        report_content = f"""
医脉通智能诊疗系统 - 症状自检报告
{'='*50}
生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
身体部位：{st.session_state.selected_body_part}
主要症状：{st.session_state.selected_symptom}
严重程度：{severity}
{'='*50}

📋 详细症状描述：
{detailed_description}

{'='*50}
⚠️ 重要提醒：
- 本报告仅供个人参考使用
- 不能替代专业医生诊断
- 如有严重症状请及时就医
- 请妥善保管个人健康信息
{'='*50}
        """
        
        st.download_button(
            label="📄 导出报告",
            data=report_content,
            file_name=f"症状自检报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            help="直接下载症状自检报告"
        )
    
    with col4:
        if st.button("📋 复制报告", key="copy_report", use_container_width=True, help="点击后显示报告内容，可手动复制"):
            # 显示报告内容
            st.markdown("### 📋 症状自检报告内容")
            st.markdown("---")
            
            # 使用st.text_area显示内容，便于复制
            st.text_area(
                "症状自检报告",
                value=report_content,
                height=300,
                help="选中全部内容后按 Ctrl+C (Mac: Cmd+C) 复制"
            )
            
            # 提供复制按钮和说明
            col_copy1, col_copy2 = st.columns([1, 1])
            with col_copy1:
                st.success("✅ 报告内容已显示")
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

def main():
    """主函数"""
    initialize_session_state()
    render_header()
    render_progress_bar()
    
    # 根据当前步骤显示相应内容
    if st.session_state.symptom_checker_step == 0:
        step_1_select_body_part()
    elif st.session_state.symptom_checker_step == 1:
        step_2_select_symptom()
    elif st.session_state.symptom_checker_step == 2:
        step_3_detailed_description()
    elif st.session_state.symptom_checker_step == 3:
        step_4_severity_assessment()
    elif st.session_state.symptom_checker_step == 4:
        step_5_generate_report()
    
    # 页面底部信息
    st.markdown("""
    <div style='margin-top: 3rem; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; text-align: center; color: white;'>
        <p style='margin: 0; font-size: 0.9rem; opacity: 0.9;'>
            🔍 症状自检工具 | 🤖 Powered by LChuck | ⚠️ 仅供医疗参考，不替代专业诊断
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 