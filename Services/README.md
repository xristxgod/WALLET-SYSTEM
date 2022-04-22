Working with auxiliary services
=======

---
> `Services/checker_system` - The service for notifying about errors and checking the operability of other systems. The messages come in Bot Alert.
---
> `Services/sender_messages` - The service notifies users about any events. Write an example about the replenishment of the balance. And not only.
---
> `Services/coins_monitor` - The service for collecting information about currencies
---

```shell
>> START:
docker-compose --file Services/services-docker-compose.yml up --build
>> STOP:
docker-compose --file Services/services-docker-compose.yml stop

>> Or you can run a bash script: 
>> START:
bash Services/run.sh
>> STOP:
bash Services/stop.sh
```