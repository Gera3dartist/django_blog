-- Post table
CREATE TABLE "blog_posts" (
  id INTEGER PRIMARY KEY NOT NULL,
  body      VARCHAR(1000),
  created TIMESTAMP WITH TIME ZONE DEFAULT now(),
  user_id INTEGER REFERENCES "auth_user"("id")
);
