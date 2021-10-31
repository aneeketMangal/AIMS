--key points to note
-- 1. Course can now be offered by any other instructor (for same sem/year)
-- 2. Course must exist.
-- 3. Grades are character grades (A+, A-, B+, B-)

--On each entry in course_offering, 2 tables will be created
-- 1. Tickets corresponding to that course offering (security definer).
-- 2. Grades corresponding to that course offering (format: "__grades").


--grade table template
CREATE OR REPLACE FUNCTION create_grade_table()
RETURNS TRIGGER
AS $_$
DECLARE
    table_name text;
    create_table_command text;
    grant_permission_command text;
BEGIN
    table_name := concat('_', NEW.id,  '_grades');
    create_table_command := 'CREATE TABLE ' || table_name || ' (';
    create_table_command := create_table_command || ' student_id char(11) NOT NULL,';
    create_table_command := create_table_command || ' grade varchar(2) NOT NULL,';
    create_table_command := create_table_command || ' PRIMARY KEY(student_id),';
    create_table_command := create_table_command || ' FOREIGN KEY(student_id) REFERENCES students(id));';
    
    EXECUTE create_table_command;

    grant_permission_command := 'GRANT ALL ON ' || table_name || ' TO deanoffice, _'||NEW.insid||';';
    EXECUTE grant_permission_command;


    return null;
END
$_$
LANGUAGE plpgsql
SECURITY DEFINER;


CREATE TRIGGER grade_table
AFTER INSERT
ON course_offering
FOR EACH ROW
EXECUTE FUNCTION create_grade_table();


--constraint update procedure
CREATE OR REPLACE PROCEDURE update_constraint
(
    offering_id integer,
    batch_list varchar,
    is_offer boolean
)
LANGUAGE plpgsql
SECURITY INVOKER
AS $$
declare
    --split the batch list into a table of batches, and define a cursor for the table
    cur CURSOR FOR (SELECT batch FROM regexp_split_to_table(batch_list, E',') AS batch);
    batch_in_list varchar;
    ins_id integer;
    offering_ins_id integer;
begin
    ins_id := CAST(substr(user, 2) AS INTEGER);
    offering_ins_id := (SELECT O.insid FROM course_offering O WHERE O.id = offering_id);
    if NOT EXISTS (SELECT 1 FROM course_offering c where c.id = offering_id) then
        RAISE EXCEPTION 'Invalid offering id.';
    END if;
    if ins_id != offering_ins_id then
        RAISE EXCEPTION 'Unauthorised Request.';
    END if;
    open cur; 
    LOOP
        FETCH cur into batch_in_list;
        EXIT when not found;
        if(is_offer) then
            INSERT INTO batch_constraint(id, batch)
            VALUES
            (offering_id, batch_in_list);
        else
            DELETE FROM batch_constraint b
            WHERE
            b.id = offering_id AND
            b.batch = batch_in_list;
        END if;
    end LOOP;
    close cur;
end;$$;

GRANT EXECUTE
ON PROCEDURE update_constraint
TO faculty;

--procedure for offering courses
--batch_list to be provided as '2019csb,2020eeb,2018ceb'
CREATE OR REPLACE PROCEDURE offer_course
(
    course_id char(5),
    semester integer,
    year integer,
    batch_list varchar,
    slot char(6),
    classroom varchar,
    CGPA float8
)
LANGUAGE plpgsql
SECURITY INVOKER
AS $$
declare
    ins_id integer;
    offering_id integer;
begin
    ins_id := CAST(substr(user, 2) AS INTEGER);

    --if the course exists
    if EXISTS(SELECT 1 FROM courses WHERE courses.course_id = $1) then
        
        -- if time slots of none of the the previous offering by ins_id
        -- conflicts with current offering's slot 
        -- insid can offer the course
        if NOT EXISTS(
            SELECT 1 FROM course_offering C WHERE 
            C.insid = ins_id and C.semester = $2 and C.year = $3 and C.slot = $5
        ) then

            SELECT count(*)
            INTO offering_id
            FROM course_offering;

            INSERT INTO course_offering(id,course_id, year, semester, insid, slot, classroom, CGPA)
            VALUES
            (offering_id,course_id, year, semester, ins_id, slot, classroom, CGPA);

            
            call update_constraint(offering_id, batch_list, true);
        
        --if the course is offered this sem-year    
        else
           -- SELECT C.id into conflict_id
           -- FROM course_offering C
           -- WHERE
           -- C.insid = ins_id and C.semester = semester and C.year = year and C.slot = slot;
            RAISE EXCEPTION '% offering will have time slot conflict with an existing offering.', course_id;
        END if;
    
    --if the course doesn't exist
    else
        RAISE EXCEPTION 'Course % does not exist.', course_id;
    END if;
end;$$;

GRANT EXECUTE
ON PROCEDURE offer_course
TO faculty;

