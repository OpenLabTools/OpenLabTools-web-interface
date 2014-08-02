#!/usr/bin/env python
# -*- coding: utf-8 -*-
from configobj import ConfigObj, Section
from uuid import uuid4

def get_config(config_fn):
    id_len = 8;
    config = ConfigObj(config_fn)

    for panel_name, panel_elems in config.items():
        print panel_elems.keys()
        if "id" not in panel_elems.keys():
            config[panel_name]["id"] = str(uuid4())[:id_len]
        for elem_name, elem_args in panel_elems.items():
            if type(elem_args) is Section:
                if "id" not in elem_args.keys():
                    elem_args["id"] = str(uuid4())[:id_len]
        
    config.write()
    return config