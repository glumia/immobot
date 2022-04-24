## yet another immobot

Get notified on Telegram when there are new ads for your search on Immobiliare.

Clone repository into your user's home directory, create a `.env` into it
for its configuration (take a look at `.env.example`), then use `crontab -e` and
add `*/15 * * * * cd immobot && . ./.env && ./immobot.py 2>&1 >> immobot.log` to
set up a cron job for immobot.

Note: this is of course an ugly and hacky solution, yet it is better than mobile app's
push notifications that arrive after more than 24h or do not arrive at all sometimes.
