#!/usr/bin/env nextflow

nextflow.enable.dsl=2

// Parameters
params.spectraFolder = ""
params.analytes = ""
params.resultsFolder = "macdii_results"
params.rtStart = 10
params.rtEnd = 110
params.precursorToleranceLower = 10
params.precursorToleranceUpper = 10
params.fragmentToleranceLower = 20000 // 0.02 DA
params.fragmentToleranceUpper = 20000 // 0.02 DA
params.output_type = "tsv"

// Runtime parameters
// Memory for the Thermo Raw File Parser, used 24 GB for a Raw file with 257409 MS scans
// and 4GB for a Raw file with 11352 MS scans (measured with `/usr/bin/time -v ...`). 10 GB seems legit for most cases.
// Based on max virtual memory
params.file_conversion__thermo_raw_conversion_mem = "10 GB"
// Memory for the tdf2mzml, used 0.39 GB for a Raw file with 298748 MS scans
// and 0.14GB for a Raw file with 35023 MS scans (measured with `/usr/bin/time -v ...`). 5 GB seems more then enough.
// Based on max virtual memory
params.file_conversion__bruker_raw_conversion_mem = "5 GB"


/**
 * Convert raw file (Thermo Fisher .raw-files) to mzML files
 * @params thermo_raw_files A list of Thermo Fisher .raw-files
 *
 * @return mzML files
 */
process convert_thermo_raw_files {
    label "msconvert_image"
    memory params.file_conversion__thermo_raw_conversion_mem

    input:
    path raw_file

    output:
    path "${raw_file.getBaseName()}.mzML"

    // can only run when profile docker is enabled
    when: workflow.profile == 'docker'

    script:
    """
    if [ ! -f ${raw_file.getBaseName()}.mzML ]; then
        wine msconvert --mzML --zlib --filter "peakPicking vendor msLevel=1-" ${raw_file}
    else
        echo "File ${raw_file.getBaseName()}.mzML already exists"
    fi
    """
}

/**
 * Convert raw files (Bruker .d-folder) to mzML files
 * @params raw_folder Bruker .d-folder
 * Source: https://github.com/mpc-bioinformatics/McQuaC/blob/21e2a19850ae09282ee26899df6cddad1e8e9335/src/io/raw_file_conversion.nf
 *
 * @return mzML file
 */
process convert_bruker_raw_folders {
    label "tdf2mzml_image"

    // Uses all cores
    cpus Runtime.runtime.availableProcessors()
    memory params.file_conversion__bruker_raw_conversion_mem

    input:
    path raw_folder

    output:
    path "${raw_folder.baseName}.mzML"

    script:
    """
    tdf2mzml -i ${raw_folder} --compression "zlib" -o ${raw_folder.baseName}.mzML
    """
}

process macdaii {
    publishDir params.resultsFolder, mode: 'move'

    label "macdii_image"
    cpus 1

    input:
    val rt_start
    val rt_end
    val precursor_tolerance_lower
    val precursor_tolerance_upper
    val fragment_tolerance_lower
    val fragment_tolerance_upper
    path analytes
    path mzml_files

    output:
    path "macdii_results"

    script:
    """
    mkdir macdii_results
    python -m macdii --output-type ${params.output_type} ${rt_start} ${rt_end} ${precursor_tolerance_lower} ${precursor_tolerance_upper} ${fragment_tolerance_lower} ${fragment_tolerance_upper} ${analytes} ./macdii_results ${mzml_files.join(' ')}
    """
}

workflow  {
    main:
    analytes = Channel.fromPath(params.analytes).first()

    // Collect thermo files
	thermo_raw_files = Channel.fromPath(params.spectraFolder + "/*.raw")

	// Collect bruker folder
	bruker_raw_folders = Channel.fromPath(params.spectraFolder + "/*.d", type: 'dir')

	// Collect mzmls
    mzmls = Channel.fromPath(params.spectraFolder + "/*.mzML")

    // Convert into open formats
    thermo_mzmls = convert_thermo_raw_files(thermo_raw_files)
    bruker_mzmls = convert_bruker_raw_folders(bruker_raw_folders)

    mzmls = mzmls.concat(thermo_mzmls, bruker_mzmls).collect()

    results = macdaii(
        params.rtStart,
        params.rtEnd,
        params.precursorToleranceLower,
        params.precursorToleranceUpper,
        params.fragmentToleranceLower,
        params.fragmentToleranceUpper,
        analytes,
        mzmls
    )
}
