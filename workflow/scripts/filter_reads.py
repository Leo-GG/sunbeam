import subprocess as sp
import sys
from collections import OrderedDict
from filter_reads_f import count_host_reads, calculate_counts, write_log

with open(snakemake.log[0], "w") as l:
    done = False
    with open(snakemake.input.hostreads) as f:
        if not f.readlines():
            s = f"WARNING: {snakemake.input.hostreads} is empty, exiting..."
            l.write(s)
            sys.stderr.write(s)
            sp.call(
                [
                    "cp",
                    snakemake.input.reads,
                    snakemake.output.reads,
                ],
                shell=True,
            )
            done = True

    if not done:
        hostdict = OrderedDict()
        net_hostlist = set()
        for hostid in snakemake.input.hostids:
            count_host_reads(hostid, hostdict, net_hostlist)

        host, nonhost = calculate_counts(snakemake.input.reads, net_hostlist)

        sp.call(
            [
                "gzip",
                "-dc",
                snakemake.input.reads,
                "|",
                "rbt",
                "fastq-filter",
                snakemake.input.hostreads,
                "|",
                "gzip",
                ">",
                snakemake.output.reads,
            ],
            shell=True,
        )

        with open(snakemake.output.log, "w") as log:
            write_log(log, hostdict, host, nonhost)
