import os
import math
from collections import Counter

PI_DIGITS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'pi_digits.txt')
NUM_DIGITS = 1_000_000

def load_pi_digits() -> str:
    """
    Loads the first 1,000,000 digits of Pi from the data directory.
    """
    if not os.path.exists(PI_DIGITS_FILE):
        raise FileNotFoundError(f"Pi digits file not found at {PI_DIGITS_FILE}")
    
    print(f"Loading {NUM_DIGITS:,} digits of Pi from {PI_DIGITS_FILE}...")
    with open(PI_DIGITS_FILE, "r") as f:
        return f.read().strip()

def search_all_occurrences(sequence: str, digits: str) -> list[int]:
    """
    Finds all occurrences of a sequence in the given digits.
    """
    positions = []
    start = 0
    while (pos := digits.find(sequence, start)) != -1:
        positions.append(pos + 1)
        start = pos + 1
    return positions

def get_snippet(digits: str, position: int, sequence: str, length: int = 20) -> str:
    """
    Extracts a snippet of digits surrounding a found sequence.
    """
    pos_0_indexed = position - 1
    start = max(0, pos_0_indexed - length)
    end = min(len(digits), pos_0_indexed + len(sequence) + length)

    before = digits[start:pos_0_indexed]
    highlighted = f'<span style="color:red; font-weight:bold">{sequence}</span>'
    after = digits[pos_0_indexed + len(sequence):end]

    return f"...{before}{highlighted}{after}..."

def digit_distribution(digits: str) -> dict:
    """
    Calculates the frequency distribution of digits.
    """
    total_digits = len(digits)
    counts = Counter(digits)
    distribution = {}
    for digit in sorted(counts.keys()):
        count = counts[digit]
        percentage = (count / total_digits) * 100
        distribution[digit] = {"count": count, "percent": round(percentage, 2)}
    return distribution

def randomness_stats(digits: str) -> dict:
    """
    Computes basic statistical measures of the digit distribution.
    """
    digit_values = [int(d) for d in digits]
    total_digits = len(digit_values)
    counts = Counter(digits)

    mean = sum(digit_values) / total_digits
    variance = sum((x - mean) ** 2 for x in digit_values) / total_digits

    entropy = 0
    for digit in counts:
        probability = counts[digit] / total_digits
        if probability > 0:
            entropy -= probability * math.log2(probability)

    return {
        "mean": round(mean, 4),
        "variance": round(variance, 4),
        "entropy": round(entropy, 4)
    }
