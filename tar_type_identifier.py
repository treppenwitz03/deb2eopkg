import subprocess as sp

class tar_type_identifier:
    def __init__(self, tar):
        source = sp.getoutput("ls workdir/ | grep " + tar)
        if 'tar.xz' in source:
            self.tar_type = '.tar.xz'
            self.comp_type = 'xf'
            self.list_command = 'tf'
        elif 'tar.gz' in source:
            self.tar_type = '.tar.gz'
            self.comp_type = 'xzf'
            self.list_command = 'tzf'
        else:
            print('No control tar archive found within your debian package...')
            exit()
