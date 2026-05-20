#!/usr/bin/env python3
"""Store PDW measurements with a synthesized flight track in DuckDB spatial,
then export GeoParquet + a folium map of pulse power along the track.

Idea: each pulse has a TOA. We interpolate the platform position (lat/lon/alt)
at that TOA from a flight track, attach it to the pulse, and store as POINT
geometry. Pulse power becomes the color on the map. This is the same pattern
described in the MotherDuck "spatial for beginners" post — just with radar
PDWs instead of taxi rides.

Usage:
    python3 pdw_to_duckdb.py --pdw pdw.hdf5 --db radar.duckdb --map track.html
"""
from __future__ import annotations

import argparse
import os

import duckdb
import h5py
import numpy as np


def load_pdw_rows(path: str) -> list[tuple]:
    with h5py.File(path, "r") as f:
        toa_c = f["toa_course"][:].astype(np.float64)
        toa_f = f["toa_fine"][:].astype(np.float64)
        pw = f["pulse_width_secs"][:].astype(np.float64)
        pp = f["pulse_power"][:].astype(np.float64)
        np_ = f["noise_power"][:].astype(np.float64)
        fs = f["freq_start"][:].astype(np.float64)
    toa = toa_c + toa_f
    return list(zip(toa, pw, pp, np_, fs))


def synth_flight_track(toa: np.ndarray) -> np.ndarray:
    """Great-circle-ish leg from Stockholm Arlanda → Gothenburg Landvetter,
    constant ground speed, FL350. Returns (lat, lon, alt_m) per TOA sample."""
    t0, t1 = toa.min(), toa.max()
    span = max(t1 - t0, 1e-9)
    frac = (toa - t0) / span
    lat0, lon0 = 59.6519, 17.9186   # ARN
    lat1, lon1 = 57.6685, 12.2950   # GOT
    lat = lat0 + (lat1 - lat0) * frac
    lon = lon0 + (lon1 - lon0) * frac
    alt = np.full_like(frac, 10668.0)  # FL350 ≈ 10 668 m
    return np.stack([lat, lon, alt], axis=1)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pdw", required=True)
    p.add_argument("--db", default="radar.duckdb")
    p.add_argument("--parquet", default="pdw_geo.parquet")
    p.add_argument("--map", default="track.html")
    args = p.parse_args()

    rows = load_pdw_rows(args.pdw)
    toa = np.array([r[0] for r in rows])
    track = synth_flight_track(toa)

    enriched = [
        (float(toa_), float(pw), float(pp), float(npw), float(fs),
         float(track[i, 0]), float(track[i, 1]), float(track[i, 2]))
        for i, (toa_, pw, pp, npw, fs) in enumerate(rows)
    ]

    if os.path.exists(args.db):
        os.remove(args.db)
    con = duckdb.connect(args.db)
    con.execute("INSTALL spatial; LOAD spatial;")

    con.execute("""
        CREATE TABLE pdw_geo (
            toa DOUBLE,
            pulse_width_s DOUBLE,
            pulse_power_db DOUBLE,
            noise_power_db DOUBLE,
            freq_start_hz DOUBLE,
            lat DOUBLE,
            lon DOUBLE,
            alt_m DOUBLE,
            geom GEOMETRY
        );
    """)
    con.executemany(
        """INSERT INTO pdw_geo VALUES
           (?, ?, ?, ?, ?, ?, ?, ?, ST_Point(?, ?))""",
        [(*row, row[6], row[5]) for row in enriched],   # ST_Point(lon, lat)
    )

    # quick spatial query: pulses within 50 km of midpoint
    mid_lat = float(np.mean([r[5] for r in enriched]))
    mid_lon = float(np.mean([r[6] for r in enriched]))
    res = con.execute(f"""
        SELECT count(*) AS n_pulses,
               avg(pulse_power_db) AS avg_power,
               max(pulse_power_db) AS peak_power
        FROM pdw_geo
        WHERE ST_Distance_Sphere(geom, ST_Point({mid_lon}, {mid_lat})) < 50000;
    """).fetchone()
    print(f"within 50 km of track midpoint: n={res[0]}, avg={res[1]:.2f} dB, peak={res[2]:.2f} dB")

    # export GeoParquet (works with kepler.gl, QGIS, geopandas)
    con.execute(f"""
        COPY (SELECT * EXCLUDE geom, ST_AsWKB(geom) AS geom FROM pdw_geo)
        TO '{args.parquet}' (FORMAT PARQUET);
    """)
    print(f"wrote {args.parquet}")

    # folium map colored by pulse power
    try:
        import folium
        from folium.plugins import HeatMap

        m = folium.Map(location=[mid_lat, mid_lon], zoom_start=7, tiles="cartodbpositron")
        # flight track
        folium.PolyLine([(r[5], r[6]) for r in enriched], color="black", weight=1, opacity=0.4).add_to(m)
        # heat-weighted by pulse power (shift to non-negative)
        ppmin = min(r[2] for r in enriched)
        HeatMap(
            [(r[5], r[6], r[2] - ppmin + 1.0) for r in enriched],
            radius=8, blur=12, min_opacity=0.3,
        ).add_to(m)
        m.save(args.map)
        print(f"wrote {args.map}")
    except ImportError:
        print("folium not installed — skipped map export")


if __name__ == "__main__":
    main()
