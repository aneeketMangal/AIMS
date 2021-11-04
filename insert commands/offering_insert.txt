-- SEM 1, 2019
-- STUDENT CANT ENROLL IN BOTH CS201 AND EE201 (same time slot)

Ins 2:- CALL offer_course('cs201', 1, 2019, '2019csb', 'ABCD00', 'M5', NULL);
Ins 3:- CALL offer_course('cs202', 1, 2019, '2019csb,2019eeb', 'ABCD01', 'M6', NULL);
Ins 1:- CALL offer_course('ee201', 1, 2019, '2019csb,2019eeb', 'ABCD00', 'M6', NULL);
Ins 4:- CALL offer_course('ee202', 1, 2019, '2019csb,2019eeb', 'ABCD02', 'M5', NULL);
Ins 9:- CALL offer_course('ma101', 1, 2019, '2019csb,2019eeb', 'ABCD06', 'M4', NULL);
Ins 5:- CALL offer_course('ge104', 1, 2019, '2019csb,2019eeb', 'ABCD07', 'M2', NULL);
Ins 8:- CALL offer_course('hs101', 1, 2019, '2019eeb', 'ABCD09', 'M3', NULL);


-- SEM 2, 2019

Ins 6:- CALL offer_course('cs203', 2, 2019, '2019csb', 'ABCD00', 'M5', NULL);
Ins 7:- CALL offer_course('cs204', 2, 2019, '2019csb,2019eeb', 'ABCD01', 'M6', NULL);
Ins 9:- CALL offer_course('ma102', 2, 2019, '2019csb,2019eeb', 'ABCD06', 'M4', 5.00);
Ins 1:- CALL offer_course('ee203', 2, 2019, '2019csb,2019eeb', 'ABCD00', 'M5', NULL);
Ins 5:- CALL offer_course('ge204', 2, 2019, '2019csb,2019eeb', 'ABCD07', 'M2', NULL);
Ins 8:- CALL offer_course('hs101', 2, 2019, '2019csb', 'ABCD09', 'M3', NULL);
Ins 8:- CALL offer_course('hs103', 2, 2019, '2019csb,2019eeb', 'ABCD04', 'M3', NULL);


--SEM 1, 2020

Ins 3:- CALL offer_course('cs301', 1, 2020, '2019csb', 'ABCD00', 'M5', NULL);
Ins 7:- CALL offer_course('cs302', 1, 2020, '2019csb', 'ABCD01', 'M5', 7.50);
Ins 6:- CALL offer_course('cs303', 1, 2020, '2019csb,2019eeb', 'ABCD02', 'M6', 8.00);
Ins 1:- CALL offer_course('ee301', 1, 2020, '2019eeb', 'ABCD03', 'M4', NULL);
Ins 4:- CALL offer_course('ee302', 1, 2020, '2019csb,2019eeb', 'ABCD01', 'M3', 7.00);
Ins 8:- CALL offer_course('ee303', 1, 2020, '2019eeb', 'ABCD05', 'M5', NULL);
Ins 10:- CALL offer_course('ph101', 1, 2020, '2019csb,2019eeb', 'ABCD07', 'M4', NULL);

