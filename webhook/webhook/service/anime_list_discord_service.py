import abc
import dataclasses
import datetime
import json

import requests

from model.show import Show
from model.discord.embed import Embed, UrlImage, Footer
from model.discord.message import Message
from service.static import WEBHOOK_URL


class AnimeListEmbedService(abc.ABC):
    @abc.abstractmethod
    def get_embed(self, show: Show) -> Embed:
        """Gets an discord for a show."""


class AnimeListDiscordPushService(abc.ABC):
    @abc.abstractmethod
    def send_message(self, message: Message):
        """Pushes a message to Discord.

        Currently uses a static webhook URL.
        """


@dataclasses.dataclass
class AnimeListEmbedServiceImpl(AnimeListEmbedService):
    def get_embed(self, show: Show) -> Embed:
        return Embed(
            title=show.title,
            description=f"Out now: {show.category}"
                        f"\n\n"
                        f"Published Date: {show.pub_date}"
                        f"\n\n"
                        f"[View on Livechart]({show.guid}) | [View General Info]({show.link})",
            thumbnail=UrlImage(show.media_thumbnail),
            footer=Footer('Broadcast information provided by livechart.me.'),
            timestamp=f"{str(datetime.datetime.now())}"
        )


@dataclasses.dataclass
class AnimeListDiscordPushServiceImpl(AnimeListDiscordPushService):
    def send_message(self, message: Message):
        headers = {
            "Content-Type": "application/json"
        }

        dict = message.to_dict()
        requests.post(WEBHOOK_URL, data=json.dumps(dict), headers=headers)
