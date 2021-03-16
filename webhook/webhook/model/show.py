import dataclasses
from typing import List


@dataclasses.dataclass
class Show:
    guid: str
    link: str
    title: str
    pub_date: str
    category: str
    enclosure: str
    media_thumbnail: str


@dataclasses.dataclass
class ShowMeta:
    description: str
    tags: List[str]
    studios: List[str]
