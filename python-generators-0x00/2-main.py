#!/usr/bin/python3

import sys

processing = __import__('1-batch_processing')

try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()
except KeyboardInterrupt:
    sys.stderr.close()
    sys.exit(0)
except Exception as e:
    sys.stderr.write(f"An error occurred: {e}\n")
    sys.stderr.close()
    sys.exit(1)