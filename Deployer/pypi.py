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
    ],
    'username': 'stephenneal',
    'password': 'pythonstealth19'
}


TWO_COL = True
COL_WIDTH = 20
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20


def gui(projects, default_username='', default_password=''):
    """GUI form for choosing packages to upload to DeployPyPi."""
    sg.SetOptions(text_justification='left')

    # Deployable project options
    options = [[sg.Checkbox(row, size=(COL_WIDTH, 1), default=False, key=row)] for row in projects]

    # DeployPyPi settings
    settings = [[sg.Text('Username', size=(8, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=default_username, size=(12, 1), key='username')],
                [sg.Text('Password', size=(8, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=default_password, size=(12, 1), font='Any {0}'.format(BODY_FONT_SIZE),
                       key='password', password_char='*')]]

    # Create form layout
    layout = [[sg.Frame('PyPi settings', settings, title_color='green', font='Any {0}'.format(HEADER_FONT_SIZE))],
              [sg.Frame('Deployable Projects', options, font='Any {0}'.format(HEADER_FONT_SIZE), title_color='blue')],
              [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('DeployPyPi Deployment Control', font=("Helvetica", HEADER_FONT_SIZE)).Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()

        if button is 'Submit':
            # Parse returned values
            user = values.pop('username')
            pw = values.pop('password')

            # Loop through project options and upload the projects that were checked
            for project, choice in values.items():
                if choice:
                    upload(project, user, pw)
            break
        elif button is 'Cancel':
            exit()


def upload(project, username, password):
    """Upload a package distribution to the DeployPyPi repository."""
    os.chdir(os.path.join(config['directory'], project))
    os.system('python setup.py sdist')
    command = 'twine upload -u {0} -p {1} dist/*'.format(username, password)
    os.system(command)


def main():
    print('\nDeployPyPi distribution control::\n')
    gui(config['projects'], config['username'], config['password'])


if __name__ == '__main__':
    main()
