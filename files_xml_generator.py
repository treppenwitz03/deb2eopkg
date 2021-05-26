from tar_type_identifier import *

from xml.dom import minidom
import subprocess as sp
import pathlib

class files_xml_generator:
    def __init__(self):
        print('Creating files.xml.')
        
        self.xml = minidom.Document()
        
    def create_files_xml(self):
        self.xml = minidom.Document()
        self.files = self.xml.createElement('Files')
        self.xml.appendChild(self.files)
        
    def manage_files_and_hash(self, data_tar, compression_type, list_command):
        sp.run(['tar', compression_type, 'workdir/' + data_tar, '-C', 'workdir/'])
        print('Checking for hash.')
        hashfile = pathlib.Path('workdir/md5sums')
        if hashfile.exists():
            print('Found md5sum hash file')
            hash_file = open('workdir/md5sums', 'r')
            contents = hash_file.readlines()
            print('Generating XML')
            for x in contents:
                content = '{}'.format(x.strip())
                hashcode = content[0:32]
                hashedfile = content[34:]
                self.get_data(hashedfile, hashcode)
        else:
            print('Found none... Creating a dummy one')
            all_files = sp.getoutput('tar ' + list_command + ' workdir/' + data_tar + ' | grep -e "[^/]$"')
            l_o_f = list(all_files.split('\n'))
            print('Generating XML')
            for hash_file in l_o_f:
                hashedfile = hash_file[2:]
                sha1sum_hash = sp.getoutput('sha1sum workdir/' + hash_file)
                sha1sum_hash = sha1sum_hash[0:40]
                if 'No' in sha1sum_hash:
                    print('There are broken packages in the package. Cannot proceed')
                    exit()
                self.get_data(hashedfile, sha1sum_hash)
                
    def get_data(self, hashed_file, hash_code):
        _file = 'workdir/' + hashed_file
        size = sp.getoutput('wc -c < "' + _file + '"')
        if size.isnumeric() is False:
            print('There are broken packages. Cannot get size data.')
            exit()
        else:
            is_executable = sp.call('type ' + _file, shell=True, stdout=sp.PIPE, stderr=sp.PIPE) == 0
            if 'man' in _file:
                file_type = 'man'
                mode = '0644'
            elif 'locale' in _file:
                file_type = 'localedata'
                mode = '0644'
            elif 'lib' in _file:
                file_type = 'library'
                mode = '0644'
            elif is_executable is True:
                file_type = 'executable'
                mode = '0755'
            else:
                file_type = 'data'
                mode = '0644'
            
            self.generate_xml(hashed_file, file_type, size, mode, hash_code)
    def generate_xml(self, _file, _type, _size, _mode, _hash):
        file_handler = self.xml.createElement('File')

        path = self.xml.createElement('Path')
        path_ = self.xml.createTextNode(_file)
        path.appendChild(path_)
        file_handler.appendChild(path)

        ftype = self.xml.createElement('Type')
        ftype_ = self.xml.createTextNode(_type)
        ftype.appendChild(ftype_)
        file_handler.appendChild(ftype)

        size = self.xml.createElement('Size')
        size_ = self.xml.createTextNode(_size)
        size.appendChild(size_)
        file_handler.appendChild(size)

        uid = self.xml.createElement('Uid')
        uid_ = self.xml.createTextNode('0')
        uid.appendChild(uid_)
        file_handler.appendChild(uid)

        gid = self.xml.createElement('Gid')
        gid_ = self.xml.createTextNode('0')
        gid.appendChild(gid_)
        file_handler.appendChild(gid)

        mode = self.xml.createElement('Mode')
        mode_ = self.xml.createTextNode(_mode)
        mode.appendChild(mode_)
        file_handler.appendChild(mode)

        fhash = self.xml.createElement('Hash')
        fhash_ = self.xml.createTextNode(_hash)
        fhash.appendChild(fhash_)
        file_handler.appendChild(fhash)

        self.files.appendChild(file_handler)
    
    def write(self):
        xml_str = self.xml.toprettyxml(indent='    ')
        with open('workdir/files.xml', 'w') as files:
            files.write(xml_str)
