import numpy as np
from rng import RNG
from nistrng import *


def main():
    """
    Run few tests on simple PRNG (pseudo-random number generator).
    More tests can be found here:
        1) NIST document SP 800-22 Rev. 1a
           https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final
        2) Handbook of Applied Cryptography, chapter 5
           https://cacr.uwaterloo.ca/hac/about/chap5.pdf

    This is not rigorous testing; test should be repeated for different seeds
    """
    N = 100000
    bin_count = 100
    bit_count = [0, 0]

    # Create pseudo-random array
    rng = RNG(123)
    rand_array = np.array([rng.get() for i in range(N)])

    #
    # Monobit test done manually
    #
    for rand in rand_array:
        population_count = rand.bit_count()
        bit_count[1] += population_count
        bit_count[0] += 8 * rng.number_len - population_count
    print(f"Number of 0: {bit_count[0]}\nNumber of 1: {bit_count[1]}")
    print(f"Ratio 1:0 = {bit_count[1]/bit_count[0]} (should be close to 1)")

    #
    # Run tests from nistrng - more or less copied from numby_rng_test.py
    # (tests based on SP 800-22 Rev. 1a)
    #
    binary_sequence = pack_sequence(rand_array)
    # Check the eligibility of the test and generate an eligible battery from the default NIST-sp800-22r1a battery
    eligible_battery: dict = check_eligibility_all_battery(
        binary_sequence, SP800_22R1A_BATTERY
    )
    # Print the eligible tests
    print("Eligible test from NIST-SP800-22r1a:")
    for name in eligible_battery.keys():
        print("-" + name)
    # Test the sequence on the eligible tests
    results = run_all_battery(binary_sequence, eligible_battery, False)
    # Print results one by one
    print("Running tests (may take a minute or two)...")
    for result, elapsed_time in results:
        if result.passed:
            print(
                "- PASSED - score: "
                + str(np.round(result.score, 3))
                + " - "
                + result.name
                + " - elapsed time: "
                + str(elapsed_time)
                + " ms"
            )
        else:
            print(
                "- FAILED - score: "
                + str(np.round(result.score, 3))
                + " - "
                + result.name
                + " - elapsed time: "
                + str(elapsed_time)
                + " ms"
            )


if __name__ == "__main__":
    main()
