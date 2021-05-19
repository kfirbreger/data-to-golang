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
    parser = argparser.ArgumentParser(description='Parse converter cli args')
    parser.add_argument('infile', help='The file containing the input json')
    parser.add_argument('-o', '--outfile', help='The name of the output file. If non is given, the input filen name will be used')
    parser.add_argument('-f', '--formats', help='Comma seperated list of formats to support (json, xml, bigquery). The input file format is always added')
    parser.add_argument('-e', help='Embed sub structs in the parent struct. This means only one type will be created', action="store_true")
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


def create_type(element, config, go_name):
    go_type = ""
    # Checking if this is a list or a dict
    if type(element) == list and config.list:
        print("Not yet supported")
    elif type(element) == dict:
        go_type += f'type {go_name} struct \{\n'
        for key, value in element.items():
            go_type += create_type(value, config, key)
        go_type += '}'
    elif type(strucutre) == str:
        go_type += f'{go_name} string\n'
    elif element in ['true', 'True', 'false', 'False']:
        go_type += f'{go_name} bool\n'
    else:
        # Numerical value. Checking for int or float
        try:
            n = int(element)
            go_type += f'{go_name} int{config.bits}\n'
        except ValueError
            try:
                n = float(element)
                go_type += f'{go_name} float{config.bits}\n'
            except ValueError:
                pass
    return go_type


def convert():
    """
    Converts the json to a golang type
    """
    config = get_config()
    with open(config.infile, 'r') as f:
        # For now assume json
        root_element = json.load(f)
        go_type = create_type(root_element, config, "")
    except as exp:
        print("Something went wrong:", exp)
        return
    with open(config.outfile, 'w') as f:
        f.write(go_type)
        print("Done")
    except as exp:
        print("Cannot write data:", exp)
        return

if __name__ == '__main__':
    convert()
