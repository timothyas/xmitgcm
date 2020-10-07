import os
import numpy as np

from .llcmodel import BaseLLCModel
from . import stores


def _requires_pleiades(func):
    def wrapper(*args, **kwargs):
        # is there a better choice
        test_path = '/home6/dmenemen'
        if not os.path.exists(test_path):
            raise OSError("Can't find %s. We must not be on Pleiades." % test_path)
        func(*args, **kwargs)
    return wrapper

def _make_http_filesystem():
    import fsspec
    from fsspec.implementations.http import HTTPFileSystem
    return HTTPFileSystem()

class LLC90Model(BaseLLCModel):
    nx = 90
    nz = 50
    delta_t = 3600
    time_units = 'seconds since 1948-01-01 12:00:00'
    calendar = 'gregorian'


class LLC2160Model(BaseLLCModel):
    nx = 2160
    nz = 90
    delta_t = 45
    iter_start = 92160
    iter_stop = 1586400 + 1
    iter_step = 80
    time_units='seconds since 2011-01-17'
    calendar = 'gregorian'
    varnames = ['Eta', 'KPPhbl', 'oceFWflx', 'oceQnet', 'oceQsw', 'oceSflux',
                'oceTAUX', 'oceTAUY', 'PhiBot', 'Salt', 'SIarea', 'SIheff',
                'SIhsalt', 'SIhsnow', 'SIuice', 'SIvice', 'Theta', 'U', 'V', 'W']
    grid_varnames = ['AngleCS','AngleSN','Depth',
                     'DRC','DRF',
                     'DXC','DXF','DXG',
                     'DYC','DYF','DYG',
                     'hFacC','hFacS','hFacW','PHrefC','PHrefF',
                     'RAC','RAS','RAW',
                     'RC','RF','RhoRef','rLowC','rLowS','rLowW',
                     'rSurfC','rSurfS','rSurfW','XC','YC',
                     'RAZ','XG','YG','DXV','DYU']
    mask_override = {'oceTAUX': 'c', 'oceTAUY': 'c'}


class LLC4320Model(BaseLLCModel):
    nx = 4320
    nz = 90
    delta_t = 25
    iter_start = 10368
    iter_stop = 1495152 + 1
    iter_step = 144
    time_units='seconds since 2011-09-10'
    calendar = 'gregorian'
    varnames = ['Eta', 'KPPhbl', 'oceFWflx', 'oceQnet', 'oceQsw', 'oceSflux',
                'oceTAUX', 'oceTAUY', 'PhiBot', 'Salt', 'SIarea', 'SIheff',
                'SIhsalt', 'SIhsnow', 'SIuice', 'SIvice', 'Theta', 'U', 'V', 'W']
    grid_varnames = ['AngleCS','AngleSN','Depth',
                     'DRC','DRF',
                     'DXC','DXF','DXG',
                     'DYC','DYF','DYG',
                     'hFacC','hFacS','hFacW','PHrefC','PHrefF',
                     'RAC','RAS','RAW','RC','RF',
                     'RhoRef','XC','YC','RAZ','XG','YG','DXV','DYU']
    mask_override = {'oceTAUX': 'c', 'oceTAUY': 'c'}

class ASTE270Model(BaseLLCModel):
    nface = 6
    nx = 270
    nz = 50
    delta_t = 600
    iter_start = 4464
    iter_stop = 4464 + 1
    iter_step = 4032
    time_units='seconds since 2002-01-01'
    dtype=np.dtype('>f8')
    calendar = 'gregorian'
    varnames = ['THETA', 'SALT']
    grid_varnames = ['AngleCS','AngleSN','Depth',
                     'DRC','DRF',
                     'DXC','DXG',
                     'DYC','DYG',
                     'hFacC','hFacS','hFacW','PHrefC','PHrefF',
                     'RAC','RAS','RAW','RC','RF',
                     'RhoRef','XC','YC','RAZ','XG','YG','DXV','DYU']
    #mask_override = {'oceTAUX': 'c', 'oceTAUY': 'c'}

class ECCOPortalLLC2160Model(LLC2160Model):

    def __init__(self):
        fs = _make_http_filesystem()
        base_path = 'https://data.nas.nasa.gov/ecco/download_data.php?file=/eccodata/llc_2160/compressed'
        grid_path = 'https://data.nas.nasa.gov/ecco/download_data.php?file=/eccodata/llc_2160/grid'
        mask_path = 'https://storage.googleapis.com/pangeo-ecco/llc/masks/llc_2160_masks.zarr/'
        store = stores.NestedStore(fs, base_path=base_path, mask_path=mask_path,
                                   grid_path=grid_path, shrunk=True, join_char='/')
        super(ECCOPortalLLC2160Model, self).__init__(store)


class ECCOPortalLLC4320Model(LLC4320Model):

    def __init__(self):
        fs = _make_http_filesystem()
        base_path = 'https://data.nas.nasa.gov/ecco/download_data.php?file=/eccodata/llc_4320/compressed'
        grid_path = 'https://data.nas.nasa.gov/ecco/download_data.php?file=/eccodata/llc_4320/grid'
        mask_path = 'https://storage.googleapis.com/pangeo-ecco/llc/masks/llc_4320_masks.zarr/'
        store = stores.NestedStore(fs, base_path=base_path, mask_path=mask_path,
                                   grid_path=grid_path, shrunk=True, join_char='/')
        super(ECCOPortalLLC4320Model, self).__init__(store)


class PleiadesLLC2160Model(LLC2160Model):

    @_requires_pleiades
    def __init__(self):
        from fsspec.implementations.local import LocalFileSystem
        fs = LocalFileSystem()
        base_path = '/home6/dmenemen/llc_2160/compressed'
        mask_path = '/nobackup/rpaberna/llc/masks/llc_2160_masks.zarr'
        store = stores.NestedStore(fs, base_path=base_path, mask_path=mask_path,
                                   shrunk=True)
        super(PleiadesLLC2160Model, self).__init__(store)


class PleiadesLLC4320Model(LLC4320Model):

    @_requires_pleiades
    def __init__(self):
        from fsspec.implementations.local import LocalFileSystem
        fs = LocalFileSystem()
        base_path = '/home6/dmenemen/llc_4320/compressed'
        mask_path = '/nobackup/rpaberna/llc/masks/llc_4320_masks.zarr'
        store = stores.NestedStore(fs, base_path=base_path, mask_path=mask_path,
                                   shrunk=True)
        super(PleiadesLLC4320Model, self).__init__(store)

class CRIOSPortalASTE270Model(ASTE270Model):

    def __init__(self):
        fs = _make_http_filesystem()
        base_path = 'https://aste-release1.s3.us-east-2.amazonaws.com/diags'
        grid_path = 'https://aste-test.s3.us-east-2.amazonaws.com/grid'
        store = stores.BaseStore(fs, base_path=base_path, grid_path=grid_path,
                                   shrunk=False, join_char='/')

        super(CRIOSPortalASTE270Model, self).__init__(store)

