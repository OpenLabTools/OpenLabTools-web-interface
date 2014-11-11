#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4
from collections import OrderedDict
id_len = 8

def get_config(config_fn):
    return parse_config(config_fn)

def get_config_by_id(config_dict, elem_id):
    for section_name, section in config_dict.iteritems():
        if elem_id == section['id']:
            return section.update({'name': section_name})
        for subsec_name, subsec in section.iteritems():
            if subsec_name != 'id' and subsec['id'] == elem_id:
                return subsec.update({'name': subsec_name})
    return None

def parse_config_old(config_fn):
    with open(config_fn, 'r') as fn:
        root = OrderedDict()
        crt_sec = None
        crt_subsec = None
        for line in fn:
            line = line.strip()
            # escape empty lines and
            if line == '' or line.startswith('#'): continue
            level = line.count('[')

            if level == 1: # start of new section
                if crt_sec != None:
                    if 'id' not in crt_sec.keys():
                        crt_sec['id'] = str(uuid4())[:id_len]
                    root[crt_sec['id']] = crt_sec
                crt_sec = OrderedDict() # temp dict
                crt_node = crt_sec
            elif level == 2: # start of new widget
                if crt_subsec != None:
                    if 'id' not in crt_subsec.keys():
                        crt_subsec['id'] = str(uuid4())[:id_len]
                    crt_sec[crt_subsec['id']] = crt_subsec
                crt_subsec = OrderedDict()
                crt_node = crt_subsec

            if level != 0:
                crt_node['name'] = line.strip(' []')
            else:
                key, value = [x.strip() for x in line.split('=')]
                crt_node[key] = value
        if 'id' not in crt_subsec.keys():
            crt_subsec['id'] = str(uuid4())[:id_len]
        crt_sec[crt_subsec['id']] = crt_subsec

        if 'id' not in crt_sec.keys():
            crt_sec['id'] = str(uuid4())[:id_len]
        root[crt_sec['id']] = crt_sec
    return root

def print_config( config_dict ):
    s = ''
    for section_name, section in config_dict.iteritems():
        s = s + '[%s]\n'%section_name
        s = s + '    id = %s\n'%section['id']
        for subsec_id, subsec in section.iteritems():
            if subsec_id != 'id':
                s = s + '    [[%s]]\n'%subsec_id
                for key, value in subsec.iteritems():
                    s = s + '         %s = %s\n'%(key, value)
    return s

def write_config( config_fn, config_dict ):
    print config_fn
    print config_dict
    with open( config_fn, 'w') as fn:
        fn.write( print_config(config_dict) )

import re

def parse_config( config_fn ):

    def parse_sec(sec):
        sec_d = OrderedDict()
        pattern = r"\[\[.+]]"
        m = re.split( pattern, sec, flags=re.MULTILINE )
        n = re.findall( pattern, sec, flags=re.MULTILINE )
        n = [x.strip('[]') for x in n]
        sec_d.update( parse_subsec( m.pop(0) ) )
        for subsec, subsec_n in zip(m, n):
            subsec_d = parse_subsec(subsec)
            sec_d[subsec_n] = subsec_d
        return sec_d

    def parse_subsec(subsec):
        d = OrderedDict()
        m = subsec.splitlines()
        for key, val in [x.split('=') for x in m if x.strip() != '']:
            key = key.strip()
            val = val.strip()
            d[key] = val
        return d

    config_d = OrderedDict()
    with open( config_fn, 'r' ) as fn:
        config_str = fn.read()
        print config_str
        pattern = r'^\[[^\[]+]'
        m = re.split( pattern,
                      config_str,
                      flags=re.MULTILINE )
        m = [ x.strip() for x in m if x != '']
        n = re.findall( pattern, config_str, flags=re.MULTILINE )
        n = [x.strip('[]') for x in n]
        for sec, sec_n in zip(m, n):
            sec_d = parse_sec(sec)
            config_d[sec_n] = sec_d

    return config_d



if __name__ == '__main__':
    import tempfile
    import os

    config_fn = 'E:\OpenLabTools-web-interface\code\examples\WidgetOverview\UI_config.ini'
    #config_fn = 'examples\OLT_cluster_config.ini'
    config1 = parse_config( config_fn )
    fileTemp = tempfile.NamedTemporaryFile(delete = False)
    write_config( fileTemp.name, config1 )
    config2 = parse_config( fileTemp.name )
    print print_config( config2 )
    assert(config1 == config2)
    fileTemp.close()
    os.remove(fileTemp.name)
    # config = parse_config_v2(config_fn)
    # print print_config(config)