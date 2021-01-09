CREATE FUNCTION demo_public_posts_search(search text)
RETURNS SETOF demo_public_posts AS $$
    SELECT *
    FROM demo_public_posts
    WHERE
      title ilike ('%' || search || '%')
      OR content ilike ('%' || search || '%')
$$ LANGUAGE sql STABLE;
