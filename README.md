# Hugin Astrometry
Using astrometry.net to create hugin control points for astrophotographic panoramas.

Hugin isn't really designed for this, so it's a bit hit or miss with the photometric matching, e.g. sometimes I'll get really blown out highlights. I've found that just adding _tons_ of control points fixes this. When you open the project it will also throw out some of the control points for some reason, perhaps because the borders of the WCS aren't to Hugin's standard, but as long as there are some left over. Usually I then run the geometric optimiser, then Hugin CPFind (prealigned), then the geometric optimiser and then the photometric optimiser (mostly because I have no idea exactly what these do in terms of how much existing alignment information they use), and that has given me reasonable results.

![image showing lunar eclipse, aurora](/../images/images/pano2_v2.jpg)

## Dependencies:
`astrometry.net`, as well as index files. I used KStars to download the index files for the FOV I was using. You can do this by running Ekos with any profile (the simulators profile works fine), and then clicking on the wee edit button next to the solve parameters. I also updated my `/etc/astrometry.cfg` to include the `/home/<username>/.local/share/kstars/astrometry` dir, which is where Ekos stores its index files.
### Python
- astropy
- numpy
- matplotlib (using mpl paths to calc intersections)

## Usage
Just run it in the directory containing your images, your WCS files, and your hugin project (which has already had all the images imported). For example, my dir looks like:

![image showing directory listing of .wcs, .jpg, and .pto files](/../images/images/example_dir.png)

and was created by running:
```bash
solve-field *.jpg -D out --continue -L 40 -H 100 -J --sigma 20 -z 3 -p
mv out/*.wcs .
python3 <path to hugin-astrometry>/main.py
```

It's required that the filename of the WCS match the name of the image, and that those are the only two files with that name (ignoring the file extension) in that directory.
The information required to associate an arbitrary WCS file with the image is in there, but it's a bit of a pain to get.

## Issues
Here, the control points are bunched up, and do not cover the whole area of intersection between the images.
![image showing control points bunched up in one corner when more overlap exists](/../images/images/showing_issues.png)

Also, as a natural limitation of this method of finding control points, if there is too long taken between shots, the sky will have rotated significantly enough for the horizon to get a bit wobbly. The image above is a combination of 6s exposures, with as little time between photos as possible.
