import pytest
from astropy import units as u
import sys
sys.path.append("/Users/huntsman/Documents/Huntsman/signal-to-noise")
import signal_to_noise as snr

@pytest.fixture
def canon():
    return snr.Optic(aperture = 139.642857143 * u.mm, \
                  focal_length = 391.0 * u.mm, \
                  throughput_filename='resources/canon_throughput.csv')
@pytest.fixture
def rasa():
    return snr.Optic(aperture = 279.0 * u.mm, \
                focal_length = 620.0 * u.mm, \
                throughput_filename='resources/rasa_tau.csv', \
                central_obstruction = 129.0 * u.mm)
@pytest.fixture
def sbig():
    return snr.Camera(pixel_size = 5.4 * u.micron / u.pixel, \
                  resolution = (3326, 2504) * u.pixel, \
                  read_noise = 9.3  * u.electron / u.pixel, \
                  dark_current = 0.04 * u.electron / (u.second * u.pixel), \
                  QE_filename = "resources/ML8300M_QE.csv", \
                  minimum_exposure = 0.1 * u.second) # Dark current 'average' at -10C
@pytest.fixture
def fli():
    return snr.Camera(pixel_size = 6.0 * u.micron / u.pixel, \
                 resolution = (8176, 6132) * u.pixel, \
                 read_noise = 11.8  * u.electron / u.pixel, \
                 dark_current = 0.015 * u.electron / (u.second * u.pixel), \
                 QE_filename = "resources/ML50100_QE.csv", \
                 minimum_exposure = 1.0 * u.second) #Dark current at -25C
@pytest.fixture
def zwo():
    return snr.Camera(pixel_size = 3.8 * u.micron / u.pixel, \
                 resolution = (4656, 3520) * u.pixel, \
                 read_noise = 2.5 * u.electron / u.pixel, \
                 dark_current = darkcur[1] * u.electron / (u.second * u.pixel), \
                 QE_filename = "resources/ZWO_QE.csv", \
                 minimum_exposure = 0.000032 * u.second) #the value of the dark current has been approximated
@pytest.fixture
def g_astrodon():
    return snr.Filter('resources/astrodon_g.csv', sky_mu = 22.5)

@pytest.fixture
def canon_sbig_psf():
    return snr.Moffat_PSF(FWHM=2 * u.arcsecond, alpha=2.5)

@pytest.fixture
def canon_sbig_g(canon, sbig, g_astrodon, canon_sbig_psf):
    return snr.Imager(canon, sbig, g_astrodon, canon_sbig_psf)

def test_imagerarray_oneimager(canon_sbig_g):
    SBIG_ImagerArray = snr.ImagerArray([canon_sbig_g])
    list_exptime = SBIG_ImagerArray.exposure_time_array(16, 25500 * u.electron, 0.37 * u.electron/u.adu, 11.0* u.ABmag, 2)
    assert len(list_exptime) == 1
    assert isinstance (list_exptime[0], u.Quantity)
    assert list_exptime[0].value - 10 <= 1 
    
def test_imagerarray_twoimager(canon_sbig_g):
    SBIG_ImagerArray = snr.ImagerArray([canon_sbig_g, canon_sbig_g])
    list_exptime = SBIG_ImagerArray.exposure_time_array(16, 25500 * u.electron, 0.37 * u.electron/u.adu, 11.0* u.ABmag, 2)
    assert len(list_exptime) == 2
    