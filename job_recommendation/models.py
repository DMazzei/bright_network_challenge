from pydantic import BaseModel


class Member(BaseModel):
    name: str
    bio: str

    def __str__(self) -> str:
        return f"{self.name}"


class Job(BaseModel):
    title: str
    location: str

    def __repr__(self) -> str:
        return f"{self.title} ({self.location})"

