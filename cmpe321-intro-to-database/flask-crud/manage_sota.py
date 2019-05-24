from flask import Flask
from flask import request
import psycopg2
from flask import render_template
from queries import delete_entry, get_papers, update_entry, update_cross, connect_db, get_table
app = Flask(__name__)

@app.route('/', methods=["GET"])
def land():
    return render_template("land.html")

@app.route('/user/home', methods=["GET"])
def home():
    return render_template("home.html", user="User")

@app.route('/admin/home', methods=["GET"])
def admin_home():
    return render_template("home.html", user="Admin")

@app.route('/admin/authors', methods=["GET", "POST"])
def admin_authors():
    if request.form:
        if request.form.get("type") == 'DELETE':
            delete_entry("Author", request.form.get("author_id"))
            authors = get_table("Author")
            return render_template("admin_authors.html", authors=authors)
        elif request.form.get("type")=='UPDATE':
            fields, values = [], []
            if request.form.get("first_name") != '':
                fields.append("first_name")
                values.append(request.form.get("first_name"))
            if request.form.get("last_name") != '':
                fields.append("last_name")
                values.append(request.form.get("last_name"))
            author_id = int(request.form.get("author_id"))
            update_entry("Author", author_id, fields, values)
            authors = get_table("Author")
            return render_template("admin_authors.html", authors=authors)

        f = request.form.get("first_name")
        l = request.form.get("last_name")
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("""
                    INSERT INTO Author(first_name, last_name)
                    VALUES('%s', '%s')
                    """%(f,l))
        connection.commit()
        connection.close()
        authors = get_table("Author")
        return render_template("admin_authors.html", authors=authors)
    else:
        authors = get_table("Author")
        return render_template("admin_authors.html", authors=authors)


@app.route('/admin/topics', methods=["GET", "POST"])
def admin_topics():
    if request.form:
        if request.form.get("type") == 'DELETE':
            delete_entry("Topic", request.form.get("topic_id"))
            topics = get_table("Topic")
            return render_template("admin_topics.html", topics=topics)
        elif request.form.get("type") == 'UPDATE':
            topic_id = int(request.form.get("topic_id"))
            new_name = request.form.get("name")
            update_entry("Topic", topic_id, ["name"], [new_name])
            topics = get_table("Topic")
            return render_template("admin_topics.html", topics=topics)

        name = request.form.get("name")
        result = "NULL"
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
                    INSERT INTO Topic(name, result)
                    VALUES('%s', %s)
                    """ % (name, result))
        connection.commit()
        connection.close()
        topics = get_table("Topic")
        return render_template("admin_topics.html", topics=topics)
    else:
        topics = get_table("Topic")
        return render_template("admin_topics.html", topics=topics)

@app.route('/admin/papers', methods=["GET", "POST"])
def admin_papers():
    if request.form:
        if request.form.get("type") == 'DELETE':
            delete_entry("Paper", request.form.get("paper_id"))
            papers = get_papers()
            return render_template("admin_papers.html", papers=papers)
        elif request.form.get("type") == 'UPDATE':
            formfields = ["title", "abstract", "result"]
            formvalues = [request.form.get(field) for field in formfields]
            fields, values = list(), list()
            for i in range(len(formvalues)):
                if formvalues[i] != '':
                    fields.append(formfields[i])
                    values.append(formvalues[i])
            paper_id = int(request.form.get("paper_id"))
            topics, authors = request.form.get("topics"),request.form.get("authors")
            authors = authors.split(",")
            authors = [a.strip() for a in authors]
            topics = topics.split(",")
            topics = [t.strip() for t in topics]
            update_cross(paper_id, topics, authors)
            update_entry("Paper", paper_id, fields, values)
            papers = get_papers()
            return render_template("admin_papers.html", papers=papers)

        title = request.form.get("title")
        authors = request.form.get("authors")
        topics = request.form.get("topics")
        abstract = request.form.get("abstract")
        result = request.form.get("result")
        authors = authors.split(",")
        authors = [a.strip() for a in authors]
        topics = topics.split(",")
        topics = [t.strip() for t in topics]
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("""
                    INSERT INTO Paper(title, abstract, result)
                    VALUES('%s', '%s', %f) RETURNING paper_id
                    """ %(title, abstract, float(result)))
        paper_id = cursor.fetchall()[0][0]
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
        papers = get_papers()
        return render_template("admin_papers.html", papers=papers)
    else:
        papers = get_papers()
        return render_template("admin_papers.html", papers=papers)




@app.route('/user/authors', methods=["GET", "POST"])
def authors():
    if request.form:
        if request.form.get("type") == 'coauthor':
            first_name = (request.form.get("first_name"))
            last_name = (request.form.get("last_name"))
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM get_coauthors('%s', '%s')""" % (first_name, last_name))
            coauthors = cursor.fetchall()
            return render_template("authors.html", authors=coauthors, title="Coauthors of %s %s" % (first_name, last_name))

        author_id = request.form.get("author_id")
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT P.*, string_agg(DISTINCT T.name, ', '), string_agg(DISTINCT (A.first_name || ' ' || A.last_name), ', ') FROM Paper P
        JOIN Paper_Authors PA ON P.paper_id = PA.paper_id
        JOIN Paper_Topics PT ON P.paper_id = PT.paper_id
        JOIN Author A ON A.author_id = PA.author_id
        JOIN Topic T on T.topic_id = PT.topic_id
        WHERE P.paper_id in (SELECT paper_id FROM Paper_Authors WHERE author_id = %d)
        GROUP BY P.paper_id
        """ % int(author_id))
        papers = cursor.fetchall()
        cursor.execute("""
            SELECT first_name, last_name FROM Author WHERE author_id = %d
            """ % int(author_id))
        names = cursor.fetchall()
        author_name = " ".join([names[0][0], names[0][1]])
        connection.close()
        return render_template("papers.html", papers=papers, title="Papers of author: "+author_name)
    else:
        authors = get_table("Author")
        return render_template("authors.html", authors=authors, title="Authors")

@app.route('/user/rankings', methods=["GET"])
def rankings():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT A.author_id, A.first_name, A.last_name, C.n_p
        FROM Author A
        LEFT JOIN
        (SELECT PA.author_id, COUNT(PA.paper_id) AS n_p FROM
        Paper_Authors PA
        JOIN 
        (SELECT P.paper_id 
        FROM Paper P
        JOIN Paper_Topics PT on P.paper_id = PT.paper_id
        JOIN Topic T on P.result = T.result
        WHERE T.topic_id=PT.topic_id) P 
        ON P.paper_id = PA.paper_id
        GROUP BY PA.author_id) C
        ON A.author_id = C.author_id
        WHERE C.n_p IS NOT NULL
        ORDER BY C.n_p DESC
    """)
    authors = cursor.fetchall()
    connection.close()
    return render_template("rankings.html", authors=authors)

@app.route('/user/papers', methods=["GET"])
def papers():
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
    return render_template("papers.html", papers=papers, title="All Papers")

@app.route('/user/search_keyword', methods=["GET", "POST"])
def search_keyword():
    if request.form:
        keyword = request.form.get("keyword")
        format_str = "'%" + keyword + "%'"
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT paper_id FROM Paper WHERE abstract LIKE %s OR title LIKE %s" % (format_str,  format_str))
        ex = cursor.fetchall()
        cursor.execute("""
            SELECT P.*, string_agg(DISTINCT T.name, ', '), string_agg(DISTINCT (A.first_name || ' ' || A.last_name), ', ') FROM Paper P
            JOIN Paper_Authors PA ON P.paper_id = PA.paper_id
            JOIN Paper_Topics PT ON P.paper_id = PT.paper_id
            JOIN Author A ON A.author_id = PA.author_id
            JOIN Topic T on T.topic_id = PT.topic_id
            WHERE P.paper_id in (SELECT paper_id FROM Paper WHERE abstract LIKE %s OR title LIKE %s)
            GROUP BY P.paper_id
            """ % (format_str,  format_str))
        papers = cursor.fetchall()
        connection.close()
        return render_template("search_keyword.html", papers=papers, title="All Papers containing the given keyword")
    else:
        return render_template("search_keyword.html" , papers=None, title="Search a keyword")

@app.route('/user/sota', methods=["GET", "POST"])
def sota():
    if request.form:
        topic_id = request.form.get("topic_id")
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT P.*, string_agg(DISTINCT T.name, ', '), string_agg(DISTINCT (A.first_name || ' ' || A.last_name), ', ') FROM Paper P
        JOIN Paper_Authors PA ON P.paper_id = PA.paper_id
        JOIN Paper_Topics PT ON P.paper_id = PT.paper_id
        JOIN Author A ON A.author_id = PA.author_id
        JOIN Topic T on T.topic_id = PT.topic_id
        WHERE P.result = (SELECT result FROM Topic WHERE topic_id = %d)
        GROUP BY P.paper_id
        """ % int(topic_id))
        result =  cursor.fetchall()
        cursor.execute("""
            SELECT name FROM Topic WHERE topic_id = %d
            """ % int(topic_id))
        topic_name = cursor.fetchall()[0][0]
        connection.close()
        topics = get_table("Topic")
        return render_template("sota.html", paper=result[0], topics=topics, title="Sota Result for Topic: "+topic_name)
    else:
        topics = get_table("Topic")
        return render_template("sota.html", paper=None, topics = topics, title="Pick a topic for the sota result")

@app.route('/user/topics', methods=["GET", "POST"])
def topics():
    if request.form:
        topic_id = request.form.get("topic_id")
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("""
        SELECT P.*, string_agg(DISTINCT T.name, ', '), string_agg(DISTINCT (A.first_name || ' ' || A.last_name), ', ') FROM Paper P
        JOIN Paper_Authors PA ON P.paper_id = PA.paper_id
        JOIN Paper_Topics PT ON P.paper_id = PT.paper_id
        JOIN Author A ON A.author_id = PA.author_id
        JOIN Topic T on T.topic_id = PT.topic_id
        WHERE P.paper_id in (SELECT paper_id FROM Paper_Topics WHERE topic_id = %d)
        GROUP BY P.paper_id
        """ % int(topic_id))
        papers = cursor.fetchall()
        cursor.execute("""
            SELECT name FROM Topic WHERE topic_id = %d
            """ % int(topic_id))
        topic_name = cursor.fetchall()[0][0]
        connection.close()
        return render_template("papers.html", papers=papers, title="Papers of Topic: "+topic_name)
    else:
        topics = get_table("Topic")
        return render_template("topics.html", topics=topics)

if __name__ == "__main__":
    app.run(debug=True)