# Problem 87:
#     Prime Power Triples
#
# Description:
#     The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28.
#     In fact, there are exactly four numbers below fifty that can be expressed in such a way:
#         28 = 2^2 + 2^3 + 2^4
#         33 = 3^2 + 2^3 + 2^4
#         49 = 5^2 + 2^3 + 2^4
#         47 = 2^2 + 3^3 + 2^4
#
#     How many numbers below fifty million can be expressed as
#       the sum of a prime square, prime cube, and prime fourth power?

from math import floor, sqrt


def primes_below(n):
    """
    Returns an ordered list of all the primes below `n`.

    Args:
        n (int): Natural number

    Returns:
        (List[int]): Ordered list of primes below `n`

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    if n < 3:
        return []
    else:
        primes = [2]
        for x in range(3, n, 2):
            # Use previous primes to check primality of x
            x_mid = floor(sqrt(x)) + 1
            i = 0
            x_prime = True
            while i < len(primes) and primes[i] < x_mid:
                p = primes[i]
                if x % p == 0:
                    x_prime = False
                    break
                else:
                    i += 1
            if x_prime:
                primes.append(x)
            else:
                continue
        return primes


def main(n):
    """
    Returns the count of numbers below `n` which can be expressed as
      the sum of a prime square, prime cube, and prime 4th power.

    Args:
        n (int): Natural number

    Returns:
        (int, int):
            Tuple of ...
              * First number that can be summed by primes in over `min_ways` ways
              * Number of ways to sum to that number

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    # Quick check
    if n < (2**2 + 2**3 + 2**4):
        return 0

    # Idea:
    #     Want to find all x (< n), where x = p^2 + q^3 + r^4 for some primes p, q, r.
    #
    #     First collect all the primes of interest, but how many?
    #     Prime `p` can go the highest, as it is only squared, rather than cubed or 4th-powered.
    #     Also know q and r are at least 2, as 2 is the least prime.
    #     Solve for upper bound on `p`:
    #         x = p^2 + q^3 + r^4 < n
    #         p^2 + q^3 + r^4 < n
    #         p^2 + 2^3 + 2^4 <= p^2 + q^3 + r^4 < n
    #         p^2 + 2^3 + 2^4 < n
    #         p^2 < n - 2^3 - 2^4
    #         p < sqrt(n - 24)
    #
    #     Find all primes within this range.
    #     Then try different triples (p, q, r) and count distinct values of `x`.
    #     Can also shorten the looping by only limiting to viable triples.

    # Collect all the primes
    primes = primes_below(floor(sqrt(n - 2**3 - 2**4)) + 1)

    # Keep track of numbers known to be formed as prime power triple sum
    triple_sums = set()

    for p in primes:  # All `p` in `primes` are already candidates to be the squared prime, so no bound needed
        p2 = p ** 2
        q_bound = floor((n - p2 - 2**4) ** (1/3)) + 1
        for q in primes:
            if q >= q_bound:
                # Must have q < (n - p^2 - 2^4)^(1/3)
                break
            else:
                q3 = q ** 3
                r_bound = floor((n - p2 - q3) ** (1/4)) + 1
                for r in primes:
                    if r >= r_bound:
                        # Must have r < (n - p^2 - q^3)^(1/4)
                        break
                    else:
                        r4 = r ** 4
                        x = p2 + q3 + r4
                        if x < n:
                            triple_sums.add(x)

    return len(triple_sums)


if __name__ == '__main__':
    upper_limit = int(input('Enter a natural number: '))
    prime_power_triple_count = main(upper_limit)
    print('Count of numbers below {} expressible as sum of a prime square, cube, and fourth power:'.format(upper_limit))
    print('  {}'.format(prime_power_triple_count))
