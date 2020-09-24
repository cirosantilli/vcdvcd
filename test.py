#!/usr/bin/env python

import unittest

from vcdvcd import VCDVCD

class Test(unittest.TestCase):
    def test_data(self):
        vcd = VCDVCD('counter_tb.vcd')
        signal = vcd['counter_tb.out[1:0]']
        self.assertEqual(
            signal.tv[:6],
            [
                ( 0,  'x'),
                ( 2,  '0'),
                ( 6,  '1'),
                ( 8, '10'),
                (10, '11'),
                (12,  '0'),
            ]
        )

        # Random access.
        self.assertEqual(signal[0], 'x')
        self.assertEqual(signal[1], 'x')
        self.assertEqual(signal[2], '0')
        self.assertEqual(signal[3], '0')
        self.assertEqual(signal[5], '0')
        self.assertEqual(signal[6], '1')
        self.assertEqual(signal[7], '1')
        self.assertEqual(signal[8], '10')

if __name__ == '__main__':
    unittest.main()
