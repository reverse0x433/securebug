CREATE TABLE "users"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT UNIQUE NOT NULL,
    "role" TEXT NOT NULL
);

CREATE TABLE "bugs"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "severity" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "reporter_id" INTEGER NOT NULL,
    "assignee_id" INTEGER,
    FOREIGN KEY("reporter_id") REFERENCES "users"("id"),
    FOREIGN KEY("assignee_id") REFERENCES "users"("id")
);

CREATE TABLE "audit_logs"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "actor_id" INTEGER NOT NULL,
    "action" TEXT NOT NULL,
    "target_type" TEXT NOT NULL,
    "target_id" INTEGER NOT NULL,
    "old_value" TEXT NOT NULL,
    "new_value" TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY("actor_id") REFERENCES "users"("id")
);

