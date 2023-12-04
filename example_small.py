#!/usr/bin/env python

from vcdvcd import VCDVCD

# Do the parsing.
vcd = VCDVCD('counter_tb.vcd')

# List all human readable signal names.
print(vcd.references_to_ids.keys())

# View all signal data.
print(vcd.data)

# Get a signal by human readable name.
signal = vcd['counter_tb.top.out[1:0]']

# tv is a list of Time/Value delta pairs for this signal.
tv = signal.tv
assert(tv[0] == (0, 'x'))
assert(tv[1] == (2, '0'))
assert(tv[2] == (6, '1'))
assert(tv[3] == (8, '10'))
assert(tv[4] == (10, '11'))
assert(tv[5] == (12, '0'))

# Random access value of the signal at a given time.
# Note how it works for times between deltas as well.
assert(signal[0] == 'x')
assert(signal[1] == 'x')
assert(signal[2] == '0')
assert(signal[3] == '0')
assert(signal[4] == '0')
assert(signal[5] == '0')
assert(signal[6] == '1')
assert(signal[7] == '1')
assert(signal[8] == '10')
assert(signal[9] == '10')
assert(signal[10] == '11')
assert(signal[11] == '11')
assert(signal[12] == '0')
assert(signal[13] == '0')
