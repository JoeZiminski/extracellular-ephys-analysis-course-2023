
import spikeinterface.extractors as si_extractors
import spikeinterface.preprocessing as si_prepro
import spikeinterface.sorters as si_sorters

from pathlib import Path

base_path = Path(r"/ceph/neuroinformatics/neuroinformatics/scratch/jziminski/extracellular-ephys-analysis-course-2023")
data_path = base_path / r"rawdata" / "sub-001" / "ses-001" / "ephys"
output_path = base_path / "derivatives" / "sub-001" / "ses-001" / "ephys"

# Loading Raw Data ---------------------------------------------------------------------
raw_recording = si_extractors.read_spikeglx(data_path)

# Preprocessing ------------------------------------------------------------------------

shifted_recording = si_prepro.phase_shift(raw_recording)

filtered_recording = si_prepro.bandpass_filter(
    shifted_recording, freq_min=300, freq_max=6000
)

common_referenced_recording = si_prepro.common_reference(
    filtered_recording, reference="global", operator="median"
)

preprocessed_recording = si_prepro.whiten(common_referenced_recording, dtype='float32')

# Sorting ------------------------------------------------------------------------------

sorting_output_path = output_path / "sorting"

sorting = si_sorters.run_sorter(
   "kilosort2_5",
   preprocessed_recording,
   output_folder=(output_path / "sorting").as_posix(),
)
