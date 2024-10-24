# generate_site.py

import os
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pygments.formatters import HtmlFormatter

from study_plan import study_plan  # Import the study plan

# Set up Jinja2 environment
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

# Function to generate slug from problem name
def generate_slug(problem_name):
    return problem_name.replace(" ", "_").replace("/", "_").replace("'", "").replace("(", "").replace(")", "").lower()

def generate_problem_pages(base_dir, week, day, problems, week_list):
    for problem_name, details in problems.items():
        problem_slug = generate_slug(problem_name)
        problem_folder = os.path.join(base_dir, week, day, problem_slug)
        os.makedirs(problem_folder, exist_ok=True)

        # Paths to code and explanation files
        code_file_path = os.path.join(week, day, f'{problem_slug}.py')
        explanation_file_path = os.path.join(week, day, f'{problem_slug}.md')

        # Create code file if it doesn't exist
        if not os.path.exists(code_file_path):
            os.makedirs(os.path.dirname(code_file_path), exist_ok=True)
            with open(code_file_path, 'w', encoding='utf-8') as f:
                f.write("# TODO: Write the solution code here.\n")
            print(f"Created code file: {code_file_path}")

        # Create explanation file if it doesn't exist
        if not os.path.exists(explanation_file_path):
            os.makedirs(os.path.dirname(explanation_file_path), exist_ok=True)
            with open(explanation_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {problem_name} Explanation\n\nTODO: Write the explanation here.")
            print(f"Created explanation file: {explanation_file_path}")

        # Read code file content
        with open(code_file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()

        # Read and convert explanation file
        with open(explanation_file_path, 'r', encoding='utf-8') as f:
            explanation_md = f.read()
        explanation_content = markdown.markdown(
            explanation_md, extensions=['fenced_code', 'codehilite']
        )

        # Get syntax highlighting CSS
        formatter = HtmlFormatter()
        code_style = formatter.get_style_defs('.codehilite')

        # Relative path to root
        relative_path_to_root = os.path.relpath(base_dir, problem_folder)

        context = {
            'problem_name': problem_name,
            'problem_slug': problem_slug,
            'link': details['link'],
            'time': details['time'],
            'week': week,
            'day': day,
            'code_content': code_content,
            'explanation_content': explanation_content,
            'code_style': code_style,
            'weeks': week_list,
            'active_page': 'problem',
            'relative_path_to_root': relative_path_to_root,
        }

        template = env.get_template('problem.html')
        output = template.render(context)

        with open(os.path.join(problem_folder, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(output)

        print(f"Generated problem page for {problem_name}")

def generate_day_index(base_dir, week, day, problems, week_list):
    day_folder = os.path.join(base_dir, week, day)
    os.makedirs(day_folder, exist_ok=True)

    problem_list = []
    for problem_name, details in problems.items():
        problem_slug = generate_slug(problem_name)
        problem_list.append({
            'name': problem_name,
            'slug': problem_slug,
            'time': details['time'],
        })

    # Relative path to root
    relative_path_to_root = os.path.relpath(base_dir, day_folder)

    context = {
        'week': week,
        'day': day,
        'problems': problem_list,
        'weeks': week_list,
        'active_page': 'days',
        'relative_path_to_root': relative_path_to_root,
    }

    template = env.get_template('day_index.html')
    output = template.render(context)

    with open(os.path.join(day_folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Generated day index for {day} - {week}")

def generate_week_index(base_dir, week, days, week_list):
    week_folder = os.path.join(base_dir, week)
    os.makedirs(week_folder, exist_ok=True)

    day_list = list(days.keys())

    # Relative path to root
    relative_path_to_root = os.path.relpath(base_dir, week_folder)

    context = {
        'week': week,
        'days': day_list,
        'weeks': week_list,
        'active_page': 'weeks',
        'relative_path_to_root': relative_path_to_root,
    }

    template = env.get_template('week_index.html')
    output = template.render(context)

    with open(os.path.join(week_folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Generated week index for {week}")

def generate_homepage(base_dir, plan):
    week_list = list(plan.keys())

    context = {
        'weeks': week_list,
        'title': 'Study Plan',
        'active_page': 'home',
        'relative_path_to_root': '.',  # Root directory
    }

    template = env.get_template('homepage.html')
    output = template.render(context)

    with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output)

    print("Generated homepage")

def generate_site(base_dir, plan):
    week_list = list(plan.keys())
    for week, days in plan.items():
        generate_week_index(base_dir, week, days, week_list)
        for day, problems in days.items():
            generate_day_index(base_dir, week, day, problems, week_list)
            generate_problem_pages(base_dir, week, day, problems, week_list)
    generate_homepage(base_dir, plan)

if __name__ == "__main__":
    base_directory = "site"
    os.makedirs(base_directory, exist_ok=True)
    generate_site(base_directory, study_plan)
