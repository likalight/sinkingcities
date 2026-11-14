"""Synthetic catalog fixtures only; never exported as observations."""
import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('catalog', Path(__file__).resolve().parents[1]/'pipeline/utils/catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


def row(start, end, **extra):
    return dict(reference_date=start, secondary_date=end, maturity='PROVISIONAL', track=1,
                frame=1, direction='ASCENDING', polarization='HH', bandwidth='40', crid='P05023',
                processing_date=extra.get('processing_date', '2026-10-01'), aoi_fraction=extra.get('aoi_fraction', 1))


def test_never_bridge_gap():
    rows = [row('2026-06-01','2026-06-13'), row('2026-07-01','2026-07-13'), row('2026-07-13','2026-07-25')]
    chain = catalog.longest_chain(rows)
    assert len(chain) == 2
    assert chain[0]['reference_date'] == '2026-07-01'


def test_reject_non_12_day_edges():
    assert catalog.longest_chain([row('2026-06-01','2026-06-25')]) == []


def test_duplicate_pairs_not_inflated():
    rows = [row('2026-06-01','2026-06-13', processing_date=d) for d in ('2026-10-01','2026-10-02')]
    result = catalog.groups(rows)[0]
    assert len(result['rows']) == len(result['chain']) == 1
    assert result['chain'][0]['processing_date'] == '2026-10-02'


def test_partial_footprint_not_full_coverage():
    assert catalog.groups([row('2026-06-01','2026-06-13',aoi_fraction=.7)])[0]['chain'] == []


def test_metadata_dates_not_catalog_span():
    assert catalog.pair_dates('GUNW_20260601T000000_20260601T000010_20260613T000001_20260613T000011') == ('2026-06-01','2026-06-13')


def test_invalid_name_fails():
    with pytest.raises(ValueError):
        catalog.pair_dates('GCOV_20260601T000000_20260601T000010')
