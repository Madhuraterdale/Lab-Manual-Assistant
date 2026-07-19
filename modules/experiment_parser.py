import re


SECTION_ALIASES = {
    "aim": ["Aim", "Objective", "Objectives"],
    "theory": ["Theory", "Background", "Concept"],
    "requirements": ["Requirements", "Requirement", "Apparatus", "Equipment", "Tools", "Software", "Components", "Materials"],
    "procedure": ["Procedure", "Algorithm", "Steps", "Method"],
    "observation": ["Observation", "Observations"],
    "result": ["Result", "Output", "Conclusion", "Expected Output"]
}


class ExperimentParser:
    def __init__(self, raw_text):
        self.raw_text = raw_text

    def find_experiments(self):
        pattern = r"(?im)^\s*(Experiment|Practical|Program|Activity|Exercise)\s*(?:No\.?)?\s*(\d+)\s*[:.\-]?\s*(.*)$"

        matches = list(re.finditer(pattern, self.raw_text))

        experiments = []

        for index, match in enumerate(matches):
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(self.raw_text)

            experiment_text = self.raw_text[start:end].strip()

            exp_type = match.group(1).title()
            number = match.group(2)
            title = match.group(3).strip()

            if title.lower().startswith(("aim", "objective")):
                title = f"{exp_type} {number}"

            if not title:
                title = f"{exp_type} {number}"

            sections = extract_sections(experiment_text)

            experiments.append({
                "type": exp_type,
                "number": number,
                "title": title,
                "content": experiment_text,
                "sections": sections
            })

        return experiments


def extract_sections(experiment_text):
    heading_to_key = {}

    all_headings = []

    for key, headings in SECTION_ALIASES.items():
        for heading in headings:
            all_headings.append(heading)
            heading_to_key[heading.lower()] = key

    heading_pattern = "|".join([re.escape(h) for h in all_headings])

    pattern = rf"(?im)^\s*({heading_pattern})\s*:?\s*(.*)$"

    matches = list(re.finditer(pattern, experiment_text))

    sections = {}

    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        inline_content = match.group(2).strip()

        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(experiment_text)

        block_content = experiment_text[start:end].strip()

        full_content = inline_content

        if block_content:
            full_content += "\n" + block_content

        key = heading_to_key.get(heading.lower())

        if key and full_content.strip():
            sections[key] = full_content.strip()

    return sections