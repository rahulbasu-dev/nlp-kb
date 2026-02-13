#!/usr/bin/env python
"""Test if examples produce output"""
from classroom_examples import example_1_basic_usage
import io
from contextlib import redirect_stdout

f = io.StringIO()
with redirect_stdout(f):
    example_1_basic_usage()
output = f.getvalue()

print("Output length:", len(output))
print("Has output:", len(output) > 0)
if output:
    print("\n" + "="*70)
    print("FIRST 500 CHARS OF OUTPUT:")
    print("="*70)
    print(output[:500])
