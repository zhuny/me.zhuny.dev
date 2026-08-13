from pydantic import BaseModel, Field


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
        # 시퀀스 - N개로 uniform하게 나뉘는 실수 array
        time_seq = range(0, 360)
        panel_seq = range(-90, 90)

        # t = 0일 때의 상태값들
        earth_rot_axis = Quaternion.euler(0, self.config.axial_tilt)
        panel_normal_zero = Quaternion.euler(0, self.config.axial_tilt + self.config.latitude)
        # {Q, Panel Range}를 갖는다.
        panel_normal = self._rotate(
            panel_normal_zero,
            Quaternion.euler(90, 90),
            panel_seq,
        )
        solar_pos = Quaternion.euler(0, 90)

        # t가 바뀌면서 변화하도록,
        # 패널의 경우 {Q, Panel Range, Time}
        panel_normal_time = self._rotate(
            earth_rot_axis, panel_normal,
            # 자전을 1번 하면 사실상 달처럼 날이 바뀌지 않는 상태(연중 0일)이 된다.
            time_seq * (self.config.day_of_year + 1)
        )
        # {Q, Time}
        solar_pos_time = self._rotate(
            Quaternion.euler(0, 0), solar_pos, time_seq
        )

        # panel과 solar의 각도 계산
        # {Q, Panel Range, Time}와 {Q, Time}가 같은 축끼리 곱한다음 합해져서
        # {Panel Range} 만 남는다. Q는 Quaternion 곱한 거에서 실수부
        solar_panel_value = max(
            panel_normal_time * solar_pos_time,  # inner product
            0
        )
        self._show(solar_panel_value, "Panel Angle", "Effective")

    def _rotate(self, rot_axis, vec, time_seq):
        """
        rot_axis기준으로 vec를 회전시키는데, time_seq 각도만큼 회전시킨 결과값
        :param rot_axis: Q, 회전시킬 각도
        :param vec: {Q, ...} 형태의 array
        :param time_seq: 시간 sequence
        :return: {Q, ..., time} 형태의 array
        """

    def _show(self, panel_value, x_label, y_label):
        """
        시간에 따른 값 시퀀스. 그래프를 그린다.
        """


def main():
    config = SolarPanelConfig(
        latitude=35.639, # 붕어섬 위도
    )
    simulation = SolarPanelSimulation(config)
    simulation.run()


if __name__ == "__main__":
    main()
