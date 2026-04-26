import sqlite3

def run_query(word_language, word_type):
    # Last modified 22/03/26
    # This function connects to flubb.db, generates a query, and
    # returns a 2-dimensional array containing the row data and
    # a list containing the column names.
    
    with sqlite3.connect('database/flubb.db') as conn:
        cursor = conn.cursor()
        query, params = generate_query(word_language, word_type)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        return rows, cols

def generate_query(word_language, word_type):
    query_string = "SELECT mw.english, mw.lemma"
    if word_type == "noun":
        query_string += ", g.gender_name"       
    if word_type == "adjective":
        query_string += ", mw.masculine_form, mw.feminine_form"
        if word_language == "DE":
            query_string += ", mw.neuter_form, mw.plural_form"           
    query_string += " FROM master_words mw"
    query_string += " JOIN word_classes wc ON mw.word_class_id = wc.id"
    query_string += " JOIN languages l ON mw.language_id = l.id"  
    if word_type == "noun":
        query_string += " LEFT JOIN genders g ON mw.gender_id = g.id"      
    query_string += " WHERE wc.class_name = ? AND l.code = ?"   
    return query_string, (word_type, word_language)
