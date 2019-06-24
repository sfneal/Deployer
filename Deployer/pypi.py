import os
import PySimpleGUI as sg


config = {
    'directory': '/Users/Stephen/scripts',
    'projects': [
        'databasetools',
        'looptools',
        'psdconvert',
        'dirutility',
        'PyPDF3',
        'PyBundle',
        'synfo',
        'ImgConverter',
        'psd-tools3',
        'differentiate',
        'mysql-toolkit',
        'awsutils-s3',
        'PillowImage',
        'RuntimeWatch',
        'Dockerizer',
    ]
}


TWO_COL = True
COL_WIDTH = 20
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20


def gui(projects):
    """GUI form for choosing packages to upload to DeployPyPi."""
    sg.SetOptions(text_justification='left')

    # Deployable project options
    options = [[sg.Checkbox(row, size=(COL_WIDTH, 1), default=False, key=row)] for row in projects]

    # DeployPyPi settings
    settings = [[sg.Text('~/.Deployer/pypi.json', font='Any {0}'.format(BODY_FONT_SIZE))]]

    # Create form layout
    layout = [[sg.Frame('Config file', settings, title_color='green', font='Any {0}'.format(
        HEADER_FONT_SIZE))],
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
    os.chdir(os.path.join(config['directory'], project))
    os.system('python setup.py sdist')
    command = 'twine upload dist/*'
    os.system(command)


def main():
    print('\nDeployPyPi distribution control::\n')
    gui(config['projects'])


if __name__ == '__main__':
    main()
