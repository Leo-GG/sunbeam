# -*- mode: Snakemake -*-


rule all_mapping:
    input:
        TARGET_MAPPING,


rule build_genome_index:
    input:
        Cfg["mapping"]["genomes_fp"] / "{genome}.fasta",
    output:
        Cfg["mapping"]["genomes_fp"] / "{genome}.fasta.amb",
    conda:
        "../../envs/mapping.yml"
    shell:
        "cd {Cfg[mapping][genomes_fp]} && bwa index {input}"


rule align_to_genome:
    input:
        reads=expand(QC_FP / "decontam" / "{{sample}}_{rp}.fastq.gz", rp=Pairs),
        index=Cfg["mapping"]["genomes_fp"] / "{genome}.fasta.amb",
    output:
        temp(MAPPING_FP / "intermediates" / "{genome}" / "{sample}.sam"),
    threads: Cfg["mapping"]["threads"]
    params:
        index_fp=Cfg["mapping"]["genomes_fp"],
    conda:
        "../../envs/mapping.yml"
    shell:
        """
        bwa mem -M -t {threads} \
        {params.index_fp}/{wildcards.genome}.fasta \
        {input.reads} -o {output}
        """


rule samtools_convert:
    input:
        MAPPING_FP / "intermediates" / "{genome}" / "{sample}.sam",
    output:
        MAPPING_FP / "{genome}" / "{sample}.bam",
    threads: Cfg["mapping"]["threads"]
    conda:
        "../../envs/mapping.yml"
    shell:
        """
        samtools view -@ {threads} -b {Cfg[mapping][samtools_opts]} {input} | \
        samtools sort -@ {threads} > {output}
        """


def _sorted_csvs(w):
    pattern = MAPPING_FP / "intermediates" / w.genome / "{sample}.csv"
    paths = sorted(expand(pattern, sample=Samples.keys()))
    return paths


rule samtools_summarize_coverage:
    input:
        _sorted_csvs,
    output:
        MAPPING_FP / "{genome}" / "coverage.csv",
    shell:
        "(head -n 1 {input[0]}; tail -q -n +2 {input}) > {output}"


rule samtools_get_coverage:
    input:
        MAPPING_FP / "{genome}" / "{sample}.bam",
    output:
        MAPPING_FP / "intermediates" / "{genome}" / "{sample}.csv",
    conda:
        "../../envs/mapping.yml"
    script:
        "../../scripts/mapping/samtools_get_coverage.py"


rule samtools_index:
    input:
        MAPPING_FP / "{genome}" / "{sample}.bam",
    output:
        MAPPING_FP / "{genome}" / "{sample}.bam.bai",
    conda:
        "../../envs/mapping.yml"
    shell:
        "samtools index {input} {output}"


rule samtools_mpileup:
    input:
        bam=MAPPING_FP / "{genome}" / "{sample}.bam",
        genome=Cfg["mapping"]["genomes_fp"] / "{genome}.fasta",
    output:
        MAPPING_FP / "{genome}" / "{sample}.raw.bcf",
    conda:
        "../../envs/mapping.yml"
    shell:
        """
        bcftools mpileup -f {input.genome} {input.bam} | \
        bcftools call -Ob -v -c - > {output}
        """
