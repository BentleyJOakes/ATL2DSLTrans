import os
import shutil

class ConvertATL2DSLTrans:

    def __init__(self, trans_dir):
        self.trans_dir = trans_dir

        self.dest_dir = "../ATL2DSLTrans/"
        self.examples_dir = "examples"
        self.dest_dir_examples = os.path.join(self.dest_dir, self.examples_dir)
        self.dest_dir_configs = os.path.join(self.dest_dir, "configs")
        self.base_script = os.path.join(self.dest_dir, "ATL2DSLTrans_BaseScript.launch")

        self.launch_group_file = os.path.join(self.dest_dir, "ATL2DSLTrans.launch")


        self.trans_moved = []
        self.trans_moved_dirs = {}

    def set_up(self):

        print("Setting up conversion from ATL to DSLTrans")

        no_trans_xmi = 0
        no_types_xmi = 0

        #move needed files
        dirs = sorted([os.path.join(self.trans_dir, d) for d in os.listdir(self.trans_dir) if os.path.isdir(os.path.join(self.trans_dir, d))])
        for d in dirs:
            trans_name = str(d.split("/")[-1]).replace(".atl", "")
            #print(trans_name + b".xmi")
            trans_xmi = [f for f in os.listdir(d) if f == trans_name + ".xmi"]
            if not trans_xmi:
                #print("Error: Transformation XMI not found in " + d)
                no_trans_xmi += 1
                continue
            else:
                trans_xmi = trans_xmi[0]

            types_xmi = [f for f in os.listdir(d) if f.endswith("Types.xmi")]


            if not types_xmi:
                #print("Error: Types XMI not found in " + d)
                no_types_xmi += 1
                continue
            else:
                types_xmi = types_xmi[0]

            mms = [f for f in os.listdir(d) if f.endswith(".ecore")]

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

            # try to autodetect source and target mms
            if source_mm and not target_mm:
                if source_mm_name in mms[0]:
                    target_mm = mms[1]
                else:
                    if source_mm_name in mms[1]:
                        target_mm = mms[0]

            if not (source_mm and target_mm):
                s = "Error: Couldn't find source and target metamodels from transformation name!\n"
                s += "Metamodels: " + str(mms) + "\n"
                s += str(source_mm)
                s += str(target_mm)
                s += "Transformation name: " + trans_name
                raise Exception(s)

            # print("Trans XMI: " + trans_xmi)
            # print(types_xmi)
            # print(source_mm)
            # print(target_mm)
            # print(trans_name)



            trans_dir = os.path.join(self.dest_dir_examples, trans_name)
            if not os.path.exists(trans_dir):
                os.mkdir(trans_dir)


            files_to_move = [trans_xmi, types_xmi, source_mm, target_mm]

            files = sorted([f for f in os.listdir(d)])
            for f in files:
                if f in files_to_move:
                    full_filename = os.path.join(d, f)
                    shutil.copyfile(full_filename, os.path.join(trans_dir, f))
                    #print(full_filename + " - " + os.path.join(trans_dir, f))

                #record this transformation moved over
                if trans_name not in self.trans_moved:
                    self.trans_moved.append(trans_name)

                self.trans_moved_dirs[trans_name] = d

                new_name = "convert_" + trans_name + ".launch"
                new_script = os.path.join(self.dest_dir_configs, new_name)

                replace_keys = {
                    "*XMIFILE*":os.path.join(self.examples_dir, trans_name, trans_xmi),
                    "*INMM*": os.path.join(self.examples_dir, trans_name, source_mm),
                    "*OUTMM*": os.path.join(self.examples_dir, trans_name, target_mm),
                    "*TYPESFILE*": os.path.join(self.examples_dir, trans_name, types_xmi),
                    "*OUTFILENAME*": trans_name,
                }
                with open(self.base_script) as base:
                    with open(new_script, 'w') as new:
                        for line in base:
                            for k, v in replace_keys.items():
                                line = line.replace(k, v)
                            new.write(line)

        with open(self.launch_group_file, 'w') as lg:
            lg.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            lg.write('<launchConfiguration type="org.eclipse.debug.core.groups.GroupLaunchConfigurationType">\n')
            for i, trans in enumerate(self.trans_moved):
                lg.write('<stringAttribute key="org.eclipse.debug.core.launchGroup.{0}.action" value="DELAY"/>\n'.format(i))
                lg.write('<stringAttribute key="org.eclipse.debug.core.launchGroup.{0}.actionParam" value="3"/>\n'.format(i))
                lg.write('<booleanAttribute key="org.eclipse.debug.core.launchGroup.{0}.adoptIfRunning" value="false"/>\n'.format(i))
                lg.write('<booleanAttribute key="org.eclipse.debug.core.launchGroup.{0}.enabled" value="true"/>\n'.format(i))
                lg.write('<stringAttribute key="org.eclipse.debug.core.launchGroup.{0}.mode" value="inherit"/>\n'.format(i))
                lg.write('<stringAttribute key="org.eclipse.debug.core.launchGroup.{0}.name" value="convert_{1}"/>\n'.format(i, trans))
            lg.write('</launchConfiguration>\n')


        print("Number of transformations possible: " + str(len(dirs)))
        print("Failed (no transformation xmi): " + str(no_trans_xmi))
        print("Failed (no types xmi): " + str(no_types_xmi))
        print("Successes: " + str(len(dirs) - no_trans_xmi - no_types_xmi))

    def convert(self):

        # #TODO: Add automation of this step
        #
        #
        # first = True
        # while True:
        #
        #     files = [f.replace(".xmi", "") for f in os.listdir(self.dest_dir_examples) if f.endswith(".xmi")]
        #
        #     missing = [x for x in self.trans_moved if x not in files]
        #     if len(missing) == 0:
        #         break
        #     else:
        #
        #         if first:
        #             print("Please manually run the ATL2XMI launch script in Eclipse.")
        #             print("This monitoring script will loop until all transformations have been converted.")
        #             first = False
        #
        #         print("Still missing: " + str(len(missing)))
        #         print(" - ".join(missing))
        #
        #     sleep(5)
        pass

    def tear_down(self):
        pass
        # num_files_moved_back = 0
        #
        # files = [f.replace(".xmi", "") for f in os.listdir(self.dest_dir_examples) if f.endswith(".xmi")]
        #
        # for f in files:
        #
        #     if f not in self.trans_moved:
        #         continue
        #
        #     filename = os.path.join(self.dest_dir_examples, f)
        #     #print(filename)
        #
        #     original_dir = self.trans_moved_dirs[f]
        #
        #     #print(original_dir)
        #     shutil.copyfile(filename+".xmi", os.path.join(original_dir, f+".xmi"))
        #     num_files_moved_back += 1
        #
        # print("Moved " + str(num_files_moved_back) + " xmi files")