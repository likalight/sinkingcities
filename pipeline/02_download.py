"""Download selected products using local Earthdata netrc; resume partial files safely."""
import argparse
import csv
import hashlib
import json
import netrc
import re
from pathlib import Path
from urllib.parse import urlparse

import asf_search as asf
import h5py

ROOT = Path(__file__).resolve().parents[1]


def validate(path, row):
    expected = int(row['bytes']) if row.get('bytes') else None
    if expected and path.stat().st_size != expected:
        raise ValueError('File size differs from catalog metadata')
    if row.get('md5'):
        digest = hashlib.md5()
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(8 * 1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest().lower() != row['md5'].lower():
            raise ValueError('Catalog MD5 verification failed')
    with h5py.File(path, 'r') as f:
        if not list(f):
            raise ValueError('Empty HDF5 product')


def download(session, row, target):
    if urlparse(row['url']).scheme != 'https' or urlparse(row['url']).hostname != 'nisar.asf.earthdatacloud.nasa.gov':
        raise ValueError('Only HTTPS NISAR ASF download URLs are accepted')
    name = row['scene'] + '.h5'
    if Path(name).name != name or not re.fullmatch(r'[A-Za-z0-9_.-]+', name):
        raise ValueError('Invalid product filename')
    final = target / name
    partial = target / (name + '.part')
    if final.exists():
        validate(final, row)
        print(f'Already verified: {name}', flush=True)
        return
    offset = partial.stat().st_size if partial.exists() else 0
    expected = int(row['bytes']) if row.get('bytes') else None
    if offset and expected and offset == expected:
        validate(partial, row)
        partial.replace(final)
        return
    if expected and offset > expected:
        raise ValueError('Partial file exceeds catalog length; inspect it before retrying')
    with session.get(row['url'], headers={'Range': f'bytes={offset}-'} if offset else {}, stream=True, timeout=(30, 120)) as response:
        if response.status_code in (401, 403) or urlparse(response.url).hostname == 'urs.earthdata.nasa.gov':
            raise RuntimeError('Earthdata authentication/authorization failed; check local netrc and EDL application access')
        response.raise_for_status()
        if 'text/html' in response.headers.get('Content-Type', ''):
            raise RuntimeError('Received an HTML login page instead of an HDF5 product')
        append = response.status_code == 206
        if append and not response.headers.get('Content-Range', '').startswith(f'bytes {offset}-'):
            raise ValueError('Server returned an unexpected byte range')
        with partial.open('ab' if append else 'wb') as f:
            for chunk in response.iter_content(8 * 1024 * 1024):
                f.write(chunk)
    validate(partial, row)
    partial.replace(final)
    (target / (name + '.provenance.json')).write_text(json.dumps(row, indent=2), encoding='utf-8')
    print(f'Verified: {name}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--city', default='semarang')
    parser.add_argument('--limit', type=int, default=1, help='Inspect one product before downloading the full chain')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    manifest = ROOT / 'data/manifests' / f'{args.city}_selected.csv'
    if not manifest.is_file():
        parser.error('Run 01_search.py for this city first')
    if args.limit < 1:
        parser.error('--limit must be positive')
    with manifest.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))[:args.limit]
    if not rows:
        parser.error('No eligible chain in this manifest')
    print(f'{len(rows)} product(s); advertised size {sum(int(r["bytes"] or 0) for r in rows):,} bytes')
    if args.dry_run:
        for row in rows:
            print(row['scene'])
        return
    credentials_file = Path.home() / '.netrc'
    if not credentials_file.is_file():
        parser.exit(2, 'BLOCKED: configure ~/.netrc locally for urs.earthdata.nasa.gov; do not paste credentials into chat.\n')
    try:
        auth = netrc.netrc(str(credentials_file)).authenticators('urs.earthdata.nasa.gov')
    except (netrc.NetrcParseError, OSError):
        parser.exit(2, 'BLOCKED: local .netrc could not be parsed.\n')
    if not auth:
        parser.exit(2, 'BLOCKED: .netrc lacks the urs.earthdata.nasa.gov entry.\n')
    try:
        session = asf.ASFSession().auth_with_creds(auth[0], auth[2])
    except Exception:
        parser.exit(2, 'BLOCKED: Earthdata authentication failed. Check local credentials and application access.\n')
    target = ROOT / 'data/raw' / args.city
    target.mkdir(parents=True, exist_ok=True)
    for row in rows:
        try:
            download(session, row, target)
        except Exception as exc:
            # HTTP exception text may contain redirected signed URLs; do not log it.
            parser.exit(2, f'Download stopped ({type(exc).__name__}); partial file retained for retry.\n')


if __name__ == '__main__':
    main()
