from zipfile import ZipFile
import os
import shutil

from collections import defaultdict

class ZipHandler:

    def __init__(self, zip_dir, trans_dir):
        self.zip_dir = zip_dir
        self.trans_dir = trans_dir

    def unzip(self):
        files = os.listdir(self.zip_dir)

        files = [os.path.join(self.zip_dir, f) for f in files if f.endswith(".zip")]
        files.sort()
        for i, zip_filename in enumerate(files):

            #if "TT2BDD" not in zip_filename:
            #   continue

            print("Opening up example: " + zip_filename)

            mms = defaultdict(list)
            trans = defaultdict(list)

            with ZipFile(zip_filename) as myzip:
                for f in myzip.infolist():
                    #print(f.filename)

                    skip_words = ["output", "test"]
                    skip = False
                    for x in skip_words:
                        if x in f.filename.lower():
                            skip = True
                            break
                    if skip:
                        continue

                    name = f.filename.split("/")[-1].split(".")[0]

                    if f.filename.endswith(".ecore") or f.filename.endswith(".xmi"):
                        mms[name]= f

                    elif f.filename.endswith(".atl"):
                        trans[name] = f

                #print("MMS: ")
                #for k, v in mms.items():
                #    print(str(k) + " : " + str(v.filename))


                #find the needed metamodels in the transformation
                for atl_trans_name, atl_trans_file in trans.items():
                    with myzip.open(atl_trans_file) as myfile:

                        #print("File: " + atl_trans_file.filename)

                        MMs = []

                        for line in myfile.readlines():
                            #print(line)
                            if not b"create " in line:
                                continue

                            line = line.decode("UTF-8").replace(";", "").replace(",","").strip()

                            #print(line)
                            spl = line.split(" ")

                            mm_indices = [i+1 for i, x in enumerate(line.split(" ")) if x == ":"]

                            MMs = [spl[x] for x in mm_indices]

                        #print(in_mm)
                        #print(out_mm)

                        built_in_MMs = ['ATL', 'XML']

                        if not MMs:
                            print("Error: Couldn't get metamodels from transformation: " + atl_trans_name)
                            #raise Exception()
                            break

                        for mm in MMs:

                            if mm not in built_in_MMs and mm not in mms.keys():
                                print("Error: Metamodel not found: " + mm)
                                #raise Exception()

                        atl_trans_dir = os.path.join(self.trans_dir, atl_trans_name)
                        #print(atl_trans_dir)
                        #print(atl_trans_file.filename)

                        if not os.path.exists(atl_trans_dir):
                            os.mkdir(atl_trans_dir)

                        self.extract_file("", myzip, atl_trans_file, atl_trans_dir)

                        for mm in MMs:
                            if mm not in built_in_MMs:
                                if mms[mm]:
                                    self.extract_file("mm_", myzip, mms[mm], atl_trans_dir)
                            else:
                                source_file = os.path.join("metamodels", mm + ".ecore")
                                target_file = os.path.join(atl_trans_dir, "mm_" + mm + ".ecore")
                                shutil.copyfile(source_file, target_file)

    def extract_file(self, prefix, zip_file, file_object, target_dir):
        source = zip_file.open(file_object)

        target_filename = file_object.filename.split("/")[-1]
        target = open(os.path.join(target_dir, prefix + target_filename), "wb")
        with source, target:
            shutil.copyfileobj(source, target)
