import ee
from ee_plugin import Map

trend = ee.ImageCollection("users/ingmarnitze/TCTrend_SR_2000-2019_TCVIS")
# elevation
arctic_dem = ee.Image("UMN/PGC/ArcticDEM/V3/2m_mosaic").select('elevation')
elevationVis = {
  'min': -50.0,
  'max': 700.0,
  'palette':['#709959', '#F0E990', '#F0CB86', '#C9957F', 
  '#CC9E89', '#EED7BC', '#F9ECD7', '#FBF5EA', '#FCFAF5', 
  '#FCFBF9', '#FCFCFC']
}
hs = ee.Terrain.hillshade(arctic_dem)

##### GMTED
gmted = ee.Image("USGS/GMTED2010").select('be75')
gmted_hs = hs = ee.Terrain.hillshade(gmted)

Map.addLayer(arctic_dem, elevationVis, 'Arctic DEM')
Map.addLayer(hs, {'min':150, 'max':200}, 'ArcticDEM Hillshade')
Map.addLayer(gmted, elevationVis, 'GMTED DEM')
Map.addLayer(gmted_hs, {}, 'GMTED Hillshade')
Map.addLayer(trend.mosaic(), {}, 'TCVIS')