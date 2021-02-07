DROP TABLE IF EXISTS docs;
DROP TABLE IF EXISTS terms;
DROP TABLE IF EXISTS docs_terms;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS topics_terms;
DROP TABLE IF EXISTS docs_topics;
DROP TABLE IF EXISTS validate;
DROP TABLE IF EXISTS word_intrusion;
DROP TABLE IF EXISTS topic_intrusion;
DELETE FROM sqlite_sequence; -- truncate table