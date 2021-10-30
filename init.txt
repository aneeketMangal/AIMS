CREATE DATABASE aims;

\c aims;

CREATE ROLE deanoffice
LOGIN
PASSWORD 'deanoffice';

CREATE ROLE faculty;
CREATE ROLE student;

--INSTRUCTOR USER NAME MUST BE '_' + INS_ID (HIS OR HER id), RATHER THAN THEIR NAME (eg, if puneet has id = 34, username = _34)