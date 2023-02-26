# USOS Monitor

---

Checks for changes in selected courses in a registration round (direct classes-groups registrations). Required Selenium
and Chrome Webdriver configured. Saves a session cookie in order to restore a session.

Uses SMTP via SSL to send notifications, tested with Gmail.

Algorithm works for Warsaw University of Technology (WUT/PW) PE registrations. Might not work on other universities'
websites.

Notifications are sent in one of the scenarios:

1. New group created for a course (or if history file didn't exist)
2. Increased/decreased number of free places in a group

Number of free places is calculated using a formula:

`new.max - new.registered - (old.max - old.registered)`

where `new` is new data downloaded from USOS, `old` - data saved last time.

### Configuration

1. Rename `config_template.py` to `config.py` and fill out missing values.
2. Run `main.py`