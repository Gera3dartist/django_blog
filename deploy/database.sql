-- Post table
CREATE TABLE "blog_posts" (
  id SERIAL PRIMARY KEY ,
  body      VARCHAR(1000),
  created TIMESTAMP WITH TIME ZONE DEFAULT now(),
  user_id INTEGER REFERENCES "auth_user"("id")
);

-- Votes table
CREATE TABLE "blog_choices"(
  id SERIAL PRIMARY KEY,
  choice_text VARCHAR(200),
  votes INTEGER DEFAULT 0,
  post INTEGER REFERENCES "blog_posts"("id")
)
