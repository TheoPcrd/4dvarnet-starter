folder_data = "/Odyssey/private/t22picar/data/sst_2020"
import copernicusmarine

copernicusmarine.subset(
  dataset_id="cmems_obs-sst_glo_phy_my_l3s_P1D-m",
  variables=["adjusted_sea_surface_temperature"],
  minimum_longitude=-179.9499969482422,
  maximum_longitude=179.9499969482422,
  minimum_latitude=-90,
  maximum_latitude=90,
  start_datetime="2020-01-20T00:00:00",
  end_datetime="2021-04-20T00:00:00",
  output_directory = folder_data
)
