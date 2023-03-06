import gzip
import os
import pytest
import shutil
import subprocess as sp
import sys
from pathlib import Path
from . import init

test_dir = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(test_dir))
from config_fixture import output_dir, config

data_dir = Path(__file__).parent / "data"


@pytest.fixture
def setup(init):
    output_dir = init

    yield output_dir

    shutil.rmtree(output_dir / "sunbeam_output")


def test_adapter_removal_paired(setup):
    output_dir = setup
    sunbeam_output_dir = output_dir / "sunbeam_output"
    r1 = sunbeam_output_dir / "qc" / "01_cutadapt" / "TEST_1.fastq.gz"
    r2 = sunbeam_output_dir / "qc" / "01_cutadapt" / "TEST_2.fastq.gz"

    sp.check_output(
        [
            "sunbeam",
            "run",
            "--profile",
            f"{output_dir}",
            "--notemp",
            "--rerun-triggers=input",
            f"{r1}",
            f"{r2}",
        ]
    )

    assert r1.stat().st_size >= 10000
    assert r2.stat().st_size >= 10000

    with gzip.open(r1) as f1, gzip.open(r2) as f2:
        assert len(f1.readlines()) == len(f2.readlines())


def test_adapater_removal_paired_no_adapters(setup):
    output_dir = setup
    sunbeam_output_dir = output_dir / "sunbeam_output"
    r1 = sunbeam_output_dir / "qc" / "01_cutadapt" / "TEST_1.fastq.gz"
    r2 = sunbeam_output_dir / "qc" / "01_cutadapt" / "TEST_2.fastq.gz"

    config_str = f"qc: {{fwd_adapters: }}"
    sp.check_output(
        [
            "sunbeam",
            "config",
            "modify",
            "-i",
            "-s",
            config_str,
            f"{output_dir / 'sunbeam_config.yml'}",
        ]
    )
    config_str = f"qc: {{rev_adapters: }}"
    sp.check_output(
        [
            "sunbeam",
            "config",
            "modify",
            "-i",
            "-s",
            config_str,
            f"{output_dir / 'sunbeam_config.yml'}",
        ]
    )

    sp.check_output(
        [
            "sunbeam",
            "run",
            "--profile",
            f"{output_dir}",
            "--notemp",
            "--rerun-triggers=input",
            f"{r1}",
            f"{r2}",
        ]
    )

    assert os.path.islink(r1)
    assert os.path.islink(r2)