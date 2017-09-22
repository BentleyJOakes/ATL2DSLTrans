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

            if "TT2BDD" not in zip_filename:
               continue

            #print(zip_filename)

            mms = defaultdict(list)
            trans = defaultdict(list)

            with ZipFile(zip_filename) as myzip:
                for f in myzip.infolist():
                    #print(f.filename)

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

                        #print(myfile.readlines())

                        in_mm = None
                        out_mm = None

                        for line in myfile.readlines():
                            #print(line)
                            if not b"create OUT" in line:
                                continue

                            line = line.decode("UTF-8").replace(";", "").strip()

                            spl = line.split(" ")
                            in_mm = spl[1].split(":")[1]
                            out_mm = spl[3].split(":")[1]

                        #print(in_mm)
                        #print(out_mm)

                        if in_mm is None or out_mm is None:
                            print("Error: Couldn't get metamodels from transformation: " + atl_trans_name)
                            continue

                        if in_mm not in mms.keys() or out_mm not in mms.keys():
                            print("Error: Metamodels not found: " + in_mm + " or " + out_mm)
                            continue

                        atl_trans_dir = os.path.join(self.trans_dir, atl_trans_name)
                        #print(atl_trans_dir)
                        #print(atl_trans_file.filename)

                        if not os.path.exists(atl_trans_dir):
                            os.mkdir(atl_trans_dir)

                        self.extract_file("", myzip, atl_trans_file, atl_trans_dir)
                        self.extract_file("source_", myzip, mms[in_mm], atl_trans_dir)
                        self.extract_file("target_", myzip, mms[out_mm], atl_trans_dir)

    def extract_file(self, prefix, zip_file, file_object, target_dir):
        source = zip_file.open(file_object)

        target_filename = file_object.filename.split("/")[-1]
        target = open(os.path.join(target_dir, prefix + target_filename), "wb")
        with source, target:
            shutil.copyfileobj(source, target)
