#!/bin/bash
set -u
pid=$(cat /mnt/data/engine-performance/evidence/test.pid)
while [ -r /proc/$pid/stat ] && [ "$(awk '{print $3}' /proc/$pid/stat)" != Z ]; do sleep 2; done
exec env PYTHONDONTWRITEBYTECODE=1 python -u /mnt/data/engine-performance/harness/measure_operations.py --repo /mnt/data/engine-performance/benchmark-checkout --output /mnt/data/engine-performance/evidence/operations --samples 3 --profile
