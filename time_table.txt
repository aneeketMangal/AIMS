CREATE TABLE time_table
(
    slot_type char(6) NOT NULL,
    day char(3) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    PRIMARY KEY(day, start_time),
    FOREIGN KEY(slot_type) REFERENCES timeslots(slot_type)
);

GRANT ALL
ON time_table
TO deanoffice;

GRANT SELECT
ON time_table
TO faculty, student;
