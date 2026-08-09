from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
import datetime


class CrewRanc(str, Enum):
    CANDET = "cadet",
    OFFICER = "officer",
    LINEUTENANT = "lieutenant",
    CAPTAIN = "captain",
    COMMANDER = "commander cadet"


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
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_rule(self):
        self.people = 0
        if not self.mission_id.startswith("M"):
            raise ValidationError
        for crewMember in self.crew:
            if (not crewMember.rank == CrewRanc.COMMANDER
                    and not crewMember.rank == CrewRanc.CAPTAIN):
                raise ValidationError
            if not crewMember.is_active:
                raise ValidationError
            if crewMember.years_experience > 5:
                self.people += 1
        if self.people < len(self.crew)/2:
            raise ValidationError


if __name__ == "__main__":
    print("=========================================")
    print("Valid mission created:")
    SpaceMission(
        mission_id = "M2024_MARS"
        mission_name = 
        destination
        launch_date
        duration_days
        crew
        mission_status
        budget_millions
    )