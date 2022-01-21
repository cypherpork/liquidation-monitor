# liquidation-monitor
You can create events tracking price changes for the currency you are interested in on **oassis.com** and other similar sites

### installing dependencies:
```pip install selenium``` and

```pip install configparser``` and

and install [geckodriver](https://github.com/mozilla/geckodriver/releases) for you OS

#### Make sure to edit the config file: ```nano example-config.conf``` or ```vim example-config.conf```

#### And rename to **config.conf**: ```mv example-config.conf config.conf```

### Setup linux and Mac

create crontab config file:

```cd ~/``` and

```nano ~/.crontab``` or ```vim ~/.crontab```

Add the check period you need:

```*/5 * * * * python /path/to/directory/scrpt/liquidation-monitor/checker.py > /dev/null 2>&1```

here i have set run every 5 minutes

 Update you task list

 ```crontab ~/.crontab```

 and be sure to check that your task is on the list

 ```crontab -l```
