#!/usr/bin/env python

from __future__ import print_function

import sys
from pprint import PrettyPrinter

from vcdvcd import VCDVCD

if (len(sys.argv) > 1):
    vcd_path = sys.argv[1]
else:
    vcd_path = 'counter_tb.vcd'
pp = PrettyPrinter()

print('# get_data()')
vcd = VCDVCD(vcd_path)
pp.pprint(vcd.get_data())
print()

print('# get_data(only_sigs=True)')
vcd = VCDVCD(vcd_path, only_sigs=True)
PrettyPrinter().pprint(vcd.get_data())
print()

print('# get_signals()')
vcd = VCDVCD(vcd_path, only_sigs=True)
pp.pprint(vcd.get_signals())
print()

print('# __init__(signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = vcd_only_sigs.get_signals()
len_signals = len(signals)
if len_signals > 0:
    print('## 0')
    vcd_signal_0 = VCDVCD(vcd_path, signals=signals[0:1])
    pp.pprint(vcd_signal_0.get_data())
    print()
    if len_signals > 1:
        print('## 1')
        vcd_signal_1 = VCDVCD(vcd_path, signals=signals[1:2])
        pp.pprint(vcd_signal_1.get_data())
        print()
        print('## 01')
        vcd_signal_01 = VCDVCD(vcd_path, signals=signals[0:2])
        pp.pprint(vcd_signal_01.get_data())
        print()
print()

print('# __init__(print_dumps=True)')
VCDVCD(vcd_path, print_dumps=True)
print()

print('# __init__(print_dumps=True, store_tvs=False)')
vcd = VCDVCD(vcd_path, print_dumps=True, store_tvs=False)
PrettyPrinter().pprint(vcd.get_data())
print()

print('# __init__(print_dumps=True, signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.get_signals())
VCDVCD(vcd_path, signals=signals[0:2], print_dumps=True, store_tvs=False)
print()
print('## reverse')
VCDVCD(vcd_path, signals=signals[1::-1], print_dumps=True, store_tvs=False)
print()
print('## repeat')
VCDVCD(vcd_path, signals=(signals[0:1] * 2), print_dumps=True, store_tvs=False)
print()

print('# __init__(print_deltas=True)')
VCDVCD(vcd_path, print_deltas=True, store_tvs=False)
print()

print('# __init__(print_deltas=True, signals=)')
vcd_only_sigs = VCDVCD(vcd_path, only_sigs=True)
signals = sorted(vcd_only_sigs.get_signals())
if signals:
    VCDVCD(vcd_path, signals=signals[0:1], print_deltas=True, store_tvs=False)
print()
