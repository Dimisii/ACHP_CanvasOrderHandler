import datetime
import traceback

import requests
import os
import zipfile


class FileHandler():

    def __init__(self):
        current_date = datetime.date.today()
        self.year = current_date.strftime("20%y")
        self.mounth = current_date.strftime("%m")
        self.day = current_date.strftime("%d")

    def download(self, download_link, order_id):
        zip_order = requests.get(download_link).content
        path = "C://Users/dms/Desktop/order_" + order_id + ".zip"
        try:
            with open(path, "wb") as file:
                file.write(zip_order)
        except Exception:
            traceback.print_exc()
            return False
        return path

    def unZIP(self, path, order_id: str="no_id"):
        zip_order = zipfile.ZipFile(path, "r", zipfile.ZIP_DEFLATED)
        file_list = zip_order.namelist()
        for file in file_list:
            if file.count("surface_[0](empty)_zone_[0](gallery).jpg")>0:
                image_path = zip_order.extract(file, f'C://Users/dms/Desktop/{self.year}/{self.mounth}/{self.day}/')
                finally_image_path = f'C://Users/dms/Desktop/{self.year}/{self.mounth}/{self.day}/{order_id}.jpg'
                os.rename(image_path, finally_image_path)
                os.removedirs(image_path[0:image_path.find("surface_[0](empty)_zone_[0](gallery).jpg")])
        return finally_image_path

