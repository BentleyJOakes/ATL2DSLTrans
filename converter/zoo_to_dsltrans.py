#takes the ATL zoo and converts it into .dsltrans files

from ZipDownloader import ZipDownloader
from ZipHandler import ZipHandler

class ZooConverter:

    def __init__(self, zip_dir, trans_dir):
        self.zip_dir = zip_dir
        self.trans_dir = trans_dir

    def download_zips(self, zoo_site):
        ZipDownloader(zoo_site, self.zip_dir)

    def separate_transformations(self):
        zh = ZipHandler(self.zip_dir, self.trans_dir)
        zh.unzip()

if __name__ == "__main__":

    zoo_site = "https://www.eclipse.org/atl/atlTransformations/"
    zip_dir = "./zip_dir"
    trans_dir = "./example_dir"
    zc = ZooConverter(zip_dir, trans_dir)

    #zc.download_zips(zoo_site)

    zc.separate_transformations()

    zc.run_atl2model()