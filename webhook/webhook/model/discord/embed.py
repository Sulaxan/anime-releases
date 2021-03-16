import dataclasses
from typing import Dict, List, Any, Optional

from model.discord.util import set_or_del, del_if_none


@dataclasses.dataclass
class Author:
    name: str
    url: str
    icon_url: str


@dataclasses.dataclass
class Footer:
    text: str
    icon_url: str = None

    def to_dict(self) -> Dict[str, Any]:
        dict = self.__dict__
        del_if_none(self.icon_url, dict, 'icon_url')
        return dict


@dataclasses.dataclass
class UrlImage:
    url: str


@dataclasses.dataclass
class Field:
    name: str
    value: str
    inline: bool


@dataclasses.dataclass
class Embed:
    title: str = None
    description: str = None
    timestamp: str = None
    color: int = 0
    author: Author = None
    footer: Footer = None
    thumbnail: UrlImage = None
    image: UrlImage = None
    fields: Optional[List[Field]] = None

    def to_dict(self) -> Dict[str, Any]:
        dict = self.__dict__

        del_if_none(self.title, 'title', dict)
        del_if_none(self.description, 'description', dict)
        del_if_none(self.timestamp, 'timestamp', dict)
        del_if_none(self.color, 'color', dict)
        set_or_del(self.author, 'author', dict, lambda: self.author.__dict__)
        set_or_del(self.footer, 'footer', dict, lambda: self.footer.__dict__)
        set_or_del(self.thumbnail, 'thumbnail', dict, lambda: self.thumbnail.__dict__)
        set_or_del(self.image, 'image', dict, lambda: self.image.__dict__)
        set_or_del(self.fields, 'fields', dict, lambda: [field.__dict__ for field in self.fields])

        return dict
