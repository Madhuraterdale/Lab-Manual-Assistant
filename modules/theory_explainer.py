from services.llm_service import ask_llm


def explain_theory(experiment):
    sections = experiment.get("sections", {})

    aim = sections.get("aim", "")
    theory = sections.get("theory", "")
    procedure = sections.get("procedure", "")

    if not aim and not theory:
        return "The uploaded manual does not contain enough aim or theory information for this experiment."

    prompt = f"""
You are an AI Lab Manual Assistant.

Use ONLY the uploaded manual content below.
Do not invent information.
If information is missing, clearly say it is not available in the manual.

Experiment Title:
{experiment.get("title", "")}

Aim:
{aim}

Theory:
{theory}

Procedure:
{procedure}

Explain in this format:

1. Simple Theory Explanation
2. Important Concepts
3. Working Principle
4. Connection Between Theory and Procedure
"""

    return ask_llm(prompt)