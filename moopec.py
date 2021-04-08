#!/usr/bin/python3
import moopec_parser
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            print(f'Parsing {file}')

            moopec_parser.parse(file)
