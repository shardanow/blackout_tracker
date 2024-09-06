# Blackout Tracker Bot

Blackout Tracker Bot is a Telegram bot that provides users with the schedule of **electricity outages** in **Івано-Франківськ** for **today** and **tomorrow**, fetched from an external API. Additionally, it **notifies** users a few minutes **before the electricity is scheduled to be turned off** in their area.

## Features

- **Today's Schedule**: Provides the current day's electricity outage schedule.
- **Tomorrow's Schedule**: Fetches and displays the electricity outage schedule for the next day.
- **Notification Alerts**: Sends notifications to users configured amount of minutes before a scheduled outage is about to begin.
- **Schedules Data**: All schedules data was saved in schedules dir in jspn format with according date in file name.

## How It Works

1. **Fetch Schedule**: The bot fetches the electricity outage schedule for today and tomorrow from an external API.
2. **Display Schedule**: Users can get the schedule for today or tomorrow, the bot will send message with the outage details.
3. **Notify Users**: The bot will automatically send a notification to users a set number of minutes before an outage occurs, ensuring they are aware in advance.
   
## Installation

1. Clone the repository or download the project files.
2. Install all custom python libraries that used in code.
3. Create config.json in project root dirrectory and fill it in with variables from example bellow. Values you could change by your vision:
```bash
{
    "TELEGRAM_BOT_TOKEN": "YOUR_TG_BOT_TOKEN",
    "USER_ADRESS": "Town,StreetName,BuildungNumber",
    "MINUTES_TO_CHECK_SCHEDULE_UPDATE": 5,
    "MINUTES_TO_CHECK_SCHEDULE": 2,
    "MINUTES_BEFORE_TO_NOTIFY_USER_BLACKOUT": 15,
    "SCHEDULES_FOLDER": "schedules",
    "DEBUG": true,
    "DEBUG_SAVE_FILE": false
}
```
4. Run it.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for details on all updates and changes.