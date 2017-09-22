
import os
import shutil

from time import sleep

class ConvertATL2XMI:


    def __init__(self, trans_dir):
        self.trans_dir = trans_dir

        self.dest_dir = "../ConvertATL2XMI/"
        self.dest_dir_examples = os.path.join(self.dest_dir, "examples")
        self.dest_dir_configs = os.path.join(self.dest_dir, "configs")
        self.base_script = os.path.join(self.dest_dir, "src", "ConvertATL2XMI.launch")

        self.trans_moved = []
        self.trans_moved_dirs = {}

    def set_up(self):

        #move ATL files
        dirs = sorted([os.path.join(self.trans_dir, d) for d in os.listdir(self.trans_dir) if os.path.isdir(os.path.join(self.trans_dir, d))])
        for d in dirs:
            files = sorted([f for f in os.listdir(d) if f.endswith(".atl")])
            for f in files:
                trans_name = f.replace(".atl", "")
                full_filename = os.path.join(d, f)
                shutil.copyfile(full_filename, os.path.join(self.dest_dir_examples, f))

                #record this transformation moved over
                if trans_name not in self.trans_moved:
                    self.trans_moved.append(trans_name)

                self.trans_moved_dirs[trans_name] = d

                with open(self.base_script) as base:

                    new_name = "convert_" + trans_name + ".launch"
                    new_script = os.path.join(self.dest_dir_configs, new_name)
                    with open(new_script, 'w') as new:
                        for line in base:

                            new_line = line.replace("Composed2Simple", trans_name)
                            new.write(new_line + "\n")

    def convert(self):

        #TODO: Add automation of this step

        print("Please manually run the launch scripts in Eclipse.")
        print("This script will loop until all transformations have been converted.")

        while True:

            files = [f.replace(".xmi", "") for f in os.listdir(self.dest_dir_examples) if f.endswith(".xmi")]

            missing = [x for x in self.trans_moved if x not in files]
            if len(missing) == 0:
                break
            else:
                print("Still missing: " + str(missing))

            sleep(5)

    def tear_down(self):

        files = [f.replace(".xmi", "") for f in os.listdir(self.dest_dir_examples) if f.endswith(".xmi")]

        for f in files:

            if f not in self.trans_moved:
                continue

            filename = os.path.join(self.dest_dir_examples, f)
            #print(filename)

            original_dir = self.trans_moved_dirs[f]

            #print(original_dir)
            shutil.copyfile(filename+".xmi", os.path.join(original_dir, f+".xmi"))
