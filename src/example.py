import math

from quaternions import Quaternion


def clean(v):
    """Округление для красивого вывода (убирает 1e-17 и -0.0)."""
    return tuple(round(c, 6) + 0.0 for c in v)


def main():
    v = (1, 0, 0)
    q_z = Quaternion.from_axis_angle((0, 0, 1), math.pi / 2)
    q_x = Quaternion.from_axis_angle((1, 0, 0), math.pi / 2)

    print("Вектор:", v)
    print("Поворот на 90° вокруг Z:", clean(q_z.rotate(v)))
    print("Затем поворот на 90° вокруг X:", clean(q_x.rotate(q_z.rotate(v))))
    print("Композиция q_x * q_z за один шаг:", clean((q_x * q_z).rotate(v)))


if __name__ == "__main__":
    main()