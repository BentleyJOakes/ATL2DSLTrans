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

        num_success = 0
        print("Extracting rule types for " + str(len(dirs)) + " transformations")
        for d in dirs:
            files = sorted([f for f in os.listdir(d)])
            print(files)

            mms = [x for x in files if x.endswith(".ecore")]
            trans = [x for x in files if x.endswith(".atl")][0]

            trans_path = os.path.abspath(os.path.join(d, trans))
            path = os.path.abspath(d)

            #print(source_MM)
            # print(target_MM)
            # print(trans)

            current_path = os.getcwd()
            os.chdir(self.jar_loc)

            #try all combos of mms
            for mm1 in mms:
                mm1_name = mm1.replace("mm_", "").replace(".ecore", "")
                mm1_path = os.path.abspath(os.path.join(path, mm1))
                #print(mm1_path)
                for mm2 in mms:
                    mm2_name = mm2.replace("mm_", "").replace(".ecore", "")
                    mm2_path = os.path.abspath(os.path.join(path, mm2))

                    suffix = "-" + mm1_name + '-' + mm2_name
                    command = "java -jar " + self.jar_name + " " + mm1_path  + " " + mm2_path  + " " + trans_path + " " + path + " " + suffix
                    print("Running: " + command)
                    out_filename = os.path.join(path, "out" + suffix + ".txt")
                    with open(out_filename, 'w') as o:
                        subprocess.run(command, shell=True, stderr = subprocess.STDOUT, stdout=o)

            os.chdir(current_path)

            files = sorted([f for f in os.listdir(d)])
            types = [f for f in files if "Types" in f]
            if types:
                num_success += 1


        print("Successfully found types for " + str(num_success) + " transformations.")
