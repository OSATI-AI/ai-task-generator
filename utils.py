from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tempfile
import time
import yaml
import os
from jinja2 import Template

LANGAUGE = "english"

def test_task(code):
    # Path to your ChromeDriver
    chrome_driver_path = 'static/chromedriver'

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    # Set up Chrome capabilities to capture console output
    cloud_options = {}
    cloud_options['goog:loggingPrefs'] = {'browser': 'ALL'}

    # Apply capabilities to Chrome options
    chrome_options.set_capability('goog:chromeOptions', cloud_options)

    # Initialize WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # embed code into a simple HTML template
    header = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Task</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css">
        </head>
        <body class="bg-gray-100 flex items-center justify-center h-screen">
            <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js" nonce="5834b41ccaf1439bb86c2c5b974a72a1"></script>
            <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css"/>
            <link href="https://cdn.jsdelivr.net/npm/daisyui@4.10.5/dist/full.min.css" rel="stylesheet" type="text/css"/>
        """

    footer = """</body>
        </html>
        """

    html_content = header + code + footer
    print(html_content)

    try:
        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as temp_file:
            temp_file.write(html_content)
            temp_file_path = temp_file.name

        # Load HTML content
        driver.get(f"file://{temp_file_path}")

        # Wait for the page to load
        time.sleep(3)

        # Capture a screenshot
        # screenshot_path = 'screenshot.png'
        # driver.save_screenshot(screenshot_path)
        # print(f'Screenshot saved to {screenshot_path}')

        # Read console output
        logs = driver.get_log('browser')
        # errors = [log for log in logs if log['level'] == 'SEVERE']
        # if errors:
        #     print("Console errors found:")
        #     for error in errors:
        #         print(error)
        # else:
        #     print("No console errors found.")
    finally:
        driver.quit()
        service.stop()
        return logs
    
def fill_text(yaml_file, language):
    # Convert YAML data to a string
    template_str = yaml.dump(yaml_file)

    # Create a Jinja2 template
    template = Template(template_str)

    # Prepare the context with the selected language
    text_data = yaml_file["text"]
    context = {key: value[language] for key, value in text_data.items()}

    # Render the template with the context
    rendered_str = template.render(text=context)

    # Convert the rendered string back to a dictionary
    return yaml.safe_load(rendered_str)

def construct_task(filename):
    # read task file
    task = open(filename, "r").read()
    task = yaml.safe_load(task)
    # fill in language dependent text segments
    task = fill_text(task, language=LANGAUGE)

    # load template
    template = os.path.join('tasks/base_templates', task['template'] + '.yaml')
    template = open(template, "r").read()
    template = yaml.safe_load(template)

    body = f"""
        <div class='card bg-white'>
            <div class='card-body' id='task_container'>
            </div>
        </div>
    """
    
    template_header = template['pyscript']['imports']
    template_generator = template['pyscript']['generator']
    task_header = task['pyscript']['imports']
    task_globals = task['pyscript']['globals']
    task_generator = task['pyscript']['generator']
    task_checker = task['pyscript']['checker']
    
    script = f"""
    <py-script>
        {task_header}
        {template_header}
        {template_generator}
        {task_globals}
        {task_generator}
        {task_checker}

        def check(event):
            result = check_answer(event)
            flag = result[0]
            if flag:
                pydom['#result'][0].html = "Correct!" 
                generate('task_container')
            else:
                pydom['#result'][0].html = "Almost! Try again!"

        def refresh(event):
            generate('task_container')

        generate('task_container')
    </py-script>
    """

    code = f"""
        {body}
        {script}
    """

    return code, task['title'][LANGAUGE]