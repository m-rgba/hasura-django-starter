CREATE OR REPLACE VIEW "public"."demo_public_posts_count" AS
  SELECT
    demo_public_posts.created_by,
    count(*) AS posts
  FROM
    demo_public_posts
  GROUP BY
    demo_public_posts.created_by;
