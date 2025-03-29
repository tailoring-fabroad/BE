from typing import List

from src.app.common import DateTimeModelMixin, IDModelMixin
from src.app.models import RWModel

class Article(IDModelMixin, DateTimeModelMixin, RWModel):
    slug: str
    title: str
    description: str
    body: str
    # image: str
    tags: List[str]
    # author: Profile
    favorited: bool
    favorites_count: int
