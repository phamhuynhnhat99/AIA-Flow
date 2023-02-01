import os
import sys
sys.path.append(os.path.dirname(__file__))

from core.Node import Node as Node_

import argparse
import configparser
config = configparser.ConfigParser()

aia_folder_path = os.path.abspath(os.path.join(__file__, os.pardir))
backend_folder_path = os.path.abspath(os.path.join(aia_folder_path, os.pardir))
config_ini_path = (os.path.join(backend_folder_path, "config.ini"))
config.read(config_ini_path)
if config["DEFAULT"]["AIA_MODE"] == 'gui':
    Node = None
else: # config["DEFAULT"]["AIA_MODE"] == 'no-gui':
    Node = Node_

def init_node_env():

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', dest='version', type=str, help='Get this version')
    parser.add_argument('--title', dest='title', type=str, help='Get this title')
    args = parser.parse_args()
    os.environ['VERSION'] = args.version if args.version is not None else "0"
    os.environ['TITLE'] = args.title if args.title is not None else "AIA Project"


def import_widgets(origin_file: str, rel_file_path='widgets.py'):

    from importlib.machinery import SourceFileLoader
    try:
        widgets_path = os.path.join(os.path.dirname(origin_file), rel_file_path)
        module_name = os.path.dirname(origin_file).split("/")[-1]
        rel_widgets = SourceFileLoader(module_name, widgets_path).load_module()
        widgets = rel_widgets.export_widgets
    except:
        widgets = None
    
    return widgets