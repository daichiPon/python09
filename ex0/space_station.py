from pydantic import BaseModel, Field, ValidationError
import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime.datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


if __name__ == "__main__":
    print("Space Station Data Validation")
    print("========================================")
    try:
        spaceStation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-08-08T10:00:00" 
        )
        print(f"ID: {spaceStation.station_id}")
        print(f"Name: {spaceStation.name}")
        print(f"Crew: {spaceStation.crew_size} people")
        print(f"Power: {spaceStation.power_level} %")
        print(f"Oxygen: {spaceStation.oxygen_level} %")
        print(f"Status: {spaceStation.is_operational}")
    except ValidationError as e:
        print(e)
    print("========================================")
    try:
        spaceStation = SpaceStation(
            station_id="ISS001aaaaaaaaaaa",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.date(2026, 8, 8)
        )
    except ValidationError as e:
        print(e)
