"""Validate existing test reviews; never assign a score from a config/query name."""
from scripts.write_reviews import validate_split


def main():
    return validate_split('test')


if __name__ == '__main__':
    main()
