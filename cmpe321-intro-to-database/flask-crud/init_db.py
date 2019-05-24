import psycopg2
from queries import connect_db

connection = connect_db()
cursor = connection.cursor()

author_command = """
CREATE TABLE Author(
    author_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    CONSTRAINT Unique_Name UNIQUE (first_name, last_name)
);
"""

paper_authors = """
CREATE TABLE Paper_Authors(
paper_id INTEGER NOT NULL,
author_id INTEGER NOT NULL,
CONSTRAINT PK_PAuthors PRIMARY KEY(paper_id, author_id),
CONSTRAINT FK_Author FOREIGN KEY(author_id) REFERENCES Author(author_id) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT FK_Paper FOREIGN KEY(paper_id) REFERENCES Paper(paper_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""


paper_command = """
CREATE TABLE Paper (
    paper_id BIGSERIAL PRIMARY KEY,  
    title VARCHAR(128) NOT NULL,
    abstract VARCHAR(200) NOT NULL,
    result FLOAT(8) NOT NULL, 
    CONSTRAINT Unique_Title UNIQUE (title)
);"""

paper_topics = """
CREATE TABLE Paper_Topics(
    paper_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    CONSTRAINT PK_PTopics PRIMARY KEY(paper_id, topic_id),
    CONSTRAINT FK_Paper FOREIGN KEY(paper_id) REFERENCES Paper(paper_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_Topic FOREIGN KEY(topic_id) REFERENCES Topic(topic_id) ON DELETE CASCADE ON UPDATE CASCADE
);

"""

topic_command = """
CREATE TABLE Topic (  
    topic_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,  
    result FLOAT(8)
);"""


coauthor_proc_command = """
CREATE OR REPLACE FUNCTION get_coauthors (f_name_auth VARCHAR(128),
                                            l_name_auth VARCHAR(128)) 
 RETURNS TABLE (
 id_author BIGINT,
 f_name VARCHAR(128),
 l_name VARCHAR(128)
)  AS $$
DECLARE
   the_author BIGINT := (SELECT author_id FROM Author WHERE 
                            first_name=f_name_auth AND last_name=l_name_auth);
BEGIN
 RETURN QUERY 
 SELECT * FROM Author 
 WHERE author_id IN
 (
 SELECT DISTINCT author_id FROM Paper_Authors
 WHERE paper_id IN (
 SELECT paper_id FROM Paper_Authors
 WHERE author_id = the_author
)
 AND author_id != the_author
 ) ;
 END; $$
 LANGUAGE 'plpgsql';
"""


trigger_fn = """
CREATE OR REPLACE FUNCTION sota_update()
    RETURNS trigger AS
$BODY$
DECLARE
   max_insert FLOAT(8) := (SELECT MAX(result) FROM Paper WHERE paper_id IN (
                        SELECT paper_id FROM Paper_Topics WHERE topic_id=NEW.topic_id
                            ));
   max_delete FLOAT(8) := (SELECT MAX(result) FROM Paper WHERE paper_id IN (
                        SELECT paper_id FROM Paper_Topics WHERE topic_id=OLD.topic_id
                            ));
BEGIN
 IF EXISTS (SELECT 1 FROM Paper WHERE paper_id = NEW.paper_id ) THEN
    UPDATE Topic 
    SET result=max_insert
    WHERE topic_id = NEW.topic_id;
    RETURN NEW;
ELSE
UPDATE Topic 
    SET result=max_delete
    WHERE topic_id = OLD.topic_id;
    RETURN OLD;
 END IF;
END;
$BODY$ LANGUAGE plpgsql;
"""




result_update_trig = """
CREATE TRIGGER SOTA_TRIGGER
  AFTER INSERT OR DELETE
  ON Paper_Topics
  FOR EACH ROW
  EXECUTE PROCEDURE sota_update();
"""

trigger_fn_2 = """
CREATE OR REPLACE FUNCTION paper_updated()
    RETURNS trigger AS
$BODY$
BEGIN
    UPDATE Topic 
    SET result=
    ( SELECT MAX(result) FROM Paper WHERE paper_id IN 
    (
        SELECT paper_id FROM Paper_Topics WHERE topic_id = Topic.topic_id
    ))
    WHERE Topic.topic_id IN 
    (
        SELECT topic_id FROM Paper_Topics WHERE paper_id=NEW.paper_id
    ) ;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql;
"""

paper_update_trig = """
CREATE TRIGGER SOTA_PAPER_TRIGGER
  AFTER UPDATE OF result ON Paper
  FOR EACH ROW
  EXECUTE PROCEDURE paper_updated();
"""


cursor.execute(author_command)
cursor.execute(paper_command)
cursor.execute(topic_command)
cursor.execute(paper_topics)
cursor.execute(paper_authors)
cursor.execute(coauthor_proc_command)
cursor.execute(trigger_fn)
cursor.execute(result_update_trig)
cursor.execute(trigger_fn_2)
cursor.execute(paper_update_trig)
connection.commit()
connection.close()

