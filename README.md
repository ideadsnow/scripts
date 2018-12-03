# scripts

CREATE TABLE lsh (
    id        INT NOT NULL DEFAULT unique_rowid(),
    app_name       string(64),
    lsh         STRING(64),
    union_id   STRING(64),
    CONSTRAINT "primary" PRIMARY KEY (id ASC),
    UNIQUE INDEX uk_app_union (app_name ASC, lsh ASC, union_id ASC),
    FAMILY "primary" (id, app_name, lsh, union_id)
);
