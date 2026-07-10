import re

class ExperimentParser:
    """Identifies individual experiments inside a lab manual and numbers them."""

    EXPERIMENT_PATTERNS = [
        r"Experiment\s*[-:]?\s*(\d+)\s*[:\-]?\s*(.+)",
        r"Exp\.?\s*(\d+)\s*[:\-]?\s*(.+)",
        r"EXPERIMENT\s*(\d+)\s*[:\-]?\s*(.+)",
    ]

    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.lines = raw_text.split("\n")

    def find_experiments(self):
        """Returns list of dicts: {number, title, start_line, end_line, content}"""
        matches = []
        for i, line in enumerate(self.lines):
            for pattern in self.EXPERIMENT_PATTERNS:
                m = re.match(pattern, line.strip(), re.IGNORECASE)
                if m:
                    matches.append({
                        "number": m.group(1),
                        "title": m.group(2).strip() if m.lastindex and m.lastindex >= 2 else "Untitled",
                        "start_line": i
                    })
                    break

        experiments = []
        for idx, exp in enumerate(matches):
            end_line = matches[idx + 1]["start_line"] if idx + 1 < len(matches) else len(self.lines)
            content = "\n".join(self.lines[exp["start_line"]:end_line]).strip()
            experiments.append({
                "number": exp["number"],
                "title": exp["title"],
                "content": content
            })
        return experiments

    def get_experiment_by_number(self, number: str):
        experiments = self.find_experiments()
        for exp in experiments:
            if exp["number"] == str(number):
                return exp
        return None