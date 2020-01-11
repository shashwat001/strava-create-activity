# Strava create activity

Manually create activity TCX file by copying strava activity of another user. Upload the TCX file to reflect activity on the profile.

## Getting Started

1. Login to strava account on the browser.
2. Open config.py and set the value of the cookie with the name given in the first line.
3. Run the script ```main.py``` as follow to get activity TCX in stdout

```
python main.py --activity=<activity-id> --start=<timestamp>
```
```timestamp``` : timestamp in epoch seconds which you want to set as start time of activity

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

