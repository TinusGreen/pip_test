#!/usr/bin/python3
import glob
import sys
import argparse

class LabelGenerator:
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

    def create_labels(self):
        #Reading files
        onlyfiles = glob.glob(self.read_dir + "*." + self.image_type)

        #Label file
        labels = open(self.write_dir + "labels.txt", "w")

        #Create the labels
        for file in onlyfiles:
            answer = file.replace("." + self.image_type,'').split('/')[-1]
            labels.write(file.split('/')[-1] + ' ' + answer + '\n')
        labels.close()

    def main(self):
        self.create_labels()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="label_generator", description=("LabelGenerator is a helper class to generate label textfiles for aocr to consume."))

    #Arguments
    parser.add_argument("--input", help="Specify the input directory, default is input/")
    parser.add_argument("--output", help="Specify the output directory, default is output/")
    parser.add_argument("--imagetype", help="Specify the image file type, default is png")
    args = parser.parse_args()

    #Startup
    generator = LabelGenerator(args)
    generator.main()
