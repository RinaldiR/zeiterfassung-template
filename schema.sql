-- Datenmodell der Zeiterfassung.
-- Wird mit "flask --app app init-db" ausgeführt. Damit das wiederholt
-- funktioniert, zuerst jede Tabelle löschen und dann neu anlegen:
--
--   DROP TABLE IF EXISTS tabellenname;
--   CREATE TABLE tabellenname (
--       id INTEGER PRIMARY KEY AUTOINCREMENT,
--       ...
--   );

-- Löscht Tabelle, falls es diese schon gibt
DROP TABLE IF EXISTS project;

-- Legt neue Tabelle an.
CREATE TABLE project (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,  -- Interne ID, zählt automatisch hoch
    number TEXT    NOT NULL UNIQUE,            -- Projekt Nummer, z.B. '1'; UNIQUE = keine Duplikate!
    name   TEXT    NOT NULL                    -- Projekt Name, z.B. 'Testing'
);

-- Startdaten: diese Projekte werden direkt nach "init-db" erstellt
INSERT INTO project (number, name) VALUES
    ('1', 'Hourly'),
    ('2', 'Testing'),
    ('3', 'Documentation');