#!/usr/bin/env python3

from metadata_xml_generator import *
from files_xml_generator import *

import subprocess as sp
import pathlib
import sys

class deb2eopkg:
    def __init__(self):
        workdir = pathlib.Path('workdir')
        if workdir.exists():
            sp.run(['rm', '-rf', 'workdir'])
            self.create_workdir()
        else:
            self.create_workdir()
            
    def create_workdir(self):
        sp.run(['mkdir', 'workdir'])
        
    def extract_deb(self, pkg):
        sp.run(['ar', 'x', pkg, '--output=workdir'])
    
    def create_eopkg(self, package_name, tar_type):
        sp.run(['mv', 'workdir/data' + tar_type, 'workdir/install' + tar_type])
        create = sp.getoutput('cd workdir/ && zip ' + package_name[:-3] + 'eopkg files.xml install' + tar_type + ' metadata.xml && mv ' + package_name[:-3] + 'eopkg .. && cd ..')
        if 'No' in create:
            print('Unable to create package...')
            exit()
    
    def clean(self):
        sp.run(['rm', '-r', 'workdir'])

def main():
    if len(sys.argv) == 1:
        print('No deb file specified!')
        exit()
    deb_package = sys.argv[1]
    converter = deb2eopkg()
    converter.extract_deb(deb_package)

    mxg = metadata_xml_generator()
    mxg.generate_xml()
    
    data = tar_type_identifier('data')
    
    fxg = files_xml_generator()
    fxg.create_files_xml()
    fxg.manage_files_and_hash('data' + data.tar_type, data.comp_type, data.list_command)
    fxg.write()
    
    converter.create_eopkg(deb_package, data.tar_type)
    converter.clean()
    
if __name__ == '__main__':
    main()
