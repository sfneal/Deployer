import PySimpleGUI as sg
from databasetools import JSON
from Deployer.aws.config import JSON_PATH, ROOT_DIRECTORY, DOCKER_USER, DOCKER_REPO_TAG


LABEL_COL_WIDTH = 20
INPUT_COL_WIDTH = 50
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20


def gui(json_path=JSON_PATH, root=ROOT_DIRECTORY):
    """GUI form for choosing packages to upload to DeployPyPi."""
    # Get most recent deployment data
    most_recent = JSON(json_path).read()['history'][-1]
    most_recent['source'] = most_recent['source'][len(root) + 1:len(most_recent['source'])]
    sg.SetOptions(text_justification='left')

    # Local directory settings
    directory_settings = [[sg.Text('Root', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                           sg.In(default_text=root, size=(INPUT_COL_WIDTH, 1), key='root')],
                          [sg.Text('Source', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                           sg.In(default_text=most_recent.get('source', None), size=(INPUT_COL_WIDTH, 1),
                                 key='source')]]

    # DockerHub settings
    docker_hub_settings = [[sg.Text('Username', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                            sg.In(default_text=most_recent.get('docker_user', DOCKER_USER), size=(INPUT_COL_WIDTH, 1),
                                  key='docker_user')],
                           [sg.Text('Repository', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                            sg.In(default_text=most_recent.get('docker_repo',
                                                               most_recent.get('aws_environment-name', '')),
                                  size=(INPUT_COL_WIDTH, 1),
                                  key='docker_repo')],
                           [sg.Text('Tag', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                            sg.In(default_text=most_recent.get('docker_repo_tag', DOCKER_REPO_TAG),
                                  size=(INPUT_COL_WIDTH, 1),
                                  key='docker_repo_tag')]
                           ]

    # AWS settings
    aws_settings = [[sg.Text(key[4:len(key)], size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
                     sg.In(default_text=val, size=(INPUT_COL_WIDTH, 1),
                           font='Any {0}'.format(BODY_FONT_SIZE),
                           key=key)]
                    for key, val in most_recent.items() if key.startswith('aws')]

    # Create form layout
    layout = [[sg.Frame('Directory settings', directory_settings, title_color='green',
                        font='Any {0}'.format(HEADER_FONT_SIZE))],
              [sg.Frame('DockerHub settings', docker_hub_settings, title_color='blue',
                        font='Any {0}'.format(HEADER_FONT_SIZE))],
              [sg.Frame('AWS Elastic Beanstalk settings', aws_settings, title_color='blue',
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
