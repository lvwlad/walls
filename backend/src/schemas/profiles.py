from pydantic import BaseModel, ConfigDict

class ProfileData(BaseModel):
    bio: str
    quote : str
    tags: list[str]
    avatar: str
    banner: str
    theme_color: str
    model_config = ConfigDict(from_attributes=True)