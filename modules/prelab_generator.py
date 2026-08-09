from services.llm_service import ask_llm


def generate_pre_lab(experiment):
    sections = experiment.get("sections", {})

    title = experiment.get("title", "")
    aim = sections.get("aim", "")
    theory = sections.get("theory", "")
    requirements = sections.get("requirements", "")
    procedure = sections.get("procedure", "")
    content = experiment.get("content", "")

    prompt = f"""
You are an AI Laboratory Assistant.

Create a PRE-LAB preparation guide for the selected experiment.

Use ONLY the information from the selected experiment.

Experiment Title:
{title}

Aim:
{aim}

Theory:
{theory}

Requirements:
{requirements}

Procedure:
{procedure}

Experiment Content:
{content}

Do not invent experiment-specific facts.

Create the following:

# Pre-Lab Preparation

## 1. What should the student know before starting?
Explain important concepts from the manual.

## 2. Objective
Explain what the experiment is trying to achieve.

## 3. Required Equipment / Software
List items mentioned in the manual.

## 4. Important Preparation Steps
List things the student should understand or prepare before starting.

## 5. Important Precautions
Mention only precautions supported by the manual.

## 6. Quick Pre-Lab Questions
Generate 5 questions with short answers.

Keep everything simple and student-friendly.
"""

    return ask_llm(prompt)