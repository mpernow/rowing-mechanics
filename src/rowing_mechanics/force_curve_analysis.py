import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid


class XYCurve:
    def __init__(self, x: np.ndarray, y: np.ndarray, x_label: str, y_label: str):
        self.x = x
        self.y = y
        self.x_label = x_label
        self.y_label = y_label

    def plot(self) -> plt.figure:
        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        return fig


class ForceTimeCurve(XYCurve):
    def __init__(self, time: np.ndarray, force: np.ndarray):
        time = (time - min(time)) / (max(time) - min(time))
        force = np.clip(force, 0, None)
        super().__init__(time, force, "Time", "Force")


class VelocityTimeCurve(XYCurve):
    def __init__(self, time: np.ndarray, velocity: np.ndarray):
        super().__init__(time, velocity, "Time", "Velocity")


class DistanceTimeCurve(XYCurve):
    def __init__(self, time: np.ndarray, distance: np.ndarray):
        super().__init__(time, distance, "Time", "Distance")


class ForceDistanceCurve(XYCurve):
    def __init__(self, distance: np.ndarray, force: np.ndarray):
        distance = (distance - min(distance)) / (max(distance) - min(distance))
        super().__init__(distance, force, "Distance", "Force")


class PhysicsEngine:
    @staticmethod
    def force_to_velocity(force_curve: ForceTimeCurve) -> VelocityTimeCurve:
        velocity = cumulative_trapezoid(force_curve.y, force_curve.x, initial=0)
        return VelocityTimeCurve(force_curve.x, velocity)

    @staticmethod
    def velocity_to_distance(velocity_curve: VelocityTimeCurve) -> DistanceTimeCurve:
        distance = cumulative_trapezoid(velocity_curve.y, velocity_curve.x, initial=0)
        return DistanceTimeCurve(velocity_curve.x, distance)

    @staticmethod
    def force_time_to_force_distance(
        force_time: ForceTimeCurve, distance_time: DistanceTimeCurve
    ) -> ForceDistanceCurve:
        return ForceDistanceCurve(distance_time.y, force_time.y)


def triangle(x: np.ndarray) -> np.ndarray:
    return np.array([v if v < 0.5 else 1 - v for v in x])


if __name__ == "__main__":
    time = np.linspace(0, 2, 100)
    force = triangle(time)
    # force = 1 * np.ones(100)

    forceCurve = ForceTimeCurve(time, force)
    velocityCurve = PhysicsEngine.force_to_velocity(forceCurve)
    distanceCurve = PhysicsEngine.velocity_to_distance(velocityCurve)
    forceDistanceCurve = PhysicsEngine.force_time_to_force_distance(
        forceCurve, distanceCurve
    )

    fig1 = forceCurve.plot()
    fig2 = velocityCurve.plot()
    fig3 = distanceCurve.plot()
    fig4 = forceDistanceCurve.plot()
    plt.show()
