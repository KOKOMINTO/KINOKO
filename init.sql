CREATE TABLE ReactionRole (
	"channel" TEXT,
	"message" TEXT,
	"emoji" TEXT,
	"role" TEXT
);

CREATE TABLE Reminder (
	"channel" TEXT,
	"message" TEXT,
	"time" DATETIME,
	"delay" INT	
);
