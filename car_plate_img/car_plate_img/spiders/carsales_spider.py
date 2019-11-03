import scrapy
import re
import os
import os.path
import urllib.request
from pathlib import Path


class CarSalesSpider(scrapy.Spider):
    name = "carsales"
    local_dir = Path('./')
    count = 0

    def start_requests(self):
        urls = [
            'https://www.carsales.com.au/cars/results/',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=12',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=24',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=36',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=48',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=60',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=72',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=84',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=96',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=108',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=120',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=132',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=144',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=156',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=168',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=180',
            'https://www.carsales.com.au/cars/results/?q=Service.Carsales.&offset=192'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        downloads_dir = self.local_dir / 'downloads'
        
        if not downloads_dir.exists():
            os.mkdir(downloads_dir)

        # loop for every pages img 
        for img in response.css('img.owl-lazy').xpath('@data-src').getall():
            img_url = img[:img.find("?")]
            img_filename = downloads_dir / img_url.split("/")[-1]
            urllib.request.urlretrieve(img_url, img_filename)

            self.log("Downloaded file %s" % img_filename)
            self.count = self.count + 1

        self.log("-----")
        self.log("TOTAL IMAGES: %s" % self.count)

        """ Save the html
        page = response.url.split("/")[-1]
        
        filenumbers = re.findall(r'\d+', page)
        if filenumbers:
            filenumber = filenumbers[-1]
        else:
            filenumber = 1

        filename = 'carsales-%s.html' % filenumber
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        """