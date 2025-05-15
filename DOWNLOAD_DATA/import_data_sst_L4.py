folder_data = "/Odyssey/private/t22picar/data/sst_L4"
import copernicusmarine

import copernicusmarine

copernicusmarine.subset(
  dataset_id="METOFFICE-GLO-SST-L4-REP-OBS-SST",
  variables=["analysed_sst"],
  minimum_longitude=-179.97500610351562,
  maximum_longitude=179.97500610351562,
  minimum_latitude=-89.9749984741211,
  maximum_latitude=89.9749984741211,
  start_datetime="2019-01-01T00:00:00",
  end_datetime="2020-01-01T00:00:00",
)