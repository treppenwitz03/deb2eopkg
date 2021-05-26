from tar_type_identifier import *

from xml.dom import minidom
import subprocess as sp

main_source = 'control'

class metadata_xml_generator:
    def __init__(self):
        tar = tar_type_identifier(main_source)
        sp.run(['tar', tar.comp_type, 'workdir/' + main_source + tar.tar_type, '-C', 'workdir/'])
        
        self.get_name()
        self.get_email()
        self.get_license()
        self.get_homepage()
        self.get_component()
        self.get_dependencies()
        self.get_description()
        self.get_version()
        self.get_date()
        self.get_size()
        
    def get_name(self):
        name = sp.getoutput('grep Package workdir/' + main_source)
        name = name[9:]
        self.name = name
        
    def get_email(self):
        # email = sp.getoutput('grep Maintainer workdir/' + main_source)
        # if email != '':
        #     email = email[12:]
        # else:
        #     email = 'unknown email of maintainer'
        print('Still working on emails...')
        email = 'maintainer@packager.com'
        self.email = email
        
    def get_license(self):
        license = sp.getoutput('grep License workdir/' + main_source)
        if license != '':
            license = license[9:]
        else:
            license = 'Unknown License'
        self.license = license
        
    def get_homepage(self):
        homepage = sp.getoutput('grep Homepage workdir/' + main_source)
        if homepage != '':
            homepage = homepage[10:]
        else:
            homepage = 'unknown email of maintainer'
        self.homepage = homepage
        
    def get_component(self):
        package = self.name
        component = sp.getoutput("eopkg info " + package + " | grep Component")
        component = '{}'.format(component.strip())
        if 'Component' in component:
            component = component[22:]
        else:
            component = 'system.utils'
        self.component = component
        
    def get_dependencies(self):
        print('I am currently working on the dependencies part so it may not work yet.')
        dependencies = 'bash'
        self.dependencies = dependencies
        
    def get_description(self):
        print('I am currently working on the descriptions part so it may not work yet.')
        description = 'All I can say is that it is something!'
        self.description = description
        
    def get_version(self):
        version = sp.getoutput('grep Version workdir/' + main_source)
        version = version[9:]
        if '-' in version:
            version = version.split('-')[0]
        elif '=' in version:
            version = version.split('=')[0]
        self.version = version
        
    def get_date(self):
        print('Date is not included in debian packages so we are just using a random one.')
        date = sp.getoutput('date +%F')
        self.date = date
        
    def get_size(self):
        size = sp.getoutput('grep Installed-Size workdir/' + main_source)
        size = size[16:]
        self.size = size
        
    def generate_xml(self):
        
        xml = minidom.Document()
        files = xml.createElement('PISI')
        xml.appendChild(files)

        source1 = xml.createElement('Source')
        
        name1 = xml.createElement('Name')
        name_ = xml.createTextNode(self.name)
        name1.appendChild(name_)
        source1.appendChild(name1)

        homepage1 = xml.createElement('Homepage')
        hp = xml.createTextNode(self.homepage)
        homepage1.appendChild(hp)
        source1.appendChild(homepage1)

        packager1 = xml.createElement('Packager')
        
        name2 = xml.createElement('Name')
        name2_ = xml.createTextNode('NONAME!')
        name2.appendChild(name2_)
        packager1.appendChild(name2)
        
        email1 = xml.createElement('Email')
        email1_ = xml.createTextNode(self.email)
        email1.appendChild(email1_)
        packager1.appendChild(email1)
        
        source1.appendChild(packager1)
        
        files.appendChild(source1)
        
        package1 = xml.createElement('Package')
        
        name2 = xml.createElement('Name')
        name2_ = xml.createTextNode(self.name)
        name2.appendChild(name2_)
        package1.appendChild(name2)
        
        summary1 = xml.createElement('Summary')
        summary1_ = xml.createTextNode('This is a fake summary!')
        summary1.setAttribute('xml:lang', 'en')
        summary1.appendChild(summary1_)
        package1.appendChild(summary1)
        
        dcp1 = xml.createElement('Description')
        dcp1_ = xml.createTextNode(self.description)
        dcp1.setAttribute('xml:lang', 'en')
        dcp1.appendChild(dcp1_)
        package1.appendChild(dcp1)
        
        comp1 = xml.createElement('PartOf')
        comp1_ = xml.createTextNode(self.component)
        comp1.setAttribute('xml:lang', 'en')
        comp1.appendChild(comp1_)
        package1.appendChild(comp1)
        
        license1 = xml.createElement('License')
        license1_ = xml.createTextNode(self.license)
        license1.appendChild(license1_)
        package1.appendChild(license1)

        rtdep = xml.createElement('RuntimeDependencies')

        dep1 = xml.createElement('Dependency')
        dep1_ = xml.createTextNode(self.dependencies)
        dep1.setAttribute('releaseFrom', '8')
        dep1.appendChild(dep1_)
        rtdep.appendChild(dep1)

        package1.appendChild(rtdep)
        
        hs1 = xml.createElement('History')
        
        update1 = xml.createElement('Update')
        update1.setAttribute('release', '1')
        
        date1 = xml.createElement('Date')
        date1_ = xml.createTextNode(self.date)
        date1.appendChild(date1_)
        update1.appendChild(date1)
        
        ver1 = xml.createElement('Version')
        ver1_ = xml.createTextNode(self.version)
        ver1.appendChild(ver1_)
        update1.appendChild(ver1)
        
        comm1 = xml.createElement('Comment')
        comm1_ = xml.createTextNode('NO COMMENT!')
        comm1.appendChild(comm1_)
        update1.appendChild(comm1)
        
        hs1.appendChild(update1)
        
        package1.appendChild(hs1)
        
        bh = xml.createElement('BuildHost')
        bh_ = xml.createTextNode('solus')
        bh.appendChild(bh_)
        package1.appendChild(bh)
        
        dist = xml.createElement('Distribution')
        dist_ = xml.createTextNode('Solus')
        dist.appendChild(dist_)
        package1.appendChild(dist)
        
        dist_r = xml.createElement('DistributionRelease')
        distr_ = xml.createTextNode('1')
        dist_r.appendChild(distr_)
        package1.appendChild(dist_r)
        
        arch = xml.createElement('Architecture')
        arch_ = xml.createTextNode('x86_64')
        arch.appendChild(arch_)
        package1.appendChild(arch)
        
        size1 = xml.createElement('InstalledSize')
        size1_ = xml.createTextNode(self.size)
        size1.appendChild(size1_)
        package1.appendChild(size1)
        
        pf = xml.createElement('PackageFormat')
        pf_ = xml.createTextNode('1.2')
        pf.appendChild(pf_)
        package1.appendChild(pf)
        
        source2 = xml.createElement('Source')
        
        name3 = xml.createElement('Name')
        name3_ = xml.createTextNode(self.name)
        name3.appendChild(name3_)
        source2.appendChild(name3)

        homepage2 = xml.createElement('Homepage')
        hp2 = xml.createTextNode(self.homepage)
        homepage2.appendChild(hp2)
        source2.appendChild(homepage2)

        packager2 = xml.createElement('Packager')
        
        name4 = xml.createElement('Name')
        name4_ = xml.createTextNode('NONAME!')
        name4.appendChild(name4_)
        packager2.appendChild(name4)
        
        email2 = xml.createElement('Email')
        email2_ = xml.createTextNode(self.email)
        email2.appendChild(email2_)
        packager2.appendChild(email2)
        
        source2.appendChild(packager2)
        
        package1.appendChild(source2)
        
        files.appendChild(package1)

        xml_str = xml.toprettyxml(indent='    ')
        with open('workdir/metadata.xml', 'w') as xml:
            xml.write(xml_str)
