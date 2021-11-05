--transcript_2019csb1124

CREATE OR REPLACE FUNCTION request_enrolment
(
	off_id course_offering.id%type,
	st_id students.id%type,
	curr_semester course_offering.semester%type,
	curr_year course_offering.year%type
)
RETURNS VOID
LANGUAGE PLPGSQL
SECURITY DEFINER
AS $$
DECLARE
	offering_row record;
	student_row record;
	credit_limit float8;
	temp record;	
	ifUser boolean := false;	
	st_batch char(7);	
	transcript_name text;
	course_check_command text;
	credit_calculate_command text;
	row_exist boolean;
	prev_year integer;
	prev_sem_credit float8;
	curr_sem_credit float8;
	course_credit float8;
	prereq_cursor refcursor;
	prereq_row record;
BEGIN
	--check if student invoking function is same
	
	ifUser := false;

	if st_id=substr(session_user,2) then
		ifUser := true;
	end if;	
	
	if session_user = 'deanoffice' then
		ifUser	:= true;
	end if;

	if ifUser=false then
		RAISE EXCEPTION 'Cannot create request for other user';
	end if;

	select * from course_offering 
	into offering_row
	where id=off_id and semester=curr_semester and year=curr_year;
	
	if not found then
		RAISE EXCEPTION 'current offering with id % not found',off_id;	
	end if;
		
	select * from students
	into student_row
	where id=st_id;

	if not found then
		RAISE EXCEPTION 'student with id % not found',st_id;	
	end if;
	
	select * from enrol E, course_offering O
	into temp
	where 
	E.offering_id = O.id
	and E.student_id = st_id
	and O.semester=curr_semester
	and O.year=curr_year
	and O.slot=offering_row.slot;

	if found then
		RAISE EXCEPTION '% has enroled course in same time slot',st_id;
	end if;	

	st_batch := CAST(student_row.batch AS char(4))||student_row.dept;
	select * from batch_constraint B
	into temp
	where
	B.id=off_id
	and B.batch=st_batch;

	if not found then
		RAISE EXCEPTION 'Your batch has not been allowed by instructor to enrol';
	end if;
	
	--have not done course before
	transcript_name:= 'transcript_'||st_id;
	course_check_command := 'SELECT EXISTS(SELECT * FROM ' || transcript_name || ' T, course_offering O WHERE T.off_id=O.id and O.course_id='''||offering_row.course_id||''' and T.grade!=''F'');';	
	EXECUTE course_check_command into row_exist;	

	if row_exist then
		RAISE EXCEPTION 'student % has done this course before',st_id;
	end if;

	--prerequisite check
	open prereq_cursor FOR EXECUTE 'SELECT * FROM prereq P where P.course_id='''||offering_row.course_id||''';';				
	LOOP 
		FETCH prereq_cursor INTO prereq_row;
		EXIT when not found;
		
		course_check_command := 'SELECT EXISTS(SELECT * FROM '||transcript_name||' T, course_offering O where T.off_id=O.id and O.course_id='''||prereq_row.prereq_id||''' and T.grade!=''F'') ;';
		EXECUTE course_check_command INTO row_exist;
		if not row_exist then
			RAISE EXCEPTION 'prerequiste course % not completed yet',prereq_row.prereq_id;
		end if;

	END LOOP;



	
	--cgpa check
	if offering_row.CGPA is not NULL then
		if cgpa_calculation(st_id)<offering_row.CGPA then
			RAISE EXCEPTION 'CGPA of student is less than minimum required CGPA';
		end if;
	end if;
			

	--credit limit check	
	if curr_year=student_row.batch then
		credit_limit := 18.0;
	else 
		prev_year:= curr_year-1;
		if curr_semester=1 then

			credit_calculate_command := 'SELECT sum(C) from '||transcript_name||' T, course_offering O, courses C where T.off_id=O.id and O.course_id=C.course_id and O.year='||prev_year||'and T.grade!=''F'' group by O.year;';								
			EXECUTE credit_calculate_command into credit_limit;

			if credit_limit is NULL then
				credit_limit := 0;
			end if;
		else

			credit_calculate_command := 'SELECT sum(C) from '||transcript_name||' T, course_offering O, courses C where T.off_id=O.id and O.course_id=C.course_id and O.year='||curr_year||' and O.semester=1 and T.grade!=''F'' group by O.year;';
			EXECUTE credit_calculate_command into credit_limit;

			if credit_limit is NULL then 
				credit_limit := 0;
			end if;

			credit_calculate_command := 'SELECT sum(C) from '||transcript_name||' T, course_offering O, courses C where T.off_id=O.id and O.course_id=C.course_id and O.year='||prev_year||' and O.semester=2 and T.grade!=''F'' group by O.year;';
			EXECUTE credit_calculate_command into prev_sem_credit;

			if prev_sem_credit is NULL then
				prev_sem_credit := 0;
			end if;

			credit_limit:= credit_limit+prev_sum_credit;
		end if;
		credit_limit := 1.25*(credit_limit/2);		
	end if;

	credit_calculate_command := 'SELECT sum(C) from enrol E, course_offering O, courses C where E.offering_id=O.id and O.course_id=C.course_id and E.student_id='''||st_id||''' and O.semester='||curr_semester||' and O.year='||curr_year||' group by O.year';
	EXECUTE credit_calculate_command into curr_sem_credit;
	
	select C from courses
	into course_credit
	where 
	course_id=offering_row.course_id;
	
	if curr_sem_credit+course_credit>credit_limit then
		--check for ticket
		RAISE EXCEPTION 'credit limit exceeded';
	else
		INSERT into enrol(student_id,offering_id) VALUES(st_id,off_id);	
	end if;

	RETURN;
	
END;
$$;

GRANT EXECUTE 
ON FUNCTION request_enrolment
TO student,deanoffice;