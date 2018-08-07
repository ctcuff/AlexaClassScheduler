import os
import zipfile


def zip_files(path, ziph):
    """
    Used to create a zip of the source files used by Alexa
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            # exclude test files and only include *.py files
            if str(file).endswith('.py') and not str(file).__contains__('test'):
                print(f'Adding {path}{file} to zip...')
                ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    zipf = zipfile.ZipFile('src.zip', 'w', zipfile.ZIP_DEFLATED)
    zip_files('src/', zipf)
    zipf.close()
