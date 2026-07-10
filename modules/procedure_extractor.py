import re

class ProcedureExtractor:
    """Extracts step-by-step procedure, theory, and safety notes from one experiment's text."""

    SECTION_HEADERS = {
        "theory": [r"theory", r"aim\s*&?\s*theory", r"objective"],
        "procedure": [r"procedure", r"method", r"steps", r"experimental procedure"],
        "safety": [r"safety", r"precautions", r"hazards"],
        "materials": [r"apparatus", r"materials required", r"equipment"],
    }

    def __init__(self, experiment_text: str):
        self.text = experiment_text

    def _extract_section(self, keys):
        lines = self.text.split("\n")
        pattern = re.compile(r"^(" + "|".join(keys) + r")\s*[:\-]?\s*$", re.IGNORECASE)
        start = None
        for i, line in enumerate(lines):
            if pattern.match(line.strip()):
                start = i + 1
                break
        if start is None:
            return ""
        end = len(lines)
        all_headers = [h for group in self.SECTION_HEADERS.values() for h in group]
        other_pattern = re.compile(r"^(" + "|".join(all_headers) + r")\s*[:\-]?\s*$", re.IGNORECASE)
        for i in range(start, len(lines)):
            if other_pattern.match(lines[i].strip()):
                end = i
                break
        return "\n".join(lines[start:end]).strip()

    def get_theory(self):
        return self._extract_section(self.SECTION_HEADERS["theory"])

    def get_safety(self):
        return self._extract_section(self.SECTION_HEADERS["safety"])

    def get_materials(self):
        return self._extract_section(self.SECTION_HEADERS["materials"])

    def get_procedure_steps(self):
        raw = self._extract_section(self.SECTION_HEADERS["procedure"])
        if not raw:
            return []
        step_pattern = re.compile(r"^\s*(\d+[\.\)]|\-|\•)\s*(.+)")
        steps = []
        for line in raw.split("\n"):
            m = step_pattern.match(line)
            if m:
                steps.append(m.group(2).strip())
            elif line.strip() and steps:
                steps[-1] += " " + line.strip()
        return steps if steps else [raw]