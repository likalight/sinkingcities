"""Print the actual HDF5 tree, metadata and candidate datasets without assuming paths."""
import argparse
import json
from pathlib import Path

import h5py
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TERMS = ('unwrappedphase', 'coherencemagnitude', 'connectedcomponents', 'ionosphere',
         'wavelength', 'frequency', 'incidence', 'projection', 'epsg', 'xcoordinates',
         'ycoordinates', 'spacing', 'zerodoppler', 'orbitpass', 'lookdirection')


def plain(value):
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='replace')
    if isinstance(value, np.ndarray):
        return [plain(v) for v in value.tolist()] if value.ndim else plain(value.item())
    if isinstance(value, np.generic):
        return plain(value.item())
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def inspect(path):
    lines, candidates = [], {}
    with h5py.File(path, 'r') as file:
        lines.append('/ attributes=' + json.dumps({k: plain(v) for k, v in file.attrs.items()}))
        def visit(name, obj):
            entry = {'kind': 'dataset' if isinstance(obj, h5py.Dataset) else 'group',
                     'attributes': {k: plain(v) for k, v in obj.attrs.items()}}
            if isinstance(obj, h5py.Dataset):
                entry.update(shape=list(obj.shape), dtype=str(obj.dtype))
                if obj.size <= 16 and obj.dtype.kind != 'V':
                    entry['value'] = plain(obj[()])
                if any(t in name.rsplit('/', 1)[-1].lower() for t in TERMS):
                    candidates['/' + name] = entry
            lines.append('/' + name + ' ' + json.dumps(entry, ensure_ascii=False))
        file.visititems(visit)
    return '\n'.join(lines)+'\n', candidates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('granule', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT/'reports/inspection')
    args = parser.parse_args()
    if not args.granule.is_file():
        parser.error('Granule missing; run 02_download.py with Earthdata credentials first')
    tree, candidates = inspect(args.granule)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'hdf5_tree.txt').write_text(tree, encoding='utf-8')
    (args.output/'candidates.json').write_text(json.dumps({'file': args.granule.name, 'candidates': candidates}, indent=2), encoding='utf-8')
    print(tree)
    print(f'Candidate layers: {len(candidates)}. Review shapes, units, CRS and fill values before extraction.')
    print('No paths selected automatically. Sign convention and stable reference remain an explicit science gate.')


if __name__ == '__main__':
    main()
