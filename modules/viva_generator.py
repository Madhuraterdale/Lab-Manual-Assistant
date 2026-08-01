from services.llm_service import ask_llm


def generate_viva_questions(experiment):
    """
    Generate viva questions and answers from selected experiment.
    """

    title = experiment.get("title", "")
    sections = experiment.get("sections", {})

    aim = sections.get("aim", "")
    theory = sections.get("theory", "")
    procedure = sections.get("procedure", "")
    result = sections.get("result", "")
    requirements = sections.get("requirements", "")
    content = experiment.get("content", "")

    prompt = f"""
You are an AI Lab Manual Assistant.

Generate viva questions and answers ONLY from the selected experiment content.

Selected Experiment:

Title:
{title}

Aim:
{aim}

Theory:
{theory}

Equipment / Requirements:
{requirements}

Procedure:
{procedure}

Result / Output:
{result}

Full Content:
{content}

Rules:
- Do not use outside knowledge.
- Questions should be based on this selected experiment only.
- If theory is missing, use aim, procedure, result, and title.
- Keep answers simple and student-friendly.

Generate in this format:

## Basic Viva Questions

1. Question:
Answer:

2. Question:
Answer:

3. Question:
Answer:

4. Question:
Answer:

5. Question:
Answer:

## Important Viva Questions

1. Question:
Answer:

2. Question:
Answer:

3. Question:
Answer:

4. Question:
Answer:

5. Question:
Answer:
"""

    return ask_llm(prompt)