#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4
from collections import OrderedDict
import re
id_len = 8

def get_config(config_fn):
    config_dict = parse_config(config_fn)
    changed = add_id(config_dict)
    if changed: write_config(config_fn, config_dict)
    return config_dict

def get_config_by_id(config_dict, elem_id):
    for section_name, section in config_dict.iteritems():
        if elem_id == section['id']:
            section.update({'name': section_name})
            return section
        for subsec_name, subsec in section.iteritems():
            if subsec_name != 'id' and subsec['id'] == elem_id:
                subsec.update({'name': subsec_name})
                return subsec
    return None

def add_id(config_dict):
    change_flag = False
    for section_name, section in config_dict.iteritems():
        if 'id' not in section.keys():
            change_flag = True
            section.update({'id': str(uuid4())[:id_len]})
        for subsec_name, subsec in section.iteritems():
            if subsec_name != 'id' and 'id' not in subsec.keys():
                change_flag = True
                subsec.update({'id': str(uuid4())[:id_len]})
    return change_flag

def print_config( config_dict ):
    s = ''
    for section_name, section in config_dict.iteritems():
        s = s + '[%s]\n'%section_name
        s = s + '    id = %s\n'%section['id']
        for subsec_id, subsec in section.iteritems():
            if subsec_id != 'id':
                s = s + '    [[%s]]\n'%subsec_id
                for key, value in subsec.iteritems():
                    s = s + '        %s = %s\n'%(key, value)
        s = s + '\n'
    return s

def write_config( config_fn, config_dict ):
    with open( config_fn, 'w') as fn:
        fn.write( print_config(config_dict) )

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
        config_str = re.sub(r'#.+', '', config_str, flags=re.MULTILINE)
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
    config1 = get_config( config_fn )
    fileTemp = tempfile.NamedTemporaryFile(delete = False)
    write_config( fileTemp.name, config1 )
    config2 = parse_config( fileTemp.name )
    #print print_config( config2 )
    assert(config1 == config2)
    fileTemp.close()
    os.remove(fileTemp.name)
    config_fn = 'examples\OLT_cluster_config.ini'
    config_dict = get_config(config_fn)
    elem_id = 'de87a652'
    get_config_by_id(config_dict, elem_id)