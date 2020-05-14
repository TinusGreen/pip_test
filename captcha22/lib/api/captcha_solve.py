#!/usr/bin/python3
import argparse
import json
import requests
import time
import glob
import cv2
import getpass

class Client:
    def __init__(self, args):
        self.username = args.username
        self.password = args.password
        self.token = ''
        self.serverURL = args.serverURL + ":" + args.serverPORT + args.serverPATH

    def build_token_headers(self):
        headers = {'X-Api-Key' : self.token}
        return headers

    def get_token(self):
        url = self.serverURL + "generate_token"
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.username,self.password))
        load = json.loads(r.content)
        if load['message'] == 'success':
            print ("Got token")
            self.token = load['token']

    def get_captcha_token(self, captchaID):
        load = json.loads(self.get_captcha_details(captchaID))
        token = load['captcha']['dataToken']
        return token

    def get_captcha_details(self, captchaID):
        url = self.serverURL +  "captchas/" + str(captchaID)
        r = requests.get(url, headers=self.build_token_headers())
        json_data = json.loads(r.content)
        print (json.dumps(json_data, indent=2))

        return r.content

    def solve_captcha(self, captchaID):
        token = self.get_captcha_token(captchaID)
        url = self.serverURL + "solve_captcha"

        import base64
        #This solver expects the images in a directory. Alter or request this if you use something else.
        image_path = "images/"
        images = glob.glob(image_path + "*.png")

        for image in images:
            with open(image, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                datas = {
                        'image' : encoded_string.decode("utf-8"),
                        'dataToken' : token
                        }
                r = requests.post(url, json=datas, headers=self.build_token_headers())
                json_data = json.loads(r.content)
                print (json.dumps(json_data, indent=2))
                img = cv2.imread(image)
                cv2.imshow('captcha', img)
                c = cv2.waitKey(0)

class Menu:
    def __init__(self, args):
        self.authed = False
        self.args = args

    def auth_to_server(self):
        print ("[+] Authenticating to Captcha22")
        count = 0
        while(count < 3):
            if (self.args.username == None):
                self.args.username = str(input("Please provide your username: "))
            if (self.args.password == None):
                self.args.password = getpass.getpass('Please provide your password: ')
            self.new_Client = Client(self.args)
            print ("[-] Attempting authentication")
            try:
                self.new_Client.get_token()
            except: pass
            if len(self.new_Client.token) > 0:
                print ("[-] Authentication successful")
                self.authed = True
                return
            else:
                time.sleep(2)
                self.args.username = None
                self.args.password = None
                print ("[x] Invalid credentials, please try again")
            count += 1

        print ("[x] Attempts failed, please try again")
        exit()

    def solve(self):
        print ("[+] Starting CAPTCHA Solving System")
        if (not self.authed):
            self.auth_to_server()
        if (not self.authed):
            return

        if (self.args.captchaID == None):
            self.args.captchaID = str(input("Please provide the CAPTCHA ID: "))

        self.new_Client.solve_captcha(self.args.captchaID)

    def main(self):
        self.solve()


    def menu_run(self):

        print ("[+] Welcome to Captcha22. What would you like to do?")
        while(True):
            print ("[1] Run Solution")
            print ("[2] Quit")

            answer = str(input("Option: "))
            if (answer == "1"):
                self.solve()
                continue
            if (answer == "2"):
                break
            print ("[x] Invalid option, please try again")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="solver", description=("Solver provides the abilty to take CAPTCHAs from a foler and request solutions from CAPTCHA22 through the AP"))

    #Arguments
    parser.add_argument("--serverURL", default="http://127.0.0.1", help="Specify the URL of the CAPTCHA22 API Server, default is http://127.0.0.1")
    parser.add_argument("--serverPATH", default="/captcha22/api/v1.0/", help="Specify the API Endpoint Path of the CAPTCHA22 API Server, default is /captcha22/api/v1.0/")
    parser.add_argument("--serverPORT", default="5000", help="Specify the PORT of the CAPTCHA22 API Server, default is 5000")
    parser.add_argument("--input", default="./input/", help="Specify the input directory, default is input/")
    parser.add_argument("--imagetype", default="png", help="Specify the image file type, default is png")
    parser.add_argument("--captchaID", default=None, help="Specify captchID from CATCHA22 API Server for the model that will be used, default will be prompted")
    parser.add_argument("--username", default=None, help="Username used for connection to CAPTCHA22, default will be prompted")
    parser.add_argument("--password", default=None, help="Password used for connection to CAPTCHA22, default will be prompted")
    args = parser.parse_args()

    #Execute
    new_menu = Menu(args)
    new_menu.main()

