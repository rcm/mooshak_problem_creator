#!/usr/bin/python3
import sys
assert sys.version_info.major == 3 and sys.version_info.minor >= 8, "This script needs at least version 3.8"
import moopec_parser
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            print(f'Parsing {file}')

            moopec_parser.parse(file)
