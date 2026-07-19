import re


def extract_equipment(experiment, procedure_steps):
    sections = experiment.get("sections", {})

    equipment_text = sections.get("requirements", "")

    items = clean_items(equipment_text)

    if not items:
        items = detect_common_tools(experiment.get("content", ""))

    equipment_data = []

    for item in items:
        equipment_data.append({
            "Equipment": item,
            "Purpose": guess_purpose(item),
            "Used In": find_step(item, procedure_steps),
            "Basic Usage": guess_usage(item)
        })

    return equipment_data


def clean_items(text):
    if not text:
        return []

    raw_items = re.split(r",|\n|•|-", text)

    cleaned = []

    for item in raw_items:
        item = item.strip()
        item = re.sub(r"^\d+[\.\)]\s*", "", item)

        if len(item) > 2 and len(item) < 80:
            cleaned.append(item)

    return list(dict.fromkeys(cleaned))


def detect_common_tools(text):
    common_tools = [
        "Python",
        "Python IDLE",
        "VS Code",
        "Jupyter Notebook",
        "Google Colab",
        "MySQL",
        "Oracle",
        "Command Prompt",
        "Terminal",
        "Compiler",
        "Interpreter"
    ]

    detected = []

    for tool in common_tools:
        if tool.lower() in text.lower():
            detected.append(tool)

    return list(dict.fromkeys(detected))


def find_step(item, procedure_steps):
    for step in procedure_steps:
        if item.lower() in step["action"].lower():
            return f"Step {step['step_number']}"

    return "Not clearly specified"


def guess_purpose(item):
    item = item.lower()

    if "python" in item:
        return "Used to write and run Python programs."

    if "vs code" in item:
        return "Used as a code editor."

    if "mysql" in item or "oracle" in item:
        return "Used for database operations."

    if "terminal" in item or "command prompt" in item:
        return "Used to execute commands."

    if "compiler" in item or "interpreter" in item:
        return "Used to run source code."

    return "Purpose is not clearly explained in the manual."


def guess_usage(item):
    item = item.lower()

    if "python" in item:
        return "Open Python, write code, and execute the program."

    if "vs code" in item:
        return "Open project files and edit code."

    if "mysql" in item or "oracle" in item:
        return "Open database tool and run queries."

    if "terminal" in item or "command prompt" in item:
        return "Type required commands and press Enter."

    return "Use according to the manual procedure."