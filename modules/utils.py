# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 13:19:51 2021

@author: initze
"""
import geopandas as gpd
import ee
from pathlib import Path
from google_drive_downloader import GoogleDriveDownloader as gdd
import geemap


ee.Initialize()

def get_ArcticDEM_slope():
    dem = ee.Image("UMN/PGC/ArcticDEM/V3/2m_mosaic")
    slope = ee.Terrain.slope(dem)
    return slope


def get_ArcticDEM_rel_el(kernel_size=300, offset=50, factor=300):
    dem = ee.Image("UMN/PGC/ArcticDEM/V3/2m_mosaic")
    conv = dem.convolve(ee.Kernel.circle(kernel_size, 'meters'))
    diff = (dem.subtract(conv).add(ee.Image.constant(offset)).multiply(ee.Image.constant(factor)).toInt16())
    return diff

def download_ee2(gdf, ee_layer, GDrive_dir='AI-CORE/slope', scale=2,  suffix='_slope', field='id'):
    
    if field == 'id':
        ids = str(int(gdf.iloc[0].id)).zfill(5)
    else:
        ids = gdf.iloc[0][field]
    name = f'{ids}{suffix}'

    ee_fc = geemap.geopandas_to_ee(gdf)
    buffered_geom = ee_fc.geometry()
    dl = ee.batch.Export.image.toDrive(
        image=ee_layer.clip(buffered_geom),
        description=name,
        folder=GDrive_dir,
        fileNamePrefix=name,
        dimensions=None,
        region=buffered_geom,
        scale=2,
        crs=None,
        crsTransform=None,
        maxPixels=1e13,
        shardSize=None,
        fileDimensions=None,
        skipEmptyTiles=None,
        fileFormat=None,
        formatOptions=None)

    dl.start()
    return dl

def download_gdrive(f, outpath):
    outfile = Path(outpath)/f['name']
    gdd.download_file_from_google_drive(file_id=f['id'],\
                                    dest_path=outfile,\
                                    unzip=False)
