import dataclasses
from typing import Any, Dict, List

from model.discord.embed import Embed
from model.discord.util import del_if_none, set_or_del


@dataclasses.dataclass
class Message:
    content: str = None
    embeds: List[Embed] = None

    def to_dict(self) -> Dict[str, Any]:
        dict = self.__dict__
        del_if_none(self.content, 'content', dict)
        set_or_del(self.embeds, 'embeds', dict, lambda: [embed.to_dict() for embed in self.embeds])
        return dict
