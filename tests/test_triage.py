"""Boundary and interaction checks for the extracted Notebook 28 rule."""

import math
import unittest

from brain_ct_triage import triage_class


def predict(edh=0, sdh=0, iph=0, sah=0, ivh=0, fracture=0, mls=0):
    return triage_class(edh, sdh, iph, sah, ivh, fracture, mls)


class RuleBoundaryTests(unittest.TestCase):
    def test_normal_and_single_low_risk_findings(self):
        self.assertEqual(predict(), 0)
        self.assertEqual(predict(sah=0.1), 1)
        self.assertEqual(predict(fracture=0.5), 1)
        self.assertEqual(predict(mls=3), 1)
        self.assertEqual(predict(mls=5), 1)

    def test_volume_thresholds(self):
        self.assertEqual(predict(edh=29.99), 1)
        self.assertEqual(predict(edh=30), 2)
        self.assertEqual(predict(sdh=70), 2)
        self.assertEqual(predict(iph=70), 2)
        self.assertEqual(predict(sah=30, ivh=30), 2)

    def test_interaction_thresholds(self):
        self.assertEqual(predict(sah=0.1, mls=5), 2)
        self.assertEqual(predict(fracture=0.5, mls=5), 2)
        self.assertEqual(predict(sah=40, mls=3), 2)
        self.assertEqual(predict(sah=15, fracture=0.5), 2)
        self.assertEqual(predict(sah=14.99, fracture=0.5), 1)

    def test_negative_and_invalid_inputs(self):
        self.assertEqual(predict(edh=-5), 0)
        with self.assertRaises(ValueError):
            predict(sdh=math.nan)
        with self.assertRaises(ValueError):
            predict(fracture=math.inf)


if __name__ == "__main__":
    unittest.main()
