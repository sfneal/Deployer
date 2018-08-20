import os
from time import sleep

projects = [
    ('Database Tools', '/Users/Stephen/Dropbox/scripts/dbtools', "C:\\Users\\Stephen\\Scripts\\pdfconduit"),
    ('Loops Tools', '/Users/Stephen/Dropbox/scripts/looptools', "C:\\Users\\Stephen\\Scripts\\pdfconduit"),
    ('PSD Convert', '/Users/Stephen/Dropbox/scripts/psdconvert', "C:\\Users\\Stephen\\Scripts\\pdfconduit"),
    ('Directory Utilities', '/Users/Stephen/Dropbox/scripts/dirutility', "C:\\Users\\Stephen\\Scripts\\pdfconduit"),
    ('PDF Conduit', '/Users/Stephen/Dropbox/scripts/pdfconduit', "C:\\Users\\Stephen\\Scripts\\pdfconduit"),
    ('PyPDF3', '/Users/Stephen/Dropbox/scripts/PyPDF3', "C:\\Users\\Stephen\\Scripts\\pdfconduit")
]

if __name__ == '__main__':
    print('PyPi distribution control::\n\n' + 'Deploy releases of...')

    for p in projects:
        name, directory_osx, directory_win = p
        update_project = input(name + ' [y/n]: ')
        if update_project == 'y':
            try:
                os.chdir(directory_osx)
            except FileNotFoundError:
                os.chdir(directory_win)
            os.system('python setup.py sdist')
            sleep(1)
            os.system('twine upload -u stephenneal -p pythonstealth19 dist/*')
            print(name + str(' successfully deployed\n'))
