import mod

class elliptic_curve:
  """
  This class intend to implement basic operations on elliptic curves of type
  y^2 = x^3 + ax + b (mod p)
  """

  def __init__(self, a, b, p):

    self.a = a
    self.b = b
    self.prime = p


  def _calc_curve(self, x):
    """
    calculate the value of y^2 for curve y^2 = x^3 + ax + b (mod p)

    :return: y^2 for x
    """
    return (x**3 + self.a * x + self.b) % self.prime


  def _get_points_util(self):
    """
    Utility function to obtain points on the curve

    :return: list of possible points on curve (superset of actual points)
    """

    points = []

    # Calulate y^2 for all the possible values of x in curve
    for i in range(self.prime):
      y2 = self._calc_curve(i)
      points.append((i, y2))

    return points


  def _quadratic_residue(self):
    """
    Get the list of all the possible quadratic residue for self.prime.
    Integer q is called a quadratic residue modulo n if it is congruent
    to a perfect square modulo n
    """

    QR = set()

    for i in range(1 , self.prime):
      y2 = (i**2) %self.prime
      QR.add(y2)

    return QR


  def _distilled_points(self):
    """
    A point (x,y) belongs to the curve only if y^2 is a quadratic residue.
    This function return all the valid points on the curve
    :return: list of all (x, y^2) on the curve
    """

    QR = self._quadratic_residue()
    points = self._get_points_util()

    distill_points = []

    for point in points:
      y2 = point[1]

      if (y2 in QR) or (y2 == 0):
        distill_points.append(point)

    return distill_points


  def _get_y_for_y2(self, y2):
    """
    Values of all possible y for y^2 on the curve
    """

    y = []

    if y2 == 0:
      return [0]

    for i in range(self.prime):
      if (i**2 % self.prime == y2):
        y.append(i)


    return y


  def valid_points(self):
    """
    Calculate all the points on the elliptic curve

    :return: list of all (x, y) on the curve
    """

    distilled_points = self._distilled_points()
    points = []

    for point in distilled_points:
      x = point[0]
      y2 = point[1]
      for y in self._get_y_for_y2(y2):
        points.append((x,y))

    return points


  def sum(self, P, Q):
    """
    To calculate P+Q on the curve
    """
    xp = P[0]
    yp = P[1]

    xq = Q[0]
    yq = Q[1]

    if P == (0, 0):
      return Q
    if Q == (0, 0):
      return P

    if P == Q:
      m = (((3 * (xp ** 2) + self.a) % self.prime) *
          mod.inverse_extended_eucledian(2 * yp, self.prime)) % self.prime
    else:
      if xp == xq:
        return (0, 0)
      else:
        m = (((yp - yq) % self.prime) *
            mod.inverse_extended_eucledian(xp - xq, self.prime)) % self.prime
    xr = (m ** 2 - xp - xq) % self.prime
    yr1 = (-yp - m * (xr - xp)) % self.prime
    yr2 = (-yq - m * (xr - xq)) % self.prime

    if yr1 == yr2:
      yr = yr1
    else:
      print("Something went wrong!")
      return

    return (xr, yr)


  def scalar_multiples(self, m, P):
    """
    :return: [P , 2P, 3P ....... mP]
    """

    multi = [P] * m

    for i in range(1, m):
      multi[i] = self.sum(P, multi[i - 1])

    return multi



