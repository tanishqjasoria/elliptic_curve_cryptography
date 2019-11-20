""" This is just a naive implementation of various modular
arithmatic operations which would be used for various operations
in analysing and solving Elliptic Curves """




def eucledian_gcd(a, b):
  """
  Implementaion of eucledian algorithm to get the GCD of two numbers

  :return: gretest common divisor of a , b
  """

  if a == 0:
    return b
  if b == 0:
    return a
  return eucledian_gcd(b, a%b)


def extended_eucledian(a,b):
  """
  Extended algorithm for calculation of GCD of two number
  It also provides additional values x,y such that ax + by = gcd(a,b)

  :return: x, y, gcd
  """

  x, y, gcd = _extended_eucledian_util( a, b, 1, 1)

  return x, y, gcd


def _extended_eucledian_util( a, b, x, y):
  """
  Utility function for calculation of x, y, gcd for ax + by = gcd(a, b)
  """

  if a == 0:
    x = 0
    y = 1
    return x, y, b

  x1, y1, gcd = _extended_eucledian_util(b%a, a, x, y)

  x = y1 -(b//a) * x1
  y = x1

  return x, y, gcd


def inverse_brute_force(n , p):
  """
  Calculation of inverse in modular arithmetic.
  Calculate inverse of n in n (mod p)

  :return: n^(-1) (mod p)
  """
  for i in range(p):
    if (n*i)%p == 1:
      return i


def inverse_extended_eucledian(n,p):
  """
  Use extended eucledian method to calculate inverse in modular arithmetic.
  Calculate inverse of n in n (mod p)

  :return: n^(-1) (mod p)
  """
  n = n % p
  inv, buff1, buff2 = extended_eucledian(n, p)
  return inv % p
