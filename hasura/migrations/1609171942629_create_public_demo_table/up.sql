CREATE TABLE "public"."public_posts"("id" serial NOT NULL, "title" text NOT NULL, "content" text NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), "created_by" integer NOT NULL, PRIMARY KEY ("id") , FOREIGN KEY ("id") REFERENCES "public"."auth_user"("id") ON UPDATE no action ON DELETE no action);
CREATE OR REPLACE FUNCTION "public"."set_current_timestamp_updated_at"()
RETURNS TRIGGER AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER "set_public_public_posts_updated_at"
BEFORE UPDATE ON "public"."public_posts"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_public_posts_updated_at" ON "public"."public_posts" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';

INSERT INTO public.auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES ('password', NULL, false, 'martin', 'Martin', 'Mark', 'martin@martinmark.com', false, false, '2020-12-28 16:33:55.689365+00') ON CONFLICT DO NOTHING;
INSERT INTO public.public_posts (title, content, created_at, updated_at, created_by) VALUES ('Test Post', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2020-12-28 16:34:37.387699+00', '2020-12-28 16:35:15.827609+00', 1) ON CONFLICT DO NOTHING;