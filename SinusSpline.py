import numpy as np
import scipy.interpolate as si


class SinusSpline:
    LOWER = 0
    UPPER = 2 * np.pi

    @staticmethod
    def _fx(x):
        return np.sin(5*x) * np.cos(x) ** 2

    def __init__(self, ticks, knots, degree):
        self.ticks = np.linspace(self.LOWER, self.UPPER, ticks)
        self.y_fx = self._fx(self.ticks)

        self.x_cp = np.linspace(self.LOWER, self.UPPER, knots)
        self.y_cp = self._fx(self.x_cp)

        self.degree = degree
        self._spl = si.splrep(self.x_cp, self.y_cp, k=self.degree)
        self._spl_coefficients = self._spl[1]
        self.y_sp = si.splev(ticks, self._spl)

        self.x_knots_add = self._spl[0]

    def _calculate_basis_elements(self, x, k, i, t):
        if k == 0:
            return 1.0 if t[i] <= x < t[i + 1] else 0.0
        if t[i + k] == t[i]:
            c1 = 0.0
        else:
            c1 = (x - t[i]) / (t[i + k] - t[i]) * self._calculate_basis_elements(x, k - 1, i, t)
        if t[i + k + 1] == t[i + 1]:
            c2 = 0.0
        else:
            c2 = (t[i + k + 1] - x) / (t[i + k + 1] - t[i + 1]) * self._calculate_basis_elements(x, k - 1, i + 1, t)
        return c1 + c2

    def _calculate_spline_basis(self, x, t, c, k):
        n = len(t) - k - 1
        assert (n >= k + 1) and (len(c) >= n)
        return sum(c[i] * self._calculate_basis_elements(x, k, i, t) for i in range(n))

    def get_base_data(self):
        return [self.ticks, self.y_fx]

    def get_original_points(self):
        return [self.x_cp, self.y_cp]

    def get_spline_native(self):
        return [self.ticks, [self._calculate_spline_basis(x, self.x_knots_add, self._spl_coefficients, self.degree) for x in self.ticks]]

    def get_spline_auto(self):
        return [self.ticks, si.splev(self.ticks, self._spl)]


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    spline = SinusSpline(ticks=200, knots=7, degree=3)
    plt.figure()
    plt.plot(*spline.get_base_data(), linestyle="--", label = "fx")
    plt.plot(*spline.get_spline_native(), label = "spline")
    # plt.plot(*spline.get_spline_auto())
    plt.scatter(*spline.get_original_points(), s=70, label ="points")
    plt.scatter(*spline.get_additional_knots(), s=80, label = "knots", marker='x')
    plt.legend(loc="best")
    plt.show()
