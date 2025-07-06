#! /usr/bin/env python3

import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate


try:
    for page in lazy_paginator(5):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()
except KeyboardInterrupt:
    sys.stderr.close()
    sys.exit(0)
except Exception as e:
    sys.stderr.write(f"An error occurred: {e}\n")
    sys.stderr.close()
    sys.exit(1)