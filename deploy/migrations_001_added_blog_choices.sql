CREATE TABLE "blog_choices"(
  id SERIAL PRIMARY KEY,
  choice_text VARCHAR(200),
  votes INTEGER DEFAULT 0,
  post_id INTEGER REFERENCES "blog_posts"("id")
)
