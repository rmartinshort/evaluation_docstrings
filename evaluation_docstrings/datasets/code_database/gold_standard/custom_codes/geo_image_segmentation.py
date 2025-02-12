import numpy as np
import rasterio
import os
from shapely import geometry
import geopandas as gpd
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from config import config


class ImageChopper(BaseEstimator, TransformerMixin):
    def __init__(self, show_info=True) -> None:
        """

        Instruct the code to chop image into chunks of size nxpixels x nypixels
        The pieces will be returned in the form of a geodataframe, where they can be manipulated individually

        """
        self.show_info = show_info

    def display_dgalinfo(self) -> None:
        os.system(f"gdalinfo {self.file_location}")

    def div_odd_even(self, n) -> tuple:
        if n % 2 != 0:
            return (n // 2, n // 2 + 1)
        else:
            return (int(n / 2), int(n / 2))

    def determine_padding(self, l, l_pad, npix) -> tuple:
        if (l + l_pad) % npix == 0:
            new_l = l + l_pad
        else:
            new_l = l + (npix - l_pad)
            l_pad = npix - l_pad

        return (l_pad, new_l)

    def fit(
        self,
        file_location,
        nxpixels=config.DEFAULT_NXPIX,
        nypixels=config.DEFAULT_NYPIX,
    ) -> "ImageChopper":
        ###
        # CHECK THAT THE FILE EXISTS
        ###

        self.file_location = file_location
        self.npixwidth = nxpixels
        self.npixheight = nypixels

        if self.show_info == True:
            self.display_dgalinfo()
            print("---------------------------------------\n\n")

        with rasterio.open(self.file_location, "r") as sat_data:
            self.lon_per_pixel = abs(sat_data.transform[0])
            self.lat_per_pixel = abs(sat_data.transform[4])

            print("Rows: {}, Columns: {}".format(sat_data.height, sat_data.width))

            # Upper left pixel
            row_min = 0
            col_min = 0

            # Lower right pixel.  Rows and columns are zero indexing.
            row_max = sat_data.height - 1
            col_max = sat_data.width - 1

            self.w = sat_data.width  # original width of dataset
            self.h = sat_data.height  # original height of dataset

            # Transform coordinates with the dataset's affine transformation.
            self.topleft = sat_data.transform * (row_min, col_min)
            self.botright = sat_data.transform * (row_max, col_max)

            print("Top left corner coordinates: {}".format(self.topleft))
            print("Bottom right corner coordinates: {}".format(self.botright))

            dataset = sat_data.read()

        w_r = self.w % self.npixwidth
        h_r = self.h % self.npixheight

        (w_r, self.new_width) = self.determine_padding(self.w, w_r, self.npixwidth)
        (h_r, self.new_height) = self.determine_padding(self.h, h_r, self.npixheight)

        self.pad_l, self.pad_r = self.div_odd_even(w_r)
        self.pad_b, self.pad_t = self.div_odd_even(h_r)

        # update the top left corner coordinares of the new grid
        self.tl_w = self.topleft[0] - self.pad_l * self.lon_per_pixel
        self.tl_h = self.topleft[1] + self.pad_t * self.lat_per_pixel

        # grid that we will fill with the final dataset
        self.even_grid = np.full(
            [np.shape(dataset)[0], self.new_height, self.new_width], np.nan
        )

        self.even_grid[
            :,
            self.pad_b : self.new_height - self.pad_t,
            self.pad_l : self.new_width - self.pad_r,
        ] = dataset

        print(f"Shape of the padded dataset = {np.shape(self.even_grid)}")

        # delete the original dataset from memory
        del dataset

        return self

    def transform(self, X: pd.DataFrame = None) -> gpd.GeoDataFrame:
        nwidth = np.shape(self.even_grid)[2]
        nheight = np.shape(self.even_grid)[1]

        # Need to convert to WGS84! Then use the dimensions per pixel to build the geometry polygons
        tl_w_orig = self.tl_w
        tl_h_orig = self.tl_h

        # seems to slice from the top left
        inc_width = 0

        data = {"slicedata": [], "nnans": [], "geometry": []}

        tl_w = tl_w_orig

        for i in range(nwidth // self.npixwidth):
            inc_height = 0
            tl_h = tl_h_orig

            for j in range(nheight // self.npixheight):
                # make the slice
                slice_ij = self.even_grid[
                    :,
                    inc_height : inc_height + self.npixheight,
                    inc_width : inc_width + self.npixwidth,
                ]

                # count the number of nans
                # This is the total number of NaNs, which is really not very useful. What we really need is the number if nans per band
                nnans = np.sum(np.isnan(slice_ij))

                # get bounds
                bounds = (
                    (tl_w, tl_h),
                    (tl_w + self.lon_per_pixel * self.npixwidth, tl_h),
                    (
                        tl_w + self.lon_per_pixel * self.npixwidth,
                        tl_h - self.lat_per_pixel * self.npixheight,
                    ),
                    (tl_w, tl_h - self.lat_per_pixel * self.npixheight),
                )

                bounding_poly = geometry.Polygon(bounds)

                data["slicedata"].append(slice_ij)
                data["nnans"].append(nnans)
                data["geometry"].append(bounding_poly)

                # increment
                inc_height += self.npixheight
                tl_h = tl_h - self.lat_per_pixel * self.npixheight

            inc_width += self.npixwidth
            tl_w = tl_w + self.lon_per_pixel * self.npixwidth

        # convert to GeoDataFrame
        geoframe = gpd.GeoDataFrame(data)

        # projection system will always be lon-lat
        geoframe.crs = {"init": "epsg:4326"}

        return geoframe
