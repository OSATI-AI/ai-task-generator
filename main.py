#!/usr/bin/env python3
from nicegui import ui, context
import os

class Task:

    def __init__(self, output):
        self.output = output

    def update(self, code):
        self.output.clear()

        with self.output:
            ui.html(code)

@ui.page('/')
def main():
	# set content width to window width
    context.client.content.classes('h-[100vh]')
    
    # Set the style for the entire page to change the background color
    ui.query('body').style(f'background-color: #f0f0f0')

    # add pyscript dependency
    ui.add_body_html("""
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js" nonce="5834b41ccaf1439bb86c2c5b974a72a1"></script>
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css"/>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.10.5/dist/full.min.css" rel="stylesheet" type="text/css"/>
    """)

    code = open("example_code.txt", "r").read()

    with ui.row().classes('w-full h-full'):
        with ui.column().classes('w-[49%] h-full justify-center'):
            editor = ui.codemirror(code, language='HTML', theme='copilot', on_change=lambda e: task.update(e.value)).classes('w-full h-[80%]').style('font-size: 8pt')

        container = ui.column().classes('w-[49%] h-full items-center justify-center')

    task = Task(container)
    task.update(code)

ui.run(title='An experimental task generator', favicon="favicon.ico", reload='FLY_ALLOC_ID' not in os.environ)