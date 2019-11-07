import apsw

def initialization(arr_keys, arr_text):
# def initialization():

    # arr_keys = ["нога", "рука", "голова"]
    # arr_text = ["У меня немного болит нога и побаливает голова", "У меня немного болит нога и побаливает голова"]

    con = apsw.Connection('../db.sqlite3')
    cur = con.cursor()
    arr = []

    try:
        cur.execute('CREATE VIRTUAL TABLE data USING fts3(content TEXT)');
    except Exception:
        cur.execute('DROP TABLE data');
        cur.execute('CREATE VIRTUAL TABLE data USING fts3(content TEXT)');


    # Добавление в базу данных текста интеллект-карт
    for i in range(0, len(arr_text)):
        cur.execute('INSERT INTO data(docid, content) VALUES (:id, :key)', {"id": i, "key": arr_text[i]})

    occur_in_text = [0] * len(arr_text)

    for i in range(0, len(arr_keys)):
        for row in cur.execute('SELECT docid FROM data WHERE content MATCH :key', {"key": arr_keys[i]}):
            occur_in_text[row[0]] += 1

    answer = []
    for i in range(0, len(arr_text)):
        answer.append(occur_in_text[i] / len(arr_keys))

    cur.execute('DROP TABLE data')
    cur.close()
    con.close()

    return answer

# initialization()