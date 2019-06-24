import os
import PySimpleGUI as sg

from databasetools import JSON


# GUI settings
TWO_COL = True
COL_WIDTH = 20
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20

# Path to PyPi config file
PYPI_JSON_PATH = os.path.join(os.path.expanduser('~'), '.Deployer', 'pypi.json')
PYPI_JSON_DEFAULT = {"projects": [], "username": "", "password": ""}


def config_exists():
    """Determine weather the PyPi config file exists."""
    return os.path.exists(PYPI_JSON_PATH)


def get_config():
    # Make JSON file if it doesn't exist
    if not config_exists():
        JSON(PYPI_JSON_PATH).write(PYPI_JSON_DEFAULT)
        print('\tadd projects to pypi.json')
    return JSON(PYPI_JSON_PATH).read()


def gui(config):
    sg.SetOptions(text_justification='left')

    # DeployPyPi settings
    settings = [[sg.Text('Username', size=(8, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=config['username'], size=(12, 1), key='username')],
                [sg.Text('Password', size=(8, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=config['password'], size=(12, 1), font='Any {0}'.format(BODY_FONT_SIZE),
                       key='password', password_char='*')],
                [sg.Text('Config file: ~/.Deployer/pypi.json', font='Any {0}'.format(BODY_FONT_SIZE))]]

    # Create form layout
    layout = [[sg.Frame('PyPi Settings', settings, title_color='green', font='Any {0}'.format(HEADER_FONT_SIZE))]]

    # Deployable project options
    if config_exists():
        options = [[sg.Checkbox(os.path.basename(row), size=(COL_WIDTH, 1), default=False, key=row)]
                   for row in config['projects']]
        layout.extend(
            [[sg.Frame('Deployable Projects', options, font='Any {0}'.format(HEADER_FONT_SIZE), title_color='blue')]]
        )

    layout.extend([[sg.Submit(), sg.Cancel()]])
    return sg.FlexForm('DeployPyPi Deployment Control', font=("Helvetica", HEADER_FONT_SIZE)).Layout(layout)


def pypi_deployer():
    """GUI form for choosing packages to upload to DeployPyPi."""
    # Read Config file
    config = get_config()

    # Launch GUI
    window = gui(config)
    while True:
        button, values = window.ReadNonBlocking()

        if button is 'Submit':
            # Loop through project options and upload the projects that were checked
            for project, choice in values.items():
                if choice:
                    upload(project)
            break
        elif button is 'Cancel':
            exit()


def upload(project):
    """Upload a package distribution to the DeployPyPi repository."""
    os.chdir(os.path.join(os.path.dirname(project), project))
    os.system('python setup.py sdist')
    command = 'twine upload dist/*'
    os.system(command)


def main():
    print('\nDeployPyPi distribution control::\n')
    pypi_deployer()


if __name__ == '__main__':
    main()
