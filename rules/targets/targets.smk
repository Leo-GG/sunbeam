# -*- mode: Snakemake -*-
#
# list the all input files for each step

# ---- Quality control
# FastQC reports
TARGET_FASTQC = [
    expand(
        QC_FP/'reports'/'{sample}_{rp}_fastqc'/'fastqc_data.txt',
        sample=Samples.keys(), rp=Pairs),
    str(QC_FP/'reports'/'fastqc_quality.tsv'),
]

# Quality-control reads
TARGET_CLEAN = expand(
    QC_FP/'cleaned'/'{sample}_{rp}.fastq.gz',
    sample = Samples.keys(), rp = Pairs)

TARGET_QC = TARGET_CLEAN + TARGET_FASTQC

# Remove host reads
TARGET_DECONTAM = [
    expand(
        QC_FP/'decontam'/'{sample}_{rp}.fastq.gz',
        sample = Samples.keys(), rp = Pairs),
    str(QC_FP/'reports'/'preprocess_summary.tsv'),
]


# ---- Classification
# Classify all reads
TARGET_CLASSIFY = [CLASSIFY_FP/'kraken'/'all_samples.tsv']


# ---- Assembly
# Assemble contigs
TARGET_ASSEMBLY = [
    expand(
        ASSEMBLY_FP/'contigs'/'{sample}-contigs.fa',
        sample = Samples.keys())
]


# ---- Mapping
# Map reads to target genomes
TARGET_MAPPING = [
    expand(
        MAPPING_FP/"{genome}"/"{sample}.bam.bai",
        genome=GenomeSegments.keys(), sample=Samples.keys()),
    expand(
        MAPPING_FP/"{genome}"/"{sample}.raw.bcf",
        genome=GenomeSegments.keys(), sample=Samples.keys()),
    expand(
        MAPPING_FP/"{genome}"/"coverage.csv",
        genome=GenomeSegments.keys())
]


# ---- Contig annotation
# Annotate all contigs
TARGET_ANNOTATE = expand(
    ANNOTATION_FP/'summary'/'{sample}.tsv',
    sample=Samples.keys())


# ---- All targets
TARGET_ALL = (
    TARGET_QC +
    TARGET_DECONTAM +
    TARGET_CLASSIFY +
    TARGET_ASSEMBLY +
    TARGET_ANNOTATE +
    TARGET_MAPPING
)
