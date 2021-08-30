#!/usr/bin/env python3

from __future__ import print_function

import sys
from pprint import PrettyPrinter

import vcdvcd
from vcdvcd import VCDVCD

if (len(sys.argv) > 1):
    vcd_path = sys.argv[1]
else:
    vcd_path = 'counter_tb.vcd'
pp = PrettyPrinter()

print('# data')
vcd = VCDVCD(vcd_path)
pp.pprint(vcd.data)
print()

print('# references_to_ids()')
pp.pprint(vcd.references_to_ids)
print()

print('# timescale')
pp.pprint(vcd.timescale)
print()

print('# signals')
pp.pprint(vcd.signals)
print()

print('# __init__(only_sigs=True)')
vcd = VCDVCD(vcd_path, only_sigs=True)
pp.pprint(vcd.data)
print()

print('# __init__(signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = vcd_only_sigs.signals
len_signals = len(signals)
if len_signals > 0:
    print('## 0')
    vcd_signal_0 = VCDVCD(vcd_path, signals=signals[0:1])
    pp.pprint(vcd_signal_0.data)
    print()
    if len_signals > 1:
        print('## 1')
        vcd_signal_1 = VCDVCD(vcd_path, signals=signals[1:2])
        pp.pprint(vcd_signal_1.data)
        print()
        print('## 01')
        vcd_signal_01 = VCDVCD(vcd_path, signals=signals[0:2])
        pp.pprint(vcd_signal_01.data)
        print()
print()

print('# __init__(callbacks=vcdvcd.PrintDeltasStreamParserCallbacks())')
VCDVCD(vcd_path, callbacks=vcdvcd.PrintDeltasStreamParserCallbacks())
print()

print('# __init__(callbacks=vcdvcd.PrintDeltasStreamParserCallbacks(), store_tvs=False)')
vcd = VCDVCD(vcd_path, callbacks=vcdvcd.PrintDeltasStreamParserCallbacks(), store_tvs=False)
pp.pprint(vcd.data)
print()

print('# __init__(callbacks=vcdvcd.PrintDeltasStreamParserCallbacks(), signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.signals)
VCDVCD(vcd_path, signals=signals[0:2], callbacks=vcdvcd.PrintDeltasStreamParserCallbacks(), store_tvs=False)
print()
print('## reverse')
VCDVCD(vcd_path, signals=signals[1::-1], callbacks=vcdvcd.PrintDeltasStreamParserCallbacks(), store_tvs=False)
print()
print('## repeat')
VCDVCD(vcd_path, signals=(signals[0:1] * 2), callbacks=vcdvcd.PrintDeltasStreamParserCallbacks(), store_tvs=False)
print()

print('# __init__(store_tvs=False, callbacks=vcdvcd.PrintDeltasStreamParserCallbacks())')
VCDVCD(
    vcd_path,
    store_tvs=False,
    callbacks=vcdvcd.PrintDeltasStreamParserCallbacks()
)
print()

print('# __init__(signals=, callbacks=vcdvcd.PrintDeltasStreamParserCallbacks())')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.signals)
if signals:
    VCDVCD(
        vcd_path,
        signals=signals[0:1],
        store_tvs=False,
        callbacks=vcdvcd.PrintDeltasStreamParserCallbacks()
    )
print()

print('# __init__(value_callback=True)')
class MyStreamParserCallbacks(vcdvcd.StreamParserCallbacks):
    def value(
        self,
        vcd,
        time,
        value,
        identifier_code,
        cur_sig_vals,
    ):
        print('{} {} {}'.format(time, value, identifier_code))
vcd = VCDVCD(vcd_path, callbacks=MyStreamParserCallbacks(), store_tvs=False)
print()
