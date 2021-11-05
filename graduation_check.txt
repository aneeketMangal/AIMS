-- TO BE CREATED BY deanoffice
-- PC, PE, SC, SE REQUIRED CREDITS HARDCODED

CREATE OR REPLACE FUNCTION graduation_check
(
    student_id char(11)
)
RETURNS boolean
LANGUAGE plpgsql
SECURITY INVOKER
AS $$
declare
    curriculum_cur REFCURSOR;
    transcript_table_name text;
    curriculum_table_row record;
    curriculum_table_name text;
    cgpa numeric(4, 2);
    pc_credits integer := 0;
    pe_credits integer := 0;
    sc_credits integer := 0;
    oe_credits integer := 0;
    row_check_command text;
    row_exist boolean;
    get_credits_command text;
    course_credits integer := 0;
begin
    --check cgpa >= 5.00
    cgpa := cgpa_calculation(student_id);
    if cgpa < 5.00 then
        RAISE NOTICE'cgpa=% less than 5',cgpa;
        return false;
    END if;

    --batch and transcript table name
    curriculum_table_name := 'curriculum_' || substr(student_id, 1, 7);
    transcript_table_name := 'transcript_' || student_id;

    --check for program core credits
    open curriculum_cur FOR EXECUTE 'SELECT * FROM ' || curriculum_table_name || ' WHERE course_type = ''PC''';
    LOOP
        FETCH curriculum_cur INTO curriculum_table_row;
        EXIT when not found;

        --check if the course is done by the student (and that he/she has passed in the course)
        row_check_command := 'SELECT EXISTS(SELECT * FROM ' || transcript_table_name || ', course_offering O, courses C WHERE C.course_id = ''' || curriculum_table_row.course_id || ''' and off_id = O.id and O.course_id = C.course_id and grade <> ''F'');';
        EXECUTE row_check_command INTO row_exist;

        --if the above condition is satisfied
        if row_exist then
            --get the course credits
            get_credits_command := 'SELECT C FROM courses WHERE course_id = ''' || curriculum_table_row.course_id || ''';';
            EXECUTE get_credits_command INTO course_credits;
            --update pc_credits
            pc_credits := pc_credits + course_credits;
        END if;
    END LOOP;
    close curriculum_cur;

    --if pc_credits is less than required
    if pc_credits < 7 then
        RAISE NOTICE 'PC credits not completed';
        return false;
    END if;

    --check for program elective credits
    open curriculum_cur FOR EXECUTE 'SELECT * FROM ' || curriculum_table_name || ' WHERE course_type = ''PE''';
    LOOP
        FETCH curriculum_cur INTO curriculum_table_row;
        EXIT when not found;

        --check if the course is done by the student (and that he/she has passed in the course)
        row_check_command := 'SELECT EXISTS(SELECT * FROM ' || transcript_table_name || ', course_offering O, courses C WHERE C.course_id = ''' || curriculum_table_row.course_id || ''' and off_id = O.id and O.course_id = C.course_id and grade <> ''F'');';
        EXECUTE row_check_command INTO row_exist;

        --if the above condition is satisfied
        if row_exist then
            --get the course credits
            get_credits_command := 'SELECT C FROM courses WHERE course_id = ''' || curriculum_table_row.course_id || ''';';
            EXECUTE get_credits_command INTO course_credits;
            --update pe_credits
            pe_credits := pe_credits + course_credits;
        END if;
    END LOOP;
    close curriculum_cur;

    --if pe_credits is less than required
    if pe_credits < 3 then
        RAISE NOTICE 'PE credits not completed';
        return false;
    END if;

    --check for science core credits
    open curriculum_cur FOR EXECUTE 'SELECT * FROM ' || curriculum_table_name || ' WHERE course_type = ''SC''';
    LOOP
        FETCH curriculum_cur INTO curriculum_table_row;
        EXIT when not found;

        --check if the course is done by the student (and that he/she has passed in the course)
        row_check_command := 'SELECT EXISTS(SELECT * FROM ' || transcript_table_name || ', course_offering O, courses C WHERE C.course_id = ''' || curriculum_table_row.course_id || ''' and off_id = O.id and O.course_id = C.course_id and grade <> ''F'');';
        EXECUTE row_check_command INTO row_exist;

        --if the above condition is satisfied
        if row_exist then
            --get the course credits
            get_credits_command := 'SELECT C FROM courses WHERE course_id = ''' || curriculum_table_row.course_id || ''';';
            EXECUTE get_credits_command INTO course_credits;
            --update sc_credits
            sc_credits := sc_credits + course_credits;
        END if;
    END LOOP;
    close curriculum_cur;

    --if sc_credits is less than required
    if sc_credits < 3 then
        RAISE NOTICE 'SC credits not completed';
        return false;
    END if;

    --check for open elective credits
    open curriculum_cur FOR EXECUTE 'SELECT * FROM ' || curriculum_table_name || ' WHERE course_type = ''OE''';
    LOOP
        FETCH curriculum_cur INTO curriculum_table_row;
        EXIT when not found;

        --check if the course is done by the student (and that he/she has passed in the course)
        row_check_command := 'SELECT EXISTS(SELECT * FROM ' || transcript_table_name || ', course_offering O, courses C WHERE C.course_id = ''' || curriculum_table_row.course_id || ''' and off_id = O.id and O.course_id = C.course_id and grade <> ''F'');';
        EXECUTE row_check_command INTO row_exist;

        --if the above condition is satisfied
        if row_exist then
            --get the course credits
            get_credits_command := 'SELECT C FROM courses WHERE course_id = ''' || curriculum_table_row.course_id || ''';';
            EXECUTE get_credits_command INTO course_credits;
            --update oe_credits
            oe_credits := oe_credits + course_credits;
        END if;
    END LOOP;
    close curriculum_cur;

    --if oe_credits is less than required
    if oe_credits < 4 then
        RAISE NOTICE 'OE credits not completed';
        return false;
    END if;

    --if all conditions are followed, return true
    RAISE NOTICE 'ALL conditions fulfilled. Ready to graduate';
    return true;
end;
$$;

GRANT EXECUTE
ON FUNCTION graduation_check
TO deanoffice;
