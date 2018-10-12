import os
import PySimpleGUI as sg
from DeployPyPi.config import BASE_DIR, PROJECTS, USERNAME, PASSWORD


TWO_COL = False
COL_WIDTH = 20


def gui(projects, default_username='', default_password=''):
    """GUI form for choosing packages to upload to DeployPyPi."""
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

    # DeployPyPi settings
    settings = [
        [sg.Text('Username', size=(8, 1)), sg.In(default_text=default_username, size=(12, 1), key='username')],
        [sg.Text('Password', size=(8, 1)), sg.In(default_text=default_password, password_char='*',
         size=(12, 1), key='password')]
    ]

    # Create form layout
    layout = [[sg.Frame('DeployPyPi settings', settings, title_color='green', font='Any 12')],
              [sg.Frame('Deployable Projects', options, font='Any 12', title_color='blue')],
              [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('DeployPyPi Deployment Control', font=("Helvetica", 12), return_keyboard_events=False).Layout(layout)

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
    os.chdir(os.path.join(BASE_DIR, project))
    os.system('python setup.py sdist')
    command = 'twine upload -u {0} -p {1} dist/*'.format(username, password)
    os.system(command)


def main():
    print('\nDeployPyPi distribution control::\n')
    gui(PROJECTS, USERNAME, PASSWORD)


if __name__ == '__main__':
    main()
