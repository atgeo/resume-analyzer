from pydantic import BaseModel, computed_field, Field, EmailStr


class Job(BaseModel):
    company: str = Field(description="Employer name")
    title: str = Field(description="Job title")
    start_date: str | None = Field(default=None, description="Start date")
    end_date: str | None = Field(default=None, description="End date")
    is_current: bool = Field(default=False, description="Whether this is the person's current job")


class Education(BaseModel):
    institution: str = Field(description="School or university name")
    degree: str | None = Field(default=None, description="Degree obtained")
    field_of_study: str | None = Field(default=None, description="Major or field of study")
    start_date: str | None = Field(default=None, description="Start date")
    end_date: str | None = Field(default=None, description="End date")


class ResumeSummary(BaseModel):
    first_name: str = Field(description="First name")
    middle_name: str | None = Field(default=None, description="Middle name")
    last_name: str = Field(description="Last name")
    email: EmailStr = Field(description="Email address")
    phone: str | None = Field(default=None, description="Phone number")
    jobs: list[Job] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)

    @computed_field
    @property
    def is_currently_working(self) -> bool:
        return any(job.is_current for job in self.jobs)
