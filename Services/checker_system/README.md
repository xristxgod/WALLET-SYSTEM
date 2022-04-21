Checker bot
====

> The bot for monitoring the entire system. He catches errors and sends a bot in order to
> notify admins and developers about the problem.

```shell
# To test the whole system.
python3 check_systems_fast.py --all
python3 check_systems_fast.py -a
# To check the subsystem.
python3 check_systems_fast.py --sub 'FINANCE'
python3 check_systems_fast.py -s 'FINANCE'
# To test a separate module (Not everyone has it)
python3 check_systems_fast.py --sub 'FINANCE' --module 'TRON'
python3 check_systems_fast.py -s 'FINANCE' -m 'TRON'
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
>>> `BOT`
>>
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