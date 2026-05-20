#!/usr/bin/env python3
"""Visualize a gr-pdw HDF5 file and optionally do a CWT on the raw IQ.

Produces:
  - pdw_strip.png    : pulse width, power, freq vs. TOA (strip charts)
  - pdw_pri.png      : PRI histogram (pulse-to-pulse interval)
  - pdw_cwt.png      : Morlet CWT scalogram of a single pulse (if --iq given)

Usage:
    python3 visualize_pdw.py --pdw pdw.hdf5 --iq iq.cf32 --samp-rate 1e6
"""
from __future__ import annotations

import argparse
import os

import h5py
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pywt


def load_pdw(path: str) -> dict:
    with h5py.File(path, "r") as f:
        d = {k: f[k][:] for k in f.keys()}
        d["_attrs"] = dict(f.attrs)
    # combine course+fine TOA into a single float-seconds axis if available
    if "toa_course" in d and "toa_fine" in d:
        d["toa"] = d["toa_course"].astype(np.float64) + d["toa_fine"].astype(np.float64)
    elif "toa" not in d:
        d["toa"] = np.arange(len(next(iter(d.values()))), dtype=np.float64)
    return d


def plot_strip(d: dict, out: str) -> None:
    toa = d["toa"]
    pw = d.get("pulse_width_secs", d.get("pulse_width_samps")) * 1e6  # microseconds
    pp = d.get("pulse_power")
    pf = d.get("freq_start")

    fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
    axes[0].plot(toa, pw, ".", ms=4, color="#1f77b4")
    axes[0].set_ylabel("PW (µs)")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(toa, pp, ".", ms=4, color="#d62728")
    axes[1].set_ylabel("Pulse power (dB)")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(toa, pf / 1e3, ".", ms=4, color="#2ca02c")
    axes[2].set_ylabel("Freq start (kHz)")
    axes[2].set_xlabel("TOA (s)")
    axes[2].grid(True, alpha=0.3)

    fig.suptitle("PDW strip chart")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def plot_pri(d: dict, out: str) -> None:
    toa = np.sort(d["toa"])
    pri = np.diff(toa) * 1e3  # ms
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(pri, bins=40, color="#9467bd", edgecolor="black")
    ax.set_xlabel("PRI (ms)")
    ax.set_ylabel("count")
    ax.set_title(f"PRI histogram — median {np.median(pri):.3f} ms, n={len(pri)}")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def plot_cwt(iq_path: str, samp_rate: float, out: str, max_samples: int = 4096) -> None:
    iq = np.fromfile(iq_path, dtype=np.complex64)
    if iq.size == 0:
        print(f"warning: {iq_path} empty, skipping CWT")
        return

    env = np.abs(iq)
    # find first pulse by simple thresholding
    thresh = env.max() * 0.3
    above = np.where(env > thresh)[0]
    if above.size == 0:
        center = len(iq) // 2
    else:
        center = above[0] + (above[-1] - above[0]) // 2
    half = max_samples // 2
    lo, hi = max(0, center - half), min(len(iq), center + half)
    snippet = iq[lo:hi]
    t = np.arange(snippet.size) / samp_rate * 1e6  # µs

    scales = np.geomspace(2, 128, num=96)
    coeffs, freqs = pywt.cwt(snippet, scales, "cmor1.5-1.0", sampling_period=1.0 / samp_rate)
    power = np.abs(coeffs)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 3]})
    ax1.plot(t, np.abs(snippet), color="#1f77b4")
    ax1.set_ylabel("|IQ|")
    ax1.grid(True, alpha=0.3)
    ax1.set_title("Pulse envelope and Morlet CWT scalogram")

    im = ax2.imshow(
        power,
        aspect="auto",
        extent=(t[0], t[-1], freqs[-1] / 1e3, freqs[0] / 1e3),
        cmap="magma",
    )
    ax2.set_ylabel("Freq (kHz)")
    ax2.set_xlabel("Time (µs)")
    fig.colorbar(im, ax=ax2, label="|CWT|", pad=0.02)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pdw", required=True)
    p.add_argument("--iq", default=None)
    p.add_argument("--samp-rate", type=float, default=1e6)
    p.add_argument("--outdir", default=".")
    args = p.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    d = load_pdw(args.pdw)
    plot_strip(d, os.path.join(args.outdir, "pdw_strip.png"))
    plot_pri(d, os.path.join(args.outdir, "pdw_pri.png"))
    if args.iq and os.path.exists(args.iq):
        plot_cwt(args.iq, args.samp_rate, os.path.join(args.outdir, "pdw_cwt.png"))
    print(f"wrote plots to {args.outdir}")


if __name__ == "__main__":
    main()
