from pydantic import BaseModel, Field, ConfigDict
import datetime
from typing import Literal, Union, List, Annotated
class CreatePost(BaseModel):
    text: str = Field(min_length=1)
    created_at: datetime.datetime = Field(default=datetime.datetime.now)

class AllPost(BaseModel):
    name: str 
    content: list[dict] 
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)



class UsersPostsModel(BaseModel):
    id: int
    content: list[dict] 
    created_at: datetime.datetime
    #name: str = Field()
    model_config = ConfigDict(from_attributes=True)

class TextBlock(BaseModel):
    type: Literal['text']
    value: str

class ImageBlock(BaseModel):
    type: Literal['image']
    url: str

BlockType = Annotated[
    Union[TextBlock, ImageBlock], 
    Field(discriminator="type")
]


# Итоговая схема поста
class PostCreate(BaseModel):
    created_at: datetime.datetime = Field(default=datetime.datetime.now)
    content_blocks: List[BlockType]

     

