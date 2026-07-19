def generate_troubleshooting(experiment):
    content = experiment.get("content", "").lower()
    title = experiment.get("title", "").lower()

    if "python" in content or "program" in title:
        return programming_errors()

    if "file" in content:
        return file_errors()

    if "database" in content or "sql" in content:
        return database_errors()

    return general_errors()


def programming_errors():
    return [
        {
            "Problem": "Program does not run",
            "Cause": "Syntax error or indentation mistake",
            "Solution": "Check syntax, indentation, brackets, and colons."
        },
        {
            "Problem": "Wrong output",
            "Cause": "Incorrect logic or wrong input",
            "Solution": "Verify the algorithm and test with simple input."
        }
    ]


def file_errors():
    return [
        {
            "Problem": "File not found",
            "Cause": "Incorrect file name or path",
            "Solution": "Check the file name and folder location."
        },
        {
            "Problem": "Data not saved",
            "Cause": "File not closed or wrong mode used",
            "Solution": "Use correct file mode and close the file."
        }
    ]


def database_errors():
    return [
        {
            "Problem": "Query does not execute",
            "Cause": "SQL syntax error",
            "Solution": "Check table name, column name, and SQL syntax."
        }
    ]


def general_errors():
    return [
        {
            "Problem": "Expected result not obtained",
            "Cause": "Procedure step missed",
            "Solution": "Repeat all steps carefully."
        },
        {
            "Problem": "Incorrect observation",
            "Cause": "Measurement or recording error",
            "Solution": "Check readings again."
        }
    ]