import re


def extract_safety_guidelines(experiment, procedure_steps):
    """
    Extract simple safety precautions and guidelines from experiment content.
    If safety is not directly mentioned, create basic guidelines using experiment context.
    """

    content = experiment.get("content", "")
    sections = experiment.get("sections", {})

    safety_items = []

    # 1. Try to extract direct safety/precaution section from manual
    direct_safety_text = extract_direct_safety_section(content)

    if direct_safety_text:
        safety_items.extend(
            convert_text_to_safety_items(
                direct_safety_text,
                "Directly mentioned in manual"
            )
        )

    # 2. Extract warning/caution type lines from whole experiment
    keyword_lines = extract_keyword_based_lines(content)

    for line in keyword_lines:
        safety_items.append({
            "Type": "Manual Guideline",
            "Precaution / Guideline": line,
            "Reason": "This line contains safety or caution related words.",
            "Source": "Detected from manual text"
        })

    # 3. Use procedure notes as safety-related guidelines
    for step in procedure_steps:
        note = step.get("important_note", "")

        if note and note.lower() not in ["no special note.", "no special note"]:
            safety_items.append({
                "Type": "Procedure Guideline",
                "Precaution / Guideline": note,
                "Reason": f"Important note detected in Step {step.get('step_number')}.",
                "Source": "Detected from procedure"
            })

    # 4. If no direct safety is found, create basic context-based guidelines
    if not safety_items:
        safety_items = create_context_based_guidelines(experiment)

    # Remove duplicates
    unique_items = []
    seen = set()

    for item in safety_items:
        text = item["Precaution / Guideline"].strip().lower()

        if text not in seen:
            seen.add(text)
            unique_items.append(item)

    return unique_items


def extract_direct_safety_section(content):
    """
    Find sections like Safety, Precautions, Caution, Warning, Guidelines.
    """

    headings = [
        "Safety",
        "Safety Precautions",
        "Precautions",
        "Precaution",
        "Caution",
        "Warning",
        "Guidelines",
        "Important Instructions",
        "Note"
    ]

    next_headings = [
        "Aim",
        "Objective",
        "Theory",
        "Procedure",
        "Algorithm",
        "Steps",
        "Observation",
        "Result",
        "Output",
        "Conclusion",
        "Viva"
    ]

    heading_pattern = "|".join([re.escape(h) for h in headings])
    next_heading_pattern = "|".join([re.escape(h) for h in next_headings])

    pattern = rf"(?is)\b({heading_pattern})\s*:?\s*(.*?)(?=\n\s*({next_heading_pattern})\s*:|\Z)"

    match = re.search(pattern, content)

    if match:
        return match.group(2).strip()

    return ""


def convert_text_to_safety_items(text, source):
    """
    Convert safety text into table format.
    """

    lines = text.split("\n")

    items = []

    for line in lines:
        line = line.strip()
        line = re.sub(r"^\d+[\.\)]\s*", "", line)
        line = re.sub(r"^[•\-]\s*", "", line)

        if len(line) > 5:
            items.append({
                "Type": "Safety Precaution",
                "Precaution / Guideline": line,
                "Reason": "This precaution is mentioned in the uploaded manual.",
                "Source": source
            })

    return items


def extract_keyword_based_lines(content):
    """
    Extract lines containing safety/caution related keywords.
    """

    keywords = [
        "carefully",
        "ensure",
        "avoid",
        "do not",
        "warning",
        "caution",
        "precaution",
        "safe",
        "safety",
        "check",
        "verify",
        "handle",
        "wear",
        "protect"
    ]

    lines = content.split("\n")
    detected_lines = []

    for line in lines:
        clean_line = line.strip()

        if len(clean_line) < 8:
            continue

        for keyword in keywords:
            if keyword in clean_line.lower():
                detected_lines.append(clean_line)
                break

    return detected_lines


def create_context_based_guidelines(experiment):
    """
    Create simple basic guidelines if the manual does not contain explicit safety section.
    These are generated from experiment context.
    """

    content = experiment.get("content", "").lower()
    title = experiment.get("title", "").lower()

    guidelines = []

    if "python" in content or "program" in title or "function" in title:
        guidelines.extend([
            {
                "Type": "Basic Programming Guideline",
                "Precaution / Guideline": "Check syntax and indentation before running the program.",
                "Reason": "Programming experiments may fail due to syntax or indentation errors.",
                "Source": "Generated from experiment context"
            },
            {
                "Type": "Basic Programming Guideline",
                "Precaution / Guideline": "Test the program with simple input values first.",
                "Reason": "Simple test cases help verify whether the logic is correct.",
                "Source": "Generated from experiment context"
            }
        ])

    elif "database" in content or "sql" in content or "mysql" in content or "oracle" in content:
        guidelines.extend([
            {
                "Type": "Database Guideline",
                "Precaution / Guideline": "Verify table names, column names, and conditions before executing queries.",
                "Reason": "Incorrect queries may give wrong results or errors.",
                "Source": "Generated from experiment context"
            },
            {
                "Type": "Database Guideline",
                "Precaution / Guideline": "Avoid deleting or updating records without checking the condition.",
                "Reason": "Wrong update or delete queries can change important data.",
                "Source": "Generated from experiment context"
            }
        ])

    elif "acid" in content or "base" in content or "chemical" in content or "solution" in content:
        guidelines.extend([
            {
                "Type": "Chemical Safety",
                "Precaution / Guideline": "Handle chemicals carefully and follow laboratory instructions.",
                "Reason": "Chemical experiments require careful handling.",
                "Source": "Generated from experiment context"
            },
            {
                "Type": "Chemical Safety",
                "Precaution / Guideline": "Use clean apparatus and avoid direct contact with chemicals.",
                "Reason": "This helps prevent contamination and unsafe handling.",
                "Source": "Generated from experiment context"
            }
        ])

    elif "circuit" in content or "voltage" in content or "current" in content or "resistor" in content:
        guidelines.extend([
            {
                "Type": "Electrical Safety",
                "Precaution / Guideline": "Check circuit connections before switching on the power supply.",
                "Reason": "Wrong connections may damage components or give wrong readings.",
                "Source": "Generated from experiment context"
            },
            {
                "Type": "Electrical Safety",
                "Precaution / Guideline": "Use proper measuring range while taking readings.",
                "Reason": "Wrong range selection may affect readings or instruments.",
                "Source": "Generated from experiment context"
            }
        ])

    else:
        guidelines.extend([
            {
                "Type": "General Guideline",
                "Precaution / Guideline": "Follow the procedure step by step without skipping any instruction.",
                "Reason": "Missing steps may lead to incorrect output or result.",
                "Source": "Generated from experiment context"
            },
            {
                "Type": "General Guideline",
                "Precaution / Guideline": "Record observations and output carefully.",
                "Reason": "Proper observation helps in understanding the experiment result.",
                "Source": "Generated from experiment context"
            }
        ])

    return guidelines

import json
import re

from services.llm_service import ask_llm


def extract_safety_guidelines(experiment, procedure_steps):
    """
    Generate experiment-specific safety precautions and practical guidelines.
    Output is based only on selected experiment content.
    """

    title = experiment.get("title", "")
    sections = experiment.get("sections", {})

    aim = sections.get("aim", "")
    theory = sections.get("theory", "")
    requirements = sections.get("requirements", "")
    procedure = sections.get("procedure", "")
    result = sections.get("result", "")
    content = experiment.get("content", "")

    procedure_text = format_procedure_steps(procedure_steps)

    prompt = f"""
You are an AI Lab Manual Assistant.

Generate safety precautions and practical guidelines ONLY for the selected experiment.

Use only the selected experiment content below.
Do not give fixed general points.
Do not give unrelated safety points.
Do not use outside knowledge.

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

Structured Procedure Steps:
{procedure_text}

Result / Output:
{result}

Full Selected Experiment Content:
{content}

Rules:
- Each guideline must be related to this selected experiment.
- If it is a programming experiment, give execution/programming guidelines related to its topic.
- If it is a function experiment, give guidelines about function definition, function call, arguments, return value, indentation, and output.
- If it is a database experiment, give guidelines about table names, queries, conditions, and output.
- If it is a chemistry experiment, give safety points related to chemicals/apparatus mentioned.
- If it is an electrical experiment, give safety points related to circuit/components mentioned.
- Mention step number if the guideline is related to a procedure step.
- Avoid generic lines like "be careful" unless connected to this experiment.

Return ONLY valid JSON in this format:

[
  {{
    "Type": "Experiment-Specific Guideline",
    "Precaution / Guideline": "write guideline here",
    "Reason": "why this is needed for this experiment",
    "Source": "Title/Aim/Procedure/Equipment/Manual Content"
  }}
]

Generate 3 to 6 guidelines.
"""

    try:
        response = ask_llm(prompt)
        safety_items = parse_json_response(response)

        if safety_items:
            return clean_safety_items(safety_items)

        return fallback_from_response(response)

    except Exception as e:
        return [{
            "Type": "Safety Generation Error",
            "Precaution / Guideline": "Safety guidelines could not be generated.",
            "Reason": str(e),
            "Source": "AI generation failed"
        }]


def format_procedure_steps(procedure_steps):
    if not procedure_steps:
        return "No structured procedure steps found."

    text = ""

    for step in procedure_steps:
        text += f"""
Step {step.get("step_number", "")}:
Action: {step.get("action", "")}
Equipment Used: {step.get("equipment_used", "")}
Expected Observation: {step.get("expected_observation", "")}
Important Note: {step.get("important_note", "")}
"""

    return text


def parse_json_response(response):
    if not response:
        return []

    response = response.strip()
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    json_match = re.search(r"\[.*\]", response, re.DOTALL)

    if json_match:
        response = json_match.group(0)

    try:
        data = json.loads(response)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def clean_safety_items(items):
    cleaned = []

    for item in items:
        guideline = item.get("Precaution / Guideline", "").strip()
        reason = item.get("Reason", "").strip()
        source = item.get("Source", "").strip()
        item_type = item.get("Type", "").strip()

        if guideline:
            cleaned.append({
                "Type": item_type if item_type else "Experiment-Specific Guideline",
                "Precaution / Guideline": guideline,
                "Reason": reason if reason else "This guideline is related to the selected experiment.",
                "Source": source if source else "Selected experiment content"
            })

    return cleaned


def fallback_from_response(response):
    return [{
        "Type": "Experiment-Specific Guideline",
        "Precaution / Guideline": response if response else "No safety guidelines generated.",
        "Reason": "Generated from selected experiment content.",
        "Source": "AI response"
    }]