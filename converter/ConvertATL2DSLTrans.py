import os
class ConvertATL2DSLTrans:

    def __init__(self, trans_dir):
        self.trans_dir = trans_dir

        self.dest_dir = "../ATL2DSLTrans/"
        self.dest_dir_examples = os.path.join(self.dest_dir, "examples")
        self.dest_dir_configs = os.path.join(self.dest_dir, "configs")
        self.base_script = os.path.join(self.dest_dir, "ATL2DSLTrans_BaseScript.launch")

        self.launch_group_file = os.path.join(self.dest_dir, "ATL2DSLTrans.launch")

    def set_up(self):

        print("Setting up conversion from ATL to DSLTrans")

        #move needed files
        dirs = sorted([os.path.join(self.trans_dir, d) for d in os.listdir(self.trans_dir) if os.path.isdir(os.path.join(self.trans_dir, d))])
        for d in dirs:
            trans_name = str(d.split("/")[-1])
            #print(trans_name + b".xmi")
            trans_xmi = [f for f in os.listdir(d) if f == trans_name + ".xmi"]
            if not trans_xmi:
                #print("Error: Transformation XMI not found in " + d)
                continue

            types_xmi = [f for f in os.listdir(d) if f.endswith(".xmi") and "Types" in f]


            if not types_xmi:
                #print("Error: Types XMI not found in " + d)
                continue

            print(trans_xmi)
            print(types_xmi)

            # files = sorted([f for f in os.listdir(d) if f.endswith(".atl")])
            # for f in files:
            #     trans_name = f.replace(".atl", "")
            #     full_filename = os.path.join(d, f)
            #     shutil.copyfile(full_filename, os.path.join(self.dest_dir_examples, f))
            #
            #     #record this transformation moved over
            #     if trans_name not in self.trans_moved:
            #         self.trans_moved.append(trans_name)
            #
            #     self.trans_moved_dirs[trans_name] = d
            #
            #     with open(self.base_script) as base:
            #
            #         new_name = "convert_" + trans_name + ".launch"
            #         new_script = os.path.join(self.dest_dir_configs, new_name)
            #         with open(new_script, 'w') as new:
            #             for line in base:
            #
            #                 new_line = line.replace("Composed2Simple", trans_name)
            #                 new.write(new_line + "\n")

        # with open(self.launch_group_file, 'w') as lg:
        #     lg.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        #     lg.write('<launchConfiguration type="org.eclipse.debug.core.groups.GroupLaunchConfigurationType">\n')
        #     for i, trans in enumerate(self.trans_moved):
        #         lg.write('<stringAttribute key="org.eclipse.debug.core.launchGroup.{0}.action" value="WAIT_FOR_TERMINATION"/>\n'.format(i))
        #         lg.write('<booleanAttribute key="org.eclipse.debug.core.launchGroup.{0}.adoptIfRunning" value="false"/>\n'.format(i))
        #         lg.write('<booleanAttribute key="org.eclipse.debug.core.launchGroup.{0}.enabled" value="true"/>\n'.format(i))
        #         lg.write('<stringAttribute key="org.eclipse.debug.core.launchGroup.{0}.mode" value="inherit"/>\n'.format(i))
        #         lg.write('<stringAttribute key="org.eclipse.debug.core.launchGroup.{0}.name" value="convert_{1}"/>\n'.format(i, trans))
        #     lg.write('</launchConfiguration>\n')
        #
        # print("Moved " + str(len(self.trans_moved)) + " ATL files")

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