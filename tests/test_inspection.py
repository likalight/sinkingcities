"""Exercise tree inspection on an explicitly synthetic fixture, never a NASA result."""
import importlib.util
from pathlib import Path
import h5py
import numpy as np

spec = importlib.util.spec_from_file_location('inspect_product', Path(__file__).resolve().parents[1]/'pipeline/03_inspect.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_arbitrary_paths_metadata_and_arrays(tmp_path):
    fixture = tmp_path/'synthetic_test_only.h5'
    with h5py.File(fixture,'w') as f:
        f.attrs['fixture'] = 'SYNTHETIC UNIT TEST — NOT NASA DATA'
        phase = f.create_dataset('unexpected/location/unwrappedPhase',data=np.ones((20,30)))
        phase.attrs['units'] = 'radians'
        phase.attrs['_FillValue'] = -9999.0
        f.create_dataset('metadata/projection',data=32749)
        f.create_dataset('metadata/label',data=b'synthetic')
    tree, candidates = module.inspect(fixture)
    entry = candidates['/unexpected/location/unwrappedPhase']
    assert entry['shape'] == [20,30]
    assert entry['attributes']['units'] == 'radians'
    assert 'value' not in entry
    assert candidates['/metadata/projection']['value'] == 32749
    assert 'synthetic' in tree
