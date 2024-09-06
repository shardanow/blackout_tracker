# Changelog

All notable changes to this project will be documented in this file.

## [0.0.2b] - 2024-09-06
### Added
- Refactor and rebuild code and project structure.
- Rework outage information in notifications.
- Add logger utility that could be turned on/off with log file or not from [config.json](config.json) 
- Add [CHANGELOG.md](CHANGELOG.md) and [README.md](README.md) 
- Add user notification with configurable minutes from [config.json](config.json) (MINUTES_BEFORE_TO_NOTIFY_USER_BLACKOUT) before electricity outage. Also interval for checking schedule could be changed in MINUTES_TO_CHECK_SCHEDULE

## [0.0.1b] - 2024-09-05
- Initial release with basic outage schedule fetching and notification functionality.