Checker bot
====

> The bot for monitoring the entire system. He catches errors and sends a bot in order to
> notify admins and developers about the problem.

```shell
# To test the whole system.
python3 ./Services/check_systems_fast.py --all
python3 ./Services/check_systems_fast.py -a
python3 ./Services/check_systems_fast.py 
# To check the subsystem.
python3 ./Services/check_systems_fast.py --sub 'FINANCE'
python3 ./Services/check_systems_fast.py -s 'FINANCE'
# To test a separate module (Not everyone has it)
python3 ./Services/check_systems_fast.py --sub 'FINANCE' --mod 'TRON'
python3 ./Services/check_systems_fast.py -s 'FINANCE' -m 'TRON'
```

> What subsystems are there:
>> `FINANCE` \
>> Its modules:
>>> `TRON`
>>
>>> `COMING SOON...`
> 
>> `ADMIN` \
>> Its modules:
>>> `SITE`
> 
>> `SERVICES` \
>> Its modules:
>>> `CHECKER`
>>
>>> `COINCER`
>>
>>> `SENDER`
>
>> `BOT`
>>> `BOT_MAIN`
>>
>>> `BOT_ALERT`
