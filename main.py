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
    page_icon="🧪",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🧪 AI Lab Manual Assistant")

st.write(
    "Upload your lab manual and understand experiments with "
    "pre-lab preparation, theory, procedure, equipment, safety, "
    "troubleshooting, viva questions, lab reports, data analysis, "
    "study notes, and AI assistance."
)


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF / DOCX / TXT",
    type=["pdf", "docx", "txt"]
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


    st.success(
        f"{len(experiments)} Experiments Detected"
    )


    # -----------------------------------------------------
    # EXPERIMENT SELECTION
    # -----------------------------------------------------

    options = [
        f"{exp['type']} {exp['number']} - {exp['title']}"
        for exp in experiments
    ]


    selected = st.selectbox(
        "Select Experiment",
        options
    )


    selected_index = options.index(selected)

    experiment = experiments[selected_index]


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

        st.header("📌 Experiment Details")

        st.write(
            f"**Experiment Number:** "
            f"{experiment['number']}"
        )

        st.write(
            f"**Title:** "
            f"{experiment['title']}"
        )


        sections = experiment.get(
            "sections",
            {}
        )


        aim = sections.get(
            "aim",
            ""
        )


        result = sections.get(
            "result",
            ""
        )


        st.subheader("🎯 Aim")

        if aim:
            st.write(aim)
        else:
            st.info(
                "Aim not found in manual."
            )


        st.subheader("✅ Result / Output")

        if result:
            st.write(result)
        else:
            st.info(
                "Result or output not found in manual."
            )


    # =====================================================
    # TAB 2 - PRE-LAB
    # =====================================================

    with tab2:

        st.header("🧑‍🔬 Pre-Lab Preparation")

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

        st.header(
            "⚙️ Step-by-Step Procedure"
        )


        if procedure_steps:

            for step in procedure_steps:

                with st.expander(
                    f"Step {step['step_number']}: "
                    f"{step['action']}"
                ):

                    st.write(
                        f"**Action:** "
                        f"{step['action']}"
                    )

                    st.write(
                        f"**Equipment Used:** "
                        f"{step['equipment_used']}"
                    )

                    st.write(
                        f"**Expected Observation:** "
                        f"{step['expected_observation']}"
                    )

                    st.write(
                        f"**Important Note:** "
                        f"{step['important_note']}"
                    )

        else:

            st.info(
                "Procedure section not found in manual."
            )


    # =====================================================
    # TAB 4 - THEORY
    # =====================================================

    with tab4:

        st.header(
            "📖 AI Theory Explanation"
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
            "🔬 Equipment / Tools"
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
            "🛡️ Experiment-Specific Safety Guidelines"
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
            "⚠️ Basic Troubleshooting"
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
            "🎤 Viva Questions"
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
            "📝 Lab Report Generator"
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

        st.header(
            "📊 Experimental Data Analysis"
        )


        st.write(
            "Enter numerical observations "
            "from your experiment."
        )


        values_text = st.text_input(
            "Enter observations separated by commas",
            placeholder="10, 12, 11, 13",
            key="observation_values"
        )


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


                    st.subheader(
                        "📈 Analysis Result"
                    )


                    for key, value in result_data.items():

                        if value is None:
                            continue


                        if isinstance(
                            value,
                            float
                        ):

                            st.write(
                                f"**{key}:** "
                                f"{value:.4f}"
                            )

                        else:

                            st.write(
                                f"**{key}:** "
                                f"{value}"
                            )


            except ValueError:

                st.error(
                    "Please enter valid numbers "
                    "separated by commas."
                )


    # =====================================================
    # TAB 11 - STUDY NOTES
    # =====================================================

    with tab11:

        st.header(
            "📚 Study & Revision Notes"
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
            "🤖 Ask AI"
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

    st.info(
        "Please upload a lab manual to begin."
    )