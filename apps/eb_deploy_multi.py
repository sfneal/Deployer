import os
import PySimpleGUI as sg
from looptools import Timer
from dirutility import SystemCommand
from Dockerizer.dockerize import main as dockerize


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

    # Change directory to source
    os.chdir(docker.source)
    print('Using root directory: {0}'.format(docker.source))

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
