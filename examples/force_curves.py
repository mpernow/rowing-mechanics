import matplotlib.pyplot as plt
import numpy as np

from rowing_mechanics.force_curve_analysis import (
    CurveConverter,
    ForceTimeCurve,
    compute_total_energy,
)


def triangle(x: np.ndarray) -> np.ndarray:
    return np.array([v if v < 0.5 else 1 - v for v in x])


def constant(x: np.ndarray) -> np.ndarray:
    return np.ones(x.size)


def quadratic(x: np.ndarray) -> np.ndarray:
    return -1 * x * (x - 1)


def gaussian(x: np.ndarray) -> np.ndarray:
    return np.exp(-((x - 0.5) ** 2) / 0.1)


def linexp(x: np.ndarray) -> np.ndarray:
    return x * np.exp(-5 * x)


def quadexp(x: np.ndarray) -> np.ndarray:
    return x**2 * np.exp(-5 * x)


if __name__ == "__main__":
    time = np.linspace(0, 1, 100)
    force = quadexp(time)

    forceCurve = ForceTimeCurve(time, force)
    velocityCurve = CurveConverter.force_to_velocity(forceCurve)
    distanceCurve = CurveConverter.velocity_to_distance(velocityCurve)
    forceDistanceCurve = CurveConverter.force_time_to_force_distance(
        forceCurve, distanceCurve
    )

    forwardForceDistanceCurve = CurveConverter.compute_forward_force(
        forceDistanceCurve, -45, 45
    )

    total_forward_energy = compute_total_energy(forwardForceDistanceCurve)

    fig1 = forceCurve.plot()
    fig2 = velocityCurve.plot()
    fig3 = distanceCurve.plot()
    fig4 = forceDistanceCurve.plot()
    fig5 = forwardForceDistanceCurve.plot()
    plt.show()

    print(f"Total forward energy is {total_forward_energy}")
