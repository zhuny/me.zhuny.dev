from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel, Field


def euler(yaw_deg: float, pitch_deg: float) -> np.ndarray:
    """+Z를 Y축으로 pitch, 이어서 Z축으로 yaw 한 단위벡터.

    euler(0, θ) = (sin θ, 0, cos θ)
    euler(0, 0) = +Z, euler(0, 90) = +X, euler(90, 90) = +Y
    """
    yaw = np.deg2rad(yaw_deg)
    pitch = np.deg2rad(pitch_deg)
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    return np.array([cy * sp, sy * sp, cp], dtype=float)


class SolarPanelConfig(BaseModel):
    axial_tilt: float = Field(
        default=23.44,
        description="지구 자전축 기울기",
        ge=0.0,
        le=90.0,
    )
    latitude: float = Field(
        description="태양광 패널이 설치된 위치의 위도",
        ge=-90.0,
        le=90.0,
    )
    day_of_year: int = Field(
        default=365,
        description="연중 일수 d",
        ge=0,
        # le=366, 상한은 굳이 필요 없음
    )


class SolarPanelSimulation:
    def __init__(self, panel_config: SolarPanelConfig):
        self.config = panel_config

    def run(self):
        samples_per_day = 24
        time_seq = np.linspace(
            0.0,
            360.0,
            self.config.day_of_year * samples_per_day,
            endpoint=False,
        )
        panel_seq = np.linspace(-90.0, 90.0, 181)

        # t = 0: 자전축이 태양 쪽(+X)으로 기울고, 관측 지점은 남중.
        earth_rot_axis = euler(0, self.config.axial_tilt)
        zenith = euler(0, 90.0 + self.config.axial_tilt - self.config.latitude)
        # 남향 기울기: 천정 법선을 동(+Y)축 기준으로 회전. {3, Panel}
        panel_normal = self._rotate(euler(90, 90), zenith, panel_seq)
        solar_pos = euler(0, 90)

        # 패널: 자전축 기준 (day_of_year+1)바퀴. 1바퀴면 달처럼 태양날이 안 바뀐다.
        panel_normal_time = self._rotate(
            earth_rot_axis,
            panel_normal,
            time_seq * (self.config.day_of_year + 1),
        )
        # 태양: 공전면 수직(+Z) 기준 1바퀴. {3, Time}
        solar_pos_time = self._rotate(euler(0, 0), solar_pos, time_seq)

        # {3, Panel, Time} · {3, Time} → {Panel, Time}, 음수는 밤이므로 0
        incidence = np.maximum(
            (panel_normal_time * solar_pos_time[:, None, :]).sum(axis=0),
            0.0,
        )
        solar_panel_value = incidence.mean(axis=-1)
        self._show(panel_seq, solar_panel_value, "Panel Angle", "Effective")
        return panel_seq, solar_panel_value

    def _rotate(self, rot_axis, vec, time_seq):
        """rot_axis 기준으로 vec를 time_seq(도)만큼 회전한다.

        :param rot_axis: (3,) 회전축
        :param vec: (3,) 또는 (3, ...) 벡터
        :param time_seq: 회전각(도) sequence
        :return: (3, ..., T)
        """
        axis = np.asarray(rot_axis, dtype=float).reshape(3)
        axis = axis / np.linalg.norm(axis)
        vec = np.asarray(vec, dtype=float)
        if vec.shape[0] != 3:
            raise ValueError("vec must have shape (3, ...)")

        extra = vec.shape[1:]
        angles = np.deg2rad(np.asarray(time_seq, dtype=float))
        cos = np.cos(angles).reshape(*(1,) * len(extra), -1)
        sin = np.sin(angles).reshape(*(1,) * len(extra), -1)

        axis_extra = axis.reshape(3, *([1] * len(extra)))
        k_dot_v = (axis_extra * vec).sum(axis=0).reshape(*extra, 1)
        kxv = np.cross(axis, vec, axisa=0, axisb=0, axisc=0).reshape(3, *extra, 1)
        k_parallel = axis.reshape(3, *(1,) * len(extra), 1) * k_dot_v

        return vec.reshape(3, *extra, 1) * cos + kxv * sin + k_parallel * (1.0 - cos)

    def _show(self, panel_angles, panel_value, x_label, y_label):
        """패널 각도에 따른 연평균 유효 코사인을 그래프로 그린다."""
        best_i = int(np.argmax(panel_value))
        best_angle = float(panel_angles[best_i])
        best_value = float(panel_value[best_i])

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(panel_angles, panel_value)
        ax.axvline(best_angle, linestyle="--", color="C1")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(
            f"lat={self.config.latitude:.3f}°, "
            f"best tilt={best_angle:.1f}° (effective={best_value:.4f})"
        )
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        out_path = Path(__file__).with_name("solar_efficiency.png")
        fig.savefig(out_path, dpi=120)
        print(f"optimal panel tilt: {best_angle:.1f} deg")
        print(f"average effective cosine: {best_value:.4f}")
        print(f"saved: {out_path}")
        plt.show()


def main():
    config = SolarPanelConfig(
        latitude=35.639,  # 붕어섬 위도
    )
    simulation = SolarPanelSimulation(config)
    simulation.run()


if __name__ == "__main__":
    main()
