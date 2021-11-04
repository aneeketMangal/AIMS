INSERT INTO instructor(id, name, dept) VALUES (1,'ipvnd','eed');
INSERT INTO instructor(id, name, dept) VALUES (2,'goi','csd');
INSERT INTO instructor(id, name, dept) VALUES (3,'qtngviq','csd');
INSERT INTO instructor(id, name, dept) VALUES (4,'wnpvon','eed');
INSERT INTO instructor(id, name, dept) VALUES (5,'xrkzzc','mcd');
INSERT INTO instructor(id, name, dept) VALUES (6,'qnds','csd');
INSERT INTO instructor(id, name, dept) VALUES (7,'jjiyfomsdv','csd');
INSERT INTO instructor(id, name, dept) VALUES (8,'wwh','eed');
INSERT INTO instructor(id, name, dept) VALUES (9,'zhtbp','mcd');
INSERT INTO instructor(id, name, dept) VALUES (10,'zmqz','mcd');

GRANT ALL
ON batches
TO deanoffice;

GRANT SELECT
ON batches
TO faculty, student; 