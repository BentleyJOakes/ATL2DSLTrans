#takes the ATL zoo and converts it into .dsltrans files

from ZipDownloader import ZipDownloader
from ZipHandler import ZipHandler

class ZooConverter:

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def download_zips(self, zoo_site):
        ZipDownloader(zoo_site, self.output_dir)

    def separate_transformations(self):
        zh = ZipHandler(self.output_dir)
        zh.unzip()

if __name__ == "__main__":

    zoo_site = "https://www.eclipse.org/atl/atlTransformations/"
    output_dir = "./output"
    zc = ZooConverter(output_dir)

    #zc.download_zips(zoo_site)

    zc.separate_transformations()