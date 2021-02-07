CREATE TABLE IF NOT EXISTS docs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_code TEXT UNIQUE NOT NULL,
  experience TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS terms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  term TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS docs_terms  (
    docs_id INTEGER,
    terms_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(docs_id) REFERENCES docs(id),
    FOREIGN KEY(terms_id) REFERENCES terms(id)
);

CREATE TABLE IF NOT EXISTS topics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS topics_terms  (
    topics_id INTEGER,
    terms_id INTEGER,
    percent REAL,
    FOREIGN KEY(topics_id) REFERENCES topics(id),
    FOREIGN KEY(terms_id) REFERENCES terms(id)
);

CREATE TABLE IF NOT EXISTS docs_topics(
    docs_id INTEGER,
    topics_id INTEGER,
    percent REAL,
    FOREIGN KEY(docs_id) REFERENCES docs(id),
    FOREIGN KEY(topics_id) REFERENCES topics(id)
    
);

CREATE TABLE IF NOT EXISTS validate(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_name TEXT UNIQUE NOT NULL    
);

CREATE TABLE IF NOT EXISTS word_intrusion(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  validate_id INTEGER NOT NULL,
  topic_name TEXT NOT NULL,
  word_one TEXT NOT NULL,
  word_two TEXT NOT NULL,
  word_three TEXT NOT NULL,
  word_four TEXT NOT NULL,
  word_five TEXT NOT NULL,
  word_intrusion TEXT NOT NULL,
  hit_answer INTEGER NOT NULL,
  FOREIGN KEY(validate_id) REFERENCES validate(id)
);

CREATE TABLE IF NOT EXISTS topic_intrusion(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  validate_id INTEGER NOT NULL,
  docs_id INTEGER NOT NULL,
  topic_one TEXT NOT NULL,
  topic_one_list_word TEXT NOT NULL,
  topic_two TEXT NOT NULL,
  topic_two_list_word TEXT NOT NULL,
  topic_three TEXT NOT NULL,
  topic_three_list_word TEXT NOT NULL,
  topic_intrusion TEXT NOT NULL,
  topic_intrusion_list_word TEXT NOT NULL,
  hit_answer INTEGER NOT NULL,
  FOREIGN KEY(validate_id) REFERENCES validate(id),
  FOREIGN KEY(docs_id) REFERENCES docs(id)
);
