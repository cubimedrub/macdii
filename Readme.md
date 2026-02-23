# MaCDII - Mass Centric Direct Infusion Inspector

Simple tool for searching fragment ions of metabolomic and lipidomic analytes in direct infusion PRM MS runs. An analyte is defined by a precursor m/z, a quantifier m/z (unique MS2 ion) and a optional qualifier m/z (non-unique MS2 ion). A analyte matches a MS2 spectum if the analyte precurosor matches the spectrum precursor and the spectrum contains a fragment matching the analytes quantifier m/z. 

For each analyte the average m/z and intensity of the quantifiers matches are calculated for quantification. 

MaCDII comes in two variants
* Python module: Can be used from CLI on Windows, Linux and macOS or imported in other Python code. Uses mzML files only.
* Nextflow workflow: Can be used from CLI on Linux and macOS or [MAcWorP](https://github.com/cubimedrub/macworp). Windows is supported via WSL2. Accepts Thermo Fisher Raw files, Bruker d-folder and mzML (the frist two are converted to mzML)

## Installation
Choose one depending on your needs. Each installation method is done via terminal (Linux & macOS) or CMD/Powershell (Windows)
 
### Python

#### Native
If you have Python 3.12+ already installed on your system, run `pip install git+https://github.com/cubimedrub/macdii.git`

#### (Ana-)Conda or Micromamba
If you prefer a isolated installation

1. Install [(ana-)conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) or [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)
2. Clone (via `git`) or download (blue button labeled `Code` and unzip) the repository from `https://github.com/cubimedrub/macdii.git`
3. Navigate to the downloaded repository
4. Run `conda env create -f environment.yml`
5. Run `conda activate macdii`

### Nextflow
1. [Install Nextflow](https://www.nextflow.io/docs/latest/install.html)
2. [Install Docker](https://docs.docker.com/desktop/) (after the installatio make sure you are able to run Docker commands)


## Usage

### Analytes TSV
Use your favorite spreadsheet software to create a table like:

| analyte | precursor_mz | quantifier_mz | qualifier_mz |
| --- | --- | --- | --- |
| FA 2:0 | 194.0564 | 151.0456 | 137.0345 |

* Keep the columns in this order.
* Precursor m/z has to be the same as stated in the PRM method. If it was rounded it needs to be rounded here.
* Quantifier m/z can be 0.0 if unneeded, which will leave the respective columns in the output file empty
* Safe the analyte table as tab-separate-format (TSV) and make sure the values uses `.` as decimal mark.


### Python

* Showing help and all available paramters: `pyhton -m macdii --help`
* Run matching
  1. Create a output folder 
  2. `python -m macdii <RETENTION_START_TIME_IN_SEC> <RETENTIONS_STOP_TIME_IN_SEC> <LOWER_PRECURSOR_TOLERANCE_IN_PPM> <UPPER_PRECURSOR_TOLERANCE_IN_PPM> <LOWER_FRAGMENT_TOLERANCE_IN_PPM> <UPPER_FRAGMENT_TOLERANCE_IN_PPM> <ANALYTES_TSV> <PATH_TO_OUTPUT_FOLDER> <PATH_TO_MZML_1> <PATH_TO_MZML_2`    
      e.g.    
      `python -m macdii 10 110 1000 1000 10 10 test_data/my_project/analytes.tsv ./macdii_results test_data/my_project/mzmls/QAT0001586.mzML test_data/my_project/mzmls/QAT0001587.mzML test_data/my_project/mzmls/QAT0001588.mzML`  

Converting files into mzML can be done via [Proteowizard msConvert](https://proteowizard.sourceforge.io/index.html) or [thermorawfileparser](https://github.com/CompOmics/ThermoRawFileParser) ([with graphical user interface](https://compomics.github.io/projects/ThermoRawFileParserGUI))

### Nextflow
The workflows does not have any help functions.

Run matching `nextflow run -profile docker main.nf --rtStart <RETENTION_START_TIME_IN_SEC> --rtEnd RETENTIONS_STOP_TIME_IN_SEC> --precursorToleranceLower <LOWER_PRECURSOR_TOLERANCE_IN_PPM> --precursorToleranceUpper <UPPER_PRECURSOR_TOLERANCE_IN_PPM> --fragmentToleranceLower <LOWER_FRAGMENT_TOLERANCE_IN_PPM> --fragmentToleranceUpper <UPPER_FRAGMENT_TOLERANCE_IN_PPM> --spectraFolder <PATH_TO_FOLDE_CONTAINING_SPECTRUM_FILES> --analytes <ANALYTES_TSV> --resultsFolder <PATH_TO_OUTPUT_FOLDER>`   
e.g.    
`nextflow run -profile docker main.nf --rtStart 10 --rtEnd 110 --precursorToleranceLower 10 --precursorToleranceUpper 10 --fragmentToleranceLower 20000 --fragmentToleranceUpper 20000 --spectraFolder test_data/my_project/raws --analytes test_data/my_project/analytes.tsv --resultsFolder macdii_results`  


## Results
MaCDII produces 4 result files.

1. `quantifier_matches.tsv`: Matching quantifiers
2. `quantification.tsv`: Average m/z and intensities of matched quantifiers per analyte

## Development
### Setup
Use the Python/Conda installation for development. Formatting and typechecking is done via [Ruff](https://docs.astral.sh/ruff/) and [Ty](https://docs.astral.sh/ty/).

### Testing
`python -m unittest discover -s ./tests -p '*_test.py'`
