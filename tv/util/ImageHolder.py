import os


class ImageHolder:
    def __init__(self):
        self.path = ''
        self.city = ''
        self.filename = ''
        self.longitude = 0
        self.latitude = 0

    def get_image_path(self):
        return self.path + "/" + self.filename

    def get_bottom(self):
        return str(int((90 + self.latitude) / 180 * 100)) + "%"

    def get_left(self):
        return str(int((180 + self.longitude) / 360 * 100)) + "%"
