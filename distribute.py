import os
from time import sleep

projects = [
    ('Database Tools', '/Users/Stephen/Dropbox/scripts/dbtools'),
    ('Loops Tools', '/Users/Stephen/Dropbox/scripts/looptools'),
    ('PSD Convert', '/Users/Stephen/Dropbox/scripts/psdconvert'),
    ('Directory Utilities', '/Users/Stephen/Dropbox/scripts/dirutility'),
    ('PDF Conduit', '/Users/Stephen/Dropbox/scripts/pdfconduit'),
    ('PyPDF3', '/Users/Stephen/Dropbox/scripts/PyPDF3')
]

if __name__ == '__main__':
    print('PyPi distribution control::\n\n' + 'Deploy releases of...')

    for name, directory in projects:
        update_project = input(name + ' [y/n]: ')
        if update_project == 'y':
            os.chdir(directory)
            os.system('python setup.py sdist')
            sleep(1)
            os.system('twine upload -u stephenneal -p pythonstealth19 dist/*')
            print(name + str(' successfully deployed\n'))
