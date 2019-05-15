import os
import PySimpleGUI as sg
from dirutility import SystemCommand
from Dockerizer.dockerize import main as dockerize


def main():
    # Get AWS EB Environment name
    layout = [[sg.Frame('Directory settings',
                        [[sg.Text('AWS EB Env', size=(20, 1), font='Any {0}'.format(20)),
                          sg.In(default_text='', size=(50, 1), key='aws_eb_env')],
                         [sg.Text('Version desc', size=(20, 1), font='Any {0}'.format(20)),
                          sg.In(default_text='', size=(50, 1), key='desc')]],
                        title_color='green', font=("Helvetica", 30))],
              [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('Docker Hub Deployment Control', font=("Helvetica", 30))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            print(values)
            break
        elif button is 'Cancel':
            exit()

    # Get Dockerize parameters
    docker = dockerize()[0]

    # Change directory to source
    os.chdir(docker.source)

    SystemCommand('eb deploy {env} --label {version} --message "{message}"'.format(
        env=values['aws_eb_env'], version=docker.tag, message=values['desc']))


if __name__ == '__main__':
    main()