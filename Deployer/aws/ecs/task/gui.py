import PySimpleGUI as sg


LABEL_COL_WIDTH = 20
INPUT_COL_WIDTH = 50
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20
DEFAULT_FONT = 'Any {0}'.format(HEADER_FONT_SIZE)


def stop():
    sg.SetOptions(text_justification='left')

    # Task settings
    task_settings = [
        # Cluster
        [sg.Text('Cluster', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='', size=(INPUT_COL_WIDTH, 1), key='cluster')],

        # Task
        [sg.Text('Task ID', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='', size=(INPUT_COL_WIDTH, 1), key='task')],

        # Reason
        [sg.Text('Reason', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='', size=(INPUT_COL_WIDTH, 1), key='reason')],
    ]

    # Create form layout
    layout = [
        [sg.Frame('Task stop settings', task_settings, title_color='green', font=DEFAULT_FONT)],
        [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('AWS ECS Task Stopper', font=("Helvetica", HEADER_FONT_SIZE))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            return values
        elif button is 'Cancel':
            exit()


def run():
    sg.SetOptions(text_justification='left')

    # Task settings
    task_settings = [
        # Cluster
        [sg.Text('Cluster', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='', size=(INPUT_COL_WIDTH, 1), key='cluster')],

        # Task
        [sg.Text('Task (family:revision)', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='', size=(INPUT_COL_WIDTH, 1), key='task')],

        # Launch Type
        [sg.Text('Launch Type', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='EC2', size=(INPUT_COL_WIDTH, 1), key='launch_type')],
    ]

    # Create form layout
    layout = [
        [sg.Frame('Task settings', task_settings, title_color='green', font=DEFAULT_FONT)],
        [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('AWS ECS Task Runner', font=("Helvetica", HEADER_FONT_SIZE))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            return values
        elif button is 'Cancel':
            exit()


def register():
    sg.SetOptions(text_justification='left')

    # Task settings
    task_settings = [
        # Family
        [sg.Text('Task family', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='persistent-storage2', size=(INPUT_COL_WIDTH, 1), key='task')],
    ]

    # Mounted Volume settings
    mv_settings = [
        # Volume Name
        [sg.Text('Volume name', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='persistent-efs', size=(INPUT_COL_WIDTH, 1), key='volume_name')],

        # Volume Path
        [sg.Text('Volume path', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='/mnt/efs', size=(INPUT_COL_WIDTH, 1), key='volume_path')],

        # Container Path
        [sg.Text('Volume path', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='/mnt/efs', size=(INPUT_COL_WIDTH, 1), key='container_path')],
    ]

    # Port settings
    port_settings = [
        # Volume Name
        [sg.Text('Protocol', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='tcp', size=(INPUT_COL_WIDTH, 1), key='port_protocol')],

        # Volume Path
        [sg.Text('Host port', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=5000, size=(INPUT_COL_WIDTH, 1), key='port_host')],

        # Container Path
        [sg.Text('Container port', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text=5000, size=(INPUT_COL_WIDTH, 1), key='port_container')],
    ]

    # Port settings
    docker_settings = [
        # Container name
        [sg.Text('Container name', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='persistent-storage', size=(INPUT_COL_WIDTH, 1), key='docker_container')],

        # Image
        [sg.Text('Image name', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='stephenneal/persistent-storage:latest', size=(INPUT_COL_WIDTH, 1), key='docker_image')],
    ]

    # Create form layout
    layout = [
        [sg.Frame('Task settings', task_settings, title_color='green', font=DEFAULT_FONT)],
        [sg.Frame('Mounted Volume settings', mv_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Frame('Port settings', port_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Frame('Docker settings', docker_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('AWS ECS Task Registration', font=("Helvetica", HEADER_FONT_SIZE))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            return values
        elif button is 'Cancel':
            exit()
