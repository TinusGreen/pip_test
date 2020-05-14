#!/usr/bin/python3
import glob
import cv2
import sys
import os
import argparse

class CaptchaLabeller:
    def __init__(self, args):
        self.read_dir = "input/"
        self.write_dir = "output/"
        self.image_type = "png"

        if args.input:
            self.read_dir = args.input
        if args.output:
            self.write_dir = args.output
        if args.imagetype:
            self.image_type = args.imagetype

    def label_captchas(self):
        #Reading files
        onlyfiles = glob.glob(self.read_dir + "*")

        #Iterate through files. All keys accepted. Press "-" to finish CAPTCHA label. Press "`" to exit program
        for o in onlyfiles:
            if(o.find(self.image_type)!=-1):
                img = cv2.imread(o)
                print ("Showing image")
                text = ''
                while(1):
                    cv2.imshow('captcha', img)
                    c = cv2.waitKey(0)
                    if c==ord('-'):
                        print ("Exiting")
                        break
                    elif c==ord('`'):
                        print ("Full exit")
                        exit()
                    else:
                        print ('you pressed %s' % chr(c))
                        text += chr(c)

                print ("Final text is: " + text)

                #Save the image
                cv2.imwrite(self.write_dir + text.upper() + '.' + self.image_type, img)
                #Remove the old image
                os.remove(o)

    def main(self):
        self.label_captchas()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="capthcha_labeller", description=("CaptchaLabeller is a legacy helper class to label CAPTCHAs. Use '`' to exit and `-` to save. Consider using Renamer instead"))

    #Arguments
    parser.add_argument("--input", help="Specify the input directory, default is input/")
    parser.add_argument("--output", help="Specify the output directory, default is output/")
    parser.add_argument("--imagetype", help="Specify the image file type, default is png")
    args = parser.parse_args()

    labeller = CaptchaLabeller(args)

    labeller.main()

