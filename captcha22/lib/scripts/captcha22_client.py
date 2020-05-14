#!/usr/bin/python3
import sys
import argparse

#Import libs

#Helper classes
#from lib.helpers.renamer import EntryWindow
#from lib.helpers.captcha_labelling import CaptchaLabeller
#from lib.helpers.label_generator import LabelGenerator

#API classes
#from lib.api.captcha22_client import client, menu
#from lib.crackers.captcha_solve import Client, Menu

#Cracker classes
#from lib.crackers.captcha_solve import
#from lib.crackers.captcha_cracking import
#from lib.crackers.pyppeteer_cracking import
#from lib.crackers.captcha_cracking import Cracker
#from lib.crackers.pyppeteer_cracking import *

#### HELPERS ####
#Execute the captcha Typer
def captchaTyper(args):
    import tkinter
    from lib.helpers.renamer import EntryWindow
    root = tkinter.Tk()
    entry_window = EntryWindow(root, self.args)
    root.title = "F-Secure Captcha Renamer"
    entry_window.mainloop()

#Execute the legacy captcha Labeller
def captchaLabeller(args):
    from lib.helpers.captcha_labelling import CaptchaLabeller
    labeller = CaptchaLabeller(args)
    labeller.main()

#Execute the AOCR label generator
def labelGenerator(args):
    from lib.helpers.label_generator import LabelGenerator
    generator = LabelGenerator(args)
    generator.main()

#Function to use the labelling scripts to label your captchas
def label(args):
    if args.script == None:
        raise argparse.ArgumentTypeError(f"script has to be provided")

    if args.script == "captchaTyper":
        print ("Executing CAPTCHA Typing Script")
        captchaTyper(args)
    elif args.script == "captchaLabeller":
        print ("Executing Legacy CAPTCHA Typing Script")
        captchaLabeller(args)
    elif args.script == "labelGenerator":
        print ("Executing AOCR Label Generator")
        labelGenerator(args)
    else:
        raise argparse.ArgumentTypeError(f"script '{args.script}' is not a valid option")

#### APIs ####
def api_full(args):
    from lib.api.captcha22_client import Menu
    new_menu = Menu(args)
    new_menu.main()

def api_basic(args):
    from lib.api.captcha_solve import Menu
    new_menu = Menu(args)
    new_menu.main()

#Function to use the API scripts to interface with CAPTCHA22
def client_api(args):
    if args.script == "full":
        print ("Executing Full CAPTCHA22 API Client")
        api_full(args)
    elif args.script == "basic":
        print ("Executing Basic CAPTCHA22 API Client")
        api_basic(args)
    else:
        raise argparse.ArgumentTypeError(f"script '{args.script} is not a valid option'")

#### CRACKERS ####
def cracker_baseline(args):
    from lib.crackers.captcha_cracking import Cracker
    temp_cracker = Cracker(args)
    temp_cracker.main()


def cracker_pyppeteer(args):
    from lib.crackers.pyppeteer_cracking import PyppeteerCracker
    puppet = PyppeteerCracker(args)
    puppet.norm_main()

#Function to use the Cracker scripts to crack captchas
def cracker(args):
    if args.script == "baseline":
        print ("Executing Baseline Cracker Script")
        cracker_baseline(args)
    elif args.script == "pyppeteer":
        print ("Executing Pyppeteer Cracker Script")
        cracker_pyppeteer(args)
    else:
        raise argparse.ArgumentTypeError(f"script '{args.script} is not a valid option'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="captcha22_client", description=("CAPTCHA22 is a program that can be used to build models of CAPTCHAs and automate the cracking process. The client is used to interface with the CAPTCHA22 server, execute helper scripts, or run cracking scripts"))

    subparsers = parser.add_subparsers(title="Commands")

    #### HELPERS ####
    label_parser = subparsers.add_parser("label", help="Use to execute CAPTCHA labelling helper scripts")
    label_parser.set_defaults(func=label)

    label_group = label_parser.add_argument_group()

    label_group.add_argument("--script", default=None, help="Type of script to execute. Choose out of captchaTyper, captchaLabeller, labelGenerator")
    label_group.add_argument("--input", default="./input/", help="Input folder for CAPTCHAs. Default is './input/'")
    label_group.add_argument("--output", default="./data/", help="Output folder for CAPTCHAs. Default is './data/'")
    label_group.add_argument("--imagetype", default="png", help="File type of the CAPTCHA images. Default is 'png'")

    #### APIs ####
    api_parser = subparsers.add_parser("api", help="Use to execute the CAPTCHA API scripts")
    api_parser.set_defaults(func=api)

    api_group = api_parser.add_argument_group()

    api_group.add_argument("--script", default="full", help="Type of script to execute. Choose out between full or basic, default is full")
    api_group.add_argument("--serverURL", default="http://127.0.0.1", help="Specify the URL of the CAPTCHA22 API Server, default is http://127.0.0.1")
    api_group.add_argument("--serverPATH", default="/captcha22/api/v1.0/", help="Specify the API Endpoint Path of the CAPTCHA22 API Server, default is /captcha22/api/v1.0/")
    api_group.add_argument("--serverPORT", default="5000", help="Specify the PORT of the CAPTCHA22 API Server, default is 5000")
    api_group.add_argument("--username", default=None, help="Username used for connection to CAPTCHA22, default will be prompted when required")
    api_group.add_argument("--password", default=None, help="Password used for connection to CAPTCHA22, default will be prompted when required")
    api_group.add_argument("--input", default="./input/", help="Specify the input directory, default is input/")
    api_group.add_argument("--imagetype", default="png", help="Specify the image file type, default is png")
    api_group.add_argument("--captchaID", default=None, help="Specify captchID from CATCHA22 API Server for the model that will be used, default will be prompted")


    #### CRACKERS ####
    cracker_parser = subparsers.add_parser("cracker", help="Use to execute the CAPTCHA cracking scripts")
    cracker_parser.set_defaults(func=cracker)

    cracker_group = cracker_parser.add_argument_group()

    cracker_group.add_argument("--script", default=None, help="Type of script to execute. Choose out between baseline or pyppeteer")

    cracker_group_server = cracker_parser.add_argument_group(title="CAPTCHA22 Server Arguments")

    #Arguments
    #Server
    cracker_group_server.add_argument("--serverURL", default="http://127.0.0.1", help="Specify the URL of the CAPTCHA22 API Server, default is http://127.0.0.1")
    cracker_group_server.add_argument("--serverPATH", default="/captcha22/api/v1.0/", help="Specify the API Endpoint Path of the CAPTCHA22 API Server, default is /captcha22/api/v1.0/")
    cracker_group_server.add_argument("--serverPORT", default="5000", help="Specify the PORT of the CAPTCHA22 API Server, default is 5000")

    #Credentials
    cracker_group_server.add_argument("--username", default=None, help="Username used for connection to CAPTCHA22, default will be prompted")
    cracker_group_server.add_argument("--password", default=None, help="Password used for connection to CAPTCHA22, default will be prompted")

    #Session var
    cracker_group_server.add_argument("--sessiontime", default=1800, help="Specify the time that a JWT session remains active")

    cracker_group_options = cracker_parser.add_argument_group(title="Local CAPTCHA Processing Arguments")

    #Options var
    cracker_group_options.add_argument("--useHashes", default=False, help="Use hash comparisons to aid cracking process", action="store_true")
    cracker_group_options.add_argument("--useFilter", default=False, help="Use image filter to aid cracking process", action="store_true")
    cracker_group_options.add_argument("--useLocal", default=False, help="Use a local copy of Tensorflow model instead of CAPTCHA22", action="store_true")

    cracker_group_storage = cracker_parser.add_argument_group(title="Storage Arguments")

    #Storage var
    cracker_group_storage.add_argument("--input", default="./input/", help="Specify the directory where solved CAPTCHAs are stored")
    cracker_group_storage.add_argument("--output", default="./output/", help="Specify the output directory where new correct and incorrect CAPTCHAs are stored")

    cracker_group_images = cracker_parser.add_argument_group(title="CAPTCHA Image Arguments")

    #Image var
    cracker_group_images.add_argument("--imagetype", default="png", help="Specify the image file type, default is png")
    cracker_group_images.add_argument("--filterlow", default=130, help="Grayscale lower limit for image filter, default is 130")
    cracker_group_images.add_argument("--filterhigh", default=142, help="Grayscale upper limit for image filter, default is 142")
    cracker_group_images.add_argument("--captchaID", default=None, help="Specify captchID from CATCHA22 API Server for the model that will be used, default will be prompted")

    cracker_group_pyppeteer = cracker_parser.add_argument_group(title="Pyppeteer Arguments")

    #Pyppeteer var
    cracker_group_pyppeteer.add_argument("--checkcaptcha", default="What code is in the image?", help="Specify the phrase that Pyppeteer can search for to determine if it is on the CAPTCHA page")
    cracker_group_pyppeteer.add_argument("--checklogin", default="Password", help="Specify the phrase that Pyppeteer can search for to determine if it is on the Login page")
    cracker_group_pyppeteer.add_argument("--verifylogin", default="The user name or password you entered isn't correct. Try entering it again.", help="Specify the prhase that Pyppeteer can search for to determine if the login attempt failed")
    cracker_group_pyppeteer.add_argument("--usernamefield", default="username", help="Specify HTML field where the username entry is located")
    cracker_group_pyppeteer.add_argument("--passwordfield", default="password", help="Specify HTML field where the password entry is located")
    cracker_group_pyppeteer.add_argument("--captchafield", default="ans", help="Specify HTML field where the CAPTCHA answer must be submitted")
    cracker_group_pyppeteer.add_argument("--attackingURL", default=None, help="Specify the URL of the website that will be attacked")

    cracker_group_attack = cracker_parser.add_argument_group(title="Attack Arguments")

    #Attacking var
    cracker_group_attack.add_argument("--usernamefile", default=None, help="Specify path to file containing usernames for brute force attack")
    cracker_group_attack.add_argument("--passwordfile", default=None, help="Specify path to file containing passwords for brute force attack")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.exit()


