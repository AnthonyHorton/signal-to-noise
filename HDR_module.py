import signal_to_noise as snr
from astropy import units as u
import yaml
config = yaml

def create_imager_array(config):
    optics = dict()
    cameras = dict()
    filters = dict()
    psfs = dict()
    imagers = dict()
    imagers_list = []

    #Setup imagers
    for imager_info in config['imagers']:
        name = imager_info['name']

        optic_name = imager_info['optic']
        try:
            # Try to get from cache
            optic = optics[optic_name]
        except KeyError:
            # Create optic from this imager
            optic_info = config['optics'][optic_name]
            optic = snr.Optic(**optic_info)

            # Put in cache
            optics[optic_name] = optic

        camera_name = imager_info['camera']    
        try:
            # Try to get from cache
            camera = cameras[camera_name]
        except KeyError:
            # Create camera for this imager
            camera_info = config['cameras'][camera_name]
            camera_info['resolution']=[int(s) for s in camera_info['resolution'].split(',')]
            camera = snr.Camera(**camera_info)

            # Put in cache
            cameras[camera_name] = camera

        filter_name = imager_info['filter']
        try:
            # Try to get from cache
            filter = filters[filter_name]
        except KeyError:
            # Create optic from this imager
            filter_info = config['filters'][filter_name]
            filter = snr.Filter(**filter_info)

            # Put in cache
            filters[filter_name] = filter

        psf_name = imager_info['psf']
        try:
            # Try to get from cache
            psf = psfs[psf_name]
        except KeyError:
            # Create optic from this imager
            psf_info = config['psfs'][psf_name]
            psf = snr.Moffat_PSF(**psf_info)

            # Put in cache
            psfs[psf_name] = psf

        imagers[name] = snr.Imager(optic = optic, camera = camera, band = filter, num_imagers = imager_info['num_imagers'],\
                                   num_computers = imager_info['num_computers'], PSF = psf)
        
        
        imagers_list.append(imagers[name])
        
    imager_array = snr.ImagerArray(imagers_list)
                  
    return imager_array

def make_HDR_table



    

    
