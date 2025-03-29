import os
import time
import numpy as np
import xarray as xr
import dask
import dask.array as da
from dask.diagnostics import ProgressBar
import torch
import xbatcher as xb
import xbatcher.loaders.torch
import sys



def load_era5_data():
      valid_time_start = '2023-01-01'
      valid_time_stop = '2023-01-02'
      ds = xr.open_zarr(
      'gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3',
      chunks='auto',
      storage_options=dict(token='anon'),
      )
      ar_full_37_1h = ds.sel(time=slice(ds.attrs['valid_time_start'], ds.attrs['valid_time_stop']))

      print(ar_full_37_1h)
      return ar_full_37_1h



if __name__ == '__main__':
      load_era5_data()
