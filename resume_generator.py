from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

def generate_resume(data):
    env = Environment(loader=FileSystemLoader(f'templates/{data["template"]}'))
    template = env.get_template(f'{data["template"]}.html')  # e.g. classic.html

    rendered_html = template.render(
        name=data.get("name", ""),
        email=data.get("email", ""),
        contact=data.get("contact", ""),
        skills=data.get("skills", ""),
        projects=data.get("projects", []),
        achievements=data.get("achievements", []),
        certifications=data.get("certifications", []),
        linkedin=data.get("linkedin", ""),
        github=data.get("github", ""),
        education=data.get("education", [])
    )

    os.makedirs("user_data", exist_ok=True)
    output_pdf = "user_data/generated_resume.pdf"
    HTML(string=rendered_html).write_pdf(output_pdf)
