import os
import subprocess

class RTEHandler:
    def __init__(self, trans_dir):
        self.trans_dir = trans_dir

        self.jar_loc = os.path.expanduser("~/Projects/ATL2DSLTrans/ruleTypeExtraction/")
        self.jar_name = "ruleTypeExtraction.jar"

    def run(self):
        dirs = sorted([os.path.join(self.trans_dir, d) for d in os.listdir(self.trans_dir) if
                       os.path.isdir(os.path.join(self.trans_dir, d))])
        for d in dirs:
            files = sorted([f for f in os.listdir(d)])
            print(files)

            source_MM = [x for x in files if x.endswith(".ecore") and x.startswith("source_")][0]
            target_MM = [x for x in files if x.endswith(".ecore") and x.startswith("target_")][0]
            trans = [x for x in files if x.endswith(".atl")][0]

            source_MM_path = os.path.abspath(os.path.join(d, source_MM))
            target_MM_path = os.path.abspath(os.path.join(d, target_MM))
            trans_path = os.path.abspath(os.path.join(d, trans))
            path = os.path.abspath(d)

            # print(source_MM)
            # print(target_MM)
            # print(trans)

            current_path = os.getcwd()
            os.chdir(self.jar_loc)

            command = "java -jar " + self.jar_name + " " + source_MM_path  + " " + target_MM_path  + " " + trans_path + " " + path
            print("Running: " + command)
            subprocess.run(command, shell=True)

            os.chdir(current_path)
