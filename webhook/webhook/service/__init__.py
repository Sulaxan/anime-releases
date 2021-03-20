import os

import redis
from service.anime_list_discord_service import AnimeListEmbedServiceImpl, AnimeListDiscordPushServiceImpl
from service.anime_list_service import (
    AnimeListServiceImpl,
    AnimeListFetchServiceImpl,
    AnimeListParseServiceImpl,
    AnimeListFilterServiceImpl,
    AnimeListMetaServiceImpl
)

REDIS_HOST = os.getenv("AR_REDIS_HOST")
REDIS_PORT = os.getenv("AR_REDIS_PORT")
REDIS_USERNAME = os.getenv("AR_REDIS_USERNAME", default=None)
REDIS_PASSWORD = os.getenv("AR_REDIS_PASSWORD", default=None)

redis_client = redis.Redis(host=REDIS_HOST,
                           port=int(REDIS_PORT),
                           username=REDIS_USERNAME,
                           password=REDIS_PASSWORD)

anime_list_parse_service = AnimeListParseServiceImpl()
anime_list_fetch_service = AnimeListFetchServiceImpl(anime_list_parse_service)
anime_list_service = AnimeListServiceImpl(redis_client)
anime_list_filter_service = AnimeListFilterServiceImpl(anime_list_service)
anime_list_meta_service = AnimeListMetaServiceImpl()

anime_list_embed_service = AnimeListEmbedServiceImpl()
anime_list_discord_push_service = AnimeListDiscordPushServiceImpl()

