from services.llm_service import ask_llm


def generate_lab_report(experiment, procedure_steps, equipment):
    """
    Generate a structured lab report from selected experiment.
    """

    title = experiment.get("title", "")
    sections = experiment.get("sections", {})

    aim = sections.get("aim", "")
    theory = sections.get("theory", "")
    procedure = sections.get("procedure", "")
    result = sections.get("result", "")
    requirements = sections.get("requirements", "")
    content = experiment.get("content", "")

    procedure_text = format_procedure_steps(procedure_steps)
    equipment_text = format_equipment(equipment)

    prompt = f"""
You are an AI Lab Manual Assistant.

Create a structured lab report using ONLY the selected experiment content.

Selected Experiment:

Title:
{title}

Aim:
{aim}

Theory:
{theory}

Equipment / Requirements:
{requirements}

Detected Equipment:
{equipment_text}

Procedure:
{procedure}

Structured Procedure Steps:
{procedure_text}

Result / Output:
{result}

Full Selected Experiment Content:
{content}

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- If any section is missing, write "Not clearly mentioned in the manual."
- Keep language simple and suitable for students.

Generate lab report in this format:

# Lab Report

## 1. Experiment Title

## 2. Aim / Objective

## 3. Theory

## 4. Equipment / Tools Required

## 5. Step-by-Step Procedure

## 6. Safety Precautions / Practical Guidelines

## 7. Expected Result / Output

## 8. Conclusion
"""

    return ask_llm(prompt)


def format_procedure_steps(procedure_steps):
    if not procedure_steps:
        return "No structured procedure steps found."

    text = ""

    for step in procedure_steps:
        text += f"{step.get('step_number', '')}. {step.get('action', '')}\n"

    return text


def format_equipment(equipment):
    if not equipment:
        return "No equipment detected."

    text = ""

    for item in equipment:
        text += f"- {item}\n"

    return text