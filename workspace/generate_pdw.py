#!/usr/bin/env python3
"""Headless gr-pdw radar pulse generator.

Runs a simulated radar pulse train through the gr-pdw detect/extract/log
pipeline and writes both an HDF5 PDW file and the raw IQ stream so the
visualizer can do a CWT on a single pulse.

Run inside the gr-pdw docker container:
    python3 generate_pdw.py --duration 0.05 --out pdw.hdf5 --iq iq.cf32
"""
from __future__ import annotations

import argparse
import time

from gnuradio import analog, blocks, gr
import pdw


class PulseTrain(gr.top_block):
    def __init__(
        self,
        samp_rate: float,
        pw_us: float,
        pri_s: float,
        pulse_freq: float,
        amp: float,
        duration_s: float,
        hdf5_path: str,
        iq_path: str,
        threshold: float = 0.1,
    ) -> None:
        super().__init__("Headless PDW Generator")

        self._duration_s = duration_s

        # Square-wave gate -> pulse envelope at baseband.
        # GR_SQR_WAVE alternates 0..amp at frequency 1/PRI; threshold_ff
        # snaps it to {0,1} for use as an envelope multiplier.
        sq = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE, 1.0 / pri_s, amp, 0)
        gate_thresh = blocks.threshold_ff(0.5, 0.5, 0)
        gate_c = blocks.float_to_complex(1)

        # CW carrier offset to simulate non-zero pulse_freq
        carrier = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, pulse_freq, 1.0, 0)
        mix = blocks.multiply_cc(1)

        # Additive complex Gaussian noise so detection threshold is meaningful
        noise = analog.noise_source_c(analog.GR_GAUSSIAN, 0.01, 0)
        add = blocks.add_cc(1)
        throttle = blocks.throttle(gr.sizeof_gr_complex, samp_rate)

        # gr-pdw chain.
        # pulse_detect has 1 input (IQ) and 2 outputs: port 0 = IQ passthrough,
        # port 1 = detection flag stream (for plotting). pulse_extract is a
        # stream sink whose PDWs come out via a *message* port ('pulse_data');
        # pdw_to_file consumes that message via its 'pdw_in' port.
        detect = pdw.pulse_detect(threshold, samp_rate)
        extract = pdw.pulse_extract(samp_rate)
        log = pdw.pdw_to_file(hdf5_path, samp_rate, 1024, True)
        null_flag = blocks.null_sink(gr.sizeof_float)

        iq_sink = blocks.file_sink(gr.sizeof_gr_complex, iq_path, False)
        iq_sink.set_unbuffered(True)

        # gate -> envelope (real -> complex with imag=0 via single-port f2c)
        self.connect(sq, gate_thresh, gate_c)
        # envelope * carrier
        self.connect(gate_c, (mix, 0))
        self.connect(carrier, (mix, 1))
        # add noise, throttle so sources don't free-run faster than real time
        self.connect(mix, (add, 0))
        self.connect(noise, (add, 1))
        self.connect(add, throttle)
        # branch: detect -> extract via streams; PDWs flow via msg port
        self.connect(throttle, detect)
        self.connect((detect, 0), extract)
        self.connect((detect, 1), null_flag)
        self.msg_connect((extract, 'pulse_data'), (log, 'pdw_in'))
        # raw IQ snapshot for the CWT plot
        self.connect(throttle, iq_sink)

    def run_for(self) -> None:
        """Run the flowgraph for duration_s wall-clock seconds, then stop."""
        print("starting...", flush=True)
        self.start()
        print(f"running for {self._duration_s}s...", flush=True)
        time.sleep(self._duration_s)
        print("stopping...", flush=True)
        self.stop()
        print("waiting...", flush=True)
        self.wait()
        print("done.", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--samp-rate", type=float, default=1e6)
    p.add_argument("--pw-us", type=float, default=5.0, help="pulse width, microseconds")
    p.add_argument("--pri", type=float, default=1e-3, help="pulse repetition interval, seconds")
    p.add_argument("--pulse-freq", type=float, default=50e3, help="baseband freq offset, Hz")
    p.add_argument("--amp", type=float, default=1.0)
    p.add_argument("--duration", type=float, default=0.05, help="capture length, seconds")
    p.add_argument("--out", default="pdw.hdf5")
    p.add_argument("--iq", default="iq.cf32")
    args = p.parse_args()

    tb = PulseTrain(
        samp_rate=args.samp_rate,
        pw_us=args.pw_us,
        pri_s=args.pri,
        pulse_freq=args.pulse_freq,
        amp=args.amp,
        duration_s=args.duration,
        hdf5_path=args.out,
        iq_path=args.iq,
    )
    tb.run_for()
    print(f"wrote {args.out} and {args.iq}")


if __name__ == "__main__":
    main()
