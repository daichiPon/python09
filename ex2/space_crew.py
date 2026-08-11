from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
import datetime


class CrewRanc(str, Enum):
    CANDET = "cadet"
    OFFICER = "officer"
    LINEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanc
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime.datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_rule(self):
        people = 0
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with M")
        if not any(crewMember.rank == CrewRanc.COMMANDER
                   or crewMember.rank == CrewRanc.CAPTAIN
                   for crewMember in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain")
        for crewMember in self.crew:
            if not crewMember.is_active:
                raise ValueError("All crew members must be active")
            if crewMember.years_experience >= 5:
                people += 1
        if self.duration_days > 365 and people < len(self.crew) / 2:
            raise ValueError("Long missions need 50% experienced crew")
        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.datetime(2024, 6, 1),
        duration_days=900,
        crew=[
            CrewMember(member_id="CM001", name="Sarah Connor",
                       rank=CrewRanc.COMMANDER, age=42,
                       specialization="Mission Command",
                       years_experience=15),
            CrewMember(member_id="CM002", name="John Smith",
                       rank=CrewRanc.LINEUTENANT, age=35,
                       specialization="Navigation",
                       years_experience=8),
            CrewMember(member_id="CM003", name="Alice Johnson",
                       rank=CrewRanc.OFFICER, age=29,
                       specialization="Engineering",
                       years_experience=6),
        ],
        budget_millions=2500.0,
    )
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for crewMember in mission.crew:
        print(f"- {crewMember.name} ({crewMember.rank.value}) "
              f"- {crewMember.specialization}")

    print()
    print("=========================================")
    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date=datetime.datetime(2024, 9, 1),
            duration_days=30,
            crew=[
                CrewMember(member_id="CM010", name="Bob Miles",
                           rank=CrewRanc.OFFICER, age=30,
                           specialization="Geology",
                           years_experience=4),
            ],
            budget_millions=120.0,
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"].removeprefix("Value error, "))