INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('cs201','DS',3,1,2,5,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('cs202','PPP',3,1,2,5,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('cs203','DLD',3,3,1,1,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('cs204','CA',1,2,3,1,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('cs301','DBMS',4,2,3,5,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('cs303','OS',3,2,4,4,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('cs302','Algo',3,1,2,3,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ma101','Calculus',4,1,4,2,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ma102','LA',4,3,2,3,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ph101','Physics',3,4,1,1,5);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ee201','Elec21',3,4,1,1,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ee202','Elec22',3,4,1,1,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ee203','Elec23',3,4,1,1,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ee301','Elec31',3,4,1,1,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ee302','Elec32',3,4,1,1,5);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ee303','Elec33',3,4,1,1,4);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ge104','Gen14',3,4,1,1,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('ge204','Gen24',3,4,1,1,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('hs101','Hs11',3,4,1,1,3);
INSERT INTO courses(course_id, Title, L, T, P, S, C) VALUES ('hs103','Hs13',3,4,1,1,3);


INSERT INTO prereq(course_id, prereq_id) VALUES ('cs301','cs201');
INSERT INTO prereq(course_id, prereq_id) VALUES ('cs302','cs202');
INSERT INTO prereq(course_id, prereq_id) VALUES ('cs303','cs203');
