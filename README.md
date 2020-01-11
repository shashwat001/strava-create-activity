# Strava create activity

Manually create activity TCX file by copying strava activity of another user. Upload the TCX file to reflect activity on the profile.

## Getting Started

1. Login to strava account on the browser.
2. Open config.py and set the value of the cookie with the name given in the first line.
3. Run the script ```main.py``` as follows to get activity TCX in stdout

```
python main.py --activityid=<activity-id> --start=<timestamp>
```
or

```
python main.py -a <activity-id> -s <timestamp>
```
```timestamp``` : timestamp in epoch seconds which you want to set as start time of activity

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

