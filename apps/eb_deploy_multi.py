import os
import shutil
import PySimpleGUI as sg
from looptools import Timer
from dirutility import SystemCommand
from Dockerizer.dockerize import main as dockerize


REMOTE_DIRECTORY = '.aws-eb-deployment'


def gui():
    # Get AWS EB Environment name
    layout = [[sg.Frame('Directory settings',
                        [[sg.Text('AWS EB Env', size=(20, 1), font='Any {0}'.format(20)),
                          sg.In(default_text='', size=(50, 1), key='aws_eb_env')],
                         [sg.Text('Version desc', size=(20, 1), font='Any {0}'.format(20)),
                          sg.In(default_text='', size=(50, 1), key='desc')],

                         # Another deployment?
                         [sg.Checkbox('Deploy another environment?', size=(50, 1), default=False,
                                      key='another_deploy')]],
                        title_color='green', font=("Helvetica", 30))],
              [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('Docker Hub Deployment Control', font=("Helvetica", 30))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            return values
        elif button is 'Cancel':
            exit()


def eb_deploy_multi(values):
    # Get Dockerize parameters
    docker = dockerize()[0]

    # Remote directory relative to Project root
    remote_dir = os.path.join(docker.source, REMOTE_DIRECTORY)

    # Copy the Dockerrun.aws.json file to '-remote' directory
    if not os.path.exists(remote_dir):
        os.mkdir(remote_dir)
    shutil.copyfile(os.path.join(docker.source, 'Dockerrun.aws.json'),
                    os.path.join(remote_dir, 'Dockerrun.aws.json'))

    # Change directory to source
    os.chdir(remote_dir)
    print(os.getcwd())
    print('Using root directory: {0}'.format(remote_dir))

    with Timer('Deployed to AWS EB'):
        SystemCommand('eb deploy {env} --label {version} --message "{message}"'.format(
            env=values['aws_eb_env'], version=docker.tag, message=values['desc']), False)
    return


def main():
    params = []
    while True:
        values = gui()
        params.append(values)
        if values['another_deploy'] is False:
            break

    [eb_deploy_multi(value) for value in params]


if __name__ == '__main__':
    main()
