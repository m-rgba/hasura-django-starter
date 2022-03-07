CREATE TABLE "public"."demo_realtime"("id" serial NOT NULL, "message" Text NOT NULL, "created_by" integer NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), PRIMARY KEY ("id"));
