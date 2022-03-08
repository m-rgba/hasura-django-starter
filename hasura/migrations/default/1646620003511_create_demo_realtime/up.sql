CREATE TABLE "public"."demo_realtime"(
    "id" serial NOT NULL, 
    "message" Text NOT NULL, 
    "created_by" integer NOT NULL, 
    "created_at" timestamptz NOT NULL DEFAULT now(), 
    PRIMARY KEY ("id")
);

ALTER TABLE "public"."demo_realtime"
  ADD CONSTRAINT "demo_realtime_created_by_fkey"
  FOREIGN KEY ("created_by")
  REFERENCES "public"."auth_user"
  ("id") ON UPDATE CASCADE ON DELETE CASCADE;