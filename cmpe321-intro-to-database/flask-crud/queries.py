import psycopg2
import json

with open("dbconfig.json") as f:
    config = json.load(f)

def connect_db():
    connection = psycopg2.connect(**config)
    return connection

def get_table(table_name):
    connection = connect_db()
    cursor = connection.cursor()
    if table_name == "Topic":
        query = """
            SELECT Topic.topic_id, Topic.name, Topic.result, T.title
                FROM Topic 
                LEFT JOIN (
            SELECT Topic.topic_id, Topic.name, Topic.result, Paper.title
                FROM Topic, Paper_Topics, Paper
                WHERE Topic.result = Paper.result
                AND   Paper.paper_id = Paper_Topics.paper_id
                AND   Topic.topic_id = Paper_Topics.topic_id
                  ) AS T on Topic.topic_id = T.topic_id
            """
        cursor.execute(query)
    else:
        cursor.execute("SELECT * FROM "+table_name)
    table = cursor.fetchall()
    connection.close()
    return table

def delete_entry(table, row_id):
    field_name = table.lower()+"_id"
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM %s WHERE %s=%d 
        """ %(table, field_name, int(row_id)))
    connection.commit()
    connection.close()

def get_papers():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT P.*, string_agg(DISTINCT T.name, ', '), string_agg(DISTINCT (A.first_name || ' ' || A.last_name), ', ') FROM Paper P
        LEFT JOIN Paper_Authors PA ON P.paper_id = PA.paper_id
        LEFT JOIN Paper_Topics PT ON P.paper_id = PT.paper_id
        LEFT JOIN Author A ON A.author_id = PA.author_id
        LEFT JOIN Topic T on T.topic_id = PT.topic_id
        GROUP BY P.paper_id
        """)
    papers = cursor.fetchall()
    connection.close()
    return papers

def update_entry(table, id, update_fields, update_values):
    field_name = table.lower()+"_id"
    connection = connect_db()
    cursor = connection.cursor()
    query = ["UPDATE",table,"\n","SET"]
    if update_fields == []:
        return
    for field, value in zip(update_fields, update_values):
        if field=="result":
            query.append(field+"="+"%d"%int(value))
            query.append(',')
        else:
            query.append(field+"="+"'%s'"%value)
            query.append(',')
    query = query[:-1]
    query.append("\n")
    query.append("WHERE %s='%s'"%(field_name, str(id)))
    query = " ".join(query)
    cursor.execute(query)
    connection.commit()
    connection.close()

def update_cross(paper_id, topics, authors):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT result from Paper WHERE paper_id=%d" % paper_id)
    result = float(cursor.fetchall()[0][0])
    print(topics)
    print(authors, "here")
    if authors != ['']:
        cursor.execute("DELETE FROM Paper_Authors WHERE paper_id=%d" % paper_id)
        for author in authors:
                names = author.split("@")
                cursor.execute("""
                    SELECT author_id FROM Author 
                    WHERE first_name='%s' AND last_name='%s'
                    """%(names[0], names[1]))
                a_id = cursor.fetchall()
                if a_id == []:
                    cursor.execute("""
                        INSERT INTO Author(first_name, last_name)
                        VALUES('%s', '%s') RETURNING author_id
                        """%(names[0], names[1]))
                    a_id = cursor.fetchall()
                a_id = a_id[0][0]
                cursor.execute("""
                    INSERT INTO Paper_Authors(paper_id, author_id)
                    VALUES(%d, %d)
                    """ % (paper_id, a_id))
    if topics != ['']:
        cursor.execute("DELETE FROM Paper_Topics WHERE paper_id=%d" % paper_id)
        for topic in topics:
            cursor.execute("""
                SELECT topic_id FROM Topic 
                WHERE name='%s'
                """%(topic))
            c_id = cursor.fetchall()
            if c_id == []:
                cursor.execute("""
                    INSERT INTO Topic(name, result)
                    VALUES('%s', '%f') RETURNING topic_id
                    """ % (topic, float(result)))
                c_id = cursor.fetchall()
            c_id = c_id[0][0]
            cursor.execute("""
                    INSERT INTO Paper_Topics(paper_id, topic_id)
                    VALUES(%d, %d)
                    """ % (paper_id, c_id))
    connection.commit()
    connection.close()



