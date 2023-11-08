#!/usr/bin/env python3

import unittest
import re

from vcdvcd import VCDVCD
import vcdvcd

class Test(unittest.TestCase):
    SMALL_CLOCK_VCD = '''$var reg 1 " clock $end
$enddefinitions $end
#0
$dumpvars
0"
$end
#1
1"
#2
0"
'''

    SINGLE_LINE_VALUE_CHANGE_VCD = '''$timescale 1 us $end
$scope module X $end
$var wire 1 ! D0 $end
$var wire 1 " D1 $end
$upscope $end
$enddefinitions $end

#0  0! 1"
#10  1!
#15  0"
#20  1"
#25  0"
#30  1"
#35  0"
#40
'''

    EXTRA_METADATA_VCD = '''$date
	Created November 08, 2023
$end
$version
	Dumped by version v1.1
$end
$timescale 6666ps $end
$scope module X $end
$var wire 1 ! D0 $end
$var wire 1 " D1 $end
$enddefinitions $end

$dumpvars
x!
x"
$end

#10  1!
#15  0"
#20  1"
'''

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
        self.assertEqual(signal[0], 'x')
        self.assertEqual(signal[1], 'x')
        self.assertEqual(signal[2], '0')
        self.assertEqual(signal[3], '0')
        self.assertEqual(signal[6], '1')
        self.assertEqual(signal[7], '1')
        self.assertEqual(signal[24], '10')
        self.assertEqual(signal[25], '10')

    def test_slice(self):
        vcd = VCDVCD('counter_tb.vcd')
        signal = vcd['counter_tb.out[1:0]']
        for t, signal_d in enumerate(signal[0:30]):
            if t < 2:
                self.assertEqual(signal_d, 'x')
            elif t < 6:
                self.assertEqual(signal_d, '0')
            else:
                self.assertEqual(int(signal_d,2), ((t - 4)//2)%4)

    def test_REs(self):
        vcd = VCDVCD('counter_tb.vcd')
        signal = vcd[re.compile('counter_tb\.out.*')]
        for t, signal_d in enumerate(signal[0:30]):
            if t < 2:
                self.assertEqual(signal_d, 'x')
            elif t < 6:
                self.assertEqual(signal_d, '0')
            else:
                self.assertEqual(int(signal_d,2), ((t - 4)//2)%4)

        signals = vcd[re.compile('out.*')]
        self.assertEqual(len(signals),2)

    def testContains(self):
        vcd = VCDVCD('counter_tb.vcd', store_scopes=True)
        scope_counter_tb = vcd[re.compile('counter_tb$')]

        for element in ['clock','enable','reset','out[1:0]','top']:
            self.assertTrue(     element in scope_counter_tb)


    def test_scopes(self):
        vcd = VCDVCD('counter_tb.vcd', store_scopes=True)
        scope_counter_tb = vcd[re.compile('counter_tb$')]

        self.assertTrue(isinstance(scope_counter_tb, vcdvcd.Scope))
        self.assertIsNotNone(scope_counter_tb['clock'])
        self.assertIsNotNone(scope_counter_tb['enable'])
        self.assertIsNotNone(scope_counter_tb['reset'])
        self.assertIsNotNone(scope_counter_tb['out[1:0]'])
        self.assertIsNotNone(scope_counter_tb['top'])

        self.assertTrue(isinstance(scope_counter_tb['clock'], vcdvcd.Signal))
        self.assertTrue(isinstance(scope_counter_tb['enable'], vcdvcd.Signal))
        self.assertTrue(isinstance(scope_counter_tb['reset'], vcdvcd.Signal))
        self.assertTrue(isinstance(scope_counter_tb['out[1:0]'], vcdvcd.Signal))
        self.assertTrue(isinstance(scope_counter_tb['top'], vcdvcd.Scope ))

        signal  = scope_counter_tb[re.compile('out.*')]
        self.assertTrue(scope_counter_tb['out[1:0]'] is signal)

        for t, signal_d in enumerate(signal[0:30]):
            if t < 2:
                self.assertEqual(signal_d, 'x')
            elif t < 6:
                self.assertEqual(signal_d, '0')
            else:
                self.assertEqual(int(signal_d,2), ((t - 4)//2)%4)

        scope_top_module = scope_counter_tb[re.compile('top$')]
        self.assertTrue(isinstance(scope_top_module, vcdvcd.Scope))
        signal  = scope_counter_tb[re.compile('top$')][re.compile('out.*')]
        self.assertTrue(signal is scope_top_module['out[1:0]'])

        self.assertIsNotNone(scope_top_module['clock'])
        self.assertIsNotNone(scope_top_module['enable'])
        self.assertIsNotNone(scope_top_module['reset'])
        self.assertIsNotNone(scope_top_module['out[1:0]'])

        self.assertTrue(isinstance(scope_top_module['clock'], vcdvcd.Signal))
        self.assertTrue(isinstance(scope_top_module['enable'], vcdvcd.Signal))
        self.assertTrue(isinstance(scope_top_module['reset'], vcdvcd.Signal))
        self.assertTrue(isinstance(scope_top_module['out[1:0]'], vcdvcd.Signal))

        for t, signal_d in enumerate(signal[0:30]):
            if t < 2:
                self.assertEqual(signal_d, 'x')
            elif t < 6:
                self.assertEqual(signal_d, '0')
            else:
                self.assertEqual(int(signal_d,2), ((t - 4)//2)%4)

    def test_toplevel_signal(self):
        vcd = VCDVCD(vcd_string=self.SMALL_CLOCK_VCD)
        signal = vcd['clock']
        self.assertEqual(signal[0], '0')
        self.assertEqual(signal[1], '1')
        self.assertEqual(signal[2], '0')
        self.assertEqual(signal[3], '0')

    def test_nonexistent_signal(self):
        vcd = VCDVCD(vcd_string=self.SMALL_CLOCK_VCD)
        with self.assertRaises(KeyError):
            vcd['non_existent_signal']

    def test_single_line_value_change(self):
        """
        Tests correct parsing when time stamp and value change are on the same
        line, separated by white space
        """
        vcd = VCDVCD(vcd_string=self.SINGLE_LINE_VALUE_CHANGE_VCD)
        D0 = vcd['X.D0']
        D1 = vcd['X.D1']
        self.assertEqual(D0[0], '0')
        self.assertEqual(D0[10], '1')

        self.assertEqual(D1[0], '1')
        self.assertEqual(D1[15], '0')
        self.assertEqual(D1[20], '1')
        self.assertEqual(D1[25], '0')
        self.assertEqual(D1[30], '1')
        self.assertEqual(D1[35], '0')

    def test_simple_timescale_values(self):
        from decimal import Decimal

        # simple timescale
        vcd = VCDVCD(vcd_string=self.SINGLE_LINE_VALUE_CHANGE_VCD)
        self.assertEqual(vcd.timescale["timescale"], Decimal('0.000001'))
        self.assertEqual(vcd.timescale["magnitude"], 1)
        self.assertEqual(vcd.timescale["unit"], "us")
        self.assertEqual(vcd.timescale["factor"], Decimal('0.000001'))

        # No timescale
        vcd = VCDVCD(vcd_string=self.SMALL_CLOCK_VCD)
        self.assertEqual(len(vcd.timescale), 0)

        # Odd timescale based on 150MHz
        vcd = VCDVCD(vcd_string=self.EXTRA_METADATA_VCD)
        self.assertEqual(vcd.timescale["timescale"], Decimal('6.666E-9'))
        self.assertEqual(vcd.timescale["magnitude"], 6666)
        self.assertEqual(vcd.timescale["unit"], "ps")
        self.assertEqual(vcd.timescale["factor"], Decimal('1E-12'))
        # but its badly rounded
        self.assertAlmostEqual(Decimal('6.666E-9') * Decimal('150E6'), 1, places=3)

if __name__ == '__main__':
    unittest.main()
