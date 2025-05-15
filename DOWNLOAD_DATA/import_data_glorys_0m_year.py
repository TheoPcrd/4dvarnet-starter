# script.py
import sys

# Récupérer les arguments passés au script
y_start = sys.argv[1]

print(f"Year start: {y_start}")

folder_data = "/Odyssey/private/t22picar/data/glorys_0m"
import copernicusmarine

copernicusmarine.subset(
  dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
  variables=["mlotst", "uo", "vo", "zos", "thetao"],
  minimum_longitude=-180,
  maximum_longitude=179.9166717529297,
  minimum_latitude=-90,
  maximum_latitude=90,
  start_datetime=f"{y_start}-01-01T00:00:00",
  end_datetime=f"{y_start}-12-31T00:00:00",
  minimum_depth=0.49402499198913574,
  maximum_depth=0.49402499198913574,
  output_directory = folder_data
)
