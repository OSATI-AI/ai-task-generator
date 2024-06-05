#!/usr/bin/env python3
from nicegui import ui, context, app
from utils import test_task
import random
from utils import construct_task
import os

class Task:

    def __init__(self, output, title_label):
        self.output = output
        self.title_label = title_label

    def update(self, code, title):
        self.output.clear()
        print(f'This is the title {title}')
        self.title_label.set_text(title)

        with self.output:
            ui.html(code)

    def update_task(self, filename):
        print(f'Updating task with {filename}')
        code, title = construct_task(filename)
        self.update(code, title)

@ui.page('/')
async def main():
    # add pyscript dependency
    #app.add_static_file(url_path='/tasks.css', local_file='tasks.css')
    # <link rel="stylesheet" type="text/tailwindcss" href="tasks.css">
    app.add_static_files("/scripts", "scripts")
    ui.add_head_html("""
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js" nonce="5834b41ccaf1439bb86c2c5b974a72a1"></script>
    <script defer src="//unpkg.com/mathlive"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css"/>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.10.5/dist/full.min.css" rel="stylesheet" type="text/css"/>
    <script type='text/javascript' src='scripts/figure.js'></script>
    <style type="text/tailwindcss">
        /* Custom styles for the question element */
        #question {
        @apply text-base text-gray-700 font-bold;
        }

        #question .text {
        @apply text-lg font-bold;
        }

        #question .math-field {
        @apply text-indigo-600 bg-gray-100 p-1 rounded;
        }
                     
        #answer {
        @apply text-base text-gray-700;
        }
                     

                     



        .choice-container {
            list-style-type: none;
            padding: 0;
        }
        
        .choice {
            background-color: white;
            border: 1px solid grey;
            border-radius: 8px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            padding: 10px 20px;
            margin: 10px 0;
            transition: background-color 0.3s ease;
            cursor: pointer;
        }
        
        .choice:hover {
            background-color: #d4edda;
        }
                     
        .choice_selected{
            background-color: #d4edda;      
        }
                     



    </style>
    """)

	# set content width to window width
    context.client.content.classes('h-[90vh]')

    # navigation bar
    with ui.header().style('background-color: #8b6d64').classes('items-center justify-between h-[10vh]'):
        with ui.row().classes('max-sm:hidden'):
            ui.button('Gallery', icon='photo_library', on_click=lambda: ui.open('/')).props('flat color=white')
            # ui.button('Editor', icon='edit', on_click=lambda: ui.open('/editor')).props('flat color=white')
            # ui.button('Templates', icon='fullscreen').props('flat color=white')
        with ui.row().classes('sm:hidden'):
            ui.button(icon='photo_library').props('flat color=white')
            # ui.button(icon='edit').props('flat color=white')
            # ui.button(icon='fullscreen').props('flat color=white')
    
    # Set the style for the entire page to change the background color
    ui.query('body').style(f'background-color: #f0f0f0')

    # get all tasks from all subfolders of tasks/ (but not base_templates)
    tasks = []
    for root, dirs, files in os.walk('new'):
        if root != os.path.join('tasks', 'base_templates'):
            for file in files:
                if file.endswith('.yaml'):
                    tasks.append(os.path.join(root, file))

    # select a random task
    try:
        filename = random.choice(tasks)
    except UnicodeDecodeError as e:
        print(filename)

    # construct the task code
    code, title = construct_task(filename)

    with ui.row().classes('w-full h-full'):
        with ui.column().classes('w-[49%] h-full justify-center'):
            for filename in tasks:
                filename = filename.replace('\\','/')
                taskname = filename.split('/')[-1]
                taskname = taskname.split('.')[0]
                taskname = ' '.join(taskname.split('_'))
                ui.button(taskname, on_click=lambda fn=filename: task.update_task(fn)).props('unelevated rounded outline color=brown-5 text-color=brown-5 size=md')

        with ui.column().classes('w-[49%] h-full items-center justify-center'):
            with ui.row().classes('w-full h-[10vh]'):
                title_label = ui.label('Math Practice: Multiply & Divide').classes('text-xl font-bold')
            
            container = ui.row().classes('w-full ')

            with ui.row().classes('w-full h-[10vh]'):
                ui.button('Check Answer', icon='check_circle').props('unelevated rounded color=brown-5 text-color=white size=md py-click="check"')
                ui.button('Refresh', icon='refresh').props('unelevated rounded color=brown-5 text-color=white size=md').props('py-click="refresh"')
                ui.label('').classes('text-lg font-bold').props('id="result"')

    task = Task(container, title_label)
    task.update(code, title)

ui.run(title='An experimental task generator', favicon="favicon.ico", reload='FLY_ALLOC_ID' not in os.environ)