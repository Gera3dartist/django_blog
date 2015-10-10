select lanname from pg_language;
create table new_book(
  id serial,
  title TEXT,
  author TEXT
);

-- Simple insert function
CREATE OR REPLACE FUNCTION ins_book(p_title TEXT, p_author TEXT)
RETURNS INTEGER AS
$$
INSERT  INTO  new_book(title, author) VALUES (p_title, p_author)
    RETURNING id;
$$
LANGUAGE 'sql' VOLATILE;

select ins_book('18 minuter', 'Bergman') AS book_id;
select ins_book('1 minute', 'Eric Bolduin') AS book_id;

-- Simple update function
CREATE OR REPLACE FUNCTION upd_book(book_id int, p_title text, p_author text)
RETURNS VOID AS
$$
  UPDATE new_book SET title=p_title, author=p_author
  WHERE id=book_id;
$$
LANGUAGE 'sql' VOLATILE;

SELECT upd_book(2, 'Startup nation', 'Rosenberg');
SELECT * from new_book;

-- return data set with TABLE
CREATE OR REPLACE FUNCTION ret_books(p_title TEXT)
RETURNS TABLE (id int, title text, author text) AS
$$
SELECT id, title, author FROM new_book
WHERE title LIKE p_title;
$$
LANGUAGE 'sql' STABLE;

select * from ret_books('%minute%');

--returns data set with OUT
CREATE OR REPLACE FUNCTION ret_books_out(p_title text, OUT p_id, OUT p_title, OUT p_author)
RETURNS SETOF RECORD AS
$$
  select *
  from new_book
  WHERE title like p_title;
$$
LANGUAGE 'sql' STABLE;

select * from ret_books('%Startup%');

--returns data set with composite data type

CREATE OR REPLACE FUNCTION ret_books_composite(p_title text)
RETURNS SETOF new_book AS
$$
SELECT *
FROM new_book
WHERE title like p_title
$$
LANGUAGE 'sql' STABLE;

select * from ret_books_composite('%minute%');



--PlSql

CREATE OR REPLACE FUNCTION ret_books_plsql()
  RETURNS TABLE(id int, title text, author text) AS
$$
BEGIN
RETURN QUERY
SELECT *
FROM new_book;
END;
$$
LANGUAGE 'plpgsql' STABLE;

SELECT * FROM ret_books_plsql();

-- Triggers
-- Create trigger associated function
CREATE OR REPLACE FUNCTION f_trig_books() RETURNS trigger AS
$$
BEGIN
NEW.title := upper(NEW.title);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql' VOLATILE;

-- Create trigger
CREATE TRIGGER trig_books
BEFORE INSERT OR UPDATE of title, author
on new_book
FOR EACH ROW
EXECUTE PROCEDURE f_trig_books();


CREATE OR REPLACE FUNCTION f_trig_send_payload() RETURNS TRIGGER AS
$$
BEGIN
--   EXECUTE 'NOTIFY MyChannel, ''' ||NEW.author || NEW.title|| ''';';
  EXECUTE 'NOTIFY MyChannel';
  RETURN NULL;
END;
$$
LANGUAGE 'plpgsql' VOLATILE;

CREATE TRIGGER trig_send_event
AFTER INSERT OR UPDATE of title, author
on new_book
FOR EACH ROW
  EXECUTE PROCEDURE f_trig_send_payload();

select ins_book('Think big', 'Nora');

drop TRIGGER trig_send_event on new_book;
drop FUNCTION f_trig_send_payload();
