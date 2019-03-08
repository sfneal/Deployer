import PySimpleGUI as sg
from databasetools import JSON
from Deployer.aws.config import DOCKER_USER, JSON_PATH, ROOT_DIRECTORY


LABEL_COL_WIDTH = 20
INPUT_COL_WIDTH = 50
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20
SKIPPED_HISTORY_KEYS = ('time', 'tasks')


def gui(default_username=DOCKER_USER, json_path=JSON_PATH, root=ROOT_DIRECTORY):
    """GUI form for choosing packages to upload to DeployPyPi."""
    # Get most recent deployment data
    most_recent = JSON(json_path).read()['history'][-1]
    most_recent['source'] = most_recent['source'][len(ROOT_DIRECTORY) + 1:len(most_recent['source'])]
    sg.SetOptions(text_justification='left')

    # DockerHub settings
    settings = [[sg.Text('Username', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=default_username, size=(INPUT_COL_WIDTH, 1), key='docker_user')],
                [sg.Text('Root directory', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                 sg.In(default_text=root, size=(INPUT_COL_WIDTH, 1), key='root')]]

    # Deployment parameters, defaults to most recent
    options = [[sg.Text(key, size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                sg.In(default_text=val, size=(INPUT_COL_WIDTH, 1),
                      font='Any {0}'.format(BODY_FONT_SIZE if key != 'source' else 12),
                      key=key)]
               for key, val in most_recent.items() if key not in SKIPPED_HISTORY_KEYS]

    # Create form layout
    layout = [[sg.Frame('DockerHub settings', settings, title_color='green', font='Any {0}'.format(HEADER_FONT_SIZE))],
              [sg.Frame('AWS Elastic Beanstalk Parameters', options, title_color='blue',
                        font='Any {0}'.format(HEADER_FONT_SIZE))],
              [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('AWS Elastic Beanstalk Deployment Control',
                         font=("Helvetica", HEADER_FONT_SIZE)).Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()

        if button is 'Submit':
            return values

        elif button is 'Cancel':
            exit()
