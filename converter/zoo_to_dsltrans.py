#takes the ATL zoo and converts it into .dsltrans files

from ZipDownloader import ZipDownloader

class ZooConverter:

    def __init__(self, zoo_site):
        output_dir = "./output"
        ZipDownloader(zoo_site, output_dir)

if __name__ == "__main__":

    zoo_site = "https://www.eclipse.org/atl/atlTransformations/"
    zc = ZooConverter(zoo_site)
    #zc.start()
