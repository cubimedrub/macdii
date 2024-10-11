# MaCDII - Mass Centric Direct Infusion Inspector

Simple tool for searching fragment ions of analytes in direct infusion PRM runs. An analyte is defined by a precursor m/z, a quantifier m/z (unique MS2 ion) and a qualifier m/z (non-unique MS2 ion). Each ion in MS1 will be checked against each analytes precursor, if it matches if is reported in the `precursor_matches.tsv`. Ions in each MS2 are check against the analytes quantifier and qualifier and will be noted in `quantifier_matches.tsv` and `qualifier_matches.tsv` respectively.

For each analyte the average m/z and intensity of the quantifiers matches are calculated for quantification. 


## Installation
First you need to clone the repository.

### Conda
```
conda env create -f environment.yml
```

### Docker
```
docker build -t local/macdii:latest .
```

## Usage

### Conda
```bash
python -m macdii ...
```

### Docker
```bash
docker run -it --rm -v <local_path>:<docker_path> local/macdii:latest ...
```

`--help` will show all option

## Results
MaCDII produces 4 result files.

1. `precursor_matches.tsv`: Ions matching in MS1 spectra, for users to check where the precursor might occurs
2. `qualifier_matches.tsv`: Matching qualifier in MS2 spectra, for users to check where the analyte might occur
3. `quantifier_matches.tsv`: Matching quantifiers
4. `quantification.tsv`: Average m/z and intensities of matched quantifiers per analyte
