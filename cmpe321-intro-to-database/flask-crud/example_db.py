import psycopg2
from queries import connect_db

def insert_paper(title, abstract, authors, result, topics):
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

insert_paper("Generative adversarial nets", 
    "We propose a new framework for estimating generative models via adversarial nets",
    "Ian@Goodfellow, Jean@Pouget-Abadie, Yoshua@Bengio",
    "90",
    "Deep Learning, Artificial Intelligence")

insert_paper("Deep learning",
    "An introduction to a broad range of topics in deep learning, covering mathematical and conceptual background, deep learning techniques used in industry, and research perspectives",
    "Ian@Goodfellow, Yoshua@Bengio, Aaron@Courville",
    "80",
    "Machine Learning, Artificial Intelligence")

insert_paper("Learning internal representations by error-propagation",
    "This paper presents a generalization of the perception learning procedure for learning the correct sets of connections for arbitrary networks.",
    "David@Rumelhart, Geoffrey@Hinton, Ronald@Williams",
    "95",
    "Math, Machine Learning")

insert_paper("Deep learning 2",
    "Deep learning allows computational models that are composed of multiple processing layers to learn representations of data with multiple levels of abstraction.",
    "Yann@LeCun, Yoshua@Bengio, Geoffrey@Hinton",
    "97",
    "Machine Learning, Artificial Intelligence"
    )

insert_paper("Neural machine translation by jointly learning to align and translate",
    "Neural machine translation is a recently proposed approach to machine translation. ",
    "Dzmitry@Bahdanau, Kyunghyun@Cho, Yoshua@Bengio",
    "92",
    "Natural Language Processing")

