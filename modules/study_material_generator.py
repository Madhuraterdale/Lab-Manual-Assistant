from services.llm_service import ask_llm


def generate_study_material(experiment):
    title = experiment.get("title", "")
    content = experiment.get("content", "")

    prompt = f"""
You are an AI Laboratory Study Assistant.

Generate study material ONLY from the selected experiment.

Experiment:
{title}

Content:
{content}

Do not use outside information.
Do not invent facts.

Create:

# Revision Notes

## 1. Key Concepts
List the important concepts.

## 2. Important Definitions
Give important definitions present in the experiment.

## 3. Important Points
Give short revision points.

## 4. Procedure in Short
Summarize the procedure.

## 5. Important Equipment
List important equipment/tools.

## 6. Safety Points
List experiment-specific precautions.

## 7. Viva Revision
Give 5 important viva questions with short answers.

## 8. One-Minute Revision
Give a very short final revision summary.

Use simple student-friendly language.
"""

    return ask_llm(prompt)