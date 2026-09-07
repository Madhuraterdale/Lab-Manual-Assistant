import streamlit as st

from modules.file_processor import extract_text_from_file
from modules.experiment_parser import ExperimentParser
from modules.procedure_extractor import ProcedureExtractor
from modules.equipment_extractor import extract_equipment
from modules.theory_explainer import explain_theory
from modules.troubleshooting import generate_troubleshooting
from modules.safety_extractor import extract_safety_guidelines
from modules.viva_generator import generate_viva_questions
from modules.lab_report_generator import generate_lab_report

# Week 6 modules
from modules.prelab_generator import generate_pre_lab
from modules.data_analyzer import analyze_data
from modules.study_material_generator import generate_study_material

from services.llm_service import ask_llm


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Lab Manual Assistant",
    page_icon=None,
    layout="wide"
)

# Custom Styling for Professional UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Main font override */
html, body, [data-testid="stAppViewContainer"], .st-emotion-cache-18ni7ap, .st-emotion-cache-12w0qpk {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

/* Gradient Text */
.gradient-text {
    background: linear-gradient(135deg, #A5B4FC 0%, #6366F1 50%, #4F46E5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: white;
    font-weight: 800;
}

/* Custom Card Container */
.custom-card {
    background: rgba(30, 41, 59, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.custom-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4) !important;
    box-shadow: 0 12px 40px 0 rgba(255, 255, 255, 1) !important;
}

/* Timeline steps */
.step-container {
    border-left: 3px solid #6366F1;
    margin-left: 20px;
    padding-left: 25px;
    position: relative;
    padding-bottom: 20px;
}
.step-badge {
    position: absolute;
    left: -13px;
    top: 0px;
    background: #6366F1;
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    box-shadow: 0 0 10px rgba(255, 255, 255, 1);
}

/* Streamlit Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(255, 255, 255, 1) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%) !important;
    border: none !important;
}

div.stButton > button:active {
    transform: translateY(1px) !important;
}

/* File Uploader styling */
[data-testid="stFileUploader"] {
    background: rgba(17, 24, 39, 0.3) !important;
    border: 1px dashed rgba(99, 102, 241, 0.4) !important;
    border-radius: 14px !important;
    padding: 14px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99, 102, 241, 0.8) !important;
    background: rgba(17, 24, 39, 0.5) !important;
}

/* Custom Sidebar styling */
.css-1542f7a, .st-emotion-cache-6qob1r {
    background-color: #111827 !important;
}

/* Tabs Navigation Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: rgba(17, 24, 39, 0.6) !important;
    padding: 8px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}
.stTabs [data-baseweb="tab"] {
    height: 42px !important;
    background-color: transparent !important;
    border-radius: 10px !important;
    color: #9CA3AF !important;
    padding: 0px 18px !important;
    font-weight: 500 !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
}
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* Custom Table Styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 14px;
    text-align: left;
}
th {
    background-color: rgba(99, 102, 241, 0.15) !important;
    color: #A5B4FC !important;
    font-weight: 600;
    padding: 12px;
    border-bottom: 2px solid rgba(99, 102, 241, 0.3);
}
td {
    padding: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    color: #E5E7EB;
}
tr:hover {
    background-color: rgba(255, 255, 255, 0.02);
}

/* Input fields styling */
div[data-baseweb="input"] {
    background-color: rgba(17, 24, 39, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
}
input {
    color: #ffffff !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px; margin-top: -30px;">
        <h1 class="gradient-text" style="margin: 0; font-size: 2.5rem; font-weight: 800; line-height: 1.2;">
            AI Lab Manual Assistant
        </h1>
    </div>
    <p style="color: #9CA3AF; font-size: 1.1rem; margin-bottom: 25px;">
        Your intelligent laboratory co-pilot. Get pre-lab guides, step-by-step procedures, data analysis, safety alerts, viva prep, and instant AI tutor.
    </p>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR / FILE UPLOAD
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px; margin-top: -10px;">
            <h2 class="gradient-text" style="margin: 0; font-size: 1.5rem; font-weight: 700;">AI Lab Console</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Upload Lab Manual",
        type=["pdf", "docx", "txt"],
        help="Upload PDF, DOCX or TXT manual"
    )


if uploaded_file:

    # -----------------------------------------------------
    # PROCESS NEW FILE
    # -----------------------------------------------------

    if (
        "file_name" not in st.session_state
        or st.session_state["file_name"] != uploaded_file.name
    ):

        with st.spinner("Reading uploaded file..."):

            text, error = extract_text_from_file(uploaded_file)

        if error:
            st.error(error)
            st.stop()

        parser = ExperimentParser(text)

        experiments = parser.find_experiments()

        st.session_state["file_name"] = uploaded_file.name
        st.session_state["manual_text"] = text
        st.session_state["experiments"] = experiments


    # -----------------------------------------------------
    # GET EXPERIMENTS
    # -----------------------------------------------------

    experiments = st.session_state["experiments"]


    if not experiments:

        st.warning(
            "No experiments detected. Use headings like "
            "Experiment 1, Practical 1, Program 1, Activity 1, "
            "or Exercise 1."
        )

        st.stop()


    # -----------------------------------------------------
    # EXPERIMENT SELECTION (IN SIDEBAR)
    # -----------------------------------------------------

    options = [
        f"{exp['type']} {exp['number']} - {exp['title']}"
        for exp in experiments
    ]

    with st.sidebar:
        st.markdown("---")
        st.markdown("### Selection")
        selected = st.selectbox(
            "Select Experiment",
            options
        )
        
        selected_index = options.index(selected)
        experiment = experiments[selected_index]

        st.markdown("---")
        st.markdown("### Console Stats")
        st.markdown(f"""
            <div style="font-size: 0.9rem; color: #9CA3AF; line-height: 1.8;">
                <div><b>File:</b> {uploaded_file.name}</div>
                <div><b>Total Labs:</b> {len(experiments)}</div>
                <div><b>Active Lab:</b> {experiment['type']} {experiment['number']}</div>
            </div>
        """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # EXTRACT EXPERIMENT INFORMATION
    # -----------------------------------------------------

    procedure_extractor = ProcedureExtractor(
        experiment
    )

    procedure_steps = (
        procedure_extractor.get_procedure_steps()
    )


    equipment = extract_equipment(
        experiment,
        procedure_steps
    )


    troubleshooting = generate_troubleshooting(
        experiment
    )


    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    (
        tab1,
        tab2,
        tab3,
        tab4,
        tab5,
        tab6,
        tab7,
        tab8,
        tab9,
        tab10,
        tab11,
        tab12
    ) = st.tabs(
        [
            "Overview",
            "Pre-Lab",
            "Procedure",
            "Theory",
            "Equipment",
            "Safety",
            "Troubleshooting",
            "Viva Questions",
            "Lab Report",
            "Data Analysis",
            "Study Notes",
            "Ask AI"
        ]
    )


    # =====================================================
    # TAB 1 - OVERVIEW
    # =====================================================

    with tab1:
        st.markdown(f"""
            <div class="custom-card" style="margin-top: 15px;">
                <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #818CF8; font-weight: 700; margin-bottom: 5px;">
                    {experiment['type']} {experiment['number']}
                </div>
                <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #FFFFFF;">
                    {experiment['title']}
                </h2>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="custom-card" style="height: 100%;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                        <h3 style="margin: 0; font-size: 1.25rem; font-weight: 600; color: #A5B4FC;">Aim / Objectives</h3>
                    </div>
            """, unsafe_allow_html=True)
            sections = experiment.get("sections", {})
            aim = sections.get("aim", "")
            if aim:
                st.write(aim)
            else:
                st.info("Aim not found in manual.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class="custom-card" style="height: 100%;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                        <h3 style="margin: 0; font-size: 1.25rem; font-weight: 600; color: #A5B4FC;">Expected Outcomes / Results</h3>
                    </div>
            """, unsafe_allow_html=True)
            result = sections.get("result", "")
            if result:
                st.write(result)
            else:
                st.info("Result or output not found in manual.")
            st.markdown("</div>", unsafe_allow_html=True)


    # =====================================================
    # TAB 2 - PRE-LAB
    # =====================================================

    with tab2:

        st.header("Pre-Lab Preparation")

        st.write(
            "Prepare for the selected experiment "
            "before starting the practical."
        )


        if st.button(
            "Generate Pre-Lab Guide",
            key="generate_prelab"
        ):

            with st.spinner(
                "Preparing pre-lab guide..."
            ):

                try:

                    prelab = generate_pre_lab(
                        experiment
                    )

                    st.markdown(prelab)

                except Exception as e:

                    st.error(
                        f"Pre-lab generation failed: {e}"
                    )


    # =====================================================
    # TAB 3 - PROCEDURE
    # =====================================================

    with tab3:
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        if procedure_steps:
            for step in procedure_steps:
                st.markdown(f"""
                    <div class="step-container">
                        <div class="step-badge">{step['step_number']}</div>
                        <div class="custom-card" style="margin: 0; padding: 20px;">
                            <h4 style="margin: 0 0 10px 0; color: #FFFFFF; font-size: 1.1rem;">
                                {step['action']}
                            </h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px; font-size: 0.9rem;">
                                <div>
                                    <span style="color: #818CF8; font-weight: 600;">Equipment:</span><br/>
                                    <span style="color: #D1D5DB;">{step['equipment_used'] or 'None specified'}</span>
                                </div>
                                <div>
                                    <span style="color: #34D399; font-weight: 600;">Expected Observation:</span><br/>
                                    <span style="color: #D1D5DB;">{step['expected_observation'] or 'None specified'}</span>
                                </div>
                                <div>
                                    <span style="color: #FBBF24; font-weight: 600;">Important Note:</span><br/>
                                    <span style="color: #D1D5DB;">{step['important_note'] or 'None specified'}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Procedure section not found in manual.")


    # =====================================================
    # TAB 4 - THEORY
    # =====================================================

    with tab4:

        st.header(
            "AI Theory Explanation"
        )


        theory = experiment.get(
            "sections",
            {}
        ).get(
            "theory",
            ""
        )


        if theory:

            st.subheader(
                "Theory from Manual"
            )

            st.write(theory)

        else:

            st.info(
                "Theory section not directly "
                "found in manual."
            )


        if st.button(
            "Generate Theory",
            key="generate_theory"
        ):

            with st.spinner(
                "Generating theory explanation..."
            ):

                try:

                    answer = explain_theory(
                        experiment
                    )

                    st.markdown(answer)

                except Exception as e:

                    st.error(
                        f"AI theory failed: {e}"
                    )


    # =====================================================
    # TAB 5 - EQUIPMENT
    # =====================================================

    with tab5:

        st.header(
            "Equipment and Tools"
        )


        if equipment:

            st.table(equipment)

        else:

            st.info(
                "No equipment or tools clearly found."
            )


    # =====================================================
    # TAB 6 - SAFETY
    # =====================================================

    with tab6:

        st.header(
            "Safety Guidelines"
        )


        st.write(
            "Generate safety precautions based "
            "on the selected experiment."
        )


        if st.button(
            "Generate Safety Guidelines",
            key="generate_safety"
        ):

            with st.spinner(
                "Generating experiment-specific "
                "safety guidelines..."
            ):

                try:

                    safety_guidelines = (
                        extract_safety_guidelines(
                            experiment,
                            procedure_steps
                        )
                    )


                    if safety_guidelines:

                        st.table(
                            safety_guidelines
                        )

                    else:

                        st.info(
                            "No safety guidelines generated."
                        )

                except Exception as e:

                    st.error(
                        f"Safety generation failed: {e}"
                    )


    # =====================================================
    # TAB 7 - TROUBLESHOOTING
    # =====================================================

    with tab7:

        st.header(
            "Troubleshooting Guide"
        )


        if troubleshooting:

            st.table(
                troubleshooting
            )

        else:

            st.info(
                "No troubleshooting suggestions available."
            )


    # =====================================================
    # TAB 8 - VIVA QUESTIONS
    # =====================================================

    with tab8:

        st.header(
            "Viva Questions"
        )


        st.write(
            "Generate viva questions and answers "
            "based on the selected experiment."
        )


        if st.button(
            "Generate Viva Questions",
            key="generate_viva"
        ):

            with st.spinner(
                "Generating viva questions..."
            ):

                try:

                    viva_answer = (
                        generate_viva_questions(
                            experiment
                        )
                    )

                    st.markdown(
                        viva_answer
                    )

                except Exception as e:

                    st.error(
                        f"Viva generation failed: {e}"
                    )


    # =====================================================
    # TAB 9 - LAB REPORT
    # =====================================================

    with tab9:

        st.header(
            "Lab Report Generator"
        )


        st.write(
            "Generate a structured lab report "
            "from the selected experiment."
        )


        if st.button(
            "Generate Lab Report",
            key="generate_lab_report"
        ):

            with st.spinner(
                "Generating lab report..."
            ):

                try:

                    report = (
                        generate_lab_report(
                            experiment,
                            procedure_steps,
                            equipment
                        )
                    )

                    st.markdown(
                        report
                    )

                except Exception as e:

                    st.error(
                        f"Lab report generation failed: {e}"
                    )


    # =====================================================
    # TAB 10 - DATA ANALYSIS
    # =====================================================

    with tab10:
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        
        col_inp1, col_inp2 = st.columns(2)
        with col_inp1:
            values_text = st.text_input(
                "Enter observations separated by commas",
                placeholder="10, 12, 11, 13",
                key="observation_values"
            )
        with col_inp2:
            theoretical_value = st.number_input(
                "Theoretical value (optional)",
                value=0.0,
                key="theoretical_value"
            )


        if st.button(
            "Analyze Data",
            key="analyze_data"
        ):

            try:

                if not values_text.strip():

                    st.warning(
                        "Please enter experimental values."
                    )

                else:

                    values = [
                        float(x.strip())
                        for x in values_text.split(",")
                    ]


                    theory = (
                        theoretical_value
                        if theoretical_value != 0
                        else None
                    )


                    result_data = analyze_data(
                        values,
                        theory
                    )

                    st.markdown("""
                        <div class="custom-card" style="margin-top: 20px;">
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 600; color: #34D399;">Analysis Metrics</h3>
                            </div>
                    """, unsafe_allow_html=True)

                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        for idx, (key, value) in enumerate(result_data.items()):
                            if value is None:
                                continue
                            if idx % 2 == 0:
                                val_str = f"{value:.4f}" if isinstance(value, float) else str(value)
                                st.markdown(f"**{key}:** `{val_str}`")
                    with col_res2:
                        for idx, (key, value) in enumerate(result_data.items()):
                            if value is None:
                                continue
                            if idx % 2 != 0:
                                val_str = f"{value:.4f}" if isinstance(value, float) else str(value)
                                st.markdown(f"**{key}:** `{val_str}`")
                    st.markdown("</div>", unsafe_allow_html=True)

            except ValueError:

                st.error(
                    "Please enter valid numbers separated by commas."
                )


    # =====================================================
    # TAB 11 - STUDY NOTES
    # =====================================================

    with tab11:

        st.header(
            "Study & Revision Notes"
        )


        st.write(
            "Generate revision material from "
            "the selected experiment."
        )


        if st.button(
            "Generate Study Material",
            key="generate_study_material"
        ):

            with st.spinner(
                "Generating revision notes..."
            ):

                try:

                    study_material = (
                        generate_study_material(
                            experiment
                        )
                    )

                    st.markdown(
                        study_material
                    )

                except Exception as e:

                    st.error(
                        f"Study material generation failed: {e}"
                    )


    # =====================================================
    # TAB 12 - ASK AI
    # =====================================================

    with tab12:

        st.header(
            "Ask AI"
        )


        question = st.text_input(
            "Ask a question about this experiment "
            "or the full lab manual",
            key="student_question"
        )


        if st.button(
            "Ask Question",
            key="ask_ai"
        ):

            if not question:

                st.warning(
                    "Please enter a question."
                )

            else:

                selected_experiment_content = (
                    experiment.get(
                        "content",
                        ""
                    )
                )


                full_manual_content = (
                    st.session_state.get(
                        "manual_text",
                        ""
                    )
                )


                prompt = f"""
You are an intelligent AI Lab Manual Assistant.

Your task is to answer student questions using ONLY
the uploaded lab manual content.

You are given two contexts.

1. SELECTED EXPERIMENT:

{selected_experiment_content}


2. FULL LAB MANUAL:

{full_manual_content}


RULES:

- First try to answer from the selected experiment.
- If the question is about another experiment or the
  whole manual, use the full manual.
- Do not use outside knowledge.
- Do not invent facts.
- You may summarize or explain information that is
  supported by the manual.
- Use the experiment title, aim, theory, procedure,
  equipment, safety information, result, and other
  relevant sections.
- For "what did we learn?", use the aim, title,
  procedure, and result.
- For safety questions, use safety information,
  procedure notes, equipment, and relevant manual content.
- For calculations, use formulas or numerical information
  actually provided in the manual.
- If the manual does not contain enough information,
  say exactly:

"The uploaded manual does not contain enough information
to answer this."


The assistant can answer questions such as:

- What is the aim?
- Explain the theory.
- Explain the experiment.
- What is the procedure?
- Give the steps.
- What equipment is required?
- What safety precautions should I follow?
- What are the possible mistakes?
- What is the expected result?
- What did we learn?
- What is the purpose?
- Summarize this experiment.
- Summarize the full manual.
- Explain the code or algorithm in the manual.
- Explain a calculation present in the manual.
- Compare two experiments from the manual.
- Give important viva questions.
- Explain the experiment in simple words.


STUDENT QUESTION:

{question}


Give the answer in simple, student-friendly language.
"""


                with st.spinner(
                    "Generating answer..."
                ):

                    try:

                        answer = ask_llm(
                            prompt
                        )

                        st.markdown(
                            answer
                        )

                    except Exception as e:

                        st.error(
                            f"AI answer failed: {e}"
                        )


# ---------------------------------------------------------
# NO FILE UPLOADED
# ---------------------------------------------------------

else:
    st.markdown("""
        <div class="custom-card" style="text-align: center; padding: 50px 30px; margin-top: 40px;">
            <h2 class="gradient-text" style="font-size: 2.2rem; margin-bottom: 10px; font-weight: 800;">
                Welcome to AI Lab Manual Assistant
            </h2>
            <p style="color: #9CA3AF; font-size: 1.1rem; max-width: 650px; margin: 0 auto 30px auto; line-height: 1.6;">
                Transform static lab manuals into an interactive digital learning environment. 
                Upload your document to generate experiment guides, safety briefings, step-by-step procedures, 
                viva preparation sets, and interactive calculations in seconds.
            </p>
            <div style="display: inline-block; padding: 12px 24px; border: 1px dashed rgba(99, 102, 241, 0.4); border-radius: 12px; color: #A5B4FC; background: rgba(99, 102, 241, 0.05); font-weight: 500;">
                Start by uploading a lab manual in the console sidebar
            </div>
        </div>
    """, unsafe_allow_html=True)