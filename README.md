# Long Beach tweet_archive
This project intends to archive Tweets from significant players in civic Long Beach for historical interest.

Tweets are stored in JSON format, sequentially, within the _data directory in a subdirectory named for the Twitter account.

This project is an activity of [HackLB](https://github.com/HackLB).

### secrets.json
You'll need to setup Twitter credentials and then store them in a secrets.json in the repo directory (it'll be gitignored) using the following format:

```
{ 
	"api-key": "YOUR-API-KEY-HERE",
	"api-secret": "YOUR-API-SECRET-HERE",
	"token-key": "YOUR-TOKEN-HERE",
	"token-secret": "YOUR-TOKEN-SECRET-HERE"
}
```