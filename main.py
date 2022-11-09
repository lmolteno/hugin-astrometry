import pathlib
import matplotlib.path as mpath
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
import itertools

from hugin import HuginProject, ControlPoint, Point

if __name__ == "__main__":
    project_fn = [*pathlib.Path('.').glob("*.pto")][0]
    wcs_files = [*pathlib.Path('.').glob("*.wcs")]

    project = HuginProject(project_fn)
    wcs = []
    footprints = []
    image_indices = []

    # Load WCS files, calculate footprints, and store image indices (which is how hugin references each image)
    for file in wcs_files:
        # turn 'IMGL7241.wcs' into 'IMGL7241' then find another non-wcs file matching 'IMGL7241.*'
        fn = file.name.split('.')[0]
        image_fn = [*filter(lambda p: p.suffix != '.wcs', pathlib.Path('.').glob(f'{fn}.*'))]
        if len(image_fn) == 0:
            raise Exception(f"Could not find image matching WCS {file}")

        f = fits.open(file)
        w = WCS(f[0].header)
        footprint = w.calc_footprint(axes=(f[0].header['IMAGEW'], f[0].header['IMAGEH']))

        wcs.append(w)
        footprints.append(footprint)
        image_indices.append(project.image_index(image_fn[0].name))
        f.close()

    # loop over every combination of images, adding control points.
    for (w1, f1, i1), (w2, f2, i2) in itertools.combinations(zip(wcs, footprints, image_indices), 2):
        f1_path = mpath.Path(vertices=f1)
        f2_path = mpath.Path(vertices=f2)

        # total maximum and minimum ra and dec (this may not behave well near the RA meridian)
        comb = np.vstack((f1, f2))
        min_c = np.amin(comb, axis=0)
        max_c = np.amax(comb, axis=0)
        points = np.random.uniform(min_c, max_c, (10000, 2))

        contained_points = points[f1_path.contains_points(points) & f2_path.contains_points(points)]
        if len(contained_points) == 0:
            continue

        # use the calculated WCS from astrometry to project those sky coordinates to pixel coordinates
        contained_points_sc = SkyCoord(contained_points, unit='deg')
        i1_pixel_coords = np.array(w1.world_to_pixel(contained_points_sc)).T
        i2_pixel_coords = np.array(w2.world_to_pixel(contained_points_sc)).T

        # add those pixel coordinates as control points to the hugin project.
        cps = []
        for i1_p, i2_p in zip(i1_pixel_coords, i2_pixel_coords):
            cps.append(ControlPoint(i1, i2, Point(*i1_p), Point(*i2_p)))

        project.add_cps(cps)
        print(f"Added {len(cps)} control points between images {i1} and {i2}")

    project.close()
