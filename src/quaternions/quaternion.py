import math


class Quaternion:
    """Кватернион q = w + xi + yj + zk."""

    def __init__(self, w=0.0, x=0.0, y=0.0, z=0.0):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def _components(self):
        return (self.w, self.x, self.y, self.z)

    def __add__(self, other):
        return Quaternion(*(a + b for a, b in zip(self._components(), other._components())))

    def __mul__(self, other):
        w1, x1, y1, z1 = self._components()
        w2, x2, y2, z2 = other._components()
        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2,
        )

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def norm(self):
        return math.sqrt(sum(c * c for c in self._components()))

    def inverse(self):
        n2 = self.norm() ** 2
        if n2 == 0:
            raise ZeroDivisionError("нулевой кватернион необратим")
        c = self.conjugate()
        return Quaternion(c.w / n2, c.x / n2, c.y / n2, c.z / n2)

    @classmethod
    def from_axis_angle(cls, axis, angle):
        """Кватернион поворота вокруг оси axis на угол angle (радианы)."""
        ax, ay, az = axis
        n = math.sqrt(ax*ax + ay*ay + az*az)
        if n == 0:
            raise ValueError("ось поворота не может быть нулевой")
        s = math.sin(angle / 2) / n
        return cls(math.cos(angle / 2), ax * s, ay * s, az * s)

    def rotate(self, v):
        """Поворот вектора v=(x, y, z) по формуле q v q^-1."""
        r = self * Quaternion(0, *v) * self.inverse()
        return (r.x, r.y, r.z)

    def __eq__(self, other):
        if not isinstance(other, Quaternion):
            return NotImplemented
        return all(
            math.isclose(a, b, abs_tol=1e-9)
            for a, b in zip(self._components(), other._components())
        )

    __hash__ = None

    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"