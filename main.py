import argparse
import sys
from solutions.solutions import solutions_dict
from utils.utils import display_result

def main():
    parser = argparse.ArgumentParser(description='Run Pandas exercises')
    parser.add_argument('problem', type=int, help='Problem number to run')
    parser.add_argument('-s', '--show-desc', action='store_true', help='Show problem description')
    parser.add_argument('-a', '--all', action='store_true', help='Run all problems')
    parser.add_argument('-l', '--list', action='store_true', help='List all available problems')
    
    args = parser.parse_args()

    if args.list:
        for num, (desc, _) in solutions_dict.items():
            print(f'Problem {num}: {desc[:60]}...')
        sys.exit(0)
    
    if args.all:
        for num, (desc, func) in solutions_dict.items():
            print(f'\n{"="*50}')
            print(f'Problem {num}: {desc[:60]}...')
            display_result(func())
    else:
        if args.problem in solutions_dict:
            desc, func = solutions_dict[args.problem]
            if args.show_desc:
                print(f'Problem {args.problem}: {desc}')
            display_result(func())
        else:
            print(f'Problem {args.problem} not found!')

if __name__ == '__main__':
    main()