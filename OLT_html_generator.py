from configobj import ConfigObj
import uuid
import pprint

def generate_html(config_fn, template_fn,temp_fn):
    config = ConfigObj(config_fn)

    for key, item in config.items():
        for sub_key in item.keys():
            item[sub_key]["id"] = str( uuid.uuid4() )[:4]
        config[key]["id"] = str( uuid.uuid4() )[:4]

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(config.dict())

    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(template_fn))

    def debug(text): print text

    env.filters['debug']=debug

    template = env.get_template(temp_fn)

    return template.render( config=config.dict() )

def unit_test():
    config_fn   = "/home/lz307/webserver/OLT_config_test.ini"
    template_fn = '/home/lz307/webserver/templates'
    temp_fn = 'OpenLabTools_temp.html'
    return generate_html( config_fn, template_fn, temp_fn )

if __name__ == "__main__":
    unit_test()