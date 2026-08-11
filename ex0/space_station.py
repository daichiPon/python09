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


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    try:
        spaceStation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.datetime(2026, 8, 8, 10, 0, 0)
        )
        print(f"ID: {spaceStation.station_id}")
        print(f"Name: {spaceStation.name}")
        print(f"Crew: {spaceStation.crew_size} people")
        print(f"Power: {spaceStation.power_level}%")
        print(f"Oxygen: {spaceStation.oxygen_level}%")
        status = ("Operational" if spaceStation.is_operational
                  else "Not operational")
        print(f"Status: {status}")
    except ValidationError as e:
        print(e)
    print("========================================")
    print("Expected validation error:")
    try:
        spaceStation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.datetime(2026, 8, 8)
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
