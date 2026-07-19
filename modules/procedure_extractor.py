import re


class ProcedureExtractor:
    def __init__(self, experiment):
        self.experiment = experiment
        self.sections = experiment.get("sections", {})

    def get_procedure_steps(self):
        procedure_text = self.sections.get("procedure", "")

        if not procedure_text:
            return []

        raw_steps = self.split_steps(procedure_text)

        structured_steps = []

        for index, step in enumerate(raw_steps, start=1):
            structured_steps.append({
                "step_number": index,
                "action": step,
                "equipment_used": self.detect_equipment(step),
                "expected_observation": self.detect_observation(step),
                "important_note": self.detect_note(step)
            })

        return structured_steps

    def split_steps(self, text):
        lines = text.split("\n")

        steps = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            line = re.sub(r"^\d+[\.\)]\s*", "", line)
            line = re.sub(r"^[•\-]\s*", "", line)

            if len(line) > 4:
                steps.append(line)

        if len(steps) <= 1:
            sentences = re.split(r"(?<=[.!?])\s+", text)
            steps = [s.strip() for s in sentences if len(s.strip()) > 4]

        return steps

    def detect_equipment(self, step):
        equipment_text = self.sections.get("requirements", "")

        if not equipment_text:
            return "Not clearly mentioned"

        items = re.split(r",|\n|•|-", equipment_text)

        found = []

        for item in items:
            item = item.strip()
            if item and item.lower() in step.lower():
                found.append(item)

        return ", ".join(found) if found else "Not clearly mentioned"

    def detect_observation(self, step):
        keywords = ["observe", "output", "record", "measure", "note", "display", "result"]

        for keyword in keywords:
            if keyword in step.lower():
                return "Observe or record the output/result for this step."

        return "No observation mentioned."

    def detect_note(self, step):
        keywords = ["carefully", "ensure", "check", "verify", "avoid", "do not"]

        for keyword in keywords:
            if keyword in step.lower():
                return "Perform this step carefully."

        return "No special note."