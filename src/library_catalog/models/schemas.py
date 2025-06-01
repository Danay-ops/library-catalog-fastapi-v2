from typing import Optional
from pydantic import BaseModel

class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None
    genre: str
    pages: int
    available: bool = True
    description: Optional[str] = None
    cover_url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
