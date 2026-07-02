# Database module

This folder contains the SQL schema, migrations, and an initializer script for the application's database.

Usage:

 - Validate schema in-memory:

```
python apps/database/init_db.py --validate
```

 - Create the runtime SQLite DB and seed sample data:

```
python apps/database/init_db.py --init
```

Persistent DB path: `apps/database/app.db`
