import os
import PySimpleGUI as sg
from time import sleep


base_dir = '/Users/Stephen/Dropbox/scripts'
TWO_COL = False
COL_WIDTH = 20


def gui(projects, default_username='', default_password=''):
    """GUI form for choosing packages to upload to PyPi."""
    sg.SetOptions(text_justification='left')

    # Deployable project options
    options = []

    while len(projects) > 0:
        # Two column listing
        if TWO_COL:
            left = projects.pop(0)
            try:
                right = projects.pop(0)
                options.append([sg.Checkbox(left, size=(COL_WIDTH, 1), default=False, key=left),
                                sg.Checkbox(right, size=(COL_WIDTH, 1), default=False, key=right)])
            except IndexError:
                options.append([sg.Checkbox(left, size=(COL_WIDTH, 1), default=False, key=left)])
        # One column listing
        else:
            row = projects.pop(0)
            options.append([sg.Checkbox(row, size=(COL_WIDTH, 1), default=False, key=row)])

    # PyPi settings
    settings = [
        [sg.Text('Username', size=(8, 1)), sg.In(default_text=default_username, size=(12, 1), key='username')],
        [sg.Text('Password', size=(8, 1)), sg.In(default_text=default_password, size=(12, 1), key='password')]
    ]

    # Create form layout
    layout = [[sg.Frame('PyPi settings', settings, title_color='green', font='Any 12')],
              [sg.Frame('Deployable Projects', options, font='Any 12', title_color='blue')],
              [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('PyPi Deployment Control', font=("Helvetica", 12), return_keyboard_events=False).Layout(layout)

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


def upload(project, username, password):
    """Upload a package distribution to the PyPi repository."""
    os.chdir(os.path.join(base_dir, project))
    os.system('python setup.py sdist')
    sleep(1)
    command = 'twine upload -u {0} -p {1} dist/*'.format(username, password)
    os.system(command)
    sg.PopupOK('{0} successfully deployed'.format(project))


def main():
    print('\nPyPi distribution control::\n')

    username = 'stephenneal'
    password = 'pythonstealth19'
    projects = [
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
    ]
    gui(projects, username, password)


if __name__ == '__main__':
    main()
