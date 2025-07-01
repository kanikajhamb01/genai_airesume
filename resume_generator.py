import os
import subprocess

def generate_resume(data):
    template_path = f"templates/{data.get('template', 'classic')}/template.tex"

    with open(template_path, "r") as file:
        latex_code = file.read()

    # Fill LaTeX placeholders
    latex_code = latex_code.replace("{{NAME}}", data.get("name", ""))
    latex_code = latex_code.replace("{{EMAIL}}", data.get("email", ""))
    latex_code = latex_code.replace("{{SKILLS}}", data.get("skills", ""))

    # Format project section
    proj_string = ""
    for proj in data.get("projects", []):
        proj_string += f"\\item \\textbf{{{proj['name']}}}: {proj['description']}\\\\\n"

    latex_code = latex_code.replace("{{PROJECTS}}", proj_string.strip())

    # Save filled LaTeX file
    os.makedirs("user_data", exist_ok=True)
    with open("user_data/generated_resume.tex", "w") as f:
        f.write(latex_code)

    # Compile to PDF
    subprocess.run(["pdflatex", "-output-directory", "user_data", "user_data/generated_resume.tex"], stdout=subprocess.DEVNULL)
