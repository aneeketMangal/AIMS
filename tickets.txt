--Create a table of tickets for Dean Academics (and grant access only to dean)
--Write a trigger, whenever a new entry is made in batches table, a table of tickets is created for the batch advisor
--For the batch advisor ticket table, "GRANT --- ON --- TO <batch advisor>"
--i.e. Access should be granted only to batch advisor rather than to faculty
--Similarly, a table can be created/updated for each student whenever he/she raises a ticket (which shows status)
--Constraints to be checked can be that the course must be offered

--

-- ticket history
CREATE TABLE tickets(
    id INTEGER NOT NULL,
    student_id char(11) NOT NULL,
    offering_id integer NOT NULL,
    faculty_ap integer NOT NULL,
    advisor_ap integer NOT NULL, 
    dean_ap integer NOT NULL,
    PRIMARY KEY(id)
);

GRANT SELECT
ON tickets
TO faculty,student;

GRANT ALL
ON tickets
TO deanoffice;


CREATE OR REPLACE FUNCTION is_faculty(
    username text
)
RETURNS boolean
AS $_$
DECLARE
    temp_query text;
    output boolean;
    temp_var text;
BEGIN
    temp_var := substr(username, 2);
    temp_query := 'SELECT EXISTS(SELECT 1 FROM instructor WHERE instructor.id = '|| temp_var ||');'; 
    EXECUTE temp_query INTO output;
    RETURN output;
END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;

CREATE OR REPLACE FUNCTION is_student(
    username text
)
RETURNS boolean
AS $_$
DECLARE
    temp_query text;
    temp_var text;
    output boolean;
BEGIN
    output := False;
    if(length(username) = 12) then
        temp_var := substr(username, 2);
        temp_query := 'SELECT EXISTS(SELECT 1 FROM students WHERE students.id = '''|| temp_var ||''');'; 
        EXECUTE temp_query INTO output;
    END if;
    RETURN output;
END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;

CREATE OR REPLACE FUNCTION is_advisor(
    username text
)
RETURNS boolean
AS $_$
DECLARE
    temp_query text;
    output boolean;
    temp_var integer;

BEGIN
    temp_var := CAST(substr(username, 2) AS INTEGER);
    temp_query := 'SELECT EXISTS(SELECT 1 FROM batches WHERE batches.adv_id = '|| temp_var ||');'; 
    EXECUTE temp_query INTO output;
    RETURN output;
END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;

-- select * from student_tickets();
CREATE OR REPLACE FUNCTION student_tickets()
    RETURNS TABLE(
        id INT,
        student_id char(11),
        offering_id INT,
        faculty_ap INT,
        advisor_ap INT,
        dean_ap INT
)
AS $_$

BEGIN
    RETURN QUERY SELECT distinct tickets.id,
    tickets.student_id, tickets.offering_id, 
    tickets.faculty_ap, tickets.advisor_ap,
    tickets.dean_ap
    FROM tickets
    where 
    tickets.student_id ILIKE substr(session_user, 2);
    
END $_$
LANGUAGE plpgsql
SECURITY DEFINER;

GRANT EXECUTE
ON FUNCTION student_tickets
TO student;

CREATE OR REPLACE FUNCTION advisor_tickets()
    RETURNS TABLE(
        id INT,
        student_id char(11),
        offering_id INT,
        faculty_ap INT,
        advisor_ap INT,
        dean_ap INT
)
AS $_$

BEGIN
    RETURN QUERY SELECT distinct tickets.id,
    tickets.student_id, tickets.offering_id, 
    tickets.faculty_ap, tickets.advisor_ap,
    tickets.dean_ap
    FROM tickets, batches
    where 
    substr(tickets.student_id, 1, 7) ILIKE batches.batch AND
    batches.adv_id = substr(session_user, 2)::integer;
    
END $_$
LANGUAGE plpgsql
SECURITY DEFINER;

GRANT EXECUTE
ON FUNCTION advisor_tickets
TO faculty;



CREATE OR REPLACE FUNCTION faculty_tickets()
    RETURNS TABLE(
        id INT,
        student_id char(11),
        offering_id INT,
        faculty_ap INT,
        advisor_ap INT,
        dean_ap INT
)
AS $_$

BEGIN
    RETURN QUERY SELECT distinct tickets.id,
    tickets.student_id, tickets.offering_id, 
    tickets.faculty_ap, tickets.advisor_ap,
    tickets.dean_ap
    FROM tickets, course_offering
    where 
    tickets.offering_id = course_offering.id AND
    course_offering.insid = substr(session_user, 2)::integer;
    
END $_$
LANGUAGE plpgsql
SECURITY DEFINER;

GRANT EXECUTE
ON FUNCTION faculty_tickets
TO faculty;



CREATE OR REPLACE FUNCTION view_ticket_status(
    ticket_id int
)
RETURNS record
AS $_$
DECLARE
    create_table_command text;
    stu_id char(11);
    ins_id integer;
    out_record record;
    temp_query text;
    temp_exist boolean;
    temp_exist_two boolean;
    temp_var text;
    batch_ text;
BEGIN
    temp_query := 'SELECT EXISTS(SELECT 1 from tickets t where t.id = ' || ticket_id || ');';
    EXECUTE temp_query INTO temp_exist;

    if NOT temp_exist then
        RAISE EXCEPTION 'Invalid ticket ID';
        RETURN NULL;
    END if;


    if session_user = 'deanoffice' then
        temp_query := 'SELECT offering_id, faculty_ap, advisor_ap, dean_ap FROM tickets WHERE tickets.id = ' || ticket_id || ';';
        EXECUTE temp_query into out_record;
        return out_record;
    END if;

    temp_query := 'SELECT is_student(''' || session_user || ''')';
    EXECUTE temp_query INTO temp_exist;
    if temp_exist then

        stu_id := substr(session_user, 2);
        temp_query := 'SELECT EXISTS(SELECT 1 FROM tickets t WHERE t.id = ' || ticket_id || ' AND t.student_id = ''' || stu_id ||''');';
        EXECUTE temp_query INTO temp_exist_two;
        if temp_exist_two then
            temp_query := 'SELECT offering_id, faculty_ap, advisor_ap, dean_ap FROM tickets WHERE tickets.id = ' || ticket_id || ';';
            EXECUTE temp_query into out_record;
            return out_record;
        else 
            RAISE EXCEPTION 'Unauthorised access';
        END if;
    END if;


    temp_query := 'SELECT is_faculty(''' || session_user || ''')';
    EXECUTE temp_query INTO temp_exist;
    if temp_exist then
        ins_id := CAST(substr(session_user, 2) AS INTEGER);
        temp_query := 'SELECT EXISTS(SELECT 1 FROM tickets t, course_offering c WHERE t.id = ' || ticket_id || ' AND c.id = t.offering_id AND c.insid = '|| ins_id||');';
        EXECUTE temp_query INTO temp_exist_two;
        if temp_exist_two then
            temp_query := 'SELECT offering_id, faculty_ap, advisor_ap, dean_ap FROM tickets WHERE tickets.id = ' || ticket_id || ';';
            EXECUTE temp_query into out_record;
            RETURN out_record;
        END if;
    END if;

    temp_query := 'SELECT is_advisor(''' || session_user || ''')';
    EXECUTE temp_query INTO temp_exist;
    if temp_exist then
        ins_id := CAST(substr(session_user, 2) AS INTEGER);
        temp_query := '(SELECT t.student_id FROM tickets t WHERE t.id = ' || ticket_id || ');';
        EXECUTE temp_query INTO stu_id;
        batch_ := substr(stu_id, 1, 7);
        temp_query := 'SELECT EXISTS(SELECT 1 FROM batches b WHERE b.batch = ''' || batch_ || ''' AND b.adv_id = '|| ins_id || ');';
        EXECUTE temp_query INTO temp_exist_two;
        if temp_exist_two then
            temp_query := 'SELECT offering_id, faculty_ap, advisor_ap, dean_ap FROM tickets WHERE tickets.id = ' || ticket_id || ';';
            EXECUTE temp_query into out_record;
            RETURN out_record;
        END if;
    END if;


    RAISE NOTICE 'Unauthorised Action';
    RETURN NULL;
    
END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;

GRANT EXECUTE
ON FUNCTION view_ticket_status
TO student,faculty, deanoffice;


--general ticket table template
CREATE OR REPLACE FUNCTION create_ticket_table(
    table_name text
)
RETURNS void
AS $_$
DECLARE
    create_table_command text;
BEGIN
    create_table_command := 'CREATE TABLE ' || table_name || ' (';

    create_table_command := create_table_command || ' id INTEGER NOT NULL,';
    create_table_command := create_table_command || ' student_id char(11) NOT NULL,';
    create_table_command := create_table_command || ' offering_id INTEGER NOT NULL,';
    create_table_command := create_table_command || ' PRIMARY KEY(id),';
    create_table_command := create_table_command || ' FOREIGN KEY(id) REFERENCES tickets(id),';
    create_table_command := create_table_command || ' FOREIGN KEY(student_id) REFERENCES students(id),';
    create_table_command := create_table_command || ' FOREIGN KEY(offering_id) REFERENCES course_offering(id));';
    EXECUTE create_table_command;
END
$_$
LANGUAGE plpgsql;

--creating dean_tickets_table;
SELECT create_ticket_table('dean_tickets');

GRANT ALL 
ON dean_tickets
TO deanoffice;


-- ticket raise by student
-- defined by superuser
CREATE OR REPLACE FUNCTION raise_ticket(
    offering_id integer
)
RETURNS void
AS $_$
DECLARE
    stu_id char(11);
    table_name text;
    ins_id integer;
    insert_command text;
    ticket_id integer;
    temp_query text;
    temp_exist boolean;
BEGIN
    stu_id := substr(session_user, 2);
    temp_query := ('SELECT EXISTS(SELECT 1 FROM course_offering c where c.id = ' || offering_id || ');');
    EXECUTE temp_query INTO temp_exist;
    if NOT temp_exist then
        RAISE EXCEPTION 'Offering not found';
    END if;

    temp_query := ('SELECT c.insid from course_offering c where c.id = ' || offering_id || ';');
    EXECUTE temp_query into ins_id;
    table_name := concat('_', ins_id,  '_instructor_tickets');

    temp_query := ('SELECT EXISTS(SELECT 1 FROM tickets t WHERE t.student_id = ''' ||stu_id || ''' AND t.offering_id = ' || offering_id || ');');
    EXECUTE temp_query INTO temp_exist;
    if temp_exist then
        RAISE EXCEPTION 'Ticket already raised';
    END if;

    ticket_id := (SELECT COUNT(*) from tickets);
    insert_command := 'INSERT INTO tickets VALUES ('  || ticket_id || ',''' || stu_id || ''',' || offering_id || ', 0, 0, 0)';
    EXECUTE insert_command;
    insert_command := 'INSERT INTO ' || table_name || ' VALUES (' ||ticket_id || ',''' || stu_id || ''',' || offering_id || ');' ;
    EXECUTE insert_command;
    RAISE NOTICE'Your ticket id is %',ticket_id;

END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;

GRANT EXECUTE
ON FUNCTION raise_ticket
TO student;


CREATE OR REPLACE FUNCTION propagate(
    ticket_id int, 
    table_from text, 
    table_to text
)
RETURNS void
AS $_$
DECLARE
    temp_query text;
BEGIN
    --RAISE NOTICE '% %',table_from,table_to;
    temp_query := 'INSERT INTO ' || table_to || ' SELECT * FROM ' || table_from || ' tf WHERE tf.id = ' || ticket_id || ';';
    --RAISE NOTICE '%',temp_query;
    EXECUTE temp_query;
    temp_query := 'DELETE FROM ' || table_from || ' tf WHERE tf.id  = ' || ticket_id || ';';
    --RAISE NOTICE '%',temp_query;
    EXECUTE temp_query;
END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;





-- updation of status of raised ticket by instructor
CREATE OR REPLACE FUNCTION instructor_ticket_response(
    ticket_id integer,
    response boolean
)
RETURNS void
AS $_$
DECLARE
    table_name text;
    department text;
    batch integer;
    adv_table_name text;
    ins_id integer;
    update_command text;
    delete_command text;
    temp_query text;
    temp_exist boolean;
BEGIN
    ins_id := CAST(substr(session_user, 2) AS INTEGER);
    table_name := concat('_', ins_id,  '_instructor_tickets');

    temp_query := 'SELECT EXISTS(SELECT 1 FROM tickets t where t.id = ' || ticket_id || ');';
    EXECUTE temp_query into temp_exist;
    if NOT temp_exist then
        RAISE EXCEPTION 'Invalid ticket ID';
    END if;


    temp_query := 'SELECT EXISTS(SELECT 1 FROM ' || table_name ||  ' t where t.id = ' || ticket_id || ');';
    EXECUTE temp_query into temp_exist;
    if NOT temp_exist then
        RAISE EXCEPTION 'Unauthorized Request';
    END if;

    if (response) then
        update_command := 'UPDATE tickets set faculty_ap = 2 WHERE id ='||ticket_id||';';
        EXECUTE update_command;
        
    else
        update_command := 'UPDATE tickets set faculty_ap = 1 WHERE id ='||ticket_id||';';
        EXECUTE update_command;
    END if;
    temp_query := 'SELECT st.batch,st.dept FROM students st WHERE st.id = (SELECT ti.student_id FROM ' 
        || table_name || ' ti WHERE ti.id = ' || ticket_id || ');';
    EXECUTE temp_query into batch,department;
    adv_table_name := concat('_', CAST(batch as text),department,  '_advisor_tickets');
    EXECUTE propagate(ticket_id,table_name, adv_table_name);

END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;

GRANT EXECUTE
ON FUNCTION instructor_ticket_response
TO faculty;


--advisor ticket response function
CREATE OR REPLACE FUNCTION advisor_ticket_response(
    ticket_id integer,
    response boolean
)
RETURNS void
AS $_$
DECLARE
    table_name text;
    batch_ text;
    ins_id integer;
    update_command text;
    delete_command text;
    temp_query text;
    temp_exist boolean;
BEGIN
    ins_id := CAST(substr(session_user, 2) AS INTEGER);
    temp_query := 'SELECT 1 from batches b WHERE b.adv_id = ' || ins_id || ';';
    EXECUTE temp_query INTO temp_exist;
    if NOT temp_exist then
        RAISE EXCEPTION 'Unauthorised Access';
    END if;

    temp_query := '(SELECT b.batch from batches b WHERE b.adv_id = ' || ins_id || ');';
    EXECUTE temp_query INTO batch_;
    table_name := concat('_', batch_,  '_advisor_tickets');

    temp_query := 'SELECT EXISTS(SELECT 1 FROM tickets t where t.id = ' || ticket_id || ');';
    EXECUTE temp_query into temp_exist;
    if NOT temp_exist then
        RAISE EXCEPTION 'Invalid ticket ID';
    END if;


    temp_query := 'SELECT EXISTS(SELECT 1 FROM ' || table_name ||  ' t where t.id = ' || ticket_id || ');';
    EXECUTE temp_query into temp_exist;
    if NOT temp_exist then
        RAISE EXCEPTION 'Unauthorized Request';
    END if;

    if (response) then
        update_command := 'UPDATE tickets SET advisor_ap = 2 WHERE id = ' || ticket_id || ';';
        EXECUTE update_command;
    else
        update_command := 'UPDATE tickets SET advisor_ap = 1 WHERE id = ' || ticket_id || ';';
        EXECUTE update_command;
    END if;
    EXECUTE propagate(ticket_id,table_name, 'dean_tickets');
END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;

-- to be changed if we want to make a advisor group
GRANT EXECUTE
ON FUNCTION advisor_ticket_response
TO faculty;

-- to be decided if ki dean_tickets wali table rakhni hai kya

CREATE OR REPLACE FUNCTION dean_ticket_response(
    ticket_id integer,
    response boolean
)
RETURNS void
AS $_$
DECLARE
    table_name text;
    update_command text;
    temp_query text;
    temp_exist boolean;
    temp_record record;
BEGIN
    temp_query := 'SELECT EXISTS(SELECT 1 FROM tickets t where t.id = ' || ticket_id || ');';
    EXECUTE temp_query into temp_exist;
    if NOT temp_exist then
        RAISE EXCEPTION 'Invalid ticket ID';
    END if;

    if (response) then
        update_command := 'UPDATE tickets SET dean_ap = 2 WHERE id = ' || ticket_id || ';';
        temp_query := 'SELECT t.student_id, t.offering_id FROM tickets t WHERE t.id = ' || ticket_id || ';';
        EXECUTE temp_query INTO temp_record;
        temp_query := 'INSERT INTO enrol VALUES(''' || temp_record.student_id ||''','||temp_record.offering_id|| ');';
        EXECUTE temp_query;
    else
        update_command := 'UPDATE tickets SET dean_ap = 1 WHERE id = ' || ticket_id || ';';
    END if;
    EXECUTE update_command;
    DELETE FROM dean_tickets WHERE dean_tickets.id = ticket_id;
    RETURN;
END
$_$
LANGUAGE plpgsql;

GRANT EXECUTE
ON FUNCTION dean_ticket_response
TO deanoffice;

