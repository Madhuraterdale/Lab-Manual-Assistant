import streamlit as st

from modules.file_processor import extract_text_from_file
from modules.experiment_parser import ExperimentParser
from modules.procedure_extractor import ProcedureExtractor
from modules.equipment_extractor import extract_equipment
from modules.theory_explainer import explain_theory
from modules.troubleshooting import generate_troubleshooting
from services.llm_service import ask_llm


st.set_page_config(
    page_title="AI Lab Manual Assistant",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 AI Lab Manual Assistant")
st.write(
    "Upload your lab manual and understand experiments with theory, procedure, equipment, and troubleshooting."
)

uploaded_file = st.file_uploader(
    "Upload PDF / DOCX / TXT",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

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

    experiments = st.session_state["experiments"]

    if not experiments:
        st.warning(
            "No experiments detected. Use headings like Experiment 1, Practical 1, Program 1, Activity 1, or Exercise 1."
        )
        st.stop()

    st.success(f"{len(experiments)} Experiments Detected")

    options = [
        f"{exp['type']} {exp['number']} - {exp['title']}"
        for exp in experiments
    ]

    selected = st.selectbox("Select Experiment", options)

    selected_index = options.index(selected)
    experiment = experiments[selected_index]

    procedure_extractor = ProcedureExtractor(experiment)
    procedure_steps = procedure_extractor.get_procedure_steps()

    equipment = extract_equipment(experiment, procedure_steps)
    troubleshooting = generate_troubleshooting(experiment)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Overview",
        "Procedure",
        "Theory",
        "Equipment",
        "Troubleshooting",
        "Ask AI"
    ])

    with tab1:
        st.header("📌 Experiment Details")

        st.write(f"**Experiment Number:** {experiment['number']}")
        st.write(f"**Title:** {experiment['title']}")

        sections = experiment.get("sections", {})

        aim = sections.get("aim", "")
        result = sections.get("result", "")

        st.subheader("🎯 Aim")
        if aim:
            st.write(aim)
        else:
            st.info("Aim not found in manual.")

        st.subheader("✅ Result / Output")
        if result:
            st.write(result)
        else:
            st.info("Result or output not found in manual.")

    with tab2:
        st.header("⚙️ Step-by-Step Procedure")

        if procedure_steps:
            for step in procedure_steps:
                with st.expander(f"Step {step['step_number']}: {step['action']}"):
                    st.write(f"**Action:** {step['action']}")
                    st.write(f"**Equipment Used:** {step['equipment_used']}")
                    st.write(f"**Expected Observation:** {step['expected_observation']}")
                    st.write(f"**Important Note:** {step['important_note']}")
        else:
            st.info("Procedure section not found in manual.")

    with tab3:
        st.header("📖 AI Theory Explanation")

        theory = experiment.get("sections", {}).get("theory", "")

        if theory:
            st.subheader("Theory from Manual")
            st.write(theory)
        else:
            st.info("Theory section not directly found in manual.")

        if st.button("Generate Theory"):
            with st.spinner("Generating theory explanation..."):
                try:
                    answer = explain_theory(experiment)
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"AI theory failed: {e}")

    with tab4:
        st.header("🔬 Equipment / Tools")

        if equipment:
            st.table(equipment)
        else:
            st.info("No equipment or tools clearly found.")

    with tab5:
        st.header("⚠️ Basic Troubleshooting")

        if troubleshooting:
            st.table(troubleshooting)
        else:
            st.info("No troubleshooting suggestions available.")

    with tab6:
        st.header("🤖 Ask AI")

        question = st.text_input(
            "Ask question about this experiment or full lab manual"
        )

        if st.button("Ask Question"):
            if not question:
                st.warning("Please enter a question.")
            else:
                selected_experiment_content = experiment.get("content", "")
                full_manual_content = st.session_state.get("manual_text", "")

                prompt = f"""
You are an intelligent AI Lab Manual Assistant.

Your task is to answer student questions using ONLY the uploaded lab manual content.

You are given two contexts:

1. Selected Experiment Content:
{selected_experiment_content}

2. Full Lab Manual Content:
{full_manual_content}

Rules:
- First try to answer from the selected experiment.
- If the question is about another experiment or the whole manual, use the full lab manual content.
- Do not use outside knowledge.
- Do not invent facts.
- If the exact answer is not directly written, you may summarize or explain using related information from the manual.
- You may use the experiment title, aim, theory, procedure, equipment, result, or output to answer.
- If the question asks "what we learned", "learning outcome", "purpose", or "summary", explain it using the aim, title, procedure, and result.
- If the manual truly does not contain enough related information, say:
"The uploaded manual does not contain enough information to answer this."

You can answer questions like:
- What is the aim?
- What is the theory?
- What is the procedure?
- What equipment is required?
- What is the result?
- What did we learn from this experiment?
- Explain this experiment in simple words.
- Give step-by-step explanation.
- What is the purpose of this experiment?
- What are possible mistakes?
- What is experiment 1 about?
- Summarize this experiment.
- Summarize the full manual.
- Explain code or algorithm if present in the manual.

Student Question:
{question}

Give the answer in simple student-friendly language.
"""

                with st.spinner("Generating answer..."):
                    try:
                        answer = ask_llm(prompt)
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"AI answer failed: {e}")

else:
    st.info("Please upload a lab manual to begin.")