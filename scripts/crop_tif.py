import rasterio
import pyproj
import numpy as np
import cv2
import os

import rasterio.transform
import rasterio.warp
import rasterio.windows


class TifClipper():
    def __init__(self):
        # Get python file path
        file_path = os.path.dirname(__file__)
        self.project_path = file_path[:file_path.rfind("/") + 1]

        self.proj_coord = pyproj.Proj(init = "epsg:32649")
        self.geo_coord = pyproj.Proj(init = "epsg:4326")


    def ReadTif(self, in_path):
        self.dataset = rasterio.open(self.project_path + in_path)
        image = self.dataset.read()
        self.image = np.dstack((image[0], image[1], image[2]))
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)


    def GetGeographicData(self, crop_range):
        geo_map = np.zeros((crop_range[3] - crop_range[1] + 1, crop_range[2] - crop_range[0] + 1, 2))
        for i, x_perspect in enumerate(range(crop_range[1], crop_range[3] + 1)):
            for j, y_perspect in enumerate(range(crop_range[0], crop_range[2] + 1)):
                geo_map[i][j][0], geo_map[i][j][1] = self.dataset.xy(x_perspect, y_perspect)
        
        return geo_map


    def Proj2Geo(self, position_proj):
        return pyproj.transform(self.proj_coord, self.geo_coord, position_proj[0], position_proj[1])


    def Geo2Proj(self, position_geo):
        return pyproj.transform(self.geo_coord, self.proj_coord, position_geo[0], position_geo[1])


    def ShowImage(self, img, duration = 0):
        cv2.imshow("img", img)
        cv2.waitKey(duration)


if __name__ == '__main__':
    tif_clipper = TifClipper()
    
    left, top, right, bottom = 970, 7084, 1730, 7925
    tif_clipper.ReadTif("img/xxx.tif")
    # tif_clipper.ShowImage(tif_clipper.image[top:bottom, left:right])

    geo_map = tif_clipper.GetGeographicData([left, top, right, bottom])
    np.save(tif_clipper.project_path + "data/xxx.npy", geo_map)
    cv2.imwrite(tif_clipper.project_path + "img/xxx.png", tif_clipper.image[top:bottom, left:right])
