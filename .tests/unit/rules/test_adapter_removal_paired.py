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

    shutil.copytree(data_dir / "qc" / "00_samples", output_dir / "sunbeam_output")

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
            "--rerun-triggers",
            "params",
            f"{r1}",
            f"{r2}",
        ]
    )

    assert os.path.isfile(r1)
    assert os.path.isfile(r2)
