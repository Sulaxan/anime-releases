import time

import service
from model.discord.message import Message


def main():
    shows = service.anime_list_fetch_service.fetch_latest_aired_shows()
    non_reported_shows = service.anime_list_filter_service.get_non_reported_shows(shows)
    for show in non_reported_shows:
        embed = service.anime_list_embed_service.get_embed(show)
        service.anime_list_service.set_reported_show(show)
        service.anime_list_discord_push_service.send_message(Message(embeds=[embed]))
        time.sleep(0.5)  # need to wait to prevent being rate limited


if __name__ == '__main__':
    main()
