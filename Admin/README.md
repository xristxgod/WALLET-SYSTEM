Services for admin!
====

---
> `Admin/admin_bot` - The bot serves exclusively for the admin. Catching bugs in other services and notifying about events.
---
> `Admin/admin_site` - Admin panel for entering statistics. Dashboard and others.
---

```shell
>> START:
docker-compose --file Admin/admin_bot/admin-site-docker-compose.yml up --build
>> STOP:
docker-compose --file Admin/admin_bot/admin-site-docker-compose.yml stop

>> Or you can run a bash script: 
>> START:
bash Admin/run.sh
>> STOP:
bash Admin/stop.sh
```