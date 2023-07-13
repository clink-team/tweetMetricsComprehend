CREATE TABLE analises_sentimentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sentiment VARCHAR(10),
  tweet TEXT,
  mixed DOUBLE,
  negative DOUBLE,
  neutral DOUBLE,
  positive DOUBLE
);