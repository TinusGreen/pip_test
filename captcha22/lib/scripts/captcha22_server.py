#!/usr/bin/python3
import sys
import argparse

#Import libs

#API classes
#from lib.api.captcha22_server_api import *

#from lib.crackers.pyppeteer_cracking import *
#Server classes
#from lib.server.captcha22 import Captcha22


#### SERVER ####
def server(args):
    from lib.server.captcha22 import Captcha22
    server = Captcha22(args)
    server.main()

#### API ####
def server_api(args):
    from lib.api.captcha22_server_api import ApiServer
    server = ApiServer(args)
    server.main()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="captcha22_server", description=("CAPTCHA22 is a program that can be used to build models of CAPTCHAs and automate the cracking process. The server is used to build and train new CAPTCHA models as well as exposed an API to serve models to clients"))

    subparsers = parser.add_subparsers(title="Commands")

    #### SERVER ONLY ####
    server_parser = subparsers.add_parser("server", help="Use to execute the CAPTCHA22 Server")
    server_parser.set_defaults(func=server)

    #Arguments
    parser_group_training = server_parser.add_argument_group(title="Training Arguments")

    parser_group_training.add_argument("--maxsteps", default=2000, help="Specify the maximum amount of training steps per CAPTCHA upload, default is 2000")
    parser_group_training.add_argument("--lossthreshold", default=0.0002, help="Specify the threshold of loss at which training should stop, default is 0.0002")
    parser_group_training.add_argument("--perplexitythreshold", default=1.00018, help="Specify the threshold of perplexity at which training should stop, default is 1.00018")
    parser_group_training.add_argument("--datasplit", default=90.0, help="Specify the data split percentage for training vs testing data, default is 90.0")

    parser_group_hosting = server_parser.add_argument_group(title="Model Hosting Arguments")

    parser_group_hosting.add_argument("--startingport", default=9000, help="Specify the starting port for new models to be hosted, default is 9000")

    parser_group_storage = server_parser.add_argument_group(title="Storage Arguments")

    parser_group_storage.add_argument("--inputfolder", default="./Unsorted", help="Specify the folder that will be monitored for new uploads, default is ./Unsorted")
    parser_group_storage.add_argument("--workfolder", default="./Busy", help="Specify the folder where training data will be stored, default is ./Busy")
    parser_group_storage.add_argument("--modelfolder", default="./Model", help="Specify the folder where CAPTCHA models will be stored, default is ./Models")

    #### API ONLY ####
    api_parser = subparsers.add_parser("api", help="Use to execute the CAPTCHA22 API Server")
    api_parser.set_defaults(func=api)

    parser_group_hosting = api_parser.add_argument_group(title="Hosting Arguments")

    parser_group_hosting.add_argument("--host", default="0.0.0.0", help="Specify host where the API would execute, default is 0.0.0.0")
    parser_group_hosting.add_argument("--port", default="5000", help="Specify port where the API would execute, default is 5000")
    parser_group_hosting.add_argument("--isDebug", default=False, help="Specify if the API service should execute in debug mode, default is False", action="store_true")

    parser_group_datastore = api_parser.add_argument_group(title="Datastore Arguments")

    parser_group_datastore.add_argument("--filedrop", default='./Unsorted/', help="Specify the folder where new CAPTCHA uploads should be stored for CAPTCHA22, default is ./Unsorted/")
    parser_group_datastore.add_argument("--maxtokens", default=5, help="Specify the maximum amount of tokens allowed per use, default is 5")
    parser_group_datastore.add_argument("--serverlocation", default='./', help="Specify the base folder of the CAPTCHA22 Server, default is ./")
    parser_group_datastore.add_argument("--userfile", default='users.txt', help="Specify file where user credentials for API is stored, default is users.txt")
    parser_group_datastore.add_argument("--workfolder", default="./Busy", help="Specify the folder where training data of CAPTCHA22 will be stored, default is ./Busy")
    parser_group_datastore.add_argument("--modelfolder", default="./Model", help="Specify the folder where CAPTCHA models of CAPTCHA22 will be stored, default is ./Models")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.exit()


