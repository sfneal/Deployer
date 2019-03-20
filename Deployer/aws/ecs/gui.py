import PySimpleGUI as sg
from Deployer.aws.config import ECS_HISTORY_JSON, DOCKER_USER, DOCKER_REPO_TAG
from Deployer.utils import most_recent_history


LABEL_COL_WIDTH = 20
INPUT_COL_WIDTH = 50
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20
DEFAULT_FONT = 'Any {0}'.format(HEADER_FONT_SIZE)


def deploy_gui():
    sg.SetOptions(text_justification='left')
    most_recent = most_recent_history(ECS_HISTORY_JSON)

    # Local directory settings
    directory_settings = [
        # Source
        [sg.Text('Source', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('source', ''), size=(INPUT_COL_WIDTH, 1), key='source',
               font='Any {0}'.format(16))]
    ]

    # DockerHub settings
    docker_hub_settings = [
        # Username
        [sg.Text('Username', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_user', DOCKER_USER), size=(INPUT_COL_WIDTH, 1), key='docker_user')],

        # Repo
        [sg.Text('Repository', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_repo', most_recent.get('aws_environment-name', '')),
               size=(INPUT_COL_WIDTH, 1), key='docker_repo')],

        # Tag
        [sg.Text('Tag', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('docker_repo_tag', DOCKER_REPO_TAG), size=(INPUT_COL_WIDTH, 1),
               key='docker_repo_tag')]
    ]

    # Task settings
    task_settings = [
        # Cluster name
        [sg.Text('Cluster name', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('cluster', ''), size=(INPUT_COL_WIDTH, 1), key='cluster')],

        # Task name
        [sg.Text('Task name', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=most_recent.get('task_name', ''), size=(INPUT_COL_WIDTH, 1), key='task_name')],
    ]

    # Create form layout
    layout = [
        [sg.Frame('Directory settings', directory_settings, title_color='green', font=DEFAULT_FONT)],
        [sg.Frame('DockerHub settings', docker_hub_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Frame('Cluster & Task settings', task_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('AWS ECS Deployer', font=("Helvetica", HEADER_FONT_SIZE))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            return values
        elif button is 'Cancel':
            exit()
