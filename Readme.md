<img src="docs/images/sunbeam_logo.gif" width=120, height=120 align="left" />

# Sunbeam: a robust, extensible metagenomic sequencing pipeline 

[![CircleCI](https://circleci.com/gh/sunbeam-labs/sunbeam/tree/dev.svg?style=shield)](https://circleci.com/gh/sunbeam-labs/sunbeam/tree/dev) [![Documentation Status](https://readthedocs.org/projects/sunbeam/badge/?version=latest)](http://sunbeam.readthedocs.io/en/latest/?badge=latest)

Sunbeam is a pipeline written in [snakemake](http://snakemake.readthedocs.io)
that simplifies and automates many of the steps in metagenomic sequencing
analysis. It uses [conda](http://conda.io) to manage dependencies, so it
doesn't have pre-existing dependencies or admin privileges, and can be deployed
on most Linux workstations and clusters. To read more, check out [our paper
in Microbiome](https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-019-0658-x).

Sunbeam currently automates the following tasks:

* Quality control, including adaptor trimming, host read removal, and quality
  filtering;
* Taxonomic assignment of reads to databases using [Kraken](https://github.com/DerrickWood/kraken);
* Assembly of reads into contigs using [Megahit](https://github.com/voutcn/megahit);
* Contig annotation using BLAST[n/p/x];
* Mapping of reads to target genomes; and
* ORF prediction using [Prodigal](https://github.com/hyattpd/Prodigal).

Sunbeam was designed to be modular and extensible. Some extensions have been built for:

- [IGV](https://github.com/sunbeam-labs/sbx_igv) for viewing read alignments
- [KrakenHLL](https://github.com/zhaoc1/sbx_krakenhll), an alternate read classifier
- [Kaiju](https://github.com/sunbeam-labs/sbx_kaiju), a read classifier that uses BWA rather than kmers
- [Anvi'o](https://github.com/sunbeam-labs/sbx_anvio), a downstream analysis pipeline that does lots of stuff!

More extensions can be found at the extension page: https://www.sunbeam-labs.org/

**To get started, see our [documentation](http://sunbeam.readthedocs.io)!**

If you use the Sunbeam pipeline in your research, please cite: 

*EL Clarke, LJ Taylor, C Zhao et al. Sunbeam: an extensible pipeline for 
analyzing metagenomic sequencing experiments. Microbiome 7:46 (2019)*

------

### Changelog:

#### Development Version (as of October 29, 2019)

 - Integration test updates to schedule weekly builds (#222)
 - Script updates to use conda commands instead of source commands (#220)
 - Add h5py package explicitly to avoid dependency metadata problem (#219)
 - Add multiQC to build QC report (#203)
 - Use multithreading for cutadapt in QC (#202)
 - Correct conda channel priority during install (#201)
 - Update documentation to spell out requirements (#199)
 - New megahit failure handling (#194)
 - Enforce sample wildcard constraints in Snakemake rules (#190)
 - Run megahit multithreaded (#189)

#### v2.0.2 (August 28, 2019)

 - Add implicit dependencies (samtools and bcftools) to environment file to make them explicit

#### v2.0.1 (July 24, 2019)

 - Increment Snakemake version requirement for compatibility with recent conda
 - Specify earlier megahit version to ensure compatbility with existing assembly behavior
 - Integration test improvements

#### v2.0.0 (January 22, 2019)

 - Start a project using resources directly from the SRA using `sunbeam init --data_acc [SRA ###]`. For more information, see [the docs](https://sunbeam.readthedocs.io/en/latest/usage.html#creating-a-new-project-using-data-from-sra)
 - New extension website: https://www.sunbeam-labs.org/
 - Improved documentation
 - Numerous bugfixes and optimizations

#### v1.2.1 (May 24, 2018)

 - Minor bugfixes

#### v1.2.0 (May 2, 2018)

 - Low-complexity reads are now removed by default rather than masked
 - Bug fixes related to single-end sequencing experiments
 - Documentation updates
 
#### v1.1.0 (April 8, 2018)

 - Reports include number of filtered reads per host, rather than in aggregate
 - Static binary dependency for [komplexity](https://github.com/eclarke/komplexity) for easier deployment
 - Remove max length filter for contigs
 
#### v1.0.0 (March 22, 2018)

 - First stable release!
 - Support for single-end sequencing experiments
 - Low-complexity read masking via [komplexity](https://github.com/eclarke/komplexity)
 - Support for extensions
 - Documentation on [ReadTheDocs.io](http://sunbeam.readthedocs.io)
 - Better assembler (megahit)
 - Better ORF finder (prodigal)
 - Can remove reads from any number of host/contaminant genomes
 - Semantic versioning checks
 - Integration tests and continuous deployment

-------

### Contributors

- Erik Clarke ([@eclarke](https://github.com/eclarke))
- Chunyu Zhao ([@zhaoc1](https://github.com/zhaoc1))
- Jesse Connell ([@ressy](https://github.com/ressy))
- Louis Taylor ([@louiejtaylor](https://github.com/louiejtaylor))
- Kyle Bittinger ([@kylebittinger](https://github.com/kylebittinger))

