# hugin-astrometry

## Dependencies:
`astrometry.net`, as well as index files.
### Python
- astropy
- numpy
- matplotlib (using mpl paths to calc intersections)

## Usage
Just run it in the directory containing your images and your WCS files. For example, my dir looks like:

and was created by running:
```bash
solve-field *.jpg -D out --continue -L 40 -H 100  -J --sigma 20 -z 3 -p
mv out/*.wcs .
```

It's required that the filename of the WCS match the name of the image, and that those are the only two files with that name (ignoring the file extension) in that directory.
The information required to associate an arbitrary WCS file with the image is in there, but it's a bit of a pain to get.
