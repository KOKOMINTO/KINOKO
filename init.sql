CREATE TABLE ReactionRole (
	"channel" TEXT,
	"message" TEXT,
	"emoji" TEXT,
	"role" TEXT
);

CREATE TABLE Reminder (
	"channel" TEXT,
	"message" TEXT,
	"time" INT,
	"repeat" INT	
);

CREATE TABLE Welcome(
	"guild" TEXT PRIMARY KEY,
	"channel" TEXT,
	"message" TEXT
);

CREATE TABLE Goodbye(
	"guild" TEXT PRIMARY KEY,
	"channel" TEXT,
	"message" TEXT
);
