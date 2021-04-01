"""File of constants."""
import os

PREFIX = "anime_releases"

REDIS_LAST_UPDATED_TIME = f"{PREFIX}_last_update_time"
REDIS_SHOW_REPORTED = "reported"
REDIS_SHOW_META_SUFFIX = "_meta"

ONE_DAY_DURATION_SECONDS = 60 * 60 * 24
DURATION_DELTA = 60 * 60  # 1 hour

# environment variables
LIVECHART_URL = os.getenv("AR_LIVECHART_URL", default="https://www.livechart.me/feeds/episodes")
WEBHOOK_URL = os.getenv("AR_WEBHOOK_URL", default="https://discord.com/api/webhooks/819795945562046475/BtYm_ORYmJqCw7tvgL4TenvQW65vQmPq3Oabi_xcKMVOxHv3XcNEdkvUBKq-E-FbtEuV")
