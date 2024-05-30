from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tempfile
import time
from bs4 import BeautifulSoup
import yaml
import os

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
    
def construct_task(filename):
    # read task file
    task = open(filename, "r").read()

    # read as YAML
    task = yaml.safe_load(task)

    # load template
    template = os.path.join('tasks/base_templates', task['template'] + '.yaml')
    template = open(template, "r").read()
    template = yaml.safe_load(template)

    # template code
    template_code = template['code']

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(template_code, 'html.parser')

    for key in template['to_fill'].keys():
        id = template['to_fill'][key]['id']

        try:
            new_content = task['fill'][key]['all']
        except KeyError:
            new_content = task['fill'][key]['english']

        # find the p-element with id
        element_p = soup.find('p', id=id)

        # Inject the new HTML content into the p-element
        element_p.append(BeautifulSoup(new_content, 'html.parser'))

    # Get the modified HTML string
    template_code = str(soup)

    # put together code
    body = f"""
<div class='card bg-white'>
    <div class='card-body'>
        {template_code}
    </div>
</div>
    """

    script_header = task['pyscript']['imports']
    script_globals = task['pyscript']['globals']
    script_generator = task['pyscript']['generator']
    script_checker = task['pyscript']['checker']

    script = f"""
<py-script>
{script_header}
{script_globals}

{script_generator}

{script_checker}

def check(event):
    result = check_answer(event)
    flag = result[0]
    if flag:
        pydom['#result'][0].html = "Correct!" 
        generate(None)
    else:
        pydom['#result'][0].html = "Almost! Try again!"

generate(None)
</py-script>
    """

    code = f"""
{body}

{script}
    """

    return code, task['title']['english']