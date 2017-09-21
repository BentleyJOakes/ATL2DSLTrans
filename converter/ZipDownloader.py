from html.parser import HTMLParser
import urllib.request

import os

class ZipDownloader(HTMLParser):

    def __init__(self, site, output_dir):
        super(ZipDownloader, self).__init__()

        self.site = site
        self.output_dir = output_dir

        self.output_files = os.listdir(output_dir)
        self.output_files = [x for x in self.output_files if x.endswith(".zip")]

        opener = urllib.request.FancyURLopener({})
        f = opener.open(site)
        content = f.read()

        #print(content)
        for line in str(content).split("\n"):
            self.feed(line)

    def download_zip(self, link):

        if link.split("/")[-1] in self.output_files:
            return

        print("Link: " + str(link))

        full_link = link
        if not full_link.startswith("http"):
            full_link = self.site + "/" + link

        full_output_link = os.path.join(self.output_dir, link.split("/")[-1])

        print("Retrieving: " + full_link)
        try:
            urllib.request.urlretrieve(full_link, full_output_link)
        except urllib.error.HTTPError as e:
            print("HTTP Error: " + str(e))

    def handle_starttag(self, tag, attrs):


        if tag != "a":
            return

        if not any(a[0] == 'href' for a in attrs):
            return

        link = [x[1] for x in attrs if x[0] == 'href']

        if not link:
           return

        link = link[0]


        if not link.endswith(".zip"):
            return


        self.download_zip(link)


    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass