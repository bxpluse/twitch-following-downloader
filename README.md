# twitch-following-downloader

## Web App
View and optionally download a CSV file of all channels a user follows with follow dates.

https://twitch-following-downloader.herokuapp.com/

## Install locally

### Get API token

Go to [dev.twitch](https://dev.twitch.tv/docs/v5/) to get a client id and client secret. Then fill in the fields in ```config.py```.

### Deploying the single page application

```
export FLASK_APP=app.py
flask run
```

### Running from the command line

```
python following.py [username]
```
