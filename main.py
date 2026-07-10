import streamlit as st
from modules.pdf_processor import PDFProcessor
from modules.experiment_parser import ExperimentParser
from modules.procedure_extractor import ProcedureExtractor

st.set_page_config(page_title="Lab Manual Assistant", page_icon="🧪", layout="wide")
st.title("🧪 Lab Manual Conversational Assistant")
st.caption("Upload a lab manual and ask about any experiment's procedure or theory.")

if "experiments" not in st.session_state:
    st.session_state.experiments = []
if "manual_text" not in st.session_state:
    st.session_state.manual_text = ""

with st.sidebar:
    st.header("📄 Upload Lab Manual")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file and st.button("Process Manual"):
        with st.spinner("Extracting text and identifying experiments..."):
            processor = PDFProcessor(uploaded_file)
            text = processor.extract_text()
            st.session_state.manual_text = text

            parser = ExperimentParser(text)
            st.session_state.experiments = parser.find_experiments()

        with st.expander("🔍 Debug: Show raw extracted text"):
            st.text(st.session_state.manual_text[:3000])

    if st.session_state.experiments:
        st.subheader("Detected Experiments")
        for exp in st.session_state.experiments:
            st.write(f"**Exp {exp['number']}**: {exp['title']}")

# Main panel
if st.session_state.experiments:
    exp_numbers = [e["number"] for e in st.session_state.experiments]
    selected = st.selectbox("Select an experiment", exp_numbers)

    exp = next(e for e in st.session_state.experiments if e["number"] == selected)
    extractor = ProcedureExtractor(exp["content"])

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Procedure", "📖 Theory", "⚠️ Safety", "🔧 Materials"])

    with tab1:
        steps = extractor.get_procedure_steps()
        if steps:
            for i, step in enumerate(steps, 1):
                st.markdown(f"**Step {i}.** {step}")
        else:
            st.info("No structured procedure detected. Showing raw content:")
            st.write(exp["content"])

    with tab2:
        theory = extractor.get_theory()
        st.write(theory if theory else "No theory section detected.")

    with tab3:
        safety = extractor.get_safety()
        st.write(safety if safety else "No explicit safety section detected — always follow your lab instructor's guidance.")

    with tab4:
        materials = extractor.get_materials()
        st.write(materials if materials else "No materials/apparatus section detected.")

    st.divider()
    st.subheader("💬 Ask a question about this experiment")
    query = st.text_input("e.g. 'What is the procedure of this experiment?'")
    if query:
        # Simple keyword-based answer for now — swap in LangChain/LLM call in Week 3-4
        if "procedure" in query.lower():
            st.write("\n".join(f"{i}. {s}" for i, s in enumerate(extractor.get_procedure_steps(), 1)))
        elif "theory" in query.lower():
            st.write(extractor.get_theory())
        elif "safety" in query.lower():
            st.write(extractor.get_safety())
        else:
            st.info("Basic keyword matching only for now. LLM-based Q&A comes in Week 3-4.")
else:
    st.info("👈 Upload a lab manual PDF from the sidebar to get started.")