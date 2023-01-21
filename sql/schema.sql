PRAGMA foreign_keys = ON;

CREATE TABLE kvpairs(
  key VARCHAR(20) NOT NULL,
  value VARCHAR(40) NOT NULL,
  PRIMARY KEY(key)
);

CREATE TABLE files(
  filename VARCHAR(20) NOT NULL,
  PRIMARY KEY(filename)
);