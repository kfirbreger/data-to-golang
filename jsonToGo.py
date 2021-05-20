"""
takes a json file and creates a go file with the types needed to marshal and unmarshal
the data in the json.
It make several assumtions which can be configured via env, see bellow
"""
import argparse
import json


def get_config_from_args():
    """
    Reads the arguments and returns a config used by the rest of the script
    """
    parser = argparse.ArgumentParser(description='Parse converter cli args')
    parser.add_argument('infile', help='The file containing the input json')
    parser.add_argument('-o', '--outfile', help='The name of the output file. If non is given, the input filen name will be used')
    parser.add_argument('-f', '--formats', help='Comma seperated list of formats to support (json, xml, bigquery). The input file format is always added')
    parser.add_argument('-e', '--embed', help='Embed sub structs in the parent struct. This means only one type will be created', action="store_true")
    parser.add_argument('-l','--list', help='Allow a list to be the root of the data', action="store_true")
    parser.add_argument('-t', '--type_name', help='The name to give the type created', default=None)
    config = parser.parse_args()
    
    # Breaking up the format into separate strings
    if config.formats:
        # Converting everything to lowercase
        config.formats = config.formats.lower()
        config.formats = config.formats.split(',')
    else:
        config.formats = []
    # Adding extension as format
    ext = config.infile.split('.')[-1]
    config.formats.append(ext)

    return config

def parse_primitive(go_name, element, config):
    """
    Parse a primitive, creating an entry in the code
    """
    print(go_name, element)
    go_type = ''
    # Everyhting is set to public so capitalized properties names
    go_name = go_name.replace('_', '.').replace('-', '.')
    property_name_parts = go_name.split('.')
    print(property_name_parts)
    property_name = ""
    for part in property_name_parts:
        property_name += part.capitalize()
    
    if type(element) == str:
        go_type += f'{property_name} string'
    elif element in ['true', 'True', 'false', 'False']:
        go_type += f'{property_name} bool'
    else:
        # Numerical value. Checking for int or float
        try:
            n = int(element)
            go_type += f'{property_name} int{config.bits}'
        except ValueError:
            try:
                n = float(element)
                go_type += f'{property_name} float{config.bits}'
            except ValueError:
                pass
    # Adding marshaling notation
    formats = []
    for frmt in config.formats:
        formats.append(f'{frmt}:"{go_name}"')
    go_type += ' `' + ' '.join(formats) + '`\n'
    return go_type

def create_type(go_name, element, config):
    print(go_name, element)
    go_type = ""
    # Checking if this is a list or a dict
    if type(element) == list:
        go_type += go_name + ' []struct {\n'
        for item in element:
            go_type += create_type("", item, config)
        go_type += '}'

    elif type(element) == dict:
        if config.embed:
            go_type += go_name + ' struct {\n'
        else:
            print('Not yet supported')
        for key, value in element.items():
            go_type += create_type(key, value, config)
        go_type += '}'
    else:
        # It is a primitive
        go_type += parse_primitive(go_name, element, config)
    return go_type


def convert():
    """
    Converts the json to a golang type
    """
    config = get_config_from_args()
    with open(config.infile, 'r') as f:
        # For now assume json
        root_element = json.load(f)
        go_type = create_type("example", root_element, config)
    with open(config.outfile, 'w') as f:
        f.write(go_type)
        print("Done")

if __name__ == '__main__':
    convert()
