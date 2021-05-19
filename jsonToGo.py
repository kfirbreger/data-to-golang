"""
takes a json file and creates a go file with the types needed to marshal and unmarshal
the data in the json.
It make several assumtions which can be configured via env, see bellow
"""
import argparse
import json

def config():
    """
    Reads the arguments and returns a config used by the rest of the script
    """
    parser = argparser.ArgumentParser(description='Parse converter cli args')
    parser.add_argument('infile', help='The file containing the input json')
    parser.add_argument('-o', '--out', help='The name of the output file. If non is given, the input filen name will be used')

if __name__ == '__main__':
    convert()
