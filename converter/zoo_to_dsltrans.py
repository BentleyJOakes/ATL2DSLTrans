#takes the ATL zoo and converts it into .dsltrans files

from ZipDownloader import ZipDownloader
from ZipHandler import ZipHandler
from ConvertATL2XMI import ConvertATL2XMI
from RTEHandler import RTEHandler
from ConvertATL2DSLTrans import ConvertATL2DSLTrans

class ZooConverter:

    def __init__(self, zip_dir, trans_dir):
        self.zip_dir = zip_dir
        self.trans_dir = trans_dir

    def download_zips(self, zoo_site):
        ZipDownloader(zoo_site, self.zip_dir)

    def separate_transformations(self):
        zh = ZipHandler(self.zip_dir, self.trans_dir)
        zh.unzip()

    def run_atl_to_xmi(self):
        cax = ConvertATL2XMI(self.trans_dir)
        cax.set_up()
        cax.convert()
        cax.tear_down()

    def run_types_trans(self):
        rte = RTEHandler(self.trans_dir)
        rte.run()

    def run_atl_to_dsltrans(self):
        catd = ConvertATL2DSLTrans(self.trans_dir)
        catd.set_up()
        catd.convert()
        catd.tear_down()

if __name__ == "__main__":

    zoo_site = "https://www.eclipse.org/atl/atlTransformations/"
    zip_dir = "./zip_dir"
    trans_dir = "./example_dir"
    zc = ZooConverter(zip_dir, trans_dir)

    zc.download_zips(zoo_site)

    zc.separate_transformations()

    zc.run_atl_to_xmi()

    zc.run_types_trans()

    zc.run_atl_to_dsltrans()