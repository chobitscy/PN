#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decimal

if __name__ == '__main__':
    print(decimal.Decimal("103228599039.125").quantize(decimal.Decimal("0.00")))
