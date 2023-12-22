CREATE TABLE IF NOT EXISTS check_in (
id INTEGER PRIMARY KEY AUTOINCREMENT,
partner_id_bitmap INTEGER,
date INTEGER
);

CREATE TABLE IF NOT EXISTS discuss_action_points (
id INTEGER PRIMARY KEY AUTOINCREMENT,
check_in_id INTEGER,
agenda_item_id INTEGER,
agenda_extra TEXT,
action_point_partner_id INTEGER,
is_resolved INTEGER,
point_descr TEXT
);

CREATE TABLE IF NOT EXISTS partner (
id INTEGER PRIMARY KEY AUTOINCREMENT,
partner_name TEXT
);

CREATE TABLE IF NOT EXISTS agenda_item (
id INTEGER PRIMARY KEY AUTOINCREMENT,
item_descr TEXT
);

INSERT into agenda_item (item_descr)
VALUES 
("Quality Time"),
("Sex"),
("Physical & Mental Health"),
("Other Partners & Friends"),
("Fights & Arguments"),
("Money"),
("Work & Projects"),
("Future Plans"),
("Family & Chosen Family"),
("Household");
