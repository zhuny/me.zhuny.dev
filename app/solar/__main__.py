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
    panel_tilt: float = Field(
        description="수평면을 기준으로 한 태양광 패널의 설치 각도",
        ge=0.0,
        le=90.0,
    )
    day_of_year: int = Field(
        default=365,
        description="연중 일수 d",
        ge=1,
        # le=366, 상한은 굳이 필요 없음
    )


class SolarPanelSimulation:
    def __init__(self, panel_config: SolarPanelConfig):
        self.panel_config = panel_config

    def run(self):
        pass


def main():
    config = SolarPanelConfig(
        latitude=37.5665,
        panel_tilt=30.0,
    )
    simulation = SolarPanelSimulation(config)
    simulation.run()


if __name__ == "__main__":
    main()
