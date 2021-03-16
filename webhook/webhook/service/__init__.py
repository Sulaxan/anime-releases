from service.anime_list_discord_service import AnimeListEmbedServiceImpl, AnimeListDiscordPushServiceImpl
from service.anime_list_service import (
    AnimeListServiceImpl,
    AnimeListFetchServiceImpl,
    AnimeListParseServiceImpl,
    AnimeListFilterServiceImpl,
    AnimeListMetaServiceImpl
)

import redis


redis_client = redis.Redis()

anime_list_parse_service = AnimeListParseServiceImpl()
anime_list_fetch_service = AnimeListFetchServiceImpl(anime_list_parse_service)
anime_list_service = AnimeListServiceImpl(redis_client)
anime_list_filter_service = AnimeListFilterServiceImpl(anime_list_service)
anime_list_meta_service = AnimeListMetaServiceImpl()

anime_list_embed_service = AnimeListEmbedServiceImpl()
anime_list_discord_push_service = AnimeListDiscordPushServiceImpl()

