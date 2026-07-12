-- SQLite schema (ported from create_table.sql / SQL Server)
-- Type mapping: IDENTITY -> AUTOINCREMENT, VARCHAR/NVARCHAR -> TEXT,
-- DATETIME DEFAULT GETDATE() -> TEXT DEFAULT CURRENT_TIMESTAMP,
-- UNIQUEIDENTIFIER -> TEXT, BIT -> INTEGER, DECIMAL -> REAL, DATE -> TEXT (ISO).

PRAGMA foreign_keys = ON;

CREATE TABLE dim_project (
    project_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    project_code    TEXT NOT NULL UNIQUE,
    project_name    TEXT NOT NULL,
    project_country TEXT,
    project_location TEXT,
    created_date    TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date   TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_work_package (
    work_package_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    work_package_code TEXT NOT NULL UNIQUE,
    work_package_name TEXT NOT NULL,
    wbs               TEXT,
    created_date      TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date     TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_equipment (
    equipment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_code TEXT NOT NULL UNIQUE,
    equipment_name TEXT NOT NULL,
    equipment_type TEXT,
    specifications TEXT,
    created_date   TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date  TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_milestone (
    milestone_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    milestone_number      TEXT,
    milestone_activity    TEXT NOT NULL,
    milestone_description TEXT,
    created_date          TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date         TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (milestone_activity, milestone_description)
);

CREATE TABLE dim_supplier (
    supplier_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_number TEXT NOT NULL UNIQUE,
    supplier_name   TEXT NOT NULL,
    contact_name    TEXT,
    contact_number  TEXT,
    email_address   TEXT,
    created_date    TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date   TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_equipment_supplier (
    equipment_supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id  INTEGER NOT NULL,
    supplier_id   INTEGER NOT NULL,
    unit_cost     REAL NOT NULL,
    is_preferred  INTEGER DEFAULT 0,
    lead_time_days INTEGER,
    remarks       TEXT,
    created_date  TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES dim_equipment(equipment_id),
    FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id),
    UNIQUE (equipment_id, supplier_id)
);

CREATE TABLE fact_purchase_order (
    purchase_order_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_order_number TEXT NOT NULL,
    line_item        TEXT,
    project_id       INTEGER NOT NULL,
    work_package_id  INTEGER NOT NULL,
    supplier_id      INTEGER NOT NULL,
    equipment_id     INTEGER NOT NULL,
    short_text       TEXT,
    remarks          TEXT,
    amount           REAL,
    created_date     TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date    TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES dim_project(project_id),
    FOREIGN KEY (work_package_id) REFERENCES dim_work_package(work_package_id),
    FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id),
    FOREIGN KEY (equipment_id) REFERENCES dim_equipment(equipment_id),
    UNIQUE (purchase_order_number, line_item)
);

CREATE TABLE fact_p6_schedule (
    p6_schedule_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id           INTEGER NOT NULL,
    work_package_id      INTEGER NOT NULL,
    equipment_id         INTEGER NOT NULL,
    milestone_id         INTEGER NOT NULL,
    p6_schedule_due_date TEXT NOT NULL,
    created_date         TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date        TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES dim_project(project_id),
    FOREIGN KEY (work_package_id) REFERENCES dim_work_package(work_package_id),
    FOREIGN KEY (equipment_id) REFERENCES dim_equipment(equipment_id),
    FOREIGN KEY (milestone_id) REFERENCES dim_milestone(milestone_id)
);

CREATE TABLE fact_equipment_milestone_schedule (
    equipment_milestone_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id      INTEGER NOT NULL,
    project_id        INTEGER NOT NULL,
    work_package_id   INTEGER NOT NULL,
    milestone_id      INTEGER NOT NULL,
    purchase_order_id INTEGER,
    equipment_milestone_due_date TEXT NOT NULL,
    status            TEXT DEFAULT 'Active',
    created_date      TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date     TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES dim_equipment(equipment_id),
    FOREIGN KEY (project_id) REFERENCES dim_project(project_id),
    FOREIGN KEY (work_package_id) REFERENCES dim_work_package(work_package_id),
    FOREIGN KEY (milestone_id) REFERENCES dim_milestone(milestone_id),
    FOREIGN KEY (purchase_order_id) REFERENCES fact_purchase_order(purchase_order_id)
);

CREATE TABLE dim_manufacturing_location (
    manufacturing_location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id     INTEGER NOT NULL,
    supplier_id      INTEGER NOT NULL,
    location_address TEXT NOT NULL,
    created_date     TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date    TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES dim_equipment(equipment_id),
    FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id)
);

CREATE TABLE dim_logistics_info (
    logistics_info_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id      INTEGER NOT NULL,
    supplier_id       INTEGER NOT NULL,
    logistics_method  TEXT NOT NULL,
    shipping_port     TEXT,
    receiving_port    TEXT,
    created_date      TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date     TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES dim_equipment(equipment_id),
    FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id)
);

-- Agent / logging tables
CREATE TABLE dim_agent_event_log (
    log_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id        TEXT NOT NULL,
    agent_name      TEXT NOT NULL,
    event_time      TEXT NOT NULL,
    action          TEXT NOT NULL,
    result_summary  TEXT,
    user_query      TEXT,
    agent_output    TEXT,
    conversation_id TEXT NOT NULL,
    session_id      TEXT,
    created_date    TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_agent_thinking_log (
    thinking_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name            TEXT NOT NULL,
    thinking_stage        TEXT NOT NULL,
    thought_content       TEXT NOT NULL,
    thinking_stage_output TEXT,
    agent_output          TEXT,
    conversation_id       TEXT NOT NULL,
    session_id            TEXT,
    agent_ref_id        TEXT,
    model_deployment_name TEXT,
    thread_id             TEXT,
    user_query            TEXT,
    status                TEXT DEFAULT 'success',
    created_date          TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_risk_report (
    report_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL,
    conversation_id TEXT NOT NULL,
    filename        TEXT NOT NULL,
    blob_url        TEXT NOT NULL,
    report_type     TEXT DEFAULT 'comprehensive',
    created_date    TEXT DEFAULT CURRENT_TIMESTAMP
);
