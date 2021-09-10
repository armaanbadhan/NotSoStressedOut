import os
import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

LOGGING_CHANNEL_ID = 885570081483030528

BOT_INVITE = "https://discord.com/api/oauth2/authorize?client_id=804057990096355420&" \
             "permissions=517543943232&scope=bot%20applications.commands"
GITHUB_LINK = "https://github.com/armaanbadhan/NotSoStressedOut"

TOKEN = os.getenv('BOT_TOKEN')

SQLITE_LOCATION = "/reminders.sqlite"


# scheduler
jobstores = {
    "default": SQLAlchemyJobStore(url=f"sqlite://{SQLITE_LOCATION}")
}
job_defaults = {
    "coalesce": True
}
scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    timezone=pytz.timezone("Asia/Kolkata"),
    job_defaults=job_defaults,
)
