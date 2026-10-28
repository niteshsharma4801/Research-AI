
import streamlit as st
from pipeline import run_research_pipeline
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ResearchAI | Multi-Agent Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #e5e7eb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    .hero {
        background: linear-gradient(135deg, #172554, #312e81, #164e63);
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #334155;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 38px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #cbd5e1;
        font-size: 16px;
    }

    .agent-card {
        background: #111c30;
        border: 1px solid #293750;
        padding: 20px;
        border-radius: 15px;
        min-height: 140px;
    }

    .agent-card h4 {
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .agent-card p {
        color: #94a3b8;
        font-size: 14px;
    }

    .report-card {
        background: #111c30;
        padding: 22px;
        border: 1px solid #293750;
        border-radius: 15px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #0891b2);
        color: white;
        border: none;
        border-radius: 10px;
        min-height: 45px;
        font-weight: 600;
        width: 100%;
    }

    .stButton > button:hover {
        border: 1px solid #67e8f9;
        color: white;
    }

    div[data-testid="stMetric"] {
        background: #111c30;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #293750;
    }

    h2, h3 {
        color: #f1f5f9;
    }

    section[data-testid="stSidebar"] {
        background: #080e1b;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🔬 ResearchAI")
    st.caption("Multi-Agent Research Platform")

    st.divider()

    st.markdown("### Agent Architecture")

    st.markdown("""
    **🔎 Search Agent**  
    Finds relevant research sources.

    **📚 Reader Agent**  
    Extracts detailed information.

    **✍️ Writer Chain**  
    Creates the research report.

    **🛡️ Critic Chain**  
    Reviews the final report.
    """)

    st.divider()

    st.markdown("### About")
    st.write(
        "An AI-powered research assistant that combines "
        "search, content extraction, report writing, "
        "and quality review."
    )

    if st.button("🗑️ Clear Research History"):
        st.session_state.research_history = []
        st.session_state.research_result = None
        st.session_state.research_topic = ""
        st.rerun()


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🔬 AI Research Workspace</h1>
    <p>
        Research smarter with collaborative AI agents.
        Discover information, analyze sources, generate reports,
        and review results in one workspace.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- METRICS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("AI Agents & Chains", "4")

with col2:
    st.metric("Research Reports", len(st.session_state.research_history))

with col3:
    st.metric("Workspace", "Ready")


# ---------------- RESEARCH INPUT ----------------

st.markdown("## 🎯 Start Your Research")

with st.form("research_form"):
    topic = st.text_area(
        "Research Topic",
        placeholder=(
            "Example: How are multi-agent AI systems "
            "transforming healthcare in 2026?"
        ),
        height=100,
        help="Enter a specific topic for more useful research."
    )

    submitted = st.form_submit_button(
        "🚀 Start AI Research",
        use_container_width=True
    )


# ---------------- RUN PIPELINE ----------------

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.research_topic = topic.strip()
        st.session_state.research_result = None

        st.markdown("## ⚙️ Research Workflow")

        progress = st.progress(0)

        status = st.empty()

        try:
            status.info("🔎 Agents are researching your topic...")
            progress.progress(10)

            with st.spinner(
                "Your AI agents are working. This may take a while..."
            ):
                result = run_research_pipeline(topic.strip())

            progress.progress(100)
            status.success("✅ Research pipeline completed!")

            st.session_state.research_result = result

            st.session_state.research_history.append({
                "topic": topic.strip(),
                "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "result": result
            })

        except Exception as e:
            status.error("❌ Research failed.")
            st.exception(e)


# ---------------- DISPLAY RESULTS ----------------

result = st.session_state.research_result

if result:
    st.divider()

    st.markdown("## 📊 Research Results")

    st.markdown(
        f"**Topic:** {st.session_state.research_topic}"
    )

    # Agent stage overview
    agent_cols = st.columns(4)

    agent_names = [
        ("🔎", "Search Agent"),
        ("📚", "Reader Agent"),
        ("✍️", "Writer Chain"),
        ("🛡️", "Critic Chain")
    ]

    for col, (emoji, name) in zip(agent_cols, agent_names):
        with col:
            st.markdown(
                f"""
                <div class="agent-card">
                    <h4>{emoji} {name}</h4>
                    <p>Pipeline stage completed</p>
                    <strong style="color:#34d399;">● Complete</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # Search results
    with st.expander("🔎 Search Agent Results", expanded=False):
        st.markdown(
            result.get("search_result", "No search results available.")
        )

    # Scraped content
    with st.expander("📚 Reader Agent — Extracted Content"):
        st.markdown(
            result.get("scraped_content", "No extracted content available.")
        )

    # Final report
    st.markdown("### 📄 Final Research Report")

    report = result.get("report", "")

    st.markdown(
        '<div class="report-card">',
        unsafe_allow_html=True
    )

    if isinstance(report, str):
        st.markdown(report)
    else:
        st.write(report)

    st.markdown("</div>", unsafe_allow_html=True)

    report_text = (
        report if isinstance(report, str) else str(report)
    )

    st.download_button(
        label="⬇️ Download Research Report",
        data=report_text,
        file_name="research_report.md",
        mime="text/markdown",
        use_container_width=True
    )

    # Critic feedback
    st.markdown("### 🛡️ Critic Review")

    feedback = result.get("feedback", "")

    with st.container(border=True):
        if isinstance(feedback, str):
            st.markdown(feedback)
        else:
            st.write(feedback)

    # Full output
    with st.expander("🧩 View Complete Pipeline Output"):
        st.json({
            "topic": st.session_state.research_topic,
            "result": {
                key: str(value)
                for key, value in result.items()
            }
        })

else:
    st.info(
        "👋 Welcome! Enter a research topic above and click "
        "**Start AI Research** to generate your first report."
    )

    st.markdown("### 💡 Try These Research Topics")

    examples = [
        "Latest advances in multi-agent AI systems",
        "Applications of machine learning in healthcare",
        "Generative AI trends and challenges in 2026"
    ]

    for example in examples:
        if st.button(example, key=f"example_{example}"):
            st.session_state.example_topic = example
            st.rerun()

    if st.session_state.get("example_topic"):
        st.caption(
            "Example selected: "
            + st.session_state.example_topic
            + ". Copy it into the Research Topic field above."
        )



# ---------------- FOOTER ----------------


st.divider()

st.markdown("---")
st.markdown(
    "<h4 style='text-align: center; color: #67e8f9;'>"
    "⚡ Powered by Nitesh Sharma ⚡"
    "</h4>",
    unsafe_allow_html=True
)
