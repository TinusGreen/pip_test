#!/usr/bin/python3
import numpy
import os
import time
import glob
import cv2
import ast
import argparse

class captcha:
    def __init__(self, path):
        self.path = path

        self.hasTrained = False
        self.busyTraining = False
        self.hasModel = False
        self.modelActive = False
        self.modelPorts = -1
        self.currentTrainingLevel = -1
        self.image_width = 0
        self.image_heigth = 0
        self.last_step = 0
        self.loss = 0
        self.perplexity = 0;
        self.checkpoint = 0;
        self.modelName = "null"
        self.modelPath = "null"
        self.modelOn = False

        try:
            f = open(self.path + 'model.txt')
            lines = f.readlines()
            self.hasTrained = ast.literal_eval(lines[0].replace("\n",""))
            self.busyTraining = ast.literal_eval(lines[1].replace("\n",""))
            self.hasModel = ast.literal_eval(lines[2].replace("\n",""))
            self.modelActive = ast.literal_eval(lines[3].replace("\n",""))
            self.modelPorts = ast.literal_eval(lines[4].replace("\n",""))
            self.currentTrainingLevel = ast.literal_eval(lines[5].replace("\n",""))
            self.image_width = ast.literal_eval(lines[6].replace("\n",""))
            self.image_height = ast.literal_eval(lines[7].replace("\n",""))
            self.last_step = ast.literal_eval(lines[8].replace("\n",""))
            self.loss = ast.literal_eval(lines[9].replace("\n",""))
            self.perplexity = ast.literal_eval(lines[10].replace("\n",""))
            self.checkpoint = ast.literal_eval(lines[11].replace("\n",""))
            self.modelName = lines[12].replace("\n","")
            self.modelPath = lines[13].replace("\n","")
            self.modelOn = ast.literal_eval(lines[14].replace("\n",""))


        except:
            self.get_image_size()
            self.update_file()
            pass

    def get_image_size(self):
        images = glob.glob(self.path + "data/*.png")
        img = cv2.imread(images[0])
        self.image_width = img.shape[1]
        self.image_height = img.shape[0]

    def update_from_file(self):
        f = open(self.path + 'model.txt')
        lines = f.readlines()
        self.hasTrained = ast.literal_eval(lines[0].replace("\n",""))
        self.busyTraining = ast.literal_eval(lines[1].replace("\n",""))
        self.hasModel = ast.literal_eval(lines[2].replace("\n",""))
        self.modelActive = ast.literal_eval(lines[3].replace("\n",""))
        self.modelPorts = ast.literal_eval(lines[4].replace("\n",""))
        self.currentTrainingLevel = ast.literal_eval(lines[5].replace("\n",""))
        self.image_width = ast.literal_eval(lines[6].replace("\n",""))
        self.image_height = ast.literal_eval(lines[7].replace("\n",""))
        self.last_step = ast.literal_eval(lines[8].replace("\n",""))
        self.loss = ast.literal_eval(lines[9].replace("\n",""))
        self.perplexity = ast.literal_eval(lines[10].replace("\n",""))
        self.checkpoint = ast.literal_eval(lines[11].replace("\n",""))
        self.modelName = lines[12].replace("\n","")
        self.modelPath = lines[13].replace("\n","")
        self.modelOn = ast.literal_eval(lines[14].replace("\n",""))

    def update_file(self):
        f = open(self.path + 'model.txt', 'w')
        f.write(str(self.hasTrained) + "\n")
        f.write(str(self.busyTraining) + "\n")
        f.write(str(self.hasModel) + "\n")
        f.write(str(self.modelActive) + "\n")
        f.write(str(self.modelPorts) + "\n")
        f.write(str(self.currentTrainingLevel) + "\n")
        f.write(str(self.image_width) + "\n")
        f.write(str(self.image_height) + "\n")
        f.write(str(self.last_step) + "\n")
        f.write(str(self.loss) + "\n")
        f.write(str(self.perplexity) + "\n")
        f.write(str(self.checkpoint) + "\n")
        f.write(str(self.modelName) + "\n")
        f.write(str(self.modelPath) + "\n")
        f.write(str(self.modelOn) + "\n")

    def export_model(self):
        print ("Going to extract the model")
        os.system("(cd " + self.path + " && aocr export --max-height " + str(self.image_height) + " --max-width " + str(self.image_width) +  " exported-model)")
        time.sleep(5)

    def run_model(self):
        print ("Starting serving model")
        print ("nohup tensorflow_model_server --port=" + str(self.modelPorts) + " --rest_api_port=" + str(self.modelPorts + 1) + " --model_name=" + self.modelName + " --model_base_path=" + os.getcwd() + "/" + self.modelPath + " 2&> /dev/null &")
        os.system("nohup tensorflow_model_server --port=" + str(self.modelPorts) + " --rest_api_port=" + str(self.modelPorts + 1) + " --model_name=" + self.modelName + " --model_base_path=" + os.getcwd() + "/" + self.modelPath + " 2&> /dev/null &")

    def stop_model(self):
        print ("Stoping serving model")
        os.system("kill $(ps aux | grep 'tensorflow_model_server --port=" + str(self.modelPorts) + "' | awk '{print $2}')")

    def model_trained(self):
        return self.hasTrained

    def busy_training(self):
        return self.busyTraining

    def test_training_level(self):
        print ("Testing training level")
        #Go read the aocr log
        f = open(self.path + "aocr.log")
        lines = f.readlines()
        lastUpdate = ""
        for line in lines:
            if line.find("Step") != -1:
                lastUpdate = line


        values = lastUpdate.split(',')
        step = ast.literal_eval(values[1].split('Step ')[1].split(':')[0])

        #We need to combine two values, the current step and the last saved step. This gives us the total step.
        current_checkpoint = 0
        try:
            f = open(self.path + "/checkpoints/checkpoint")
            lines = f.readlines()
            current_checkpoint = ast.literal_eval(lines[0].split('ckpt-')[1].split("\"")[0])
        except:
            print ("No current checkpoint")
            pass


        while (step > 100):
            step -= 100


        self.last_step = current_checkpoint + step
        self.loss = ast.literal_eval(values[2].split('loss: ')[1])
        self.perplexity = ast.literal_eval(values[3].split('perplexity: ')[1].split('.')[0] + "." + values[3].split('perplexity: ')[1].split('.')[1])
        self.checkpoint = current_checkpoint

        print ("Values are: ")
        print ("Step: ", self.last_step)
        print ("Loss: ", self.loss)
        print ("Perplexity: ", self.perplexity)
        print ("Checkpoint: ", self.checkpoint)

        self.update_file()


    def determine_endpoint(self, steps, loss, perplex):
        if self.checkpoint >= steps:
            #Time to end
            return True

        if self.loss < loss and self.perplexity < perplex:
            return True

        return False

    def stop_training(self):
        #Sometime the kill is not respected. Do this three times to ensure it is killed
        print ("Going to stop training")
        os.system("kill $(ps aux | grep 'aocr' | awk '{print $2}')")
        print ("training stopped, waiting")
        time.sleep(5)
        os.system("kill $(ps aux | grep 'aocr' | awk '{print $2}')")
        print ("training stopped, waiting")
        time.sleep(5)
        os.system("kill $(ps aux | grep 'aocr' | awk '{print $2}')")
        print ("training stopped, waiting")
        time.sleep(5)
        self.busyTraining = False
        self.hasTrained = True
        self.update_file()

    def test_training(self):
        print ("Testing")
        print ("(cd " + self.path + " && aocr test --max-height " + str(self.image_height) + " --max-width " + str(self.image_width) + " labels/testing.tfrecords 2>&1 | tee test.txt)")
        os.system("(cd " + self.path + " && aocr test --max-height " + str(self.image_height) + " --max-width " + str(self.image_width) + " labels/testing.tfrecords 2>&1 | tee test.txt)")
        time.sleep(30)

    def start_training(self):
        print ("Starting training")
        self.busyTraining = True
        self.update_file()
        os.system("(cd " + self.path + " && nohup aocr train --max-height " + str(self.image_height) + " --max-width " + str(self.image_width) + " labels/training.tfrecords &>/dev/null &)")

class Captcha22:
    def __init__(self, args):
        print ("Class start")
        self.args = args
        self.busyTraining = False

        self.training_steps_max = int(args.maxsteps)
        self.training_loss_min = float(args.lossthreshold)
        self.training_perplexity_min = float(args.perplexitythreshold)

        self.currentPort = int(args.startingport)

        self.unsorted_URL = args.inputfolder
        self.busy_URL = args.workfolder
        self.model_URL = args.modelfolder

        self.data_split = float(args.datasplit)

        self.new_models = []
        self.existing_models = []

    def copy_files(self, file):
        print ("Starting the copy of files")
        names = file.split(".")[0].split("/")[-1].split("_")

        #Creating folder structure data
        os.system('mkdir ' + self.busy_URL + "/" + names[0])
        os.system('mkdir ' + self.busy_URL + "/" + names[0] + "/" + names[1])
        os.system('mkdir ' + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2])
        os.system('mkdir ' + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/" + "labels")

        #Creating folder structure for model
        os.system('mkdir ' + self.model_URL + "/" + names[0])
        os.system('mkdir ' + self.model_URL + "/" + names[0] + "/" + names[1])
        os.system('mkdir ' + self.model_URL + "/" + names[0] + "/" + names[1] + "/" + names[2])
        os.system('mkdir ' + self.model_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/exported-model")
        os.system('mkdir ' + self.model_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/exported-model/1")

        #Copy the file to the directory
        os.system("cp " + file.replace("\n","") + " " + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2])
        os.system("rm " + file.replace("\n",""))

        #Unzip the file
        os.system("unzip " + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/" +  file.split("/")[-1] + " -d " + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/")
        os.system("rm " + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/" +  file.split("/")[-1])

    def export_model(self,model):
        paths = model.path.split("/")
        shortPath = paths[1] + "/" + paths[2] + "/" + paths[3]
        print ("Path is ", shortPath)
        #Ask model to create the model
        model.export_model()
        #Copy the model to the correct path for safekeeping
        os.system("cp -r " + model.path + "exported-model/* " + self.model_URL + "/" + shortPath + "/exported-model/1/")
        print ("Model copied")

    def run_model(self, model):
        #Single command to start the model
        print ("Start model")
        model.run_model()

    def stop_model(self,model):
        print ("Stop model")
        model.stop_model()


    def label_captchas(self, file):
        #Function used to label the captchas
        names = file.split(".")[0].split("/")[-1].split("_")
        read_dir = self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/data/"
        write_dir = self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/labels/"

        print ("Directories is:")
        print (read_dir)
        print (write_dir)

        onlyfiles = glob.glob(read_dir + "*.png")

        count = len(onlyfiles)
        train_count = int(count * (self.data_split / 100.0))
        test_count = count - train_count

        #Create train labels
        count = 0
        labels = open(write_dir + "training_labels.txt", "w")
        while (count < train_count):
            file = onlyfiles[count]
            answer = file.replace('.png','').split('/')[-1]

            labels.write(self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/data/" + file.split('/')[-1] + ' ' + answer + '\n')

            count += 1

        labels.close()

        #Create test labels
        count = 0
        labels = open(write_dir + "testing_labels.txt", "w")
        while (count < test_count):
            file = onlyfiles[train_count + count]

            answer = file.replace('.png','').split('/')[-1]
            labels.write(self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/data/" + file.split('/')[-1] + ' ' + answer + '\n')

            count += 1
        labels.close()

    def generate_aocr_records(self, file):
        names = file.split(".")[0].split("/")[-1].split("_")

        #Creating folder structure data
        os.system('aocr dataset ' + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/labels/training_labels.txt " + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/labels/training.tfrecords")
        time.sleep(1)
        os.system('aocr dataset ' + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/labels/testing_labels.txt " + self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/labels/testing.tfrecords")
        time.sleep(5)

    def create_model(self, file):
        print (file)
        names = file.split(".")[0].split("/")[-1].split("_")
        path = self.busy_URL + "/" + names[0] + "/" + names[1] + "/" + names[2] + "/"
        model = captcha(path)

        if model.model_trained():
            self.existing_models.append(model)
        else:
            self.new_models.append(model)

    def reload_models(self, path):
        model = captcha(path)
        if model.model_trained():
            self.existing_models.append(model)
        else:
            if model.busy_training():
                model.start_training()

            self.new_models.append(model)

    def check_files(self):
        print ("Checking is there is any new files")

        files = glob.glob(self.unsorted_URL + "/*.zip")

        print (files)

        print ("Start running")

        for file in files:
            print ("Copy files")
            self.copy_files(file)
            print ("Create labels")
            self.label_captchas(file)
            print ("Generate aocr")
            self.generate_aocr_records(file)
            print ("Create model")
            self.create_model(file)
            print ("Updating file")
            self.update_file()
            print ("Done")

    def update_file(self):
        f = open('models.txt', 'w')
        for model in self.existing_models:
            f.write(model.path + "\n")

        for model in self.new_models:
            f.write(model.path + "\n")

        f.close()

    def continue_training(self):
        if len(self.new_models) == 0:
            self.busyTraining = False
            return

        #If there is models, we need to check the first one.
        self.busyTraining = True
        model = self.new_models[0]

        #Check if this model is busy training
        if model.busy_training():
            #Request an update and kill if needed
            print ("Model update")
            model.test_training_level()
            if model.determine_endpoint(self.training_steps_max, self.training_loss_min, self.training_perplexity_min):
                #We need to stop training
                model.stop_training()
                #Do other things such as moving the model

                #Test the training of the model
                model.test_training()

                #Export the model
                self.export_model(model)
                model.hasModel = True

                paths = model.path.split("/")
                shortPath = paths[1] + "/" + paths[2] + "/" + paths[3]
                model.modelName = paths[1] + "_" + paths[2]
                model.modelPath = self.model_URL + "/" + shortPath + "/exported-model/"
                model.modelPorts = self.currentPort
                self.currentPort + 2
                model.update_file()

                #Create the server for the model
                #Run the server

                self.existing_models.append(model)
                #Delete model
                del self.new_models[0]
                self.update_file()

        else:
            print ("Going to start the model training procedure")
            #Model not training, start training
            model.start_training()

    def start_model_server(self):
        print ("Checking the models")
        print (len(self.existing_models))
        for model in self.existing_models:
            model.update_from_file()
            #Check if the start var has been set and active not, then start
            if model.modelOn and not model.modelActive:
                #The model needs to be started
                print ("Starting model")
                model.modelActive = True
                self.run_model(model)

            if not model.modelOn and model.modelActive:
                #The model is on but needs to be killed
                print ("Killing model")
                model.modelActive = False
                self.stop_model(model)
            model.update_file()


    def run_server(self):

        while (True):
            if (not self.busyTraining):
                self.check_files()
            self.continue_training()
            if (not self.busyTraining):
                self.start_model_server()
            print ("Starting wait cycle")
            time.sleep(30)

    def first_start(self):
        #Load all models
        try:
            f = open('models.txt')
            lines = f.readlines()
            for line in lines:
                self.reload_models(line.replace("\n",""))
        except:
            pass

    def main(self):
        self.first_start()
        self.run_server()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="captchaserver", description=("CaptchaServer is the primary server class that will manage CAPTCHA training, storage, and model hosting"))

    #Arguments
    parser_group_training = parser.add_argument_group(title="Training Arguments")

    parser_group_training.add_argument("--maxsteps", default=2000, help="Specify the maximum amount of training steps per CAPTCHA upload, default is 2000")
    parser_group_training.add_argument("--lossthreshold", default=0.0002, help="Specify the threshold of loss at which training should stop, default is 0.0002")
    parser_group_training.add_argument("--perplexitythreshold", default=1.00018, help="Specify the threshold of perplexity at which training should stop, default is 1.00018")
    parser_group_training.add_argument("--datasplit", default=90.0, help="Specify the data split percentage for training vs testing data, default is 90.0")

    parser_group_hosting = parser.add_argument_group(title="Model Hosting Arguments")

    parser_group_hosting.add_argument("--startingport", default=9000, help="Specify the starting port for new models to be hosted, default is 9000")

    parser_group_storage = parser.add_argument_group(title="Storage Arguments")

    parser_group_storage.add_argument("--inputfolder", default="./Unsorted", help="Specify the folder that will be monitored for new uploads, default is ./Unsorted")
    parser_group_storage.add_argument("--workfolder", default="./Busy", help="Specify the folder where training data will be stored, default is ./Busy")
    parser_group_storage.add_argument("--modelfolder", default="./Model", help="Specify the folder where CAPTCHA models will be stored, default is ./Models")

    args = parser.parse_args()

    server = Captcha22(args)
    server.main()
