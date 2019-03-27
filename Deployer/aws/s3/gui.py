import PySimpleGUI as sg
from Deployer.aws.config import S3_ACL

LABEL_COL_WIDTH = 20
INPUT_COL_WIDTH = 50
HEADER_FONT_SIZE = 30
BODY_FONT_SIZE = 20
DEFAULT_FONT = 'Any {0}'.format(HEADER_FONT_SIZE)


def sync():
    """GUI form for choosing packages to upload to DeployPyPi."""
    # Get most recent deployment data
    sg.SetOptions(text_justification='left')

    # S3 Bucket settings
    bucket_settings = [
        # Source
        [sg.Text('Bucket', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(BODY_FONT_SIZE)),
         sg.In(default_text='hpadesign-projects', size=(20, 1), key='bucket',
               font='Any {0}'.format(INPUT_COL_WIDTH))]
    ]

    # AWS S3 CLI sync settings
    sync_settings = [
        # Source
        [sg.Text('Source', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(16)),
         sg.In(default_text='/Volumes/Storage II/HPA Design/SNeal ('
                            'Media)/WebServer/Backups/2-GoDaddy/backup-hpadesign.net-2019-3-19/public_html/projects'
                            '.hpadesign'
                            '.net/public/uploads',
               size=(90, 1), key='source', font='Any {0}'.format(12))],

        # Destination
        [sg.Text('Destination', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(16)),
         sg.In(default_text='uploads', size=(90, 1), key='destination', font='Any {0}'.format(12))],

        # Delete
        [sg.Text('Delete', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(16)),
         sg.Checkbox('', size=(90, 1), default=False, key='delete', font='Any {0}'.format(12))],

        # ACL
        [sg.Text('acl', size=(LABEL_COL_WIDTH, 1), font='Any {0}'.format(16)),
         sg.DropDown(S3_ACL, size=(LABEL_COL_WIDTH, 1), key='acl')],
    ]

    # Create form layout
    layout = [
        [sg.Frame('Bucket settings', bucket_settings, title_color='green', font=DEFAULT_FONT)],
        [sg.Frame('sync settings', sync_settings, title_color='blue', font=DEFAULT_FONT)],
        [sg.Submit(), sg.Cancel()]]
    window = sg.FlexForm('AWS S3 file sync Control', font=("Helvetica", HEADER_FONT_SIZE))
    window.Layout(layout)

    while True:
        button, values = window.ReadNonBlocking()
        if button is 'Submit':
            return values
        elif button is 'Cancel':
            exit()
