from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

def generate_resume(data):
    env = Environment(loader=FileSystemLoader(f'templates/{data["template"]}'))
    template = env.get_template(f'{data["template"]}.html')  # e.g. classic.html

    rendered_html = template.render(
        name=data["name"],
        email=data["email"],
        skills=data["skills"],
        projects=data["projects"]
    )

    os.makedirs("user_data", exist_ok=True)
    output_pdf = "user_data/generated_resume.pdf"
    HTML(string=rendered_html).write_pdf(output_pdf)


