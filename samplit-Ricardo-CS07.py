import random
import sys

# Randomly sample lines (feature branch version)
def main():
    if len(sys.argv) != 2:
        print("Usage: python samplit-Ricardo-CS07.py <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        for line in f:
            if random.random() < 0.01:
                print(line, end="")

main()
