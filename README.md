# music-genre-classifier

### dataset

We used [AcousticBrainz](https://acousticbrainz.org/) low-level [data](ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-lowlevel-json-20150129.tar.bz2) to fit a music genre classifier model. These free downloadable data are the result of spectral, harmonical and rhythmic analysis of over a milion tracks by means of [Essentia](https://essentia.upf.edu/documentation/) algorithms; each track in the dataset is stored  as a *JSON* file, therefore we had first to transform each track into a *.csv* row by normalizing *JSON* files and then to retrieve from the [MusicBrainz](https://musicbrainz.org/) database, if not already present in the file itself, the track's genre (that is, our target). 

### model

We first aggregated the hundreds of different genres in 9 classes (*Pop-other*, *Rock*, *Blues*, *Funk*, *Jazz*, *Classical* , *Metal*, *Techno-House*, *Hip-Hop*) and, yet, the problem was still untractable. Since *Pop-other* and *Rock* classes were too generic and, coversely, *Funk* and *Blues* classes were too specific, we bdecided to focus on the classification of the remaining classes, ignoring all the tracks whose genre were too specific or too generic.
We fitted *Lasso multi-logit regression*, *Ridge multi-logit regression* and *Linear Discriminant analysis*  models, each one on either dimensionality reduced data by means of *Principal Components Analysis* and original data. 
The best model was *Linear Discrimant Analysis* on reduced data, which classified tracks' genre with an accuracy of about 86%

### tools

- We used *Python 3.6* and the *Jupyter Notebook* either on local machines and on an *Hadoop cluster*. 
- We implemented a simple *Python* module, named *ModuloProgetto*, which has been used to speed up data preprocessing 
- We used the efficient and useful Classes contained in *SciKitLearn* module to fit models and reduce dimensionality
- We researched optimal hyper-parameters by means of *Cross-Validation*, which has been run in parallel on the the *Hadoop* cluster
- *Google Cloud Platform* has been used as a service to build the *Hadoop* cluster of virtual machines

### files
- *ModuloProgetto* is the folder of the module mentioned in previous section
- *Esplorazione file - spiegazione idea progetto* is the notebook (run on local machine) used to take a first look at data
- *1_Trasformazione dati.ipynb* is the notebook (run on local machine) to transform data from *JSON* to *csv*
- *2_analisi esplorativa.ipynb* is the notebook (run on local machine) in which data are explored and visualized
- *3_Classificazione (GCP DataProc)* is the notebook (run on Hadoop cluster) in which models have been fitted and optimal hyper-parameters have been researched
- *progetto MSDB* is a *PDF* file which contains the project presentation slides



###### notebooks, comments and slides haven't been translated from italian yet;  we apologize for that
