# music-genre-classifier

###The dataset
We used [AcousticBrainz](https://acousticbrainz.org/) low-level [data](ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-lowlevel-json-20150129.tar.bz2) to fit a music genre classifier model. These free downloadable data are the result of spectral, harmonical and rhytmic analysis of over a milion tracks by means of [Essentia](https://essentia.upf.edu/documentation/) algorithms; each track in the dataset is stored  as a *JSON* file, therefore we had first to transform each track into a *.csv* row by normalizing *JSON* files and then to retrieve from the MusicBrainz database, if not already present in the file itself, the track's genre (that is, our target). 

###The model
We first aggregatied the hundreds of differnt genres in 9 classes (Pop-other, Rock, Blues, Funk, Jazz, Classical , Metal, Techno-House, Hip-Hop) and, yet, the problem was still untractable. Since *Pop-other* and *Rock* classes were too generic and, coversely, *Funk* and *Blues* classes were too specific, we bdecided to focus on the classification of the remaining classes, ignoring all the tracks whose genre were too specific or too generic.
We fitted *Lasso multi-logit regression*, *Ridge multi-logit regression* and *Linear Discriminant analysis*  models, each one on either dimensionality reduced by means of *Principal Components Analysis* data and original data. 
The best model was *Linear Discrimant Analysis* on reduced data, which classified tracks'genre with an accuracy of about 86%
