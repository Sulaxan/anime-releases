import abc
import dataclasses
import json
from typing import List
from xml.etree import ElementTree

import bs4
import redis
import requests

from model.show import Show, ShowMeta
from service.static import *


class AnimeListService(abc.ABC):
    @abc.abstractmethod
    def get_last_update(self) -> int:
        """Gets the last list update."""

    @abc.abstractmethod
    def set_last_update(self, time):
        """Updates the last updated time to the specified value.

        Args:
            time: The new time to set the last updated time to.
        """

    @abc.abstractmethod
    def is_show_reported(self, show: Show) -> bool:
        """Returns whether a show has been reported

        Args:
            show: The show to check whether or not it has been reported

        Returns:
            True if the show has been reported, False otherwise.
        """

    @abc.abstractmethod
    def set_reported_show(self, show: Show):
        """Sets a show as reported to some persistent store.

        Args:
            show: The show to set as reported.
        """

    @abc.abstractmethod
    def get_show_meta(self, show: Show, default=None) -> ShowMeta:
        """Gets a show's meta from the cache if it exists.

        Args:
            show: The show to get the meta for.
            default: The default value to return if the meta does not exist.

        Returns:
            The show meta if exists, otherwise the None or the default specified value.
        """

    @abc.abstractmethod
    def set_show_meta(self, show: Show, meta: ShowMeta):
        """Sets a show's meta in the cache.

        Args:
            show: The show to set the meta for.
            meta: The meta to set for the show.
        """


class AnimeListFetchService(abc.ABC):
    @abc.abstractmethod
    def fetch_latest_aired_shows(self) -> List[Show]:
        """Fetches all recently aired shows.

        Returns:
            A list of recently aired shows.
        """


class AnimeListParseService(abc.ABC):
    @abc.abstractmethod
    def parse_shows(self, xml: str) -> List[Show]:
        """Parses XML into a list of shows.

        The provided XML must be in the form provided by livechart.me RSS feeds.

        Args:
            xml: The XML as a string.

        Returns:
            The list of shows parsed from the XML.
        """


class AnimeListFilterService(abc.ABC):
    @abc.abstractmethod
    def get_non_reported_shows(self, shows: List[Show]) -> List[Show]:
        """Filters out shows that have already been reported.

        Args:
            shows: The list of shows to filter.

        Returns:
            The filtered list of shows, removing any reported shows.
        """


class AnimeListMetaService(abc.ABC):
    @abc.abstractmethod
    def get_meta(self, show: Show) -> ShowMeta:
        """Fetches the meta for a show.

        Meta is fetched from livechart.me.

        Args:
            show: The show to fetch the meta for.

        Returns:
            The meta for the specified show.
        """


@dataclasses.dataclass
class AnimeListServiceImpl(AnimeListService):
    redis_client: redis.Redis

    def get_last_update(self) -> int:
        return self.redis_client.get(REDIS_LAST_UPDATED_TIME)

    def set_last_update(self, time):
        self.redis_client.set(REDIS_LAST_UPDATED_TIME, time)

    def is_show_reported(self, show: Show) -> bool:
        return self.redis_client.exists(show.guid) > 0

    def set_reported_show(self, show: Show):
        # ensure keys expire after a day (no need to keep them for longer) + add some minor delta just to be sure we
        # don't double report broadcasted shows
        self.redis_client.setex(show.guid, ONE_DAY_DURATION_SECONDS + DURATION_DELTA, REDIS_SHOW_REPORTED)

    def get_show_meta(self, show: Show, default=None) -> ShowMeta:
        json_meta = self.redis_client.get(f"{show.guid}{REDIS_SHOW_META_SUFFIX}")
        if json_meta is None:
            return default

        dict_meta = json.loads(json_meta)
        meta = ShowMeta(**dict_meta)

        return meta

    def set_show_meta(self, show: Show, meta: ShowMeta):
        dict_meta = meta.__dict__
        self.redis_client.setex(f"{show.guid}{REDIS_SHOW_META_SUFFIX}",
                                ONE_DAY_DURATION_SECONDS * 2,
                                json.dumps(dict_meta))


@dataclasses.dataclass
class AnimeListFetchServiceImpl(AnimeListFetchService):
    parse_service: AnimeListParseService

    def fetch_latest_aired_shows(self) -> List[Show]:
        response = requests.get(LIVECHART_URL)
        xml = response.text
        return self.parse_service.parse_shows(xml)


class AnimeListParseServiceImpl(AnimeListParseService):

    def parse_shows(self, xml) -> List[Show]:
        root = ElementTree.fromstring(xml)
        channel_elem = root[0]

        shows = []

        for item in channel_elem.findall("item"):
            guid = item[0].text
            link = item[1].text
            title = item[2].text
            pub_date = item[3].text
            category = item[4].text
            enclosure = item[5].attrib["url"]
            media_thumbnail = item[6].attrib["url"]

            shows.append(Show(
                guid,
                link,
                title,
                pub_date,
                category,
                enclosure,
                media_thumbnail
            ))

        return shows


@dataclasses.dataclass
class AnimeListFilterServiceImpl(AnimeListFilterService):
    anime_list_service: AnimeListService

    def get_non_reported_shows(self, shows: List[Show]) -> List[Show]:
        filtered_shows = []

        for show in shows:
            if self.anime_list_service.is_show_reported(show):
                continue
            filtered_shows.append(show)

        return filtered_shows


class AnimeListMetaServiceImpl(AnimeListMetaService):
    def get_meta(self, show: Show) -> ShowMeta:
        # currently does not work due to CloudFlare preventing scraping
        response = requests.get(show.link)
        page = response.content
        soup = bs4.BeautifulSoup(page, "html.parser")

        # description
        desc_div = soup.find("div", class_="expandable-text-body")
        for child in desc_div.children:
            print(child.text)

        return ShowMeta('', [], [])
