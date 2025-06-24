import os
import json
import subprocess
import tempfile
import shutil

def fill_latex_template(template_path, user_data):
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace placeholders with actual values
    for key, value in user_data.items():
        if isinstance(value, list):
            value = ', '.join(value)
        template = template.replace(f"<<{key}>>", value if value else "N/A")

    return template

def generate_resume(user_data, template_path):
    try:
        # Create a temporary directory for LaTeX build
        temp_dir = tempfile.mkdtemp()
        tex_file_path = os.path.join(temp_dir, "resume.tex")
        pdf_output_path = os.path.join(temp_dir, "resume.pdf")

        # Fill LaTeX template
        latex_content = fill_latex_template(template_path, user_data)

        # Write the .tex file
        with open(tex_file_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        # Compile the LaTeX to PDF using pdflatex
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file_path], cwd=temp_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if os.path.exists(pdf_output_path):
            final_output = os.path.join("user_data", "AI_Resume.pdf")
            shutil.copy(pdf_output_path, final_output)
            return final_output
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
