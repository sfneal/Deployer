import os
import PySimpleGUI as sg


config = {
    'projects': [
        '/Users/Stephen/scripts/databasetools',
        '/Users/Stephen/scripts/looptools',
        '/Users/Stephen/scripts/psdconvert',
        '/Users/Stephen/scripts/dirutility',
        '/Users/Stephen/scripts/PyPDF3',
        '/Users/Stephen/scripts/PyBundle',
        '/Users/Stephen/scripts/synfo',
        '/Users/Stephen/scripts/ImgConverter',
        '/Users/Stephen/scripts/psd-tools3',
        '/Users/Stephen/scripts/differentiate',
        '/Users/Stephen/scripts/mysql-toolkit',
        '/Users/Stephen/scripts/awsutils-s3',
        '/Users/Stephen/scripts/PillowImage',
        '/Users/Stephen/scripts/RuntimeWatch',
        '/Users/Stephen/scripts/Dockerizer',
    ],
    'username': 'stephenneal',
    'password': 'pythonstealth19'
}


TWO_COL = True
COL_WIDTH = 20
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20


def get_config():
    return config


def gui():
    """GUI form for choosing packages to upload to DeployPyPi."""
    sg.SetOptions(text_justification='left')
    config = get_config()

    # Deployable project options
    options = [[sg.Checkbox(os.path.basename(row), size=(COL_WIDTH, 1), default=False, key=row)]
               for row in config['projects']]

    # DeployPyPi settings
    settings = [[sg.Text('Username', size=(8, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=config['username'], size=(12, 1), key='username')],
                [sg.Text('Password', size=(8, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=config['password'], size=(12, 1), font='Any {0}'.format(BODY_FONT_SIZE),
                       key='password', password_char='*')],
                [sg.Text('Config file: ~/.Deployer/pypi.json', font='Any {0}'.format(BODY_FONT_SIZE))]]

    # Create form layout
    layout = [[sg.Frame('PyPi Settings', settings, title_color='green', font='Any {0}'.format(HEADER_FONT_SIZE))],
              [sg.Frame('Deployable Projects', options, font='Any {0}'.format(HEADER_FONT_SIZE), title_color='blue')],
              [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('DeployPyPi Deployment Control', font=("Helvetica", HEADER_FONT_SIZE)).Layout(layout)

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
    gui()


if __name__ == '__main__':
    main()
