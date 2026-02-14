#!/usr/bin/env python3
"""A simple dice roller script."""

import argparse
import random


def roll_dice(num_dice=1, num_faces=6):
    """Roll dice and return a list of results.

    Args:
        num_dice: Number of dice to roll.
        num_faces: Number of faces on each die.

    Returns:
        A list of integers, one per die rolled.
    """
    if num_faces < 1:
        raise ValueError("num_faces must be at least 1")
    if num_dice < 0:
        raise ValueError("num_dice must be non-negative")
    return [random.randint(1, num_faces) for _ in range(num_dice)]


def calculate_total(results):
    """Calculate the total of dice results.

    Args:
        results: A list of integers representing dice rolls.

    Returns:
        The sum of all results.
    """
    return sum(results)


def main():
    parser = argparse.ArgumentParser(description="Roll dice and show results.")
    parser.add_argument(
        "--num-dice", type=int, default=1, help="Number of dice to roll (default: 1)"
    )
    parser.add_argument(
        "--num-faces",
        type=int,
        default=6,
        help="Number of faces on each die (default: 6)",
    )
    args = parser.parse_args()

    if args.num_dice < 0:
        parser.error("--num-dice must be non-negative")
    if args.num_faces < 1:
        parser.error("--num-faces must be at least 1")

    results = roll_dice(args.num_dice, args.num_faces)
    total = calculate_total(results)

    print(f"Rolling {args.num_dice} dice with {args.num_faces} faces each:")
    for i, result in enumerate(results, 1):
        print(f"  Die {i}: {result}")
    print(f"Total: {total}")


if __name__ == "__main__":
    main()
