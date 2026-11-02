import math
import pytest
from quaternions import Quaternion

ONE = Quaternion(1, 0, 0, 0)
I = Quaternion(0, 1, 0, 0)
J = Quaternion(0, 0, 1, 0)
K = Quaternion(0, 0, 0, 1)


@pytest.fixture
def q_z90():
    return Quaternion.from_axis_angle((0, 0, 1), math.pi / 2)


# --- арифметика ---
def test_add():
    assert Quaternion(1, 2, 3, 4) + Quaternion(4, 3, 2, 1) == Quaternion(5, 5, 5, 5)

def test_hamilton_units():
    assert I * I == Quaternion(-1, 0, 0, 0)
    assert I * J == K
    assert J * K == I
    assert K * I == J

def test_mul_not_commutative():
    assert I * J != J * I

def test_conjugate():
    assert Quaternion(1, 2, 3, 4).conjugate() == Quaternion(1, -2, -3, -4)

def test_norm():
    assert Quaternion(1, 2, 3, 4).norm() == pytest.approx(math.sqrt(30))

def test_inverse():
    q = Quaternion(1, 2, 3, 4)
    assert q * q.inverse() == ONE

def test_inverse_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Quaternion(0, 0, 0, 0).inverse()


# --- поворот ---
def test_from_axis_angle_is_unit(q_z90):
    assert q_z90.norm() == pytest.approx(1.0)

def test_zero_axis_raises():
    with pytest.raises(ValueError):
        Quaternion.from_axis_angle((0, 0, 0), 1.0)

def test_rotate_x_around_z(q_z90):
    assert q_z90.rotate((1, 0, 0)) == pytest.approx((0, 1, 0), abs=1e-9)

@pytest.mark.parametrize("axis, angle, v, expected", [
    ((0, 0, 1), math.pi,     (1, 0, 0), (-1, 0, 0)),
    ((1, 0, 0), math.pi / 2, (0, 1, 0), (0, 0, 1)),
    ((0, 1, 0), math.pi / 2, (0, 0, 1), (1, 0, 0)),
    ((0, 0, 1), 0,           (1, 2, 3), (1, 2, 3)),
    ((0, 0, 2), math.pi / 2, (1, 0, 0), (0, 1, 0)),  # ось не единичная
])
def test_rotations(axis, angle, v, expected):
    r = Quaternion.from_axis_angle(axis, angle).rotate(v)
    assert r == pytest.approx(expected, abs=1e-9)

def test_rotation_preserves_length(q_z90):
    r = q_z90.rotate((1, 2, 3))
    assert math.hypot(*r) == pytest.approx(math.sqrt(14))

def test_composition():
    q1 = Quaternion.from_axis_angle((0, 0, 1), math.pi / 2)
    q2 = Quaternion.from_axis_angle((1, 0, 0), math.pi / 2)
    v = (1, 0, 0)
    assert (q2 * q1).rotate(v) == pytest.approx(q2.rotate(q1.rotate(v)), abs=1e-9)

def test_inverse_rotation_returns_vector(q_z90):
    v = (1, 2, 3)
    assert q_z90.inverse().rotate(q_z90.rotate(v)) == pytest.approx(v, abs=1e-9)