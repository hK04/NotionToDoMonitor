# NotionToDoMonitor

1. To set up `main.py` it's necessary to obtain a notion's [secret token](https://www.notion.so/profile/integrations) and database id and put them into `settings.json` as:

```json
{
    "token" : "YOUR TOKEN",
    "databaseID" : "YOUR DATABASE"
}
```

2. To use an analysis pipeline you should download data from your database into `data.csv` and use it as described in `analysis.ipynb` 
