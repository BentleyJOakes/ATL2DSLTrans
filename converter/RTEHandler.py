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
            trans_name = trans.replace(".atl", "")

            trans_path = os.path.abspath(os.path.join(d, trans))
            path = os.path.abspath(d)

            #print(source_MM)
            # print(target_MM)
            # print(trans)

            current_path = os.getcwd()
            os.chdir(self.jar_loc)

            source_mm = None
            source_mm_name = None

            target_mm = None
            target_mm_name = None

            for mm in mms:
                mm_name = mm.replace("mm_", "").replace(".ecore", "")

                if trans_name.lower().startswith(mm_name.lower()):
                    source_mm = mm
                    source_mm_name = mm_name
                elif trans_name.lower().endswith(mm_name.lower()):
                    target_mm = mm

            if len(mms) == 1:
                source_mm = mms[0]
                target_mm = mms[0]

            #try to autodetect source and target mms
            if source_mm and not target_mm:
                if source_mm_name in mms[0]:
                    target_mm = mms[1]
                else:
                    if source_mm_name in mms[1]:
                        target_mm = mms[0]



            if not (source_mm and target_mm):
                s = "Error: Couldn't find source and target metamodels from transformation name!\n"
                s += "Metamodels: " + str(mms) + "\n"
                s+= str(source_mm)
                s += str(target_mm)
                s += "Transformation name: " + trans
                raise Exception(s)



            source_mm_path = os.path.abspath(os.path.join(path, source_mm))
            target_mm_path = os.path.abspath(os.path.join(path, target_mm))

            suffix = ""#""-" + mm1_name + '-' + mm2_name
            command = "java -jar " + self.jar_name + " " + source_mm_path  + " " + target_mm_path  + " " + trans_path + " " + path + " " + suffix
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
