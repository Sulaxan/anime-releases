# anime-releases
Discord webhook for notifying new anime releases via livechart.me RSS feeds

## How it works
The webhook does the following processes when it's run:
- Fetch the latest RSS feed from livechart.me (currently does not include `If-Modified-Since` header to save 
  bandwidth/run time -- maybe a future improvement!)
  - Convert XML to a list of `Show` objects
- Filter the shows by ones that have not been notified yet (Redis caches the notified shows for 1 day + 1 hour)
- Go through all the shows and push the notification via Discord webhooks (currently only supports 1 channel)
- Cache the notified shows in Redis with a time-to-live (TTL) of 1 day + 1 hour
  - Livechart.me only returns the broadcasted shows in the last 24 hours, so *theoretically*, by the time the Redis TTL 
    expires, the show should no longer be in the broadcast RSS feed
    - An extra 1 hour is added just to be sure we don't double notify shows
    
### Docker
Docker is used to manage the webhook and the Redis instance. The webhook container has a cronjob that runs every 5 mins to
check for new shows and send out notifications for them. There is also a Redis container used to cache the notified shows.
Technically, the Redis container is optional if you plan to host this yourself and have your own Redis instance you would
like to use. Redis host/port/password/etc., can be changed with environment variables. See [Dockerfile](webhook/Dockerfile),
[docker-compose.yml](webhook/docker-compose.yml), [ar.env](webhook/ar.env), and [ar-cronjob](webhook/ar-crobjob).

## Project Layout / Future
The project, currently, is very simple, and only consists of a webhook. Not knowing where this project might go in the
future, the webhook project is setup with setuptools and exists within its own package to more easily add other packages
in the future. Some possibilities include:
- Converting the webhook into to some script that just pushes new anime-releases through Redis publish-subscribe
  - A bot can then be created that will process the pubsub messages and send the notification out to multiple 
    channels/multiple servers 
