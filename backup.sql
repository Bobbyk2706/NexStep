--
-- PostgreSQL database dump
--

\restrict WKVq8s8q1VDx5dp9IyWccvw5tvwF4tLWdH2zDofUCz5RVfhbqhCaNegioUdOO75

-- Dumped from database version 17.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: auth; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA auth;


ALTER SCHEMA auth OWNER TO supabase_admin;

--
-- Name: extensions; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA extensions;


ALTER SCHEMA extensions OWNER TO postgres;

--
-- Name: graphql; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA graphql;


ALTER SCHEMA graphql OWNER TO supabase_admin;

--
-- Name: graphql_public; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA graphql_public;


ALTER SCHEMA graphql_public OWNER TO supabase_admin;

--
-- Name: pgbouncer; Type: SCHEMA; Schema: -; Owner: pgbouncer
--

CREATE SCHEMA pgbouncer;


ALTER SCHEMA pgbouncer OWNER TO pgbouncer;

--
-- Name: realtime; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA realtime;


ALTER SCHEMA realtime OWNER TO supabase_admin;

--
-- Name: storage; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA storage;


ALTER SCHEMA storage OWNER TO supabase_admin;

--
-- Name: vault; Type: SCHEMA; Schema: -; Owner: supabase_admin
--

CREATE SCHEMA vault;


ALTER SCHEMA vault OWNER TO supabase_admin;

--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA extensions;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: supabase_vault; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS supabase_vault WITH SCHEMA vault;


--
-- Name: EXTENSION supabase_vault; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION supabase_vault IS 'Supabase Vault Extension';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA extensions;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: aal_level; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.aal_level AS ENUM (
    'aal1',
    'aal2',
    'aal3'
);


ALTER TYPE auth.aal_level OWNER TO supabase_auth_admin;

--
-- Name: code_challenge_method; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.code_challenge_method AS ENUM (
    's256',
    'plain'
);


ALTER TYPE auth.code_challenge_method OWNER TO supabase_auth_admin;

--
-- Name: factor_status; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.factor_status AS ENUM (
    'unverified',
    'verified'
);


ALTER TYPE auth.factor_status OWNER TO supabase_auth_admin;

--
-- Name: factor_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.factor_type AS ENUM (
    'totp',
    'webauthn',
    'phone',
    'recovery_code'
);


ALTER TYPE auth.factor_type OWNER TO supabase_auth_admin;

--
-- Name: oauth_authorization_status; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_authorization_status AS ENUM (
    'pending',
    'approved',
    'denied',
    'expired'
);


ALTER TYPE auth.oauth_authorization_status OWNER TO supabase_auth_admin;

--
-- Name: oauth_client_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_client_type AS ENUM (
    'public',
    'confidential'
);


ALTER TYPE auth.oauth_client_type OWNER TO supabase_auth_admin;

--
-- Name: oauth_registration_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_registration_type AS ENUM (
    'dynamic',
    'manual'
);


ALTER TYPE auth.oauth_registration_type OWNER TO supabase_auth_admin;

--
-- Name: oauth_response_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.oauth_response_type AS ENUM (
    'code'
);


ALTER TYPE auth.oauth_response_type OWNER TO supabase_auth_admin;

--
-- Name: one_time_token_type; Type: TYPE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TYPE auth.one_time_token_type AS ENUM (
    'confirmation_token',
    'reauthentication_token',
    'recovery_token',
    'email_change_token_new',
    'email_change_token_current',
    'phone_change_token'
);


ALTER TYPE auth.one_time_token_type OWNER TO supabase_auth_admin;

--
-- Name: action; Type: TYPE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TYPE realtime.action AS ENUM (
    'INSERT',
    'UPDATE',
    'DELETE',
    'TRUNCATE',
    'ERROR'
);


ALTER TYPE realtime.action OWNER TO supabase_realtime_admin;

--
-- Name: equality_op; Type: TYPE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TYPE realtime.equality_op AS ENUM (
    'eq',
    'neq',
    'lt',
    'lte',
    'gt',
    'gte',
    'in',
    'like',
    'ilike',
    'is',
    'match',
    'imatch',
    'isdistinct'
);


ALTER TYPE realtime.equality_op OWNER TO supabase_realtime_admin;

--
-- Name: user_defined_filter; Type: TYPE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TYPE realtime.user_defined_filter AS (
	column_name text,
	op realtime.equality_op,
	value text,
	negate boolean
);


ALTER TYPE realtime.user_defined_filter OWNER TO supabase_realtime_admin;

--
-- Name: wal_column; Type: TYPE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TYPE realtime.wal_column AS (
	name text,
	type_name text,
	type_oid oid,
	value jsonb,
	is_pkey boolean,
	is_selectable boolean
);


ALTER TYPE realtime.wal_column OWNER TO supabase_realtime_admin;

--
-- Name: wal_rls; Type: TYPE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TYPE realtime.wal_rls AS (
	wal jsonb,
	is_rls_enabled boolean,
	subscription_ids uuid[],
	errors text[]
);


ALTER TYPE realtime.wal_rls OWNER TO supabase_realtime_admin;

--
-- Name: buckettype; Type: TYPE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TYPE storage.buckettype AS ENUM (
    'STANDARD',
    'ANALYTICS',
    'VECTOR'
);


ALTER TYPE storage.buckettype OWNER TO supabase_storage_admin;

--
-- Name: email(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.email() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.email', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'email')
  )::text
$$;


ALTER FUNCTION auth.email() OWNER TO supabase_auth_admin;

--
-- Name: FUNCTION email(); Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON FUNCTION auth.email() IS 'Deprecated. Use auth.jwt() -> ''email'' instead.';


--
-- Name: jwt(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.jwt() RETURNS jsonb
    LANGUAGE sql STABLE
    AS $$
  select 
    coalesce(
        nullif(current_setting('request.jwt.claim', true), ''),
        nullif(current_setting('request.jwt.claims', true), '')
    )::jsonb
$$;


ALTER FUNCTION auth.jwt() OWNER TO supabase_auth_admin;

--
-- Name: role(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.role() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.role', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'role')
  )::text
$$;


ALTER FUNCTION auth.role() OWNER TO supabase_auth_admin;

--
-- Name: FUNCTION role(); Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON FUNCTION auth.role() IS 'Deprecated. Use auth.jwt() -> ''role'' instead.';


--
-- Name: uid(); Type: FUNCTION; Schema: auth; Owner: supabase_auth_admin
--

CREATE FUNCTION auth.uid() RETURNS uuid
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')
  )::uuid
$$;


ALTER FUNCTION auth.uid() OWNER TO supabase_auth_admin;

--
-- Name: FUNCTION uid(); Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON FUNCTION auth.uid() IS 'Deprecated. Use auth.jwt() -> ''sub'' instead.';


--
-- Name: grant_pg_cron_access(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.grant_pg_cron_access() RETURNS event_trigger
    LANGUAGE plpgsql
    SET search_path TO ''
    AS $$
BEGIN
  IF EXISTS (
    SELECT
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_cron'
  )
  THEN
    grant usage on schema cron to postgres with grant option;

    alter default privileges in schema cron grant all on tables to postgres with grant option;
    alter default privileges in schema cron grant all on functions to postgres with grant option;
    alter default privileges in schema cron grant all on sequences to postgres with grant option;

    alter default privileges for user supabase_admin in schema cron grant all
        on sequences to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on tables to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on functions to postgres with grant option;

    grant all privileges on all tables in schema cron to postgres with grant option;
    revoke all on table cron.job from postgres;
    grant select on table cron.job to postgres with grant option;
    revoke trigger on cron.job_run_details from postgres;
  END IF;
END;
$$;


ALTER FUNCTION extensions.grant_pg_cron_access() OWNER TO supabase_admin;

--
-- Name: FUNCTION grant_pg_cron_access(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.grant_pg_cron_access() IS 'Grants access to pg_cron';


--
-- Name: grant_pg_graphql_access(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.grant_pg_graphql_access() RETURNS event_trigger
    LANGUAGE plpgsql
    SET search_path TO ''
    AS $_$
begin
    if not exists (
        select 1
        from pg_catalog.pg_event_trigger_ddl_commands() ev
        join pg_catalog.pg_extension e on ev.objid = e.oid
        where e.extname = 'pg_graphql'
    ) then
        return;
    end if;

    drop function if exists graphql_public.graphql;
    create or replace function graphql_public.graphql(
        "operationName" text default null,
        query text default null,
        variables jsonb default null,
        extensions jsonb default null
    )
        returns jsonb
        language sql
    as $$
        select graphql.resolve(
            query := query,
            variables := coalesce(variables, '{}'),
            "operationName" := "operationName",
            extensions := extensions
        );
    $$;

    -- Attach the wrapper to the extension so DROP EXTENSION cascades to it,
    -- which in turn triggers set_graphql_placeholder to reinstall the "not enabled" stub.
    alter extension pg_graphql add function graphql_public.graphql(text, text, jsonb, jsonb);

    grant usage on schema graphql to postgres, anon, authenticated, service_role;
    grant execute on function graphql.resolve to postgres, anon, authenticated, service_role;
    grant usage on schema graphql to postgres with grant option;
    grant usage on schema graphql_public to postgres with grant option;
end;
$_$;


ALTER FUNCTION extensions.grant_pg_graphql_access() OWNER TO supabase_admin;

--
-- Name: FUNCTION grant_pg_graphql_access(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.grant_pg_graphql_access() IS 'Grants access to pg_graphql';


--
-- Name: grant_pg_net_access(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.grant_pg_net_access() RETURNS event_trigger
    LANGUAGE plpgsql
    SET search_path TO ''
    AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_net'
  )
  THEN
    IF NOT EXISTS (
      SELECT 1
      FROM pg_roles
      WHERE rolname = 'supabase_functions_admin'
    )
    THEN
      CREATE USER supabase_functions_admin NOINHERIT CREATEROLE LOGIN NOREPLICATION;
    END IF;

    GRANT USAGE ON SCHEMA net TO supabase_functions_admin, postgres, anon, authenticated, service_role;

    IF EXISTS (
      SELECT FROM pg_extension
      WHERE extname = 'pg_net'
      -- all versions in use on existing projects as of 2025-02-20
      -- version 0.12.0 onwards don't need these applied
      AND extversion IN ('0.2', '0.6', '0.7', '0.7.1', '0.8.0', '0.10.0', '0.11.0')
    ) THEN
      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;

      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;

      REVOKE ALL ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;
      REVOKE ALL ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;

      GRANT EXECUTE ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
      GRANT EXECUTE ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
    END IF;
  END IF;
END;
$$;


ALTER FUNCTION extensions.grant_pg_net_access() OWNER TO supabase_admin;

--
-- Name: FUNCTION grant_pg_net_access(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.grant_pg_net_access() IS 'Grants access to pg_net';


--
-- Name: pgrst_ddl_watch(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.pgrst_ddl_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    SET search_path TO ''
    AS $$
DECLARE
  cmd record;
BEGIN
  FOR cmd IN SELECT * FROM pg_event_trigger_ddl_commands()
  LOOP
    IF cmd.command_tag IN (
      'CREATE SCHEMA', 'ALTER SCHEMA'
    , 'CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO', 'ALTER TABLE'
    , 'CREATE FOREIGN TABLE', 'ALTER FOREIGN TABLE'
    , 'CREATE VIEW', 'ALTER VIEW'
    , 'CREATE MATERIALIZED VIEW', 'ALTER MATERIALIZED VIEW'
    , 'CREATE FUNCTION', 'ALTER FUNCTION'
    , 'CREATE TRIGGER'
    , 'CREATE TYPE', 'ALTER TYPE'
    , 'CREATE RULE'
    , 'COMMENT'
    )
    -- don't notify in case of CREATE TEMP table or other objects created on pg_temp
    AND cmd.schema_name is distinct from 'pg_temp'
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


ALTER FUNCTION extensions.pgrst_ddl_watch() OWNER TO supabase_admin;

--
-- Name: pgrst_drop_watch(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.pgrst_drop_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    SET search_path TO ''
    AS $$
DECLARE
  obj record;
BEGIN
  FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
  LOOP
    IF obj.object_type IN (
      'schema'
    , 'table'
    , 'foreign table'
    , 'view'
    , 'materialized view'
    , 'function'
    , 'trigger'
    , 'type'
    , 'rule'
    )
    AND obj.is_temporary IS false -- no pg_temp objects
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


ALTER FUNCTION extensions.pgrst_drop_watch() OWNER TO supabase_admin;

--
-- Name: set_graphql_placeholder(); Type: FUNCTION; Schema: extensions; Owner: supabase_admin
--

CREATE FUNCTION extensions.set_graphql_placeholder() RETURNS event_trigger
    LANGUAGE plpgsql
    SET search_path TO ''
    AS $_$
    DECLARE
    graphql_is_dropped bool;
    BEGIN
    graphql_is_dropped = (
        SELECT ev.schema_name = 'graphql_public'
        FROM pg_event_trigger_dropped_objects() AS ev
        WHERE ev.schema_name = 'graphql_public'
    );

    IF graphql_is_dropped
    THEN
        create or replace function graphql_public.graphql(
            "operationName" text default null,
            query text default null,
            variables jsonb default null,
            extensions jsonb default null
        )
            returns jsonb
            language plpgsql
            set search_path to ''
        as $$
            DECLARE
                server_version float;
            BEGIN
                server_version = (SELECT (SPLIT_PART((select version()), ' ', 2))::float);

                IF server_version >= 14 THEN
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql extension is not enabled.'
                            )
                        )
                    );
                ELSE
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql is only available on projects running Postgres 14 onwards.'
                            )
                        )
                    );
                END IF;
            END;
        $$;
    END IF;

    END;
$_$;


ALTER FUNCTION extensions.set_graphql_placeholder() OWNER TO supabase_admin;

--
-- Name: FUNCTION set_graphql_placeholder(); Type: COMMENT; Schema: extensions; Owner: supabase_admin
--

COMMENT ON FUNCTION extensions.set_graphql_placeholder() IS 'Reintroduces placeholder function for graphql_public.graphql';


--
-- Name: graphql(text, text, jsonb, jsonb); Type: FUNCTION; Schema: graphql_public; Owner: supabase_admin
--

CREATE FUNCTION graphql_public.graphql("operationName" text DEFAULT NULL::text, query text DEFAULT NULL::text, variables jsonb DEFAULT NULL::jsonb, extensions jsonb DEFAULT NULL::jsonb) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
            DECLARE
                server_version float;
            BEGIN
                server_version = (SELECT (SPLIT_PART((select version()), ' ', 2))::float);

                IF server_version >= 14 THEN
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql extension is not enabled.'
                            )
                        )
                    );
                ELSE
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql is only available on projects running Postgres 14 onwards.'
                            )
                        )
                    );
                END IF;
            END;
        $$;


ALTER FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) OWNER TO supabase_admin;

--
-- Name: get_auth(text); Type: FUNCTION; Schema: pgbouncer; Owner: supabase_admin
--

CREATE FUNCTION pgbouncer.get_auth(p_usename text) RETURNS TABLE(username text, password text)
    LANGUAGE plpgsql SECURITY DEFINER
    SET search_path TO ''
    AS $_$
  BEGIN
      RAISE DEBUG 'PgBouncer auth request: %', p_usename;

      RETURN QUERY
      SELECT
          rolname::text,
          CASE WHEN rolvaliduntil < now()
              THEN null
              ELSE rolpassword::text
          END
      FROM pg_authid
      WHERE rolname=$1 and rolcanlogin;
  END;
  $_$;


ALTER FUNCTION pgbouncer.get_auth(p_usename text) OWNER TO supabase_admin;

--
-- Name: apply_rls(jsonb, integer); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer DEFAULT (1024 * 1024)) RETURNS SETOF realtime.wal_rls
    LANGUAGE plpgsql
    AS $$
declare
    -- Regclass of the table e.g. public.notes
    entity_ regclass = (quote_ident(wal ->> 'schema') || '.' || quote_ident(wal ->> 'table'))::regclass;

    -- I, U, D, T: insert, update ...
    action realtime.action = (
        case wal ->> 'action'
            when 'I' then 'INSERT'
            when 'U' then 'UPDATE'
            when 'D' then 'DELETE'
            else 'ERROR'
        end
    );

    -- Is row level security enabled for the table
    is_rls_enabled bool = relrowsecurity from pg_class where oid = entity_;

    subscriptions realtime.subscription[] = array_agg(subs)
        from
            realtime.subscription subs
        where
            subs.entity = entity_
            -- Filter by action early - only get subscriptions interested in this action
            -- action_filter column can be: '*' (all), 'INSERT', 'UPDATE', or 'DELETE'
            and (subs.action_filter = '*' or subs.action_filter = action::text);

    -- Subscription vars
    working_role regrole;
    working_selected_columns text[];
    claimed_role regrole;
    claims jsonb;

    subscription_id uuid;
    subscription_has_access bool;
    visible_to_subscription_ids uuid[] = '{}';

    -- structured info for wal's columns
    columns realtime.wal_column[];
    -- previous identity values for update/delete
    old_columns realtime.wal_column[];

    error_record_exceeds_max_size boolean = octet_length(wal::text) > max_record_bytes;

    -- Primary jsonb output for record
    output jsonb;

    -- Loop record for iterating unique roles (outer loop)
    role_record record;
    -- Loop record for iterating unique selected_columns within a role (inner loop)
    cols_record record;
    -- Subscription ids visible at the role level (before fanning out by selected_columns)
    visible_role_sub_ids uuid[] = '{}';

begin
    perform set_config('role', null, true);

    columns =
        array_agg(
            (
                x->>'name',
                x->>'type',
                x->>'typeoid',
                realtime.cast(
                    (x->'value') #>> '{}',
                    coalesce(
                        (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                        (x->>'type')::regtype
                    )
                ),
                (pks ->> 'name') is not null,
                true
            )::realtime.wal_column
        )
        from
            jsonb_array_elements(wal -> 'columns') x
            left join jsonb_array_elements(wal -> 'pk') pks
                on (x ->> 'name') = (pks ->> 'name');

    old_columns =
        array_agg(
            (
                x->>'name',
                x->>'type',
                x->>'typeoid',
                realtime.cast(
                    (x->'value') #>> '{}',
                    coalesce(
                        (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                        (x->>'type')::regtype
                    )
                ),
                (pks ->> 'name') is not null,
                true
            )::realtime.wal_column
        )
        from
            jsonb_array_elements(wal -> 'identity') x
            left join jsonb_array_elements(wal -> 'pk') pks
                on (x ->> 'name') = (pks ->> 'name');

    for role_record in
        select claims_role
        from (select distinct claims_role from unnest(subscriptions)) t
        order by claims_role::text
    loop
        working_role := role_record.claims_role;

        -- Update `is_selectable` for columns and old_columns (once per role)
        columns =
            array_agg(
                (
                    c.name,
                    c.type_name,
                    c.type_oid,
                    c.value,
                    c.is_pkey,
                    pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
                )::realtime.wal_column
            )
            from
                unnest(columns) c;

        old_columns =
                array_agg(
                    (
                        c.name,
                        c.type_name,
                        c.type_oid,
                        c.value,
                        c.is_pkey,
                        pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
                    )::realtime.wal_column
                )
                from
                    unnest(old_columns) c;

        if action <> 'DELETE' and count(1) = 0 from unnest(columns) c where c.is_pkey then
            -- Fan out 400 error per distinct selected_columns for this role
            for cols_record in
                select selected_columns
                from (select distinct selected_columns from unnest(subscriptions) s where s.claims_role = working_role) t
                order by coalesce(array_to_string(selected_columns, ','), '')
            loop
                working_selected_columns := cols_record.selected_columns;
                return next (
                    jsonb_build_object(
                        'schema', wal ->> 'schema',
                        'table', wal ->> 'table',
                        'type', action
                    ),
                    is_rls_enabled,
                    (select array_agg(s.subscription_id) from unnest(subscriptions) as s where s.claims_role = working_role and (s.selected_columns is not distinct from working_selected_columns)),
                    array['Error 400: Bad Request, no primary key']
                )::realtime.wal_rls;
            end loop;

        -- The claims role does not have SELECT permission to the primary key of entity
        elsif action <> 'DELETE' and sum(c.is_selectable::int) <> count(1) from unnest(columns) c where c.is_pkey then
            -- Fan out 401 error per distinct selected_columns for this role
            for cols_record in
                select selected_columns
                from (select distinct selected_columns from unnest(subscriptions) s where s.claims_role = working_role) t
                order by coalesce(array_to_string(selected_columns, ','), '')
            loop
                working_selected_columns := cols_record.selected_columns;
                return next (
                    jsonb_build_object(
                        'schema', wal ->> 'schema',
                        'table', wal ->> 'table',
                        'type', action
                    ),
                    is_rls_enabled,
                    (select array_agg(s.subscription_id) from unnest(subscriptions) as s where s.claims_role = working_role and (s.selected_columns is not distinct from working_selected_columns)),
                    array['Error 401: Unauthorized']
                )::realtime.wal_rls;
            end loop;

        else
            -- Create the prepared statement (once per role)
            if is_rls_enabled and action <> 'DELETE' then
                if (select 1 from pg_prepared_statements where name = 'walrus_rls_stmt' limit 1) > 0 then
                    deallocate walrus_rls_stmt;
                end if;
                execute realtime.build_prepared_statement_sql('walrus_rls_stmt', entity_, columns);
            end if;

            -- Collect all visible subscription IDs for this role (filter check + RLS check)
            visible_role_sub_ids = '{}';

            for subscription_id, claims in (
                    select
                        subs.subscription_id,
                        subs.claims
                    from
                        unnest(subscriptions) subs
                    where
                        subs.entity = entity_
                        and subs.claims_role = working_role
                        and (
                            realtime.is_visible_through_filters(columns, subs.filters)
                            or (
                              action = 'DELETE'
                              and realtime.is_visible_through_filters(old_columns, subs.filters)
                            )
                        )
            ) loop

                if not is_rls_enabled or action = 'DELETE' then
                    visible_role_sub_ids = visible_role_sub_ids || subscription_id;
                else
                    -- Check if RLS allows the role to see the record
                    perform
                        -- Trim leading and trailing quotes from working_role because set_config
                        -- doesn't recognize the role as valid if they are included
                        set_config('role', trim(both '"' from working_role::text), true),
                        set_config('request.jwt.claims', claims::text, true);

                    execute 'execute walrus_rls_stmt' into subscription_has_access;

                    -- Reset the role on every FOR..LOOP batch execution.
                    -- The first batch of 10 rows is pre-fetched using the current connection role (PG internal behaviour)
                    -- then we have to reset it again otherwise it would use the role defined in the `set_config` above
                    -- to fetch the remaining rows when rows>10, which could be a user-defined role that lacks execution grants.
                    -- The flow is:
                    --   1. run batch with conn role
                    --   2. set_config working_role
                    --   3. execute walrus
                    --   4. reset role (revert)
                    --   5. repeat
                    perform set_config('role', null, true);

                    if subscription_has_access then
                        visible_role_sub_ids = visible_role_sub_ids || subscription_id;
                    end if;
                end if;
            end loop;

            perform set_config('role', null, true);

            -- Inner loop: per distinct selected_columns for this role
            for cols_record in
                select selected_columns
                from (select distinct selected_columns from unnest(subscriptions) s where s.claims_role = working_role) t
                order by coalesce(array_to_string(selected_columns, ','), '')
            loop
                working_selected_columns := cols_record.selected_columns;

                output = jsonb_build_object(
                    'schema', wal ->> 'schema',
                    'table', wal ->> 'table',
                    'type', action,
                    'commit_timestamp', to_char(
                        ((wal ->> 'timestamp')::timestamptz at time zone 'utc'),
                        'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"'
                    ),
                    'columns', (
                        select
                            jsonb_agg(
                                jsonb_build_object(
                                    'name', pa.attname,
                                    'type', pt.typname
                                )
                                order by pa.attnum asc
                            )
                        from
                            pg_attribute pa
                            join pg_type pt
                                on pa.atttypid = pt.oid
                            left join (
                                select unnest(conkey) as pkey_attnum
                                from pg_constraint
                                where conrelid = entity_ and contype = 'p'
                            ) pk on pk.pkey_attnum = pa.attnum
                        where
                            attrelid = entity_
                            and attnum > 0
                            and pg_catalog.has_column_privilege(working_role, entity_, pa.attname, 'SELECT')
                            and (working_selected_columns is null or pa.attname = any(working_selected_columns) or pk.pkey_attnum is not null)
                    )
                )
                -- Add "record" key for insert and update
                || case
                    when action in ('INSERT', 'UPDATE') then
                        jsonb_build_object(
                            'record',
                            (
                                select
                                    jsonb_object_agg(
                                        -- if unchanged toast, get column name and value from old record
                                        coalesce((c).name, (oc).name),
                                        case
                                            when (c).name is null then (oc).value
                                            else (c).value
                                        end
                                    )
                                from
                                    unnest(columns) c
                                    full outer join unnest(old_columns) oc
                                        on (c).name = (oc).name
                                where
                                    coalesce((c).is_selectable, (oc).is_selectable)
                                    and (working_selected_columns is null or coalesce((c).name, (oc).name) = any(working_selected_columns) or coalesce((c).is_pkey, (oc).is_pkey))
                                    and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                            )
                        )
                    else '{}'::jsonb
                end
                -- Add "old_record" key for update and delete
                || case
                    when action = 'UPDATE' then
                        jsonb_build_object(
                                'old_record',
                                (
                                    select jsonb_object_agg((c).name, (c).value)
                                    from unnest(old_columns) c
                                    where
                                        (c).is_selectable
                                        and (working_selected_columns is null or (c).name = any(working_selected_columns) or (c).is_pkey)
                                        and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                                )
                            )
                    when action = 'DELETE' then
                        jsonb_build_object(
                            'old_record',
                            (
                                select jsonb_object_agg((c).name, (c).value)
                                from unnest(old_columns) c
                                where
                                    (c).is_selectable
                                    and (working_selected_columns is null or (c).name = any(working_selected_columns) or (c).is_pkey)
                                    and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                                    and ( not is_rls_enabled or (c).is_pkey ) -- if RLS enabled, we can't secure deletes so filter to pkey
                            )
                        )
                    else '{}'::jsonb
                end;

                -- Filter visible_role_sub_ids to those matching the current selected_columns group
                visible_to_subscription_ids = coalesce(
                    (
                        select array_agg(s.subscription_id)
                        from unnest(subscriptions) s
                        where s.claims_role = working_role
                          and (s.selected_columns is not distinct from working_selected_columns)
                          and s.subscription_id = any(visible_role_sub_ids)
                    ),
                    '{}'::uuid[]
                );

                return next (
                    output,
                    is_rls_enabled,
                    visible_to_subscription_ids,
                    case
                        when error_record_exceeds_max_size then array['Error 413: Payload Too Large']
                        else '{}'
                    end
                )::realtime.wal_rls;
            end loop;

        end if;
    end loop;

    perform set_config('role', null, true);
end;
$$;


ALTER FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) OWNER TO supabase_realtime_admin;

--
-- Name: broadcast_changes(text, text, text, text, text, record, record, text); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text DEFAULT 'ROW'::text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    -- Declare a variable to hold the JSONB representation of the row
    row_data jsonb := '{}'::jsonb;
BEGIN
    IF level = 'STATEMENT' THEN
        RAISE EXCEPTION 'function can only be triggered for each row, not for each statement';
    END IF;
    -- Check the operation type and handle accordingly
    IF operation = 'INSERT' OR operation = 'UPDATE' OR operation = 'DELETE' THEN
        row_data := jsonb_build_object('old_record', OLD, 'record', NEW, 'operation', operation, 'table', table_name, 'schema', table_schema);
        PERFORM realtime.send (row_data, event_name, topic_name);
    ELSE
        RAISE EXCEPTION 'Unexpected operation type: %', operation;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Failed to process the row: %', SQLERRM;
END;

$$;


ALTER FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text) OWNER TO supabase_realtime_admin;

--
-- Name: build_prepared_statement_sql(text, regclass, realtime.wal_column[]); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) RETURNS text
    LANGUAGE sql
    AS $$
      /*
      Builds a sql string that, if executed, creates a prepared statement to
      tests retrive a row from *entity* by its primary key columns.
      Example
          select realtime.build_prepared_statement_sql('public.notes', '{"id"}'::text[], '{"bigint"}'::text[])
      */
          select
      'prepare ' || prepared_statement_name || ' as
          select
              exists(
                  select
                      1
                  from
                      ' || entity || '
                  where
                      ' || string_agg(quote_ident(pkc.name) || '=' || quote_nullable(pkc.value #>> '{}') , ' and ') || '
              )'
          from
              unnest(columns) pkc
          where
              pkc.is_pkey
          group by
              entity
      $$;


ALTER FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) OWNER TO supabase_realtime_admin;

--
-- Name: cast(text, regtype); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime."cast"(val text, type_ regtype) RETURNS jsonb
    LANGUAGE plpgsql IMMUTABLE
    AS $$
declare
  res jsonb;
begin
  if type_::text = 'bytea' then
    return to_jsonb(val);
  end if;
  execute format('select to_jsonb(%L::'|| type_::text || ')', val) into res;
  return res;
end
$$;


ALTER FUNCTION realtime."cast"(val text, type_ regtype) OWNER TO supabase_realtime_admin;

--
-- Name: check_equality_op(realtime.equality_op, regtype, text, text); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) RETURNS boolean
    LANGUAGE plpgsql IMMUTABLE
    AS $$
/*
Casts *val_1* and *val_2* as type *type_* and check the *op* condition for truthiness
*/
declare
    op_symbol text = (
        case
            when op = 'eq' then '='
            when op = 'neq' then '!='
            when op = 'lt' then '<'
            when op = 'lte' then '<='
            when op = 'gt' then '>'
            when op = 'gte' then '>='
            when op = 'in' then '= any'
            else 'UNKNOWN OP'
        end
    );
    res boolean;
begin
    execute format(
        'select %L::'|| type_::text || ' ' || op_symbol
        || ' ( %L::'
        || (
            case
                when op = 'in' then type_::text || '[]'
                else type_::text end
        )
        || ')', val_1, val_2) into res;
    return res;
end;
$$;


ALTER FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) OWNER TO supabase_realtime_admin;

--
-- Name: check_equality_op(realtime.equality_op, regtype, text, text, boolean); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean) RETURNS boolean
    LANGUAGE plpgsql STABLE
    AS $$
declare
    op_symbol text;
    res boolean;
begin
    -- IS DISTINCT FROM / IS NOT DISTINCT FROM: infix, both sides typed literals
    if op = 'isdistinct' then
        execute format(
            'select %L::%s %s %L::%s',
            val_1,
            type_::text,
            case when negate then 'IS NOT DISTINCT FROM' else 'IS DISTINCT FROM' end,
            val_2,
            type_::text
        ) into res;
        return res;
    end if;

    -- IS requires a keyword RHS (NULL, TRUE, FALSE, UNKNOWN), not a typed literal
    if op = 'is' then
        if val_2 not in ('null', 'true', 'false', 'unknown') then
            raise exception 'invalid value for is filter: must be null, true, false, or unknown';
        end if;
        execute format(
            'select %L::%s %s %s',
            val_1,
            type_::text,
            case when negate then 'IS NOT' else 'IS' end,
            upper(val_2)
        ) into res;
        return res;
    end if;

    op_symbol = case
        when op = 'eq'    then '='
        when op = 'neq'   then '!='
        when op = 'lt'    then '<'
        when op = 'lte'   then '<='
        when op = 'gt'    then '>'
        when op = 'gte'   then '>='
        when op = 'in'    then '= any'
        when op = 'like'   then 'LIKE'
        when op = 'ilike'  then 'ILIKE'
        when op = 'match'  then '~'
        when op = 'imatch' then '~*'
        else null
    end;

    if op_symbol is null then
        raise exception 'unsupported equality operator: %', op::text;
    end if;

    execute format(
        'select %L::%s %s (%L::%s)',
        val_1,
        type_::text,
        op_symbol,
        val_2,
        case when op = 'in' then type_::text || '[]' else type_::text end
    ) into res;

    return case when negate then not res else res end;
end;
$$;


ALTER FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean) OWNER TO supabase_realtime_admin;

--
-- Name: is_visible_through_filters(realtime.wal_column[], realtime.user_defined_filter[]); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$
    select
        filters is null
        or array_length(filters, 1) is null
        or coalesce(
            count(col.name) = count(1)
            and sum(
                realtime.check_equality_op(
                    op:=f.op,
                    type_:=coalesce(col.type_oid::regtype, col.type_name::regtype),
                    val_1:=col.value #>> '{}',
                    val_2:=f.value,
                    negate:=coalesce(f.negate, false)
                )::int
            ) filter (where col.name is not null) = count(col.name),
            false
        )
    from
        unnest(filters) f
        left join unnest(columns) col
            on f.column_name = col.name;
$$;


ALTER FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) OWNER TO supabase_realtime_admin;

--
-- Name: list_changes(name, name, integer, integer); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) RETURNS TABLE(wal jsonb, is_rls_enabled boolean, subscription_ids uuid[], errors text[], slot_changes_count bigint)
    LANGUAGE sql
    SET log_min_messages TO 'fatal'
    AS $$
  WITH pub AS (
    SELECT
      concat_ws(
        ',',
        CASE WHEN bool_or(pubinsert) THEN 'insert' ELSE NULL END,
        CASE WHEN bool_or(pubupdate) THEN 'update' ELSE NULL END,
        CASE WHEN bool_or(pubdelete) THEN 'delete' ELSE NULL END
      ) AS w2j_actions,
      coalesce(
        string_agg(
          realtime.quote_wal2json(format('%I.%I', schemaname, tablename)::regclass),
          ','
        ) filter (WHERE ppt.tablename IS NOT NULL),
        ''
      ) AS w2j_add_tables
    FROM pg_publication pp
    LEFT JOIN pg_publication_tables ppt ON pp.pubname = ppt.pubname
    WHERE pp.pubname = publication
    GROUP BY pp.pubname
    LIMIT 1
  ),
  -- MATERIALIZED ensures pg_logical_slot_get_changes is called exactly once
  w2j AS MATERIALIZED (
    SELECT x.*, pub.w2j_add_tables
    FROM pub,
         pg_logical_slot_get_changes(
           slot_name, null, max_changes,
           'include-pk', 'true',
           'include-transaction', 'false',
           'include-timestamp', 'true',
           'include-type-oids', 'true',
           'format-version', '2',
           'actions', pub.w2j_actions,
           'add-tables', pub.w2j_add_tables
         ) x
  ),
  slot_count AS (
    SELECT count(*)::bigint AS cnt
    FROM w2j
    WHERE w2j.w2j_add_tables <> ''
  ),
  rls_filtered AS (
    SELECT xyz.wal, xyz.is_rls_enabled, xyz.subscription_ids, xyz.errors
    FROM w2j,
         realtime.apply_rls(
           wal := w2j.data::jsonb,
           max_record_bytes := max_record_bytes
         ) xyz(wal, is_rls_enabled, subscription_ids, errors)
    WHERE w2j.w2j_add_tables <> ''
      AND xyz.subscription_ids[1] IS NOT NULL
  )
  SELECT rf.wal, rf.is_rls_enabled, rf.subscription_ids, rf.errors, sc.cnt
  FROM rls_filtered rf, slot_count sc

  UNION ALL

  SELECT null, null, null, null, sc.cnt
  FROM slot_count sc
  WHERE NOT EXISTS (SELECT 1 FROM rls_filtered)
$$;


ALTER FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) OWNER TO supabase_realtime_admin;

--
-- Name: list_changes_sync(name, name, integer, integer); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.list_changes_sync(publication name, slot_name name, max_changes integer, max_record_bytes integer) RETURNS TABLE(wal jsonb, is_rls_enabled boolean, subscription_ids uuid[], errors text[], slot_changes_count bigint)
    LANGUAGE sql
    SET log_min_messages TO 'fatal'
    AS $$
  WITH pub AS (
    SELECT
      concat_ws(
        ',',
        CASE WHEN bool_or(pubinsert) THEN 'insert' ELSE NULL END,
        CASE WHEN bool_or(pubupdate) THEN 'update' ELSE NULL END,
        CASE WHEN bool_or(pubdelete) THEN 'delete' ELSE NULL END
      ) AS w2j_actions,
      coalesce(
        string_agg(
          realtime.quote_wal2json(format('%I.%I', schemaname, tablename)::regclass),
          ','
        ) filter (WHERE ppt.tablename IS NOT NULL),
        ''
      ) AS w2j_add_tables
    FROM pg_publication pp
    LEFT JOIN pg_publication_tables ppt ON pp.pubname = ppt.pubname
    WHERE pp.pubname = publication
    GROUP BY pp.pubname
    LIMIT 1
  ),
  -- MATERIALIZED ensures the slot is read exactly once.
  consumed AS MATERIALIZED (
    SELECT x.*, pub.w2j_add_tables
    FROM pub,
         realtime.settled_changes(
           slot_name, max_changes,
           'include-pk', 'true',
           'include-transaction', 'false',
           'include-timestamp', 'true',
           'include-type-oids', 'true',
           'format-version', '2',
           'actions', pub.w2j_actions,
           'add-tables', pub.w2j_add_tables
         ) x
  ),
  slot_count AS (
    SELECT count(*)::bigint AS cnt
    FROM consumed
    WHERE consumed.w2j_add_tables <> ''
  ),
  rls_filtered AS (
    SELECT xyz.wal, xyz.is_rls_enabled, xyz.subscription_ids, xyz.errors
    FROM consumed,
         realtime.apply_rls(
           wal := consumed.data::jsonb,
           max_record_bytes := max_record_bytes
         ) xyz(wal, is_rls_enabled, subscription_ids, errors)
    WHERE consumed.w2j_add_tables <> ''
      AND xyz.subscription_ids[1] IS NOT NULL
  )
  SELECT rf.wal, rf.is_rls_enabled, rf.subscription_ids, rf.errors, sc.cnt
  FROM rls_filtered rf, slot_count sc

  UNION ALL

  SELECT null, null, null, null, sc.cnt
  FROM slot_count sc
  WHERE NOT EXISTS (SELECT 1 FROM rls_filtered)
$$;


ALTER FUNCTION realtime.list_changes_sync(publication name, slot_name name, max_changes integer, max_record_bytes integer) OWNER TO supabase_realtime_admin;

--
-- Name: quote_wal2json(regclass); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.quote_wal2json(entity regclass) RETURNS text
    LANGUAGE sql IMMUTABLE STRICT
    AS $$
  SELECT
    realtime.wal2json_escape_identifier(nsp.nspname::text)
    || '.'
    || realtime.wal2json_escape_identifier(pc.relname::text)
  FROM pg_class pc
  JOIN pg_namespace nsp ON pc.relnamespace = nsp.oid
  WHERE pc.oid = entity
$$;


ALTER FUNCTION realtime.quote_wal2json(entity regclass) OWNER TO supabase_realtime_admin;

--
-- Name: send(jsonb, text, text, boolean); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean DEFAULT true) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
  generated_id uuid;
  final_payload jsonb;
BEGIN
  BEGIN
    generated_id := gen_random_uuid();

    -- Check if payload has an 'id' key, if not, add the generated UUID
    IF payload ? 'id' THEN
      final_payload := payload;
    ELSE
      final_payload := jsonb_set(payload, '{id}', to_jsonb(generated_id));
    END IF;

    -- Set the topic configuration
    EXECUTE format('SET LOCAL realtime.topic TO %L', topic);

    INSERT INTO realtime.messages (id, payload, event, topic, private, extension)
    VALUES (generated_id, final_payload, event, topic, private, 'broadcast');
  EXCEPTION
    WHEN OTHERS THEN
      RAISE WARNING 'WarnSendingBroadcastMessage: %', SQLERRM;
  END;
END;
$$;


ALTER FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean) OWNER TO supabase_realtime_admin;

--
-- Name: send_binary(bytea, text, text, boolean); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.send_binary(payload bytea, event text, topic text, private boolean DEFAULT true) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
  generated_id uuid;
BEGIN
  BEGIN
    generated_id := gen_random_uuid();

    EXECUTE format('SET LOCAL realtime.topic TO %L', topic);

    INSERT INTO realtime.messages (id, binary_payload, event, topic, private, extension)
    VALUES (generated_id, payload, event, topic, private, 'broadcast');
  EXCEPTION
    WHEN OTHERS THEN
      RAISE WARNING 'WarnSendingBroadcastMessage: %', SQLERRM;
  END;
END;
$$;


ALTER FUNCTION realtime.send_binary(payload bytea, event text, topic text, private boolean) OWNER TO supabase_realtime_admin;

--
-- Name: settled_changes(name, integer, text[]); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.settled_changes(slot_name name, max_changes integer, VARIADIC opts text[]) RETURNS TABLE(lsn pg_lsn, xid xid, data text)
    LANGUAGE plpgsql
    AS $$
declare
  upto pg_lsn;
  total bigint;
  xids xid[];
  starts bigint[];
  snapshot pg_snapshot;
  running_xids xid[];
  xmax_age int;
  cut bigint;
begin
  -- Each statement in a volatile function takes its own snapshot, which is what lets the
  -- check below see a writer that was still in flight when the peek ran. Under REPEATABLE
  -- READ the snapshot never advances, so a deferred change would never be released.
  if current_setting('transaction_isolation') <> 'read committed' then
    raise exception 'realtime.settled_changes requires READ COMMITTED';
  end if;

  -- The peek and the read below cover the same WAL, so the read cannot reach a commit the
  -- check never saw.
  upto := pg_current_wal_flush_lsn();

  -- One entry per transaction, in commit order: its xid and the position of its first
  -- change. The peek uses the caller's own options, so max_changes counts exactly what the
  -- read counts. A non-transactional logical message is emitted as soon as it is decoded,
  -- tagged with the xid of whatever transaction wrote it, so it does not mark where that
  -- transaction starts.
  select coalesce(sum(g.n), 0),
         array_agg(g.x order by g.first) filter (where g.first is not null),
         array_agg(g.first order by g.first) filter (where g.first is not null)
    into total, xids, starts
    from (
      select p.xid as x, count(*) as n,
             min(p.ord) filter (where not case
               when starts_with(p.data, '{"action":"M"') then (p.data::jsonb->>'transactional')::boolean is false
               else false
             end) as first
      from pg_logical_slot_peek_changes(slot_name, upto, max_changes, variadic opts)
           with ordinality as p(lsn, xid, data, ord)
      group by p.xid
    ) g;

  -- Nothing for the caller, but the slot still has to move past what the peek covered.
  if total = 0 then
    perform pg_replication_slot_advance(slot_name, upto);
    return;
  end if;

  if xids is not null then
    -- Taken after the peek is materialized, so a writer that was still in flight during
    -- decoding is guaranteed to show up here.
    snapshot := pg_current_snapshot();

    -- A commit record reaches the WAL before the writer leaves the proc array, so a change
    -- can be decoded while its row is invisible. apply_rls would resolve a policy against a
    -- row it cannot see and authorize it for nobody, while the read consumed it regardless.
    --
    -- xip lists transactions running when the snapshot was taken. It does not cover a writer
    -- whose xid sits at or beyond xmax, which never appears there, so the horizon is checked
    -- too. age() counts backwards from the current xid and so compares correctly across
    -- wraparound.
    select coalesce(array_agg(running.x::xid), array[]::xid[])
      into running_xids
      from pg_snapshot_xip(snapshot) running(x);
    xmax_age := age(pg_snapshot_xmax(snapshot)::xid);

    select min(u.s) into cut
      from unnest(xids, starts) as u(x, s)
      where u.x = any(running_xids) or age(u.x) <= xmax_age;
  end if;

  -- The read stops right after the commit that brings its count to upto_nchanges, so the
  -- count of changes in front of the first unsettled transaction stops it just before that
  -- transaction.
  if cut is null then
    return query
      select p.* from pg_logical_slot_get_changes(slot_name, upto, max_changes, variadic opts) p;
  elsif cut > 1 then
    return query
      select p.* from pg_logical_slot_get_changes(slot_name, upto, (cut - 1)::int, variadic opts) p;
  end if;
end;
$$;


ALTER FUNCTION realtime.settled_changes(slot_name name, max_changes integer, VARIADIC opts text[]) OWNER TO supabase_realtime_admin;

--
-- Name: subscription_check_filters(); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.subscription_check_filters() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare
    col_names text[] = coalesce(
            array_agg(a.attname order by a.attnum),
            '{}'::text[]
        )
        from
            pg_catalog.pg_attribute a
        where
            a.attrelid = new.entity
            and a.attnum > 0
            and not a.attisdropped
            and pg_catalog.has_column_privilege(
                (new.claims ->> 'role'),
                a.attrelid,
                a.attnum,
                'SELECT'
            );
    filter realtime.user_defined_filter;
    col_type regtype;
    in_val jsonb;
    selected_col text;
begin
    for filter in select * from unnest(new.filters) loop
        if not filter.column_name = any(col_names) then
            raise exception 'invalid column for filter %', filter.column_name;
        end if;

        col_type = (
            select atttypid::regtype
            from pg_catalog.pg_attribute
            where attrelid = new.entity
                  and attname = filter.column_name
        );
        if col_type is null then
            raise exception 'failed to lookup type for column %', filter.column_name;
        end if;

        if filter.op = 'in'::realtime.equality_op then
            in_val = realtime.cast(filter.value, (col_type::text || '[]')::regtype);
            if coalesce(jsonb_array_length(in_val), 0) > 100 then
                raise exception 'too many values for `in` filter. Maximum 100';
            end if;
        elsif filter.op = 'is'::realtime.equality_op then
            -- `is` requires a keyword RHS rather than a typed literal
            if filter.value not in ('null', 'true', 'false', 'unknown') then
                raise exception 'invalid value for is filter: must be null, true, false, or unknown';
            end if;
            -- IS NULL works for any type, but IS TRUE/FALSE/UNKNOWN require a boolean
            -- operand. Reject the non-null keywords on non-boolean columns here so they
            -- don't abort apply_rls at WAL time.
            if filter.value <> 'null' and col_type <> 'boolean'::regtype then
                raise exception 'is % filter requires a boolean column, got %', filter.value, col_type::text;
            end if;
        elsif filter.op in ('like'::realtime.equality_op, 'ilike'::realtime.equality_op) then
            -- like/ilike apply the text pattern operator (~~); reject column types that
            -- have no such operator instead of failing at WAL time
            if not exists (
                select 1 from pg_catalog.pg_operator
                where oprname = '~~' and oprleft = col_type
            ) then
                raise exception 'operator % requires a text-compatible column type, got %', filter.op::text, col_type::text;
            end if;
        elsif filter.op in ('match'::realtime.equality_op, 'imatch'::realtime.equality_op) then
            -- match/imatch apply the regex operators ~ / ~*; reject column types that have
            -- no such operator (e.g. integer) instead of failing at WAL time, mirroring the
            -- like/ilike guard above.
            if not exists (
                select 1 from pg_catalog.pg_operator
                where oprname = case when filter.op = 'imatch'::realtime.equality_op then '~*' else '~' end
                  and oprleft = col_type
                  and oprright = col_type
                  and oprresult = 'boolean'::regtype
            ) then
                raise exception 'operator % requires a text-compatible column type, got %', filter.op::text, col_type::text;
            end if;
            -- validate the regex eagerly so a bad pattern is rejected here, not inside
            -- apply_rls where it would abort the WAL stream for the entity
            begin
                perform '' ~ filter.value;
            exception when others then
                raise exception 'invalid regular expression for % filter: %', filter.op::text, sqlerrm;
            end;
        else
            -- eq/neq/lt/lte/gt/gte: value must be coercable to the type
            perform realtime.cast(filter.value, col_type);
        end if;
    end loop;

    if new.selected_columns is not null then
        for selected_col in select * from unnest(new.selected_columns) loop
            if not selected_col = any(col_names) then
                raise exception 'invalid column for select %', selected_col;
            end if;
        end loop;
    end if;

    -- Apply consistent order to filters so the unique constraint can't be tricked by a
    -- different filter order. negate is part of the sort key.
    new.filters = coalesce(
        array_agg(f order by f.column_name, f.op, f.value, f.negate),
        '{}'
    ) from unnest(new.filters) f;

    -- Normalize selected_columns order so ARRAY['a','b'] and ARRAY['b','a'] are treated
    -- as the same subscription group in apply_rls. Preserve an empty array as '{}'
    -- ("primary keys only") so it stays distinct from NULL ("all columns"); array_agg
    -- over an empty set would otherwise collapse '{}' back to NULL.
    if new.selected_columns is not null then
        new.selected_columns = coalesce(
            (
                select array_agg(c order by c)
                from unnest(new.selected_columns) c
            ),
            '{}'::text[]
        );
    end if;

    return new;
end;
$$;


ALTER FUNCTION realtime.subscription_check_filters() OWNER TO supabase_realtime_admin;

--
-- Name: to_regrole(text); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.to_regrole(role_name text) RETURNS regrole
    LANGUAGE sql IMMUTABLE
    AS $$ select role_name::regrole $$;


ALTER FUNCTION realtime.to_regrole(role_name text) OWNER TO supabase_realtime_admin;

--
-- Name: topic(); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.topic() RETURNS text
    LANGUAGE sql STABLE
    AS $$
select nullif(current_setting('realtime.topic', true), '')::text;
$$;


ALTER FUNCTION realtime.topic() OWNER TO supabase_realtime_admin;

--
-- Name: wal2json_escape_identifier(text); Type: FUNCTION; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE FUNCTION realtime.wal2json_escape_identifier(name text) RETURNS text
    LANGUAGE sql IMMUTABLE STRICT
    AS $$
  -- Prefix `\`, `,`, `.`, and any whitespace with `\`
  SELECT regexp_replace(name, '([\\,.[:space:]])', '\\\1', 'g')
$$;


ALTER FUNCTION realtime.wal2json_escape_identifier(name text) OWNER TO supabase_realtime_admin;

--
-- Name: allow_any_operation(text[]); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.allow_any_operation(expected_operations text[]) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$
  WITH current_operation AS (
    SELECT storage.operation() AS raw_operation
  ),
  normalized AS (
    SELECT CASE
      WHEN raw_operation LIKE 'storage.%' THEN substr(raw_operation, 9)
      ELSE raw_operation
    END AS current_operation
    FROM current_operation
  )
  SELECT EXISTS (
    SELECT 1
    FROM normalized n
    CROSS JOIN LATERAL unnest(expected_operations) AS expected_operation
    WHERE expected_operation IS NOT NULL
      AND expected_operation <> ''
      AND n.current_operation = CASE
        WHEN expected_operation LIKE 'storage.%' THEN substr(expected_operation, 9)
        ELSE expected_operation
      END
  );
$$;


ALTER FUNCTION storage.allow_any_operation(expected_operations text[]) OWNER TO supabase_storage_admin;

--
-- Name: allow_only_operation(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.allow_only_operation(expected_operation text) RETURNS boolean
    LANGUAGE sql STABLE
    AS $$
  WITH current_operation AS (
    SELECT storage.operation() AS raw_operation
  ),
  normalized AS (
    SELECT
      CASE
        WHEN raw_operation LIKE 'storage.%' THEN substr(raw_operation, 9)
        ELSE raw_operation
      END AS current_operation,
      CASE
        WHEN expected_operation LIKE 'storage.%' THEN substr(expected_operation, 9)
        ELSE expected_operation
      END AS requested_operation
    FROM current_operation
  )
  SELECT CASE
    WHEN requested_operation IS NULL OR requested_operation = '' THEN FALSE
    ELSE COALESCE(current_operation = requested_operation, FALSE)
  END
  FROM normalized;
$$;


ALTER FUNCTION storage.allow_only_operation(expected_operation text) OWNER TO supabase_storage_admin;

--
-- Name: can_insert_object(text, text, uuid, jsonb); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.can_insert_object(bucketid text, name text, owner uuid, metadata jsonb) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT INTO "storage"."objects" ("bucket_id", "name", "owner", "metadata") VALUES (bucketid, name, owner, metadata);
  -- hack to rollback the successful insert
  RAISE sqlstate 'PT200' using
  message = 'ROLLBACK',
  detail = 'rollback successful insert';
END
$$;


ALTER FUNCTION storage.can_insert_object(bucketid text, name text, owner uuid, metadata jsonb) OWNER TO supabase_storage_admin;

--
-- Name: enforce_bucket_lifecycle_service_role(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.enforce_bucket_lifecycle_service_role() RETURNS trigger
    LANGUAGE plpgsql
    SET search_path TO 'pg_catalog'
    AS $$
BEGIN
  IF current_user::text IS DISTINCT FROM TG_ARGV[0]
     AND (
       OLD.lifecycle_configuration IS DISTINCT FROM NEW.lifecycle_configuration
       OR OLD.lifecycle_configuration_generation IS DISTINCT FROM NEW.lifecycle_configuration_generation
     ) THEN
    -- AFTER runs only after caller RLS has accepted the proposed row. The API
    -- recognizes this specific error after rolling back its permission probe;
    -- direct non-service writes still fail and cannot persist the change.
    RAISE EXCEPTION 'bucket control columns may only be changed by the configured storage service role'
      USING ERRCODE = 'PST01',
            SCHEMA = TG_TABLE_SCHEMA,
            TABLE = TG_TABLE_NAME,
            CONSTRAINT = TG_NAME;
  END IF;

  RETURN NULL;
END;
$$;


ALTER FUNCTION storage.enforce_bucket_lifecycle_service_role() OWNER TO supabase_storage_admin;

--
-- Name: enforce_bucket_name_length(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.enforce_bucket_name_length() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if length(new.name) > 100 then
        raise exception 'bucket name "%" is too long (% characters). Max is 100.', new.name, length(new.name);
    end if;
    return new;
end;
$$;


ALTER FUNCTION storage.enforce_bucket_name_length() OWNER TO supabase_storage_admin;

--
-- Name: extension(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.extension(name text) RETURNS text
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    _parts text[];
    _filename text;
BEGIN
    -- Split on "/" to get path segments
    SELECT string_to_array(name, '/') INTO _parts;
    -- Get the last path segment (the actual filename)
    SELECT _parts[array_length(_parts, 1)] INTO _filename;
    -- Extract extension: reverse, split on '.', then reverse again
    RETURN reverse(split_part(reverse(_filename), '.', 1));
END
$$;


ALTER FUNCTION storage.extension(name text) OWNER TO supabase_storage_admin;

--
-- Name: filename(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.filename(name text) RETURNS text
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    _parts text[];
BEGIN
    SELECT string_to_array(name, '/') INTO _parts;
    RETURN _parts[array_length(_parts, 1)];
END
$$;


ALTER FUNCTION storage.filename(name text) OWNER TO supabase_storage_admin;

--
-- Name: foldername(text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.foldername(name text) RETURNS text[]
    LANGUAGE plpgsql IMMUTABLE
    AS $$
DECLARE
    _parts text[];
BEGIN
    -- Split on "/" to get path segments
    SELECT string_to_array(name, '/') INTO _parts;
    -- Return everything except the last segment
    RETURN _parts[1 : array_length(_parts,1) - 1];
END
$$;


ALTER FUNCTION storage.foldername(name text) OWNER TO supabase_storage_admin;

--
-- Name: get_common_prefix(text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.get_common_prefix(p_key text, p_prefix text, p_delimiter text) RETURNS text
    LANGUAGE sql IMMUTABLE
    AS $$
SELECT CASE
    WHEN p_delimiter <> ''
         AND position(p_delimiter IN substring(p_key FROM length(p_prefix) + 1)) > 0
    THEN left(
        p_key,
        length(p_prefix)
            + position(p_delimiter IN substring(p_key FROM length(p_prefix) + 1))
            + length(p_delimiter) - 1
    )
    ELSE NULL
END;
$$;


ALTER FUNCTION storage.get_common_prefix(p_key text, p_prefix text, p_delimiter text) OWNER TO supabase_storage_admin;

--
-- Name: get_size_by_bucket(text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.get_size_by_bucket(noncurrent_versions text DEFAULT 'include'::text, delete_markers text DEFAULT 'include'::text) RETURNS TABLE(size bigint, bucket_id text)
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
    -- COALESCE first: NULL NOT IN (...) evaluates to NULL (not TRUE), so a
    -- bare NOT IN check silently leaves an explicit NULL argument unreset.
    noncurrent_versions := COALESCE(noncurrent_versions, 'include');
    delete_markers := COALESCE(delete_markers, 'include');
    IF noncurrent_versions NOT IN ('exclude', 'only', 'include') THEN
        noncurrent_versions := 'include';
    END IF;
    IF delete_markers NOT IN ('exclude', 'only', 'include') THEN
        delete_markers := 'include';
    END IF;

    return query
        select sum((metadata->>'size')::bigint)::bigint as size, obj.bucket_id
        from "storage".objects as obj
        where (noncurrent_versions != 'exclude' OR obj.archived_at IS NULL)
          and (noncurrent_versions != 'only' OR obj.archived_at IS NOT NULL)
          and (delete_markers != 'exclude' OR NOT obj.is_delete_marker)
          and (delete_markers != 'only' OR obj.is_delete_marker)
        group by obj.bucket_id;
END
$$;


ALTER FUNCTION storage.get_size_by_bucket(noncurrent_versions text, delete_markers text) OWNER TO supabase_storage_admin;

--
-- Name: list_multipart_uploads_with_delimiter(text, text, text, integer, text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.list_multipart_uploads_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, next_key_token text DEFAULT ''::text, next_upload_token text DEFAULT ''::text, raw_prefix_param text DEFAULT NULL::text) RETURNS TABLE(key text, id text, created_at timestamp with time zone)
    LANGUAGE sql STABLE
    AS $_$
WITH candidates AS (
    SELECT
        upload.key AS object_key,
        CASE
            WHEN position($3 IN substring(upload.key FROM length(coalesce($7, $2)) + 1)) > 0
            THEN left(
                upload.key,
                length(coalesce($7, $2))
                    + position($3 IN substring(upload.key FROM length(coalesce($7, $2)) + 1))
                    + length($3) - 1
            )
            ELSE upload.key
        END AS result_key,
        upload.id,
        upload.created_at,
        position($3 IN substring(upload.key FROM length(coalesce($7, $2)) + 1)) > 0 AS is_common_prefix
    FROM storage.s3_multipart_uploads AS upload
    WHERE upload.bucket_id = $1
      AND upload.key COLLATE "C" LIKE $2 || '%'
), filtered AS (
    SELECT candidate.*
    FROM candidates AS candidate
    WHERE $5 = ''
       OR candidate.result_key COLLATE "C" > $5
       OR (
           candidate.result_key COLLATE "C" = $5
           AND NOT candidate.is_common_prefix
           AND $6 <> ''
           -- A completed or aborted marker repeats the remaining same-key uploads.
           AND COALESCE(
               (candidate.created_at, candidate.id COLLATE "C") > (
                   SELECT marker.created_at, marker.id COLLATE "C"
                   FROM storage.s3_multipart_uploads AS marker
                   WHERE marker.bucket_id = $1
                     AND marker.key COLLATE "C" = $5
                     AND marker.id = $6
               ),
               TRUE
           )
       )
), ranked AS (
    SELECT
        filtered.*,
        row_number() OVER (
            PARTITION BY filtered.result_key COLLATE "C"
            ORDER BY filtered.created_at, filtered.id COLLATE "C"
        ) AS prefix_rank
    FROM filtered
)
SELECT ranked.result_key, ranked.id, ranked.created_at
FROM ranked
WHERE NOT ranked.is_common_prefix OR ranked.prefix_rank = 1
ORDER BY ranked.result_key COLLATE "C", ranked.created_at, ranked.id COLLATE "C"
LIMIT $4;
$_$;


ALTER FUNCTION storage.list_multipart_uploads_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer, next_key_token text, next_upload_token text, raw_prefix_param text) OWNER TO supabase_storage_admin;

--
-- Name: list_objects_with_delimiter(text, text, text, integer, text, text, text, text, text, timestamp with time zone, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.list_objects_with_delimiter(_bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, start_after text DEFAULT ''::text, next_token text DEFAULT ''::text, sort_order text DEFAULT 'asc'::text, noncurrent_versions text DEFAULT 'exclude'::text, delete_markers text DEFAULT 'exclude'::text, next_token_archived_at timestamp with time zone DEFAULT NULL::timestamp with time zone, next_token_version text DEFAULT ''::text) RETURNS TABLE(name text, id uuid, metadata jsonb, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, version text, archived_at timestamp with time zone, is_delete_marker boolean, is_versioned boolean)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_peek_name TEXT;
    v_current RECORD;
    v_common_prefix TEXT;

    -- Configuration
    v_is_asc BOOLEAN;
    v_prefix TEXT;
    v_start TEXT;
    v_start_relative TEXT;
    v_upper_bound TEXT;
    v_file_batch_size INT;
    v_version_filter TEXT;

    -- true when noncurrent_versions can return >1 row per name; keeps them
    -- ordered most-recent-first and lets pagination resume mid-key
    v_multi_row BOOLEAN;
    v_name_order TEXT;
    v_exact_range_predicate TEXT;
    v_strict_range_predicate TEXT;
    v_inclusive_range_predicate TEXT;

    -- Seek state for the current name. archived_at is normalized to JavaScript's
    -- millisecond precision and version breaks ties within the same millisecond.
    -- Current rows use 'infinity'; NULL means no tiebreak has been established.
    v_next_seek TEXT;
    v_next_seek_at TIMESTAMPTZ;
    v_next_seek_version TEXT;
    v_next_seek_strict BOOLEAN := false;
    v_cursor_is_folder BOOLEAN;
    v_count INT := 0;
    v_previous_seek TEXT;
    v_previous_seek_at TIMESTAMPTZ;
    v_previous_seek_version TEXT;
    v_previous_count INT;

    -- Dynamic SQL for batch query only
    v_batch_query TEXT;
    v_batch_query_strict TEXT;
    v_delete_marker_peek_query TEXT;
    v_delete_marker_peek_query_strict TEXT;

BEGIN
    -- ========================================================================
    -- INITIALIZATION
    -- ========================================================================
    v_is_asc := lower(coalesce(sort_order, 'asc')) = 'asc';
    v_prefix := coalesce(prefix_param, '');
    v_start := CASE WHEN coalesce(next_token, '') <> '' THEN next_token ELSE coalesce(start_after, '') END;
    v_file_batch_size := LEAST(GREATEST(max_keys * 2, 100), 1000);
    v_next_seek_at := NULL;
    v_next_seek_version := '';

    -- COALESCE first: NULL NOT IN (...) evaluates to NULL (not TRUE), so a
    -- bare NOT IN check silently leaves an explicit NULL argument unreset.
    noncurrent_versions := COALESCE(noncurrent_versions, 'exclude');
    delete_markers := COALESCE(delete_markers, 'exclude');
    IF noncurrent_versions NOT IN ('exclude', 'only', 'include') THEN
        noncurrent_versions := 'exclude';
    END IF;
    IF delete_markers NOT IN ('exclude', 'only', 'include') THEN
        delete_markers := 'exclude';
    END IF;

    v_multi_row := noncurrent_versions IN ('only', 'include');
    v_name_order := CASE WHEN v_is_asc THEN 'ASC' ELSE 'DESC' END;

    v_version_filter := '';
    IF noncurrent_versions = 'exclude' THEN
        v_version_filter := v_version_filter || ' AND o.archived_at IS NULL';
    ELSIF noncurrent_versions = 'only' THEN
        v_version_filter := v_version_filter || ' AND o.archived_at IS NOT NULL';
    END IF;
    IF delete_markers = 'exclude' THEN
        v_version_filter := v_version_filter || ' AND NOT o.is_delete_marker';
    ELSIF delete_markers = 'only' THEN
        v_version_filter := v_version_filter || ' AND o.is_delete_marker';
    END IF;

    -- Calculate upper bound for prefix filtering (bytewise, using COLLATE "C")
    IF v_prefix = '' THEN
        v_upper_bound := NULL;
    ELSE
        v_upper_bound := left(v_prefix, -1) || chr(ascii(right(v_prefix, 1)) + 1);
    END IF;

    -- Keep caller-provided cursors inside the requested prefix range.
    IF v_start <> '' AND v_upper_bound IS NOT NULL THEN
        IF v_is_asc THEN
            IF v_start COLLATE "C" < v_prefix COLLATE "C" THEN
                v_start := '';
            ELSIF v_start COLLATE "C" >= v_upper_bound COLLATE "C" THEN
                RETURN;
            END IF;
        ELSE
            IF v_start COLLATE "C" < v_prefix COLLATE "C" THEN
                RETURN;
            ELSIF v_start COLLATE "C" >= v_upper_bound COLLATE "C" THEN
                v_start := '';
            END IF;
        END IF;
    END IF;

    v_start_relative := substring(v_start FROM length(v_prefix) + 1);

    -- Direction affects only the indexed name range and its ordering. Cursor
    -- state transitions and within-key version ordering stay shared.
    IF v_is_asc THEN
        v_exact_range_predicate := 'TRUE';
        v_strict_range_predicate := 'o.name COLLATE "C" > $2';
        v_inclusive_range_predicate := 'o.name COLLATE "C" >= $2';
        IF v_upper_bound IS NOT NULL THEN
            v_exact_range_predicate := 'o.name COLLATE "C" < $3';
            v_strict_range_predicate := v_strict_range_predicate || ' AND o.name COLLATE "C" < $3';
            v_inclusive_range_predicate := v_inclusive_range_predicate || ' AND o.name COLLATE "C" < $3';
        END IF;
    ELSE
        v_exact_range_predicate := 'TRUE';
        v_strict_range_predicate := 'o.name COLLATE "C" < $2';
        v_inclusive_range_predicate := 'o.name COLLATE "C" < $2';
        IF v_prefix <> '' THEN
            v_exact_range_predicate := 'o.name COLLATE "C" >= $3';
            v_strict_range_predicate := v_strict_range_predicate || ' AND o.name COLLATE "C" >= $3';
            v_inclusive_range_predicate := v_inclusive_range_predicate || ' AND o.name COLLATE "C" >= $3';
        END IF;
    END IF;

    -- Build batch query (dynamic SQL - called infrequently, amortized over many rows)
    -- The multi-row order matches the externally serialized cursor exactly:
    -- archived_at at millisecond precision, then version as the final tiebreak.
    --
    -- When v_multi_row, the seek is a keyset tuple comparison ("name > $2 OR
    -- (name = $2 AND tiebreak)") - Postgres won't split that OR into indexable
    -- form (confirmed even with fully literal values), so as one WHERE clause
    -- it forces a full bucket scan filtered row-by-row. Splitting it into two
    -- independently-indexable branches (exact name match with the tiebreak
    -- filter, vs. strictly-past names) combined with UNION ALL lets each
    -- branch keep name as a real index condition; the outer ORDER BY/LIMIT
    -- re-merges them into the same page the single query used to produce.
    IF v_multi_row THEN
        v_batch_query := format(
            $sql$
            SELECT *
            FROM (
                (
                    SELECT o.name, o.id, o.updated_at, o.created_at,
                           o.last_accessed_at, o.metadata, o.version,
                           o.archived_at, o.is_delete_marker, o.is_versioned
                    FROM storage.objects o
                    WHERE o.bucket_id = $1
                      AND o.name COLLATE "C" = $2
                      AND %s
                      AND NOT $7::boolean
                      AND (
                          $5::timestamptz IS NULL
                          OR COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) < $5
                          OR (
                              COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) = $5
                              AND COALESCE(o.version, '') > $6
                          )
                      )
                      %s
                    ORDER BY
                        COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) DESC,
                        COALESCE(o.version, '') ASC
                    LIMIT $4
                )
                UNION ALL
                (
                    SELECT o.name, o.id, o.updated_at, o.created_at,
                           o.last_accessed_at, o.metadata, o.version,
                           o.archived_at, o.is_delete_marker, o.is_versioned
                    FROM storage.objects o
                    WHERE o.bucket_id = $1
                      AND %s
                      %s
                    ORDER BY
                        o.name COLLATE "C" %s,
                        COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) DESC,
                        COALESCE(o.version, '') ASC
                    LIMIT $4
                )
            ) sub
            ORDER BY
                sub.name COLLATE "C" %s,
                COALESCE(date_trunc('milliseconds', sub.archived_at), 'infinity'::timestamptz) DESC,
                COALESCE(sub.version, '') ASC
            LIMIT $4
            $sql$,
            v_exact_range_predicate,
            v_version_filter,
            v_strict_range_predicate,
            v_version_filter,
            v_name_order,
            v_name_order
        );
    ELSE
        v_batch_query := format(
            $sql$
            SELECT o.name, o.id, o.updated_at, o.created_at,
                   o.last_accessed_at, o.metadata, o.version,
                   o.archived_at, o.is_delete_marker, o.is_versioned
            FROM storage.objects o
            WHERE o.bucket_id = $1
              AND %s
              %s
            ORDER BY o.name COLLATE "C" %s, o.archived_at DESC
            LIMIT $4
            $sql$,
            v_inclusive_range_predicate,
            v_version_filter,
            v_name_order
        );

        -- Strict counterpart of the query above: used once the single-row
        -- ASC batch advance (below) has left v_next_seek pointing at the
        -- last row already emitted, so an inclusive predicate would
        -- re-match it forever. Only single-row mode ever sets strict mode,
        -- so this variant is never needed when v_multi_row.
        v_batch_query_strict := format(
            $sql$
            SELECT o.name, o.id, o.updated_at, o.created_at,
                   o.last_accessed_at, o.metadata, o.version,
                   o.archived_at, o.is_delete_marker, o.is_versioned
            FROM storage.objects o
            WHERE o.bucket_id = $1
              AND %s
              %s
            ORDER BY o.name COLLATE "C" %s, o.archived_at DESC
            LIMIT $4
            $sql$,
            v_strict_range_predicate,
            v_version_filter,
            v_name_order
        );
    END IF;

    -- The static peek predicates cannot use the partial delete-marker index
    -- once PL/pgSQL switches to a generic plan because whether
    -- is_delete_marker is required remains parameter-dependent. Reuse the
    -- already-specialized batch query with a one-row limit for this sparse
    -- filter so the plan sees a literal `o.is_delete_marker` predicate.
    IF delete_markers = 'only' THEN
        v_delete_marker_peek_query :=
            'SELECT marker_page.name FROM (' || v_batch_query || ') marker_page LIMIT 1';
        IF NOT v_multi_row THEN
            v_delete_marker_peek_query_strict :=
                'SELECT marker_page.name FROM (' || v_batch_query_strict || ') marker_page LIMIT 1';
        END IF;
    END IF;

    -- ========================================================================
    -- SEEK INITIALIZATION: Determine starting position
    -- ========================================================================
    IF v_start = '' THEN
        IF v_is_asc THEN
            v_next_seek := v_prefix;
        ELSE
            -- DESC without cursor performs one specialized initial seek so
            -- partial current-version and delete-marker indexes remain available.
            EXECUTE format(
                'SELECT o.name FROM storage.objects o WHERE o.bucket_id = $1%s%s ORDER BY o.name COLLATE "C" DESC LIMIT 1',
                CASE WHEN v_upper_bound IS NOT NULL
                    THEN ' AND o.name COLLATE "C" >= $2 AND o.name COLLATE "C" < $3'
                    ELSE ''
                END,
                v_version_filter
            )
            INTO v_next_seek
            USING _bucket_id, v_prefix, v_upper_bound;

            IF v_next_seek IS NOT NULL THEN
                v_next_seek := v_next_seek || delimiter_param;
            ELSE
                RETURN;
            END IF;
        END IF;
    ELSE
        -- Folder continuation tokens retain their trailing delimiter. A
        -- delimiter-less startAfter is always a literal key boundary.
        v_cursor_is_folder := delimiter_param <> ''
            AND v_start_relative <> ''
            AND right(v_start_relative, length(delimiter_param)) = delimiter_param;

        IF v_cursor_is_folder THEN
            v_next_seek := CASE
                WHEN right(v_start, length(delimiter_param)) = delimiter_param
                    THEN v_start
                ELSE v_start || delimiter_param
            END;
            IF v_is_asc THEN
                v_next_seek := left(v_next_seek, -1)
                    || chr(ascii(right(v_next_seek, 1)) + 1);
            END IF;
            v_next_seek_strict := NOT v_is_asc;
        ELSE
            -- leaf object: when v_multi_row, stay on v_start with the
            -- caller-supplied tiebreak so a page boundary mid-key resumes
            -- that key's remaining rows instead of skipping them. Truncate
            -- to milliseconds like every other v_next_seek_at assignment -
            -- harmless today since object.ts's cursor always round-trips
            -- through JS Date first, but this shouldn't rely on that.
            IF v_multi_row THEN
                v_next_seek := v_start;
                v_next_seek_at := date_trunc('milliseconds', next_token_archived_at);
                v_next_seek_version := coalesce(next_token_version, '');
                v_next_seek_strict := coalesce(next_token, '') = '';
            ELSIF v_is_asc THEN
                v_next_seek := v_start;
                v_next_seek_strict := true;
            ELSE
                v_next_seek := v_start;
            END IF;
        END IF;
    END IF;

    -- ========================================================================
    -- MAIN LOOP: Hybrid peek-then-batch algorithm
    -- Uses STATIC SQL for peek (hot path) and DYNAMIC SQL for batch
    -- ========================================================================
    LOOP
        EXIT WHEN v_count >= max_keys;

        v_previous_seek := v_next_seek;
        v_previous_seek_at := v_next_seek_at;
        v_previous_seek_version := v_next_seek_version;
        v_previous_count := v_count;

        -- STEP 1: PEEK using STATIC SQL (plan cached, very fast)
        -- v_multi_row is branched here (rather than folded into the WHERE
        -- clause as a bound parameter) so each concrete query keeps an
        -- unconditional seek predicate - once PL/pgSQL switches to its
        -- cached generic plan (after 5 calls), a parameter-gated
        -- "(NOT v_multi_row AND name >= $x) OR (v_multi_row AND ...)"
        -- predicate stops the planner from using name as an index
        -- condition at all, degrading every subsequent peek to a full
        -- index scan filtered row-by-row instead of a bounded range scan.
        -- v_multi_row's seek predicate is a keyset tuple comparison
        -- ("name > x OR (name = x AND tiebreak)") - Postgres does not
        -- split this OR into indexable form even with fully literal
        -- values, so it falls back to a full scan filtered row-by-row.
        -- Splitting it into two independently-indexable branches (exact
        -- name match with the tiebreak filter, vs. strictly-past name)
        -- combined with UNION ALL lets each branch keep name as a real
        -- index condition; the outer ORDER BY/LIMIT picks whichever of
        -- the (at most 2) rows sorts first.
        IF delete_markers = 'only' THEN
            EXECUTE CASE WHEN v_next_seek_strict AND NOT v_multi_row
                THEN v_delete_marker_peek_query_strict
                ELSE v_delete_marker_peek_query
            END
                INTO v_peek_name
                USING _bucket_id, v_next_seek,
                    CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix) ELSE v_prefix END,
                    1, v_next_seek_at, v_next_seek_version, v_next_seek_strict;
        ELSIF v_multi_row THEN
            IF v_is_asc THEN
                IF v_upper_bound IS NOT NULL THEN
                    SELECT sub.name INTO v_peek_name FROM (
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" = v_next_seek
                           AND o.name COLLATE "C" < v_upper_bound
                           AND NOT v_next_seek_strict
                           AND (v_next_seek_at IS NULL
                                OR COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) < v_next_seek_at
                                OR (COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) = v_next_seek_at
                                    AND COALESCE(o.version, '') > v_next_seek_version))
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) DESC, COALESCE(o.version, '') ASC LIMIT 1)
                        UNION ALL
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" > v_next_seek AND o.name COLLATE "C" < v_upper_bound
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY o.name COLLATE "C" ASC LIMIT 1)
                    ) sub ORDER BY sub.name COLLATE "C" ASC LIMIT 1;
                ELSE
                    SELECT sub.name INTO v_peek_name FROM (
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" = v_next_seek
                           AND NOT v_next_seek_strict
                           AND (v_next_seek_at IS NULL
                                OR COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) < v_next_seek_at
                                OR (COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) = v_next_seek_at
                                    AND COALESCE(o.version, '') > v_next_seek_version))
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) DESC, COALESCE(o.version, '') ASC LIMIT 1)
                        UNION ALL
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" > v_next_seek
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY o.name COLLATE "C" ASC LIMIT 1)
                    ) sub ORDER BY sub.name COLLATE "C" ASC LIMIT 1;
                END IF;
            ELSE
                IF v_upper_bound IS NOT NULL THEN
                    SELECT sub.name INTO v_peek_name FROM (
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" = v_next_seek
                           AND o.name COLLATE "C" >= v_prefix
                           AND NOT v_next_seek_strict
                           AND (v_next_seek_at IS NULL
                                OR COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) < v_next_seek_at
                                OR (COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) = v_next_seek_at
                                    AND COALESCE(o.version, '') > v_next_seek_version))
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) DESC, COALESCE(o.version, '') ASC LIMIT 1)
                        UNION ALL
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek AND o.name COLLATE "C" >= v_prefix
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY o.name COLLATE "C" DESC LIMIT 1)
                    ) sub ORDER BY sub.name COLLATE "C" DESC LIMIT 1;
                ELSE
                    SELECT sub.name INTO v_peek_name FROM (
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" = v_next_seek
                           AND NOT v_next_seek_strict
                           AND (v_next_seek_at IS NULL
                                OR COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) < v_next_seek_at
                                OR (COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) = v_next_seek_at
                                    AND COALESCE(o.version, '') > v_next_seek_version))
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY COALESCE(date_trunc('milliseconds', o.archived_at), 'infinity'::timestamptz) DESC, COALESCE(o.version, '') ASC LIMIT 1)
                        UNION ALL
                        (SELECT o.name FROM storage.objects o
                         WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek
                           AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                           AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                           AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                           AND (delete_markers != 'only' OR o.is_delete_marker)
                         ORDER BY o.name COLLATE "C" DESC LIMIT 1)
                    ) sub ORDER BY sub.name COLLATE "C" DESC LIMIT 1;
                END IF;
            END IF;
        ELSE
            -- Single-row mode is always noncurrent_versions='exclude'. Keep
            -- this predicate literal so generic plans use the current index.
            IF v_is_asc THEN
                IF v_next_seek_strict AND v_upper_bound IS NOT NULL THEN
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = _bucket_id
                      AND o.name COLLATE "C" > v_next_seek
                      AND o.name COLLATE "C" < v_upper_bound
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                      AND (delete_markers != 'only' OR o.is_delete_marker)
                    ORDER BY o.name COLLATE "C" ASC LIMIT 1;
                ELSIF v_next_seek_strict THEN
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = _bucket_id
                      AND o.name COLLATE "C" > v_next_seek
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                      AND (delete_markers != 'only' OR o.is_delete_marker)
                    ORDER BY o.name COLLATE "C" ASC LIMIT 1;
                ELSIF v_upper_bound IS NOT NULL THEN
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = _bucket_id
                      AND o.name COLLATE "C" >= v_next_seek
                      AND o.name COLLATE "C" < v_upper_bound
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                      AND (delete_markers != 'only' OR o.is_delete_marker)
                    ORDER BY o.name COLLATE "C" ASC LIMIT 1;
                ELSE
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = _bucket_id
                      AND o.name COLLATE "C" >= v_next_seek
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                      AND (delete_markers != 'only' OR o.is_delete_marker)
                    ORDER BY o.name COLLATE "C" ASC LIMIT 1;
                END IF;
            ELSE
                IF v_upper_bound IS NOT NULL THEN
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = _bucket_id
                      AND o.name COLLATE "C" < v_next_seek
                      AND o.name COLLATE "C" >= v_prefix
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                      AND (delete_markers != 'only' OR o.is_delete_marker)
                    ORDER BY o.name COLLATE "C" DESC LIMIT 1;
                ELSE
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = _bucket_id
                      AND o.name COLLATE "C" < v_next_seek
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                      AND (delete_markers != 'only' OR o.is_delete_marker)
                    ORDER BY o.name COLLATE "C" DESC LIMIT 1;
                END IF;
            END IF;
        END IF;

        EXIT WHEN v_peek_name IS NULL;

        -- STEP 2: Check if this is a FOLDER or FILE
        v_common_prefix := storage.get_common_prefix(v_peek_name, v_prefix, delimiter_param);

        IF v_common_prefix IS NOT NULL THEN
            -- FOLDER: Emit and skip to next folder (no heap access needed)
            name := v_common_prefix;
            id := NULL;
            updated_at := NULL;
            created_at := NULL;
            last_accessed_at := NULL;
            metadata := NULL;
            version := NULL;
            archived_at := NULL;
            is_delete_marker := NULL;
            is_versioned := NULL;
            RETURN NEXT;
            v_count := v_count + 1;

            -- Advance seek past the folder range
            IF v_is_asc THEN
                v_next_seek := left(v_common_prefix, -1)
                    || chr(ascii(right(v_common_prefix, 1)) + 1);
            ELSE
                v_next_seek := v_common_prefix;
            END IF;
            v_next_seek_at := NULL;
            v_next_seek_version := '';
            v_next_seek_strict := NOT v_is_asc;
        ELSE
            -- FILE: Batch fetch using DYNAMIC SQL (overhead amortized over many rows)
            -- For ASC: upper_bound is the exclusive upper limit (< condition)
            -- For DESC: prefix is the inclusive lower limit (>= condition)
            FOR v_current IN EXECUTE CASE WHEN v_next_seek_strict AND NOT v_multi_row THEN v_batch_query_strict ELSE v_batch_query END
                USING _bucket_id, v_next_seek,
                CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix) ELSE v_prefix END, v_file_batch_size, v_next_seek_at, v_next_seek_version,
                v_next_seek_strict
            LOOP
                v_common_prefix := storage.get_common_prefix(v_current.name, v_prefix, delimiter_param);

                IF v_common_prefix IS NOT NULL THEN
                    -- Hit a folder: exit batch, let peek handle it. Reset
                    -- strict mode too it may have been set by an earlier
                    -- row in this same batch (see the single-row ASC advance
                    -- below), and v_next_seek here is the folder-triggering
                    -- row's own name, which the next peek must find inclusively.
                    v_next_seek := CASE
                        WHEN v_is_asc THEN v_current.name
                        ELSE v_current.name || delimiter_param
                    END;
                    v_next_seek_at := NULL;
                    v_next_seek_version := '';
                    v_next_seek_strict := false;
                    EXIT;
                END IF;

                -- Emit file
                name := v_current.name;
                id := v_current.id;
                updated_at := v_current.updated_at;
                created_at := v_current.created_at;
                last_accessed_at := v_current.last_accessed_at;
                metadata := v_current.metadata;
                version := v_current.version;
                archived_at := v_current.archived_at;
                is_delete_marker := v_current.is_delete_marker;
                is_versioned := v_current.is_versioned;
                RETURN NEXT;
                v_count := v_count + 1;

                -- when v_multi_row, stay on this name and record its
                -- archived_at as the new tiebreak so remaining rows for the
                -- same key are picked up before moving to the next name
                IF v_multi_row THEN
                    v_next_seek := v_current.name;
                    v_next_seek_at := COALESCE(date_trunc('milliseconds', v_current.archived_at), 'infinity'::timestamptz);
                    v_next_seek_version := COALESCE(v_current.version, '');
                    v_next_seek_strict := false;
                ELSIF v_is_asc THEN
                    -- Appending the delimiter as a fake lexical successor
                    -- would skip a real key like `name || '!'` (or any
                    -- character sorting below the delimiter), which sorts
                    -- between `name` and `name || delimiter`. Track the real
                    -- name and mark the next comparison strict instead.
                    v_next_seek := v_current.name;
                    v_next_seek_strict := true;
                ELSE
                    v_next_seek := v_current.name;
                END IF;

                EXIT WHEN v_count >= max_keys;
            END LOOP;
        END IF;

        IF v_count = v_previous_count
           AND v_next_seek IS NOT DISTINCT FROM v_previous_seek
           AND v_next_seek_at IS NOT DISTINCT FROM v_previous_seek_at
           AND v_next_seek_version IS NOT DISTINCT FROM v_previous_seek_version THEN
            RAISE EXCEPTION 'storage.list_objects_with_delimiter made no progress at seek (%, %, %)',
                v_next_seek, v_next_seek_at, v_next_seek_version;
        END IF;
    END LOOP;
END;
$_$;


ALTER FUNCTION storage.list_objects_with_delimiter(_bucket_id text, prefix_param text, delimiter_param text, max_keys integer, start_after text, next_token text, sort_order text, noncurrent_versions text, delete_markers text, next_token_archived_at timestamp with time zone, next_token_version text) OWNER TO supabase_storage_admin;

--
-- Name: operation(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.operation() RETURNS text
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
    RETURN current_setting('storage.operation', true);
END;
$$;


ALTER FUNCTION storage.operation() OWNER TO supabase_storage_admin;

--
-- Name: protect_bucket_control_columns(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.protect_bucket_control_columns() RETURNS trigger
    LANGUAGE plpgsql
    SET search_path TO 'pg_catalog'
    AS $$
DECLARE
  configuration_changed boolean;
BEGIN
  IF TG_OP = 'INSERT' THEN
    IF NEW.lifecycle_configuration IS NOT NULL
       OR NEW.lifecycle_configuration_generation IS NOT NULL THEN
      IF NOT pg_has_role(current_user, TG_ARGV[0], 'MEMBER') THEN
        RAISE EXCEPTION 'only members of the configured storage service role may insert lifecycle policy state'
          USING ERRCODE = '42501',
                HINT = format(
                  'Insert with both lifecycle columns NULL and configure lifecycle through the Storage API afterward, or insert as a member of %I.',
                  TG_ARGV[0]
                );
      END IF;
    END IF;

    RETURN NEW;
  END IF;

  configuration_changed =
    OLD.lifecycle_configuration IS DISTINCT FROM NEW.lifecycle_configuration
    OR OLD.lifecycle_configuration_generation IS DISTINCT FROM NEW.lifecycle_configuration_generation;

  IF NOT configuration_changed THEN
    RETURN NEW;
  END IF;

  IF NEW.type IS DISTINCT FROM 'STANDARD' THEN
    RAISE EXCEPTION 'bucket versioning and lifecycle controls require a Standard bucket'
      USING ERRCODE = '0A000';
  END IF;

  IF NEW.lifecycle_configuration IS NULL
     AND NEW.lifecycle_configuration_generation IS NULL THEN
    RETURN NEW;
  END IF;

  IF NEW.lifecycle_configuration IS NULL
     OR NEW.lifecycle_configuration_generation IS NULL
     OR OLD.lifecycle_configuration IS NOT DISTINCT FROM NEW.lifecycle_configuration
     OR OLD.lifecycle_configuration_generation IS NOT DISTINCT FROM NEW.lifecycle_configuration_generation THEN
    RAISE EXCEPTION 'a changed lifecycle policy requires a new non-null generation'
      USING ERRCODE = '22023';
  END IF;

  RETURN NEW;
END;
$$;


ALTER FUNCTION storage.protect_bucket_control_columns() OWNER TO supabase_storage_admin;

--
-- Name: protect_delete(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.protect_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Check if storage.allow_delete_query is set to 'true'
    IF COALESCE(current_setting('storage.allow_delete_query', true), 'false') != 'true' THEN
        RAISE EXCEPTION 'Direct deletion from storage tables is not allowed. Use the Storage API instead.'
            USING HINT = 'This prevents accidental data loss from orphaned objects.',
                  ERRCODE = '42501';
    END IF;
    RETURN NULL;
END;
$$;


ALTER FUNCTION storage.protect_delete() OWNER TO supabase_storage_admin;

--
-- Name: search(text, text, integer, integer, integer, text, text, text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.search(prefix text, bucketname text, limits integer DEFAULT 100, levels integer DEFAULT 1, offsets integer DEFAULT 0, search text DEFAULT ''::text, sortcolumn text DEFAULT 'name'::text, sortorder text DEFAULT 'asc'::text, noncurrent_versions text DEFAULT 'exclude'::text, delete_markers text DEFAULT 'exclude'::text) RETURNS TABLE(name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb, version text, archived_at timestamp with time zone, is_delete_marker boolean, is_versioned boolean)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_peek_name TEXT;
    v_current RECORD;
    v_common_prefix TEXT;
    v_delimiter CONSTANT TEXT := '/';

    -- Configuration
    v_limit INT;
    v_prefix TEXT;
    v_prefix_lower TEXT;
    v_prefix_len INT;
    v_prefix_start INT;
    v_combined_levels INT;
    v_is_asc BOOLEAN;
    v_order_by TEXT;
    v_sort_order TEXT;
    v_upper_bound TEXT;
    v_file_batch_size INT;
    v_version_filter TEXT;
    v_multi_row BOOLEAN;

    -- Dynamic SQL for batch query only
    v_batch_query TEXT;
    v_delete_marker_peek_query TEXT;
    v_delete_marker_peek_query_strict TEXT;

    -- Seek state
    v_next_seek TEXT;
    v_next_seek_at TIMESTAMPTZ;
    v_next_seek_version TEXT;
    v_next_seek_strict BOOLEAN := false;
    v_count INT := 0;
    v_skipped INT := 0;
    v_previous_seek TEXT;
    v_previous_seek_at TIMESTAMPTZ;
    v_previous_seek_version TEXT;
    v_previous_count INT;
    v_previous_skipped INT;
BEGIN
    -- ========================================================================
    -- INITIALIZATION
    -- ========================================================================
    v_limit := LEAST(coalesce(limits, 100), 1500);
    v_prefix := coalesce(prefix, '') || coalesce(search, '');
    v_prefix_lower := lower(v_prefix);
    v_prefix_len := length(coalesce(prefix, ''));
    v_prefix_start := coalesce(array_length(string_to_array(coalesce(prefix, ''), v_delimiter), 1), 1);
    v_combined_levels := coalesce(array_length(string_to_array(v_prefix, v_delimiter), 1), 1);
    v_is_asc := lower(coalesce(sortorder, 'asc')) = 'asc';
    v_file_batch_size := LEAST(GREATEST(v_limit * 2, 100), 1000);
    v_next_seek_at := NULL;
    v_next_seek_version := '';

    -- COALESCE first: NULL NOT IN (...) evaluates to NULL (not TRUE), so a
    -- bare NOT IN check silently leaves an explicit NULL argument unreset.
    noncurrent_versions := COALESCE(noncurrent_versions, 'exclude');
    delete_markers := COALESCE(delete_markers, 'exclude');
    IF noncurrent_versions NOT IN ('exclude', 'only', 'include') THEN
        noncurrent_versions := 'exclude';
    END IF;
    IF delete_markers NOT IN ('exclude', 'only', 'include') THEN
        delete_markers := 'exclude';
    END IF;

    v_multi_row := noncurrent_versions IN ('only', 'include');

    v_version_filter := '';
    IF noncurrent_versions = 'exclude' THEN
        v_version_filter := v_version_filter || ' AND o.archived_at IS NULL';
    ELSIF noncurrent_versions = 'only' THEN
        v_version_filter := v_version_filter || ' AND o.archived_at IS NOT NULL';
    END IF;
    IF delete_markers = 'exclude' THEN
        v_version_filter := v_version_filter || ' AND NOT o.is_delete_marker';
    ELSIF delete_markers = 'only' THEN
        v_version_filter := v_version_filter || ' AND o.is_delete_marker';
    END IF;

    -- Validate sort column
    CASE lower(coalesce(sortcolumn, 'name'))
        WHEN 'name' THEN v_order_by := 'name';
        WHEN 'updated_at' THEN v_order_by := 'updated_at';
        WHEN 'created_at' THEN v_order_by := 'created_at';
        WHEN 'last_accessed_at' THEN v_order_by := 'last_accessed_at';
        ELSE v_order_by := 'name';
    END CASE;

    v_sort_order := CASE WHEN v_is_asc THEN 'asc' ELSE 'desc' END;

    -- ========================================================================
    -- NON-NAME SORTING: Use path_tokens approach
    -- ========================================================================
    IF v_order_by != 'name' THEN
        RETURN QUERY EXECUTE format(
            $sql$
            WITH folders AS (
                SELECT array_to_string(path_tokens[$1:$2], '/') AS folder
                FROM storage.objects
                WHERE objects.name ILIKE $3 || '%%'
                  AND bucket_id = $4
                  AND array_length(objects.path_tokens, 1) <> $2
                  AND ($7 != 'exclude' OR objects.archived_at IS NULL)
                  AND ($7 != 'only' OR objects.archived_at IS NOT NULL)
                  AND ($8 != 'exclude' OR NOT objects.is_delete_marker)
                  AND ($8 != 'only' OR objects.is_delete_marker)
                GROUP BY folder
                ORDER BY folder %s
            )
            (SELECT folder AS "name",
                   NULL::uuid AS id,
                   NULL::timestamptz AS updated_at,
                   NULL::timestamptz AS created_at,
                   NULL::timestamptz AS last_accessed_at,
                   NULL::jsonb AS metadata,
                   NULL::text AS version,
                   NULL::timestamptz AS archived_at,
                   NULL::boolean AS is_delete_marker,
                   NULL::boolean AS is_versioned FROM folders)
            UNION ALL
            (SELECT array_to_string(path_tokens[$1:$2], '/') AS "name",
                   id, updated_at, created_at, last_accessed_at, metadata,
                   version, archived_at, is_delete_marker, is_versioned
             FROM storage.objects
             WHERE objects.name ILIKE $3 || '%%'
               AND bucket_id = $4
               AND array_length(objects.path_tokens, 1) = $2
               AND ($7 != 'exclude' OR objects.archived_at IS NULL)
               AND ($7 != 'only' OR objects.archived_at IS NOT NULL)
               AND ($8 != 'exclude' OR NOT objects.is_delete_marker)
               AND ($8 != 'only' OR objects.is_delete_marker)
             -- name, then version, as tiebreaks so two versions of the same
             -- key tying on the sort column still sort deterministically
             ORDER BY %I %s, name COLLATE "C" %s, COALESCE(version, '') %s)
            LIMIT $5 OFFSET $6
            $sql$, v_sort_order, v_order_by, v_sort_order, v_sort_order, v_sort_order
        ) USING v_prefix_start, v_combined_levels, v_prefix, bucketname, v_limit, offsets, noncurrent_versions, delete_markers;
        RETURN;
    END IF;

    -- ========================================================================
    -- NAME SORTING: Hybrid skip-scan with batch optimization
    -- ========================================================================

    -- Calculate upper bound for prefix filtering
    IF v_prefix_lower = '' THEN
        v_upper_bound := NULL;
    ELSIF right(v_prefix_lower, 1) = v_delimiter THEN
        v_upper_bound := left(v_prefix_lower, -1) || chr(ascii(v_delimiter) + 1);
    ELSE
        v_upper_bound := left(v_prefix_lower, -1) || chr(ascii(right(v_prefix_lower, 1)) + 1);
    END IF;

    -- Build a resume-safe batch query. The exact-name branch returns remaining
    -- versions after the current (archived_at, version) boundary; the strict
    -- name branch returns subsequent keys. UNION ALL keeps both predicates
    -- independently indexable.
    IF v_is_asc THEN
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT * FROM (' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" = $2 AND ($5::timestamptz IS NULL OR COALESCE(o.archived_at, ''infinity''::timestamptz) < $5 OR (COALESCE(o.archived_at, ''infinity''::timestamptz) = $5 AND COALESCE(o.version, '''') > $6))' ||
                v_version_filter || ' ORDER BY COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4) UNION ALL ' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" > $2 AND lower(o.name) COLLATE "C" < $3' || v_version_filter ||
                ' ORDER BY lower(o.name) COLLATE "C" ASC, COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4)' ||
                ') sub ORDER BY lower(sub.name) COLLATE "C" ASC, COALESCE(sub.archived_at, ''infinity''::timestamptz) DESC, COALESCE(sub.version, '''') ASC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT * FROM (' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" = $2 AND ($5::timestamptz IS NULL OR COALESCE(o.archived_at, ''infinity''::timestamptz) < $5 OR (COALESCE(o.archived_at, ''infinity''::timestamptz) = $5 AND COALESCE(o.version, '''') > $6))' ||
                v_version_filter || ' ORDER BY COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4) UNION ALL ' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" > $2' || v_version_filter ||
                ' ORDER BY lower(o.name) COLLATE "C" ASC, COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4)' ||
                ') sub ORDER BY lower(sub.name) COLLATE "C" ASC, COALESCE(sub.archived_at, ''infinity''::timestamptz) DESC, COALESCE(sub.version, '''') ASC LIMIT $4';
        END IF;
    ELSE
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT * FROM (' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" = $2 AND ($5::timestamptz IS NULL OR COALESCE(o.archived_at, ''infinity''::timestamptz) < $5 OR (COALESCE(o.archived_at, ''infinity''::timestamptz) = $5 AND COALESCE(o.version, '''') > $6))' ||
                v_version_filter || ' ORDER BY COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4) UNION ALL ' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" < $2 AND lower(o.name) COLLATE "C" >= $3' || v_version_filter ||
                ' ORDER BY lower(o.name) COLLATE "C" DESC, COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4)' ||
                ') sub ORDER BY lower(sub.name) COLLATE "C" DESC, COALESCE(sub.archived_at, ''infinity''::timestamptz) DESC, COALESCE(sub.version, '''') ASC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT * FROM (' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" = $2 AND ($5::timestamptz IS NULL OR COALESCE(o.archived_at, ''infinity''::timestamptz) < $5 OR (COALESCE(o.archived_at, ''infinity''::timestamptz) = $5 AND COALESCE(o.version, '''') > $6))' ||
                v_version_filter || ' ORDER BY COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4) UNION ALL ' ||
                '(SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata, o.version, o.archived_at, o.is_delete_marker, o.is_versioned FROM storage.objects o ' ||
                'WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" < $2' || v_version_filter ||
                ' ORDER BY lower(o.name) COLLATE "C" DESC, COALESCE(o.archived_at, ''infinity''::timestamptz) DESC, COALESCE(o.version, '''') ASC LIMIT $4)' ||
                ') sub ORDER BY lower(sub.name) COLLATE "C" DESC, COALESCE(sub.archived_at, ''infinity''::timestamptz) DESC, COALESCE(sub.version, '''') ASC LIMIT $4';
        END IF;
    END IF;

    -- Keep the delete-marker predicate literal so the cached generic
    -- plan can use idx_objects_delete_markers during the main-loop peek.
    IF delete_markers = 'only' THEN
        IF v_multi_row THEN
            v_delete_marker_peek_query :=
                'SELECT marker_page.name FROM (' || v_batch_query || ') marker_page LIMIT 1';
        ELSIF v_is_asc THEN
            -- Two separate literal query strings, not one gated by a bound
            -- boolean: folding "$n AND op1 OR NOT $n AND op2" into a single
            -- query defeats the generic plan's ability to push either
            -- comparison into the index. Branching in PL/pgSQL control flow
            -- instead keeps each query's index condition intact.
            v_delete_marker_peek_query :=
                'SELECT o.name FROM storage.objects o WHERE o.bucket_id = $1 ' ||
                'AND lower(o.name) COLLATE "C" >= $2' ||
                CASE WHEN v_upper_bound IS NOT NULL
                    THEN ' AND lower(o.name) COLLATE "C" < $3'
                    ELSE ''
                END ||
                v_version_filter ||
                ' ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1';
            -- Strict variant: used once the single-row ASC batch advance
            -- (below) has left v_next_seek pointing at the last row already
            -- emitted, so a plain >= would re-match it forever.
            v_delete_marker_peek_query_strict :=
                'SELECT o.name FROM storage.objects o WHERE o.bucket_id = $1 ' ||
                'AND lower(o.name) COLLATE "C" > $2' ||
                CASE WHEN v_upper_bound IS NOT NULL
                    THEN ' AND lower(o.name) COLLATE "C" < $3'
                    ELSE ''
                END ||
                v_version_filter ||
                ' ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1';
        ELSE
            v_delete_marker_peek_query :=
                'SELECT o.name FROM storage.objects o WHERE o.bucket_id = $1 ' ||
                'AND lower(o.name) COLLATE "C" < $2' ||
                CASE WHEN v_upper_bound IS NOT NULL
                    THEN ' AND lower(o.name) COLLATE "C" >= $3'
                    ELSE ''
                END ||
                v_version_filter ||
                ' ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1';
        END IF;
    END IF;

    -- Initialize seek position
    IF v_is_asc THEN
        v_next_seek := v_prefix_lower;
    ELSE
        -- DESC performs one specialized initial seek so partial current-version
        -- and delete-marker indexes remain available.
        EXECUTE format(
            'SELECT o.name FROM storage.objects o WHERE o.bucket_id = $1%s%s ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1',
            CASE WHEN v_upper_bound IS NOT NULL
                THEN ' AND lower(o.name) COLLATE "C" >= $2 AND lower(o.name) COLLATE "C" < $3'
                ELSE ''
            END,
            v_version_filter
        )
        INTO v_peek_name
        USING bucketname, v_prefix_lower, v_upper_bound;

        IF v_peek_name IS NOT NULL THEN
            v_next_seek := lower(v_peek_name) || v_delimiter;
        ELSE
            RETURN;
        END IF;
    END IF;

    -- ========================================================================
    -- MAIN LOOP: Hybrid peek-then-batch algorithm
    -- Uses STATIC SQL for peek (hot path) and DYNAMIC SQL for batch and
    -- the delete-marker-only path
    -- ========================================================================
    LOOP
        EXIT WHEN v_count >= v_limit;

        v_previous_seek := v_next_seek;
        v_previous_seek_at := v_next_seek_at;
        v_previous_seek_version := v_next_seek_version;
        v_previous_count := v_count;
        v_previous_skipped := v_skipped;

        -- STEP 1: PEEK
        v_peek_name := NULL;
        IF delete_markers = 'only' THEN
            EXECUTE CASE WHEN v_next_seek_strict
                THEN v_delete_marker_peek_query_strict
                ELSE v_delete_marker_peek_query
            END
                INTO v_peek_name
                USING bucketname, v_next_seek,
                    CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix_lower) ELSE v_prefix_lower END,
                    1, v_next_seek_at, v_next_seek_version;
        ELSIF v_multi_row AND v_next_seek_at IS NOT NULL THEN
            SELECT o.name INTO v_peek_name
            FROM storage.objects o
            WHERE o.bucket_id = bucketname
              AND lower(o.name) COLLATE "C" = v_next_seek
              AND (COALESCE(o.archived_at, 'infinity'::timestamptz) < v_next_seek_at
                   OR (COALESCE(o.archived_at, 'infinity'::timestamptz) = v_next_seek_at
                       AND COALESCE(o.version, '') > v_next_seek_version))
              AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
              AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
              AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
              AND (delete_markers != 'only' OR o.is_delete_marker)
            ORDER BY COALESCE(o.archived_at, 'infinity'::timestamptz) DESC,
                     COALESCE(o.version, '') ASC
            LIMIT 1;

            -- The current key is exhausted. Clear its version boundary and
            -- make the following ASC name peek strict. Appending '/' is not a
            -- valid lexical successor because keys ending in characters such
            -- as '!' sort between the exhausted name and name || '/'.
            IF v_peek_name IS NULL THEN
                IF v_is_asc THEN
                    v_next_seek_strict := true;
                END IF;
                v_next_seek_at := NULL;
                v_next_seek_version := '';
            END IF;
        END IF;

        -- Single-row mode is always noncurrent_versions='exclude'. Keep the
        -- current-row predicate literal so generic plans use the current index.
        IF delete_markers != 'only' AND v_peek_name IS NULL AND NOT v_multi_row THEN
            IF v_is_asc THEN
                IF v_next_seek_strict AND v_upper_bound IS NOT NULL THEN
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" > v_next_seek AND lower(o.name) COLLATE "C" < v_upper_bound
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                    ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
                ELSIF v_next_seek_strict THEN
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" > v_next_seek
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                    ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
                ELSIF v_upper_bound IS NOT NULL THEN
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek AND lower(o.name) COLLATE "C" < v_upper_bound
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                    ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
                ELSE
                    SELECT o.name INTO v_peek_name FROM storage.objects o
                    WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek
                      AND o.archived_at IS NULL
                      AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                    ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
                END IF;
            ELSIF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek AND lower(o.name) COLLATE "C" >= v_prefix_lower
                  AND o.archived_at IS NULL
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek
                  AND o.archived_at IS NULL
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            END IF;
        ELSIF delete_markers != 'only' AND v_peek_name IS NULL AND v_is_asc THEN
            IF v_next_seek_strict AND v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" > v_next_seek AND lower(o.name) COLLATE "C" < v_upper_bound
                  AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                  AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                  AND (delete_markers != 'only' OR o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            ELSIF v_next_seek_strict THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" > v_next_seek
                  AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                  AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                  AND (delete_markers != 'only' OR o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            ELSIF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek AND lower(o.name) COLLATE "C" < v_upper_bound
                  AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                  AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                  AND (delete_markers != 'only' OR o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek
                  AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                  AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                  AND (delete_markers != 'only' OR o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            END IF;
        ELSIF delete_markers != 'only' AND v_peek_name IS NULL THEN
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek AND lower(o.name) COLLATE "C" >= v_prefix_lower
                  AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                  AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                  AND (delete_markers != 'only' OR o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek
                  AND (noncurrent_versions != 'exclude' OR o.archived_at IS NULL)
                  AND (noncurrent_versions != 'only' OR o.archived_at IS NOT NULL)
                  AND (delete_markers != 'exclude' OR NOT o.is_delete_marker)
                  AND (delete_markers != 'only' OR o.is_delete_marker)
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            END IF;
        END IF;

        EXIT WHEN v_peek_name IS NULL;

        -- If the peek landed on a different key than we were tracking, any
        -- version boundary belongs to the OLD key and must not leak into the
        -- new one - e.g. the deleteMarkers='only' peek doesn't know or care
        -- whether it's continuing the same key or jumping to a new one, so
        -- it never clears these itself.
        IF lower(v_peek_name) IS DISTINCT FROM v_next_seek THEN
            v_next_seek_at := NULL;
            v_next_seek_version := '';
        END IF;

        -- The peek is authoritative for the next key to process. This is
        -- especially important after exhausting a multi-version key: the
        -- version boundary has been cleared, so executing the batch against
        -- a stale v_next_seek would replay every version of that old key.
        v_next_seek := lower(v_peek_name);
        v_next_seek_strict := false;

        -- STEP 2: Check if this is a FOLDER or FILE
        v_common_prefix := storage.get_common_prefix(lower(v_peek_name), v_prefix_lower, v_delimiter);

        IF v_common_prefix IS NOT NULL THEN
            -- FOLDER: Handle offset, emit if needed, skip to next folder
            IF v_skipped < offsets THEN
                v_skipped := v_skipped + 1;
            ELSE
                name := substring(rtrim(storage.get_common_prefix(v_peek_name, v_prefix, v_delimiter), v_delimiter) from v_prefix_len + 1);
                id := NULL;
                updated_at := NULL;
                created_at := NULL;
                last_accessed_at := NULL;
                metadata := NULL;
                version := NULL;
                archived_at := NULL;
                is_delete_marker := NULL;
                is_versioned := NULL;
                RETURN NEXT;
                v_count := v_count + 1;
            END IF;

            -- Advance seek past the folder range
            IF v_is_asc THEN
                v_next_seek := lower(left(v_common_prefix, -1)) || chr(ascii(v_delimiter) + 1);
            ELSE
                v_next_seek := lower(v_common_prefix);
            END IF;
            v_next_seek_at := NULL;
            v_next_seek_version := '';
        ELSE
            -- FILE: Batch fetch using DYNAMIC SQL (overhead amortized over many rows)
            -- For ASC: upper_bound is the exclusive upper limit (< condition)
            -- For DESC: prefix_lower is the inclusive lower limit (>= condition)
            FOR v_current IN EXECUTE v_batch_query
                USING bucketname, v_next_seek,
                    CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix_lower) ELSE v_prefix_lower END, v_file_batch_size,
                    v_next_seek_at, v_next_seek_version
            LOOP
                v_common_prefix := storage.get_common_prefix(lower(v_current.name), v_prefix_lower, v_delimiter);

                IF v_common_prefix IS NOT NULL THEN
                    -- Hit a folder: exit batch, let peek handle it. Reset
                    -- strict mode too - it may have been set by an earlier
                    -- row in this same batch (see the single-row ASC advance
                    -- below), and v_next_seek here is the folder-triggering
                    -- row's own name, which the next peek must find inclusively.
                    v_next_seek := CASE
                        WHEN v_is_asc THEN lower(v_current.name)
                        ELSE lower(v_current.name) || v_delimiter
                    END;
                    v_next_seek_at := NULL;
                    v_next_seek_version := '';
                    v_next_seek_strict := false;
                    EXIT;
                END IF;

                -- Handle offset skipping
                IF v_skipped < offsets THEN
                    v_skipped := v_skipped + 1;
                ELSE
                    -- Emit file
                    name := substring(v_current.name from v_prefix_len + 1);
                    id := v_current.id;
                    updated_at := v_current.updated_at;
                    created_at := v_current.created_at;
                    last_accessed_at := v_current.last_accessed_at;
                    metadata := v_current.metadata;
                    version := v_current.version;
                    archived_at := v_current.archived_at;
                    is_delete_marker := v_current.is_delete_marker;
                    is_versioned := v_current.is_versioned;
                    RETURN NEXT;
                    v_count := v_count + 1;
                END IF;

                -- Multi-row mode must remain on this key until all of its
                -- versions have crossed the internal batch boundary.
                IF v_multi_row THEN
                    v_next_seek := lower(v_current.name);
                    v_next_seek_at := COALESCE(v_current.archived_at, 'infinity'::timestamptz);
                    v_next_seek_version := COALESCE(v_current.version, '');
                ELSIF v_is_asc THEN
                    -- Appending the delimiter as a fake lexical successor would
                    -- skip a real key like `name || '!'` (or any character
                    -- sorting below the delimiter), which sorts between `name`
                    -- and `name || delimiter`. Track the real name and mark the
                    -- next comparison strict instead - same fix as the
                    -- exhausted-key case above.
                    v_next_seek := lower(v_current.name);
                    v_next_seek_strict := true;
                ELSE
                    v_next_seek := lower(v_current.name);
                END IF;

                EXIT WHEN v_count >= v_limit;
            END LOOP;
        END IF;

        IF v_count = v_previous_count
           AND v_skipped = v_previous_skipped
           AND v_next_seek IS NOT DISTINCT FROM v_previous_seek
           AND v_next_seek_at IS NOT DISTINCT FROM v_previous_seek_at
           AND v_next_seek_version IS NOT DISTINCT FROM v_previous_seek_version THEN
            RAISE EXCEPTION 'storage.search made no progress at seek (%, %, %)',
                v_next_seek, v_next_seek_at, v_next_seek_version;
        END IF;
    END LOOP;
END;
$_$;


ALTER FUNCTION storage.search(prefix text, bucketname text, limits integer, levels integer, offsets integer, search text, sortcolumn text, sortorder text, noncurrent_versions text, delete_markers text) OWNER TO supabase_storage_admin;

--
-- Name: search_by_timestamp(text, text, integer, integer, text, text, text, text, text, text, text); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.search_by_timestamp(p_prefix text, p_bucket_id text, p_limit integer, p_level integer, p_start_after text, p_sort_order text, p_sort_column text, p_sort_column_after text, noncurrent_versions text DEFAULT 'exclude'::text, delete_markers text DEFAULT 'exclude'::text, p_start_after_version text DEFAULT ''::text) RETURNS TABLE(key text, name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb, version text, archived_at timestamp with time zone, is_delete_marker boolean, is_versioned boolean)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_cursor_op text;
    v_query text;
    v_prefix text;
    v_prefix_pattern text;
    v_sort_order text;
    v_sort_column text;
    v_version_tiebreak text;
BEGIN
    v_prefix := coalesce(p_prefix, '');
    -- Keep the raw prefix for common-prefix calculations and escape only LIKE metacharacters.
    v_prefix_pattern := replace(v_prefix, chr(92), chr(92) || chr(92));
    v_prefix_pattern := replace(v_prefix_pattern, '%', chr(92) || '%');
    v_prefix_pattern := replace(v_prefix_pattern, '_', chr(92) || '_');

    -- COALESCE first: NULL NOT IN (...) evaluates to NULL (not TRUE), so a
    -- bare NOT IN check silently leaves an explicit NULL argument unreset.
    noncurrent_versions := COALESCE(noncurrent_versions, 'exclude');
    delete_markers := COALESCE(delete_markers, 'exclude');
    IF noncurrent_versions NOT IN ('exclude', 'only', 'include') THEN
        noncurrent_versions := 'exclude';
    END IF;
    IF delete_markers NOT IN ('exclude', 'only', 'include') THEN
        delete_markers := 'exclude';
    END IF;

    -- $9 is only populated in multi-row mode; it's always '' otherwise, so
    -- only use each row's real version as a tiebreak in multi-row mode.
    v_version_tiebreak := CASE WHEN noncurrent_versions IN ('only', 'include') THEN 'COALESCE(version, '''')' ELSE '''''' END;

    -- Defense-in-depth: this function is independently reachable and must
    -- not trust p_sort_order/p_sort_column to already be validated by a
    -- caller. Normalize to the same strict allow-list storage.search_v2
    -- uses before interpolating anything into dynamic SQL below.
    v_sort_order := lower(coalesce(p_sort_order, 'asc'));
    IF v_sort_order NOT IN ('asc', 'desc') THEN
        v_sort_order := 'asc';
    END IF;

    v_sort_column := lower(coalesce(p_sort_column, 'updated_at'));
    IF v_sort_column NOT IN ('updated_at', 'created_at') THEN
        v_sort_column := 'updated_at';
    END IF;

    IF v_sort_order = 'asc' THEN
        v_cursor_op := '>';
    ELSE
        v_cursor_op := '<';
    END IF;

    v_query := format($sql$
        WITH raw_objects AS (
            SELECT
                o.name AS obj_name,
                o.id AS obj_id,
                o.updated_at AS obj_updated_at,
                o.created_at AS obj_created_at,
                o.last_accessed_at AS obj_last_accessed_at,
                o.metadata AS obj_metadata,
                o.version AS obj_version,
                o.archived_at AS obj_archived_at,
                o.is_delete_marker AS obj_is_delete_marker,
                o.is_versioned AS obj_is_versioned,
                storage.get_common_prefix(o.name, $1, '/') AS common_prefix
            FROM storage.objects o
            WHERE o.bucket_id = $2
              AND o.name COLLATE "C" LIKE $10 || '%%'
              AND ($7 != 'exclude' OR o.archived_at IS NULL)
              AND ($7 != 'only' OR o.archived_at IS NOT NULL)
              AND ($8 != 'exclude' OR NOT o.is_delete_marker)
              AND ($8 != 'only' OR o.is_delete_marker)
        ),
        -- Aggregate common prefixes (folders)
        -- Both created_at and updated_at use MIN(obj_created_at) to match the old prefixes table behavior
        aggregated_prefixes AS (
            SELECT
                common_prefix AS name,
                NULL::uuid AS id,
                MIN(obj_created_at) AS updated_at,
                MIN(obj_created_at) AS created_at,
                NULL::timestamptz AS last_accessed_at,
                NULL::jsonb AS metadata,
                NULL::text AS version,
                NULL::timestamptz AS archived_at,
                NULL::boolean AS is_delete_marker,
                NULL::boolean AS is_versioned,
                TRUE AS is_prefix
            FROM raw_objects
            WHERE common_prefix IS NOT NULL
            GROUP BY common_prefix
        ),
        leaf_objects AS (
            SELECT
                obj_name AS name,
                obj_id AS id,
                obj_updated_at AS updated_at,
                obj_created_at AS created_at,
                obj_last_accessed_at AS last_accessed_at,
                obj_metadata AS metadata,
                obj_version AS version,
                obj_archived_at AS archived_at,
                obj_is_delete_marker AS is_delete_marker,
                obj_is_versioned AS is_versioned,
                FALSE AS is_prefix
            FROM raw_objects
            WHERE common_prefix IS NULL
        ),
        combined AS (
            SELECT * FROM aggregated_prefixes
            UNION ALL
            SELECT * FROM leaf_objects
        ),
        filtered AS (
            SELECT *
            FROM combined
            WHERE (
                $5 = ''
                OR ROW(
                    COALESCE(date_trunc('milliseconds', %I), 'epoch'::timestamptz),
                    name COLLATE "C",
                    %s
                ) %s ROW(
                    -- truncated the same way as the stored value above
                    date_trunc('milliseconds', COALESCE(NULLIF($6, '')::timestamptz, 'epoch'::timestamptz)),
                    $5,
                    $9
                )
            )
        )
        SELECT
            split_part(name, '/', $3) AS key,
            name,
            id,
            updated_at,
            created_at,
            last_accessed_at,
            metadata,
            version,
            archived_at,
            is_delete_marker,
            is_versioned
        FROM filtered
        ORDER BY
            COALESCE(date_trunc('milliseconds', %I), 'epoch'::timestamptz) %s,
            name COLLATE "C" %s,
            COALESCE(version, '') %s
        LIMIT $4
    $sql$,
        v_sort_column,
        v_version_tiebreak,
        v_cursor_op,
        v_sort_column,
        v_sort_order,
        v_sort_order,
        v_sort_order
    );

    -- version is the third tiebreak component for two versions of the same
    -- key tying on both timestamp and name (see filtered CTE / ORDER BY above)
    RETURN QUERY EXECUTE v_query
    USING v_prefix, p_bucket_id, p_level, p_limit, p_start_after, p_sort_column_after, noncurrent_versions, delete_markers, coalesce(p_start_after_version, ''), v_prefix_pattern;
END;
$_$;


ALTER FUNCTION storage.search_by_timestamp(p_prefix text, p_bucket_id text, p_limit integer, p_level integer, p_start_after text, p_sort_order text, p_sort_column text, p_sort_column_after text, noncurrent_versions text, delete_markers text, p_start_after_version text) OWNER TO supabase_storage_admin;

--
-- Name: search_v2(text, text, integer, integer, text, text, text, text, text, text, timestamp with time zone, text, boolean); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.search_v2(prefix text, bucket_name text, limits integer DEFAULT 100, levels integer DEFAULT 1, start_after text DEFAULT ''::text, sort_order text DEFAULT 'asc'::text, sort_column text DEFAULT 'name'::text, sort_column_after text DEFAULT ''::text, noncurrent_versions text DEFAULT 'exclude'::text, delete_markers text DEFAULT 'exclude'::text, start_after_archived_at timestamp with time zone DEFAULT NULL::timestamp with time zone, start_after_version text DEFAULT ''::text, start_after_is_continuation boolean DEFAULT false) RETURNS TABLE(key text, name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb, version text, archived_at timestamp with time zone, is_delete_marker boolean, is_versioned boolean)
    LANGUAGE plpgsql STABLE
    AS $$
DECLARE
    v_sort_col text;
    v_sort_ord text;
    v_limit int;
BEGIN
    -- Cap limit to maximum of 1500 records
    v_limit := LEAST(coalesce(limits, 100), 1500);

    -- Validate and normalize sort_order
    v_sort_ord := lower(coalesce(sort_order, 'asc'));
    IF v_sort_ord NOT IN ('asc', 'desc') THEN
        v_sort_ord := 'asc';
    END IF;

    -- Validate and normalize sort_column
    v_sort_col := lower(coalesce(sort_column, 'name'));
    IF v_sort_col NOT IN ('name', 'updated_at', 'created_at') THEN
        v_sort_col := 'name';
    END IF;

    -- Route to appropriate implementation
    IF v_sort_col = 'name' THEN
        -- Use list_objects_with_delimiter for name sorting (most efficient: O(k * log n))
        RETURN QUERY
        SELECT
            split_part(l.name, '/', levels) AS key,
            l.name AS name,
            l.id,
            l.updated_at,
            l.created_at,
            l.last_accessed_at,
            l.metadata,
            l.version,
            l.archived_at,
            l.is_delete_marker,
            l.is_versioned
        FROM storage.list_objects_with_delimiter(
            bucket_name,
            coalesce(prefix, ''),
            '/',
            v_limit,
            CASE WHEN start_after_is_continuation THEN '' ELSE start_after END,
            CASE WHEN start_after_is_continuation THEN start_after ELSE '' END,
            v_sort_ord,
            noncurrent_versions,
            delete_markers,
            start_after_archived_at,
            start_after_version
        ) l;
    ELSE
        -- Use aggregation approach for timestamp sorting
        -- Not efficient for large datasets but supports correct pagination
        RETURN QUERY SELECT * FROM storage.search_by_timestamp(
            prefix, bucket_name, v_limit, levels, start_after,
            v_sort_ord, v_sort_col, sort_column_after,
            noncurrent_versions, delete_markers, start_after_version
        );
    END IF;
END;
$$;


ALTER FUNCTION storage.search_v2(prefix text, bucket_name text, limits integer, levels integer, start_after text, sort_order text, sort_column text, sort_column_after text, noncurrent_versions text, delete_markers text, start_after_archived_at timestamp with time zone, start_after_version text, start_after_is_continuation boolean) OWNER TO supabase_storage_admin;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: storage; Owner: supabase_storage_admin
--

CREATE FUNCTION storage.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW; 
END;
$$;


ALTER FUNCTION storage.update_updated_at_column() OWNER TO supabase_storage_admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_log_entries; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.audit_log_entries (
    instance_id uuid,
    id uuid NOT NULL,
    payload json,
    created_at timestamp with time zone,
    ip_address character varying(64) DEFAULT ''::character varying NOT NULL
);


ALTER TABLE auth.audit_log_entries OWNER TO supabase_auth_admin;

--
-- Name: TABLE audit_log_entries; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.audit_log_entries IS 'Auth: Audit trail for user actions.';


--
-- Name: custom_oauth_providers; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.custom_oauth_providers (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    provider_type text NOT NULL,
    identifier text NOT NULL,
    name text NOT NULL,
    client_id text NOT NULL,
    client_secret text NOT NULL,
    acceptable_client_ids text[] DEFAULT '{}'::text[] NOT NULL,
    scopes text[] DEFAULT '{}'::text[] NOT NULL,
    pkce_enabled boolean DEFAULT true NOT NULL,
    attribute_mapping jsonb DEFAULT '{}'::jsonb NOT NULL,
    authorization_params jsonb DEFAULT '{}'::jsonb NOT NULL,
    enabled boolean DEFAULT true NOT NULL,
    email_optional boolean DEFAULT false NOT NULL,
    issuer text,
    discovery_url text,
    skip_nonce_check boolean DEFAULT false NOT NULL,
    cached_discovery jsonb,
    discovery_cached_at timestamp with time zone,
    authorization_url text,
    token_url text,
    userinfo_url text,
    jwks_uri text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    custom_claims_allowlist text[] DEFAULT '{}'::text[] NOT NULL,
    CONSTRAINT custom_oauth_providers_authorization_url_https CHECK (((authorization_url IS NULL) OR (authorization_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_authorization_url_length CHECK (((authorization_url IS NULL) OR (char_length(authorization_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_client_id_length CHECK (((char_length(client_id) >= 1) AND (char_length(client_id) <= 512))),
    CONSTRAINT custom_oauth_providers_discovery_url_length CHECK (((discovery_url IS NULL) OR (char_length(discovery_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_identifier_format CHECK ((identifier ~ '^[a-z0-9][a-z0-9:-]{0,48}[a-z0-9]$'::text)),
    CONSTRAINT custom_oauth_providers_issuer_length CHECK (((issuer IS NULL) OR ((char_length(issuer) >= 1) AND (char_length(issuer) <= 2048)))),
    CONSTRAINT custom_oauth_providers_jwks_uri_https CHECK (((jwks_uri IS NULL) OR (jwks_uri ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_jwks_uri_length CHECK (((jwks_uri IS NULL) OR (char_length(jwks_uri) <= 2048))),
    CONSTRAINT custom_oauth_providers_name_length CHECK (((char_length(name) >= 1) AND (char_length(name) <= 100))),
    CONSTRAINT custom_oauth_providers_oauth2_requires_endpoints CHECK (((provider_type <> 'oauth2'::text) OR ((authorization_url IS NOT NULL) AND (token_url IS NOT NULL) AND (userinfo_url IS NOT NULL)))),
    CONSTRAINT custom_oauth_providers_oidc_discovery_url_https CHECK (((provider_type <> 'oidc'::text) OR (discovery_url IS NULL) OR (discovery_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_oidc_issuer_https CHECK (((provider_type <> 'oidc'::text) OR (issuer IS NULL) OR (issuer ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_oidc_requires_issuer CHECK (((provider_type <> 'oidc'::text) OR (issuer IS NOT NULL))),
    CONSTRAINT custom_oauth_providers_provider_type_check CHECK ((provider_type = ANY (ARRAY['oauth2'::text, 'oidc'::text]))),
    CONSTRAINT custom_oauth_providers_token_url_https CHECK (((token_url IS NULL) OR (token_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_token_url_length CHECK (((token_url IS NULL) OR (char_length(token_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_userinfo_url_https CHECK (((userinfo_url IS NULL) OR (userinfo_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_userinfo_url_length CHECK (((userinfo_url IS NULL) OR (char_length(userinfo_url) <= 2048)))
);


ALTER TABLE auth.custom_oauth_providers OWNER TO supabase_auth_admin;

--
-- Name: flow_state; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.flow_state (
    id uuid NOT NULL,
    user_id uuid,
    auth_code text,
    code_challenge_method auth.code_challenge_method,
    code_challenge text,
    provider_type text NOT NULL,
    provider_access_token text,
    provider_refresh_token text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    authentication_method text NOT NULL,
    auth_code_issued_at timestamp with time zone,
    invite_token text,
    referrer text,
    oauth_client_state_id uuid,
    linking_target_id uuid,
    email_optional boolean DEFAULT false NOT NULL
);


ALTER TABLE auth.flow_state OWNER TO supabase_auth_admin;

--
-- Name: TABLE flow_state; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.flow_state IS 'Stores metadata for all OAuth/SSO login flows';


--
-- Name: identities; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.identities (
    provider_id text NOT NULL,
    user_id uuid NOT NULL,
    identity_data jsonb NOT NULL,
    provider text NOT NULL,
    last_sign_in_at timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    email text GENERATED ALWAYS AS (lower((identity_data ->> 'email'::text))) STORED,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE auth.identities OWNER TO supabase_auth_admin;

--
-- Name: TABLE identities; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.identities IS 'Auth: Stores identities associated to a user.';


--
-- Name: COLUMN identities.email; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.identities.email IS 'Auth: Email is a generated column that references the optional email property in the identity_data';


--
-- Name: instances; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.instances (
    id uuid NOT NULL,
    uuid uuid,
    raw_base_config text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE auth.instances OWNER TO supabase_auth_admin;

--
-- Name: TABLE instances; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.instances IS 'Auth: Manages users across multiple sites.';


--
-- Name: mfa_amr_claims; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_amr_claims (
    session_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    authentication_method text NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE auth.mfa_amr_claims OWNER TO supabase_auth_admin;

--
-- Name: TABLE mfa_amr_claims; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.mfa_amr_claims IS 'auth: stores authenticator method reference claims for multi factor authentication';


--
-- Name: mfa_challenges; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_challenges (
    id uuid NOT NULL,
    factor_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    verified_at timestamp with time zone,
    ip_address inet NOT NULL,
    otp_code text,
    web_authn_session_data jsonb
);


ALTER TABLE auth.mfa_challenges OWNER TO supabase_auth_admin;

--
-- Name: TABLE mfa_challenges; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.mfa_challenges IS 'auth: stores metadata about challenge requests made';


--
-- Name: mfa_factors; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_factors (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    friendly_name text,
    factor_type auth.factor_type NOT NULL,
    status auth.factor_status NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    secret text,
    phone text,
    last_challenged_at timestamp with time zone,
    web_authn_credential jsonb,
    web_authn_aaguid uuid,
    last_webauthn_challenge_data jsonb
);


ALTER TABLE auth.mfa_factors OWNER TO supabase_auth_admin;

--
-- Name: TABLE mfa_factors; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.mfa_factors IS 'auth: stores metadata about factors';


--
-- Name: COLUMN mfa_factors.last_webauthn_challenge_data; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.mfa_factors.last_webauthn_challenge_data IS 'Stores the latest WebAuthn challenge data including attestation/assertion for customer verification';


--
-- Name: mfa_recovery_code_sets; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_recovery_code_sets (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    mfa_factor_id uuid NOT NULL,
    failed_verification_count integer DEFAULT 0 NOT NULL,
    verification_locked_until timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT mfa_recovery_code_sets_failed_verification_count_check CHECK ((failed_verification_count >= 0))
);


ALTER TABLE auth.mfa_recovery_code_sets OWNER TO supabase_auth_admin;

--
-- Name: mfa_recovery_codes; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.mfa_recovery_codes (
    id uuid NOT NULL,
    mfa_recovery_code_set_id uuid NOT NULL,
    code_hash text NOT NULL,
    consumed_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE auth.mfa_recovery_codes OWNER TO supabase_auth_admin;

--
-- Name: oauth_authorizations; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_authorizations (
    id uuid NOT NULL,
    authorization_id text NOT NULL,
    client_id uuid NOT NULL,
    user_id uuid,
    redirect_uri text NOT NULL,
    scope text NOT NULL,
    state text,
    resource text,
    code_challenge text,
    code_challenge_method auth.code_challenge_method,
    response_type auth.oauth_response_type DEFAULT 'code'::auth.oauth_response_type NOT NULL,
    status auth.oauth_authorization_status DEFAULT 'pending'::auth.oauth_authorization_status NOT NULL,
    authorization_code text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone DEFAULT (now() + '00:03:00'::interval) NOT NULL,
    approved_at timestamp with time zone,
    nonce text,
    CONSTRAINT oauth_authorizations_authorization_code_length CHECK ((char_length(authorization_code) <= 255)),
    CONSTRAINT oauth_authorizations_code_challenge_length CHECK ((char_length(code_challenge) <= 128)),
    CONSTRAINT oauth_authorizations_expires_at_future CHECK ((expires_at > created_at)),
    CONSTRAINT oauth_authorizations_nonce_length CHECK ((char_length(nonce) <= 255)),
    CONSTRAINT oauth_authorizations_redirect_uri_length CHECK ((char_length(redirect_uri) <= 2048)),
    CONSTRAINT oauth_authorizations_resource_length CHECK ((char_length(resource) <= 2048)),
    CONSTRAINT oauth_authorizations_scope_length CHECK ((char_length(scope) <= 4096)),
    CONSTRAINT oauth_authorizations_state_length CHECK ((char_length(state) <= 4096))
);


ALTER TABLE auth.oauth_authorizations OWNER TO supabase_auth_admin;

--
-- Name: oauth_client_states; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_client_states (
    id uuid NOT NULL,
    provider_type text NOT NULL,
    code_verifier text,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE auth.oauth_client_states OWNER TO supabase_auth_admin;

--
-- Name: TABLE oauth_client_states; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.oauth_client_states IS 'Stores OAuth states for third-party provider authentication flows where Supabase acts as the OAuth client.';


--
-- Name: oauth_clients; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_clients (
    id uuid NOT NULL,
    client_secret_hash text,
    registration_type auth.oauth_registration_type NOT NULL,
    redirect_uris text NOT NULL,
    grant_types text NOT NULL,
    client_name text,
    client_uri text,
    logo_uri text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone,
    client_type auth.oauth_client_type DEFAULT 'confidential'::auth.oauth_client_type NOT NULL,
    token_endpoint_auth_method text NOT NULL,
    CONSTRAINT oauth_clients_client_name_length CHECK ((char_length(client_name) <= 1024)),
    CONSTRAINT oauth_clients_client_uri_length CHECK ((char_length(client_uri) <= 2048)),
    CONSTRAINT oauth_clients_logo_uri_length CHECK ((char_length(logo_uri) <= 2048)),
    CONSTRAINT oauth_clients_token_endpoint_auth_method_check CHECK ((token_endpoint_auth_method = ANY (ARRAY['client_secret_basic'::text, 'client_secret_post'::text, 'none'::text])))
);


ALTER TABLE auth.oauth_clients OWNER TO supabase_auth_admin;

--
-- Name: oauth_consents; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.oauth_consents (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    client_id uuid NOT NULL,
    scopes text NOT NULL,
    granted_at timestamp with time zone DEFAULT now() NOT NULL,
    revoked_at timestamp with time zone,
    CONSTRAINT oauth_consents_revoked_after_granted CHECK (((revoked_at IS NULL) OR (revoked_at >= granted_at))),
    CONSTRAINT oauth_consents_scopes_length CHECK ((char_length(scopes) <= 2048)),
    CONSTRAINT oauth_consents_scopes_not_empty CHECK ((char_length(TRIM(BOTH FROM scopes)) > 0))
);


ALTER TABLE auth.oauth_consents OWNER TO supabase_auth_admin;

--
-- Name: one_time_tokens; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.one_time_tokens (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    token_type auth.one_time_token_type NOT NULL,
    token_hash text NOT NULL,
    relates_to text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone,
    CONSTRAINT one_time_tokens_token_hash_check CHECK ((char_length(token_hash) > 0))
);


ALTER TABLE auth.one_time_tokens OWNER TO supabase_auth_admin;

--
-- Name: refresh_tokens; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.refresh_tokens (
    instance_id uuid,
    id bigint NOT NULL,
    token character varying(255),
    user_id character varying(255),
    revoked boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    parent character varying(255),
    session_id uuid
);


ALTER TABLE auth.refresh_tokens OWNER TO supabase_auth_admin;

--
-- Name: TABLE refresh_tokens; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.refresh_tokens IS 'Auth: Store of tokens used to refresh JWT tokens once they expire.';


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: auth; Owner: supabase_auth_admin
--

CREATE SEQUENCE auth.refresh_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE auth.refresh_tokens_id_seq OWNER TO supabase_auth_admin;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: auth; Owner: supabase_auth_admin
--

ALTER SEQUENCE auth.refresh_tokens_id_seq OWNED BY auth.refresh_tokens.id;


--
-- Name: saml_providers; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.saml_providers (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    entity_id text NOT NULL,
    metadata_xml text NOT NULL,
    metadata_url text,
    attribute_mapping jsonb,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    name_id_format text,
    CONSTRAINT "entity_id not empty" CHECK ((char_length(entity_id) > 0)),
    CONSTRAINT "metadata_url not empty" CHECK (((metadata_url = NULL::text) OR (char_length(metadata_url) > 0))),
    CONSTRAINT "metadata_xml not empty" CHECK ((char_length(metadata_xml) > 0))
);


ALTER TABLE auth.saml_providers OWNER TO supabase_auth_admin;

--
-- Name: TABLE saml_providers; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.saml_providers IS 'Auth: Manages SAML Identity Provider connections.';


--
-- Name: saml_relay_states; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.saml_relay_states (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    request_id text NOT NULL,
    for_email text,
    redirect_to text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    flow_state_id uuid,
    CONSTRAINT "request_id not empty" CHECK ((char_length(request_id) > 0))
);


ALTER TABLE auth.saml_relay_states OWNER TO supabase_auth_admin;

--
-- Name: TABLE saml_relay_states; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.saml_relay_states IS 'Auth: Contains SAML Relay State information for each Service Provider initiated login.';


--
-- Name: schema_migrations; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.schema_migrations (
    version character varying(255) NOT NULL
);


ALTER TABLE auth.schema_migrations OWNER TO supabase_auth_admin;

--
-- Name: TABLE schema_migrations; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.schema_migrations IS 'Auth: Manages updates to the auth system.';


--
-- Name: scim_tokens; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.scim_tokens (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    token_hash text NOT NULL,
    prefix text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone,
    revoked_at timestamp with time zone,
    last_used_at timestamp with time zone,
    CONSTRAINT scim_tokens_expires_at_future CHECK (((expires_at IS NULL) OR (expires_at > created_at))),
    CONSTRAINT scim_tokens_revoked_after_created CHECK (((revoked_at IS NULL) OR (revoked_at >= created_at))),
    CONSTRAINT scim_tokens_token_hash_check CHECK ((token_hash ~ '^[0-9a-f]{64}$'::text))
);


ALTER TABLE auth.scim_tokens OWNER TO supabase_auth_admin;

--
-- Name: scim_users; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.scim_users (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    user_id uuid,
    resource jsonb NOT NULL,
    user_name text GENERATED ALWAYS AS (lower((resource ->> 'userName'::text))) STORED NOT NULL,
    external_id text GENERATED ALWAYS AS ((resource ->> 'externalId'::text)) STORED,
    active boolean GENERATED ALWAYS AS (COALESCE(((resource ->> 'active'::text))::boolean, true)) STORED NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE auth.scim_users OWNER TO supabase_auth_admin;

--
-- Name: sessions; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    factor_id uuid,
    aal auth.aal_level,
    not_after timestamp with time zone,
    refreshed_at timestamp without time zone,
    user_agent text,
    ip inet,
    tag text,
    oauth_client_id uuid,
    refresh_token_hmac_key text,
    refresh_token_counter bigint,
    scopes text,
    CONSTRAINT sessions_scopes_length CHECK ((char_length(scopes) <= 4096))
);


ALTER TABLE auth.sessions OWNER TO supabase_auth_admin;

--
-- Name: TABLE sessions; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.sessions IS 'Auth: Stores session data associated to a user.';


--
-- Name: COLUMN sessions.not_after; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sessions.not_after IS 'Auth: Not after is a nullable column that contains a timestamp after which the session should be regarded as expired.';


--
-- Name: COLUMN sessions.refresh_token_hmac_key; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sessions.refresh_token_hmac_key IS 'Holds a HMAC-SHA256 key used to sign refresh tokens for this session.';


--
-- Name: COLUMN sessions.refresh_token_counter; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sessions.refresh_token_counter IS 'Holds the ID (counter) of the last issued refresh token.';


--
-- Name: sso_domains; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.sso_domains (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    domain text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    CONSTRAINT "domain not empty" CHECK ((char_length(domain) > 0))
);


ALTER TABLE auth.sso_domains OWNER TO supabase_auth_admin;

--
-- Name: TABLE sso_domains; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.sso_domains IS 'Auth: Manages SSO email address domain mapping to an SSO Identity Provider.';


--
-- Name: sso_providers; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.sso_providers (
    id uuid NOT NULL,
    resource_id text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    disabled boolean,
    CONSTRAINT "resource_id not empty" CHECK (((resource_id = NULL::text) OR (char_length(resource_id) > 0)))
);


ALTER TABLE auth.sso_providers OWNER TO supabase_auth_admin;

--
-- Name: TABLE sso_providers; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.sso_providers IS 'Auth: Manages SSO identity provider information; see saml_providers for SAML.';


--
-- Name: COLUMN sso_providers.resource_id; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.sso_providers.resource_id IS 'Auth: Uniquely identifies a SSO provider according to a user-chosen resource ID (case insensitive), useful in infrastructure as code.';


--
-- Name: users; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.users (
    instance_id uuid,
    id uuid NOT NULL,
    aud character varying(255),
    role character varying(255),
    email character varying(255),
    encrypted_password character varying(255),
    email_confirmed_at timestamp with time zone,
    invited_at timestamp with time zone,
    confirmation_token character varying(255),
    confirmation_sent_at timestamp with time zone,
    recovery_token character varying(255),
    recovery_sent_at timestamp with time zone,
    email_change_token_new character varying(255),
    email_change character varying(255),
    email_change_sent_at timestamp with time zone,
    last_sign_in_at timestamp with time zone,
    raw_app_meta_data jsonb,
    raw_user_meta_data jsonb,
    is_super_admin boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    phone text DEFAULT NULL::character varying,
    phone_confirmed_at timestamp with time zone,
    phone_change text DEFAULT ''::character varying,
    phone_change_token character varying(255) DEFAULT ''::character varying,
    phone_change_sent_at timestamp with time zone,
    confirmed_at timestamp with time zone GENERATED ALWAYS AS (LEAST(email_confirmed_at, phone_confirmed_at)) STORED,
    email_change_token_current character varying(255) DEFAULT ''::character varying,
    email_change_confirm_status smallint DEFAULT 0,
    banned_until timestamp with time zone,
    reauthentication_token character varying(255) DEFAULT ''::character varying,
    reauthentication_sent_at timestamp with time zone,
    is_sso_user boolean DEFAULT false NOT NULL,
    deleted_at timestamp with time zone,
    is_anonymous boolean DEFAULT false NOT NULL,
    CONSTRAINT users_email_change_confirm_status_check CHECK (((email_change_confirm_status >= 0) AND (email_change_confirm_status <= 2)))
);


ALTER TABLE auth.users OWNER TO supabase_auth_admin;

--
-- Name: TABLE users; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON TABLE auth.users IS 'Auth: Stores user login data within a secure schema.';


--
-- Name: COLUMN users.is_sso_user; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON COLUMN auth.users.is_sso_user IS 'Auth: Set this column to true when the account comes from SSO. These accounts can have duplicate emails.';


--
-- Name: webauthn_challenges; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.webauthn_challenges (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    challenge_type text NOT NULL,
    session_data jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    CONSTRAINT webauthn_challenges_challenge_type_check CHECK ((challenge_type = ANY (ARRAY['signup'::text, 'registration'::text, 'authentication'::text])))
);


ALTER TABLE auth.webauthn_challenges OWNER TO supabase_auth_admin;

--
-- Name: webauthn_credentials; Type: TABLE; Schema: auth; Owner: supabase_auth_admin
--

CREATE TABLE auth.webauthn_credentials (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    credential_id bytea NOT NULL,
    public_key bytea NOT NULL,
    attestation_type text DEFAULT ''::text NOT NULL,
    aaguid uuid,
    sign_count bigint DEFAULT 0 NOT NULL,
    transports jsonb DEFAULT '[]'::jsonb NOT NULL,
    backup_eligible boolean DEFAULT false NOT NULL,
    backed_up boolean DEFAULT false NOT NULL,
    friendly_name text DEFAULT ''::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_used_at timestamp with time zone
);


ALTER TABLE auth.webauthn_credentials OWNER TO supabase_auth_admin;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin (
    admin_id integer NOT NULL,
    name text NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(100) NOT NULL,
    account_status character varying(10) DEFAULT 'active'::character varying,
    updated_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    created_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    token_version character varying
);


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: admin_admin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admin_admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admin_admin_id_seq OWNER TO postgres;

--
-- Name: admin_admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admin_admin_id_seq OWNED BY public.admin.admin_id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: auditlog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auditlog (
    audit_id integer NOT NULL,
    admin_id integer,
    action_type character varying(30) NOT NULL,
    entity_type character varying(50) NOT NULL,
    entity_id integer,
    description text,
    old_value text,
    new_value text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.auditlog OWNER TO postgres;

--
-- Name: auditlog_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auditlog_audit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auditlog_audit_id_seq OWNER TO postgres;

--
-- Name: auditlog_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auditlog_audit_id_seq OWNED BY public.auditlog.audit_id;


--
-- Name: chathistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chathistory (
    chat_id integer NOT NULL,
    student_id integer NOT NULL,
    user_message text NOT NULL,
    ai_response text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.chathistory OWNER TO postgres;

--
-- Name: chathistory_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chathistory_chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chathistory_chat_id_seq OWNER TO postgres;

--
-- Name: chathistory_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chathistory_chat_id_seq OWNED BY public.chathistory.chat_id;


--
-- Name: conducting_body; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conducting_body (
    body_id integer NOT NULL,
    name text NOT NULL,
    main_website text NOT NULL,
    description text,
    logo_url text
);


ALTER TABLE public.conducting_body OWNER TO postgres;

--
-- Name: conducting_body_body_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conducting_body_body_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.conducting_body_body_id_seq OWNER TO postgres;

--
-- Name: conducting_body_body_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conducting_body_body_id_seq OWNED BY public.conducting_body.body_id;


--
-- Name: education; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.education (
    education_id integer NOT NULL,
    student_id integer NOT NULL,
    qualification text NOT NULL,
    course text,
    specialization text,
    college text,
    university text,
    cgpa numeric(4,2),
    percentage numeric(5,2),
    year_of_passing integer,
    current_year integer,
    is_current boolean DEFAULT false,
    institution character varying,
    year_of_study_label character varying,
    is_higher_qualification boolean,
    CONSTRAINT chk_cgpa CHECK (((cgpa IS NULL) OR ((cgpa >= (0)::numeric) AND (cgpa <= (10)::numeric)))),
    CONSTRAINT chk_current_year CHECK (((current_year IS NULL) OR (current_year > 0))),
    CONSTRAINT chk_percentage CHECK (((percentage IS NULL) OR ((percentage >= (0)::numeric) AND (percentage <= (100)::numeric)))),
    CONSTRAINT chk_year_of_passing CHECK (((year_of_passing IS NULL) OR ((year_of_passing >= 1900) AND (year_of_passing <= 2100))))
);


ALTER TABLE public.education OWNER TO postgres;

--
-- Name: education_education_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.education_education_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.education_education_id_seq OWNER TO postgres;

--
-- Name: education_education_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.education_education_id_seq OWNED BY public.education.education_id;


--
-- Name: eligibilityattribute; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eligibilityattribute (
    attribute_id integer NOT NULL,
    attribute_name text NOT NULL,
    source_table character varying(30) NOT NULL,
    source_column character varying(20) NOT NULL,
    data_type character varying(20) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.eligibilityattribute OWNER TO postgres;

--
-- Name: eligibilityattribute_attrubute_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eligibilityattribute_attrubute_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eligibilityattribute_attrubute_id_seq OWNER TO postgres;

--
-- Name: eligibilityattribute_attrubute_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eligibilityattribute_attrubute_id_seq OWNED BY public.eligibilityattribute.attribute_id;


--
-- Name: eligibilityrule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eligibilityrule (
    rule_id integer NOT NULL,
    group_id integer NOT NULL,
    attribute_id integer NOT NULL,
    operator character varying(10) NOT NULL,
    value text NOT NULL,
    CONSTRAINT chk_rule_operator CHECK (((operator)::text = ANY (ARRAY[('='::character varying)::text, ('!='::character varying)::text, ('>'::character varying)::text, ('>='::character varying)::text, ('<'::character varying)::text, ('<='::character varying)::text])))
);


ALTER TABLE public.eligibilityrule OWNER TO postgres;

--
-- Name: eligibilityrule_rule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eligibilityrule_rule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eligibilityrule_rule_id_seq OWNER TO postgres;

--
-- Name: eligibilityrule_rule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eligibilityrule_rule_id_seq OWNED BY public.eligibilityrule.rule_id;


--
-- Name: eligibilityrulegroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eligibilityrulegroup (
    group_id integer NOT NULL,
    notification_id integer NOT NULL,
    group_number integer NOT NULL,
    logical_operator character varying(5) NOT NULL,
    parent_group_id integer,
    CONSTRAINT chk_group_logical_operator CHECK (((logical_operator)::text = ANY (ARRAY[('AND'::character varying)::text, ('OR'::character varying)::text])))
);


ALTER TABLE public.eligibilityrulegroup OWNER TO postgres;

--
-- Name: eligibilityrulegroup_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.eligibilityrulegroup_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.eligibilityrulegroup_group_id_seq OWNER TO postgres;

--
-- Name: eligibilityrulegroup_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.eligibilityrulegroup_group_id_seq OWNED BY public.eligibilityrulegroup.group_id;


--
-- Name: exam; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exam (
    exam_id integer NOT NULL,
    body_id integer NOT NULL,
    name text NOT NULL,
    type text NOT NULL,
    description text,
    off_exam_page text,
    status character varying(20)
);


ALTER TABLE public.exam OWNER TO postgres;

--
-- Name: exam_exam_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exam_exam_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exam_exam_id_seq OWNER TO postgres;

--
-- Name: exam_exam_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exam_exam_id_seq OWNED BY public.exam.exam_id;


--
-- Name: examdate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.examdate (
    exam_date_id integer NOT NULL,
    notification_id integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL
);


ALTER TABLE public.examdate OWNER TO postgres;

--
-- Name: examdate_exam_date_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.examdate_exam_date_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.examdate_exam_date_id_seq OWNER TO postgres;

--
-- Name: examdate_exam_date_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.examdate_exam_date_id_seq OWNED BY public.examdate.exam_date_id;


--
-- Name: extractionhistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.extractionhistory (
    extraction_id integer NOT NULL,
    notification_id integer NOT NULL,
    extraction_type character varying(30) NOT NULL,
    source_pdf_path text NOT NULL,
    extracted_content text,
    ai_summary text,
    change_detected boolean DEFAULT false NOT NULL,
    change_details text,
    extraction_status character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.extractionhistory OWNER TO postgres;

--
-- Name: extractionhistory_extraction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.extractionhistory_extraction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.extractionhistory_extraction_id_seq OWNER TO postgres;

--
-- Name: extractionhistory_extraction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.extractionhistory_extraction_id_seq OWNED BY public.extractionhistory.extraction_id;


--
-- Name: monitoringreview; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.monitoringreview (
    review_id integer NOT NULL,
    notification_id integer NOT NULL,
    old_document_hash text NOT NULL,
    new_document_hash text NOT NULL,
    old_extraction text NOT NULL,
    new_extraction text NOT NULL,
    structural_changes text NOT NULL,
    semantic_analysis text NOT NULL,
    impact_analysis text NOT NULL,
    review_status character varying(20) DEFAULT 'PENDING'::character varying NOT NULL,
    rejection_reason text,
    reviewed_by integer,
    reviewed_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.monitoringreview OWNER TO postgres;

--
-- Name: monitoringreview_review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.monitoringreview_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.monitoringreview_review_id_seq OWNER TO postgres;

--
-- Name: monitoringreview_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.monitoringreview_review_id_seq OWNED BY public.monitoringreview.review_id;


--
-- Name: notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification (
    notification_id integer NOT NULL,
    student_id integer NOT NULL,
    exam_id integer,
    notification_type character varying(30) NOT NULL,
    title text NOT NULL,
    message text NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    read_at timestamp without time zone,
    dedupe_key character varying(200),
    email_status character varying(20),
    email_sent_at timestamp without time zone,
    email_error character varying
);


ALTER TABLE public.notification OWNER TO postgres;

--
-- Name: notification_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notification_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notification_notification_id_seq OWNER TO postgres;

--
-- Name: notification_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_notification_id_seq OWNED BY public.notification.notification_id;


--
-- Name: officialnotification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.officialnotification (
    notification_id integer NOT NULL,
    exam_id integer NOT NULL,
    title text NOT NULL,
    notification_type character varying(20) NOT NULL,
    release_date date,
    application_start_date date,
    application_end_date date,
    official_url text NOT NULL,
    pdf_path text NOT NULL,
    ai_summary text,
    ai_change_summary text,
    approval_status character varying(20) DEFAULT 'PENDING'::character varying NOT NULL,
    rejection_reason text,
    downloaded_on timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    document_url text,
    document_hash text
);


ALTER TABLE public.officialnotification OWNER TO postgres;

--
-- Name: officialnotification_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.officialnotification_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.officialnotification_notification_id_seq OWNER TO postgres;

--
-- Name: officialnotification_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.officialnotification_notification_id_seq OWNED BY public.officialnotification.notification_id;


--
-- Name: pending_signup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pending_signup (
    pending_id integer NOT NULL,
    email character varying(320) NOT NULL,
    name character varying(200) NOT NULL,
    password_hash character varying(200) NOT NULL,
    code_hash character varying(200) NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    attempts integer DEFAULT 0 NOT NULL,
    send_count integer DEFAULT 1 NOT NULL,
    last_sent_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.pending_signup OWNER TO postgres;

--
-- Name: pending_signup_pending_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pending_signup_pending_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pending_signup_pending_id_seq OWNER TO postgres;

--
-- Name: pending_signup_pending_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pending_signup_pending_id_seq OWNED BY public.pending_signup.pending_id;


--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    student_id bigint NOT NULL,
    name text NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(100) NOT NULL,
    phone_number character varying(20),
    date_of_birth date,
    gender character varying(10),
    account_status character varying(10) DEFAULT 'active'::character varying,
    created_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    nationality character varying(20),
    state character varying(30),
    token_version character varying
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Name: student_student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_student_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_student_id_seq OWNER TO postgres;

--
-- Name: student_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_student_id_seq OWNED BY public.student.student_id;


--
-- Name: studentexameligibility; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.studentexameligibility (
    eligibility_id integer NOT NULL,
    student_id integer NOT NULL,
    exam_id integer NOT NULL,
    eligibility_status character varying(20) NOT NULL,
    reason text,
    evaluated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_eligibility_status CHECK (((eligibility_status)::text = ANY (ARRAY[('ELIGIBLE'::character varying)::text, ('NOT_ELIGIBLE'::character varying)::text])))
);


ALTER TABLE public.studentexameligibility OWNER TO postgres;

--
-- Name: studentexameligibility_eligibility_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.studentexameligibility_eligibility_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.studentexameligibility_eligibility_id_seq OWNER TO postgres;

--
-- Name: studentexameligibility_eligibility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.studentexameligibility_eligibility_id_seq OWNED BY public.studentexameligibility.eligibility_id;


--
-- Name: trackedexam; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trackedexam (
    tracking_id integer NOT NULL,
    student_id integer NOT NULL,
    exam_id integer NOT NULL,
    tracked_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    tracking_status character varying(20) DEFAULT 'ACTIVE'::character varying NOT NULL,
    CONSTRAINT chk_tracking_status CHECK (((tracking_status)::text = ANY (ARRAY[('ACTIVE'::character varying)::text, ('INACTIVE'::character varying)::text])))
);


ALTER TABLE public.trackedexam OWNER TO postgres;

--
-- Name: trackedexam_tracking_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trackedexam_tracking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trackedexam_tracking_id_seq OWNER TO postgres;

--
-- Name: trackedexam_tracking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trackedexam_tracking_id_seq OWNED BY public.trackedexam.tracking_id;


--
-- Name: work_experience; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.work_experience (
    work_experience_id integer NOT NULL,
    student_id integer NOT NULL,
    company character varying,
    role character varying,
    duration character varying
);


ALTER TABLE public.work_experience OWNER TO postgres;

--
-- Name: work_experience_work_experience_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.work_experience_work_experience_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.work_experience_work_experience_id_seq OWNER TO postgres;

--
-- Name: work_experience_work_experience_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.work_experience_work_experience_id_seq OWNED BY public.work_experience.work_experience_id;


--
-- Name: messages; Type: TABLE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TABLE realtime.messages (
    topic text NOT NULL,
    extension text NOT NULL,
    payload jsonb,
    event text,
    private boolean DEFAULT false,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    inserted_at timestamp without time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    binary_payload bytea,
    skip_broadcast boolean DEFAULT false NOT NULL
)
PARTITION BY RANGE (inserted_at);


ALTER TABLE realtime.messages OWNER TO supabase_realtime_admin;

--
-- Name: schema_migrations; Type: TABLE; Schema: realtime; Owner: supabase_admin
--

CREATE TABLE realtime.schema_migrations (
    version bigint NOT NULL,
    inserted_at timestamp(0) without time zone DEFAULT now()
);


ALTER TABLE realtime.schema_migrations OWNER TO supabase_admin;

--
-- Name: subscription; Type: TABLE; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TABLE realtime.subscription (
    id bigint NOT NULL,
    subscription_id uuid NOT NULL,
    entity regclass NOT NULL,
    filters realtime.user_defined_filter[] DEFAULT '{}'::realtime.user_defined_filter[] NOT NULL,
    claims jsonb NOT NULL,
    claims_role regrole GENERATED ALWAYS AS (realtime.to_regrole((claims ->> 'role'::text))) STORED NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    action_filter text DEFAULT '*'::text,
    selected_columns text[],
    CONSTRAINT subscription_action_filter_check CHECK ((action_filter = ANY (ARRAY['*'::text, 'INSERT'::text, 'UPDATE'::text, 'DELETE'::text])))
);


ALTER TABLE realtime.subscription OWNER TO supabase_realtime_admin;

--
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: realtime; Owner: supabase_realtime_admin
--

ALTER TABLE realtime.subscription ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME realtime.subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: buckets; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.buckets (
    id text NOT NULL,
    name text NOT NULL,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    public boolean DEFAULT false,
    avif_autodetection boolean DEFAULT false,
    file_size_limit bigint,
    allowed_mime_types text[],
    owner_id text,
    type storage.buckettype DEFAULT 'STANDARD'::storage.buckettype NOT NULL,
    versioning_status text DEFAULT 'DISABLED'::text NOT NULL,
    lifecycle_configuration jsonb,
    lifecycle_configuration_generation uuid,
    CONSTRAINT buckets_lifecycle_configuration_pair_check CHECK (((lifecycle_configuration IS NULL) = (lifecycle_configuration_generation IS NULL))),
    CONSTRAINT buckets_lifecycle_configuration_shape_check CHECK (((lifecycle_configuration IS NULL) OR ((jsonb_typeof(lifecycle_configuration) = 'object'::text) AND (lifecycle_configuration ? 'rules'::text) AND
CASE
    WHEN (jsonb_typeof((lifecycle_configuration -> 'rules'::text)) = 'array'::text) THEN ((jsonb_array_length((lifecycle_configuration -> 'rules'::text)) >= 1) AND (jsonb_array_length((lifecycle_configuration -> 'rules'::text)) <= 1000))
    ELSE false
END))),
    CONSTRAINT buckets_lifecycle_configuration_standard_only_check CHECK (((type = 'STANDARD'::storage.buckettype) OR ((lifecycle_configuration IS NULL) AND (lifecycle_configuration_generation IS NULL)))),
    CONSTRAINT buckets_versioning_dark_check CHECK ((versioning_status = 'DISABLED'::text)),
    CONSTRAINT buckets_versioning_standard_only_check CHECK (((type = 'STANDARD'::storage.buckettype) OR (versioning_status = 'DISABLED'::text))),
    CONSTRAINT buckets_versioning_status_check CHECK ((versioning_status = ANY (ARRAY['DISABLED'::text, 'ENABLED'::text, 'SUSPENDED'::text])))
);


ALTER TABLE storage.buckets OWNER TO supabase_storage_admin;

--
-- Name: COLUMN buckets.owner; Type: COMMENT; Schema: storage; Owner: supabase_storage_admin
--

COMMENT ON COLUMN storage.buckets.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: buckets_analytics; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.buckets_analytics (
    name text NOT NULL,
    type storage.buckettype DEFAULT 'ANALYTICS'::storage.buckettype NOT NULL,
    format text DEFAULT 'ICEBERG'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE storage.buckets_analytics OWNER TO supabase_storage_admin;

--
-- Name: buckets_vectors; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.buckets_vectors (
    id text NOT NULL,
    type storage.buckettype DEFAULT 'VECTOR'::storage.buckettype NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE storage.buckets_vectors OWNER TO supabase_storage_admin;

--
-- Name: migrations; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.migrations (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    hash character varying(40) NOT NULL,
    executed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE storage.migrations OWNER TO supabase_storage_admin;

--
-- Name: objects; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.objects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    bucket_id text,
    name text,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    last_accessed_at timestamp with time zone DEFAULT now(),
    metadata jsonb,
    path_tokens text[] GENERATED ALWAYS AS (string_to_array(name, '/'::text)) STORED,
    version text,
    owner_id text,
    user_metadata jsonb,
    archived_at timestamp with time zone,
    is_delete_marker boolean DEFAULT false NOT NULL,
    is_versioned boolean DEFAULT false NOT NULL
);


ALTER TABLE storage.objects OWNER TO supabase_storage_admin;

--
-- Name: COLUMN objects.owner; Type: COMMENT; Schema: storage; Owner: supabase_storage_admin
--

COMMENT ON COLUMN storage.objects.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: s3_multipart_uploads; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.s3_multipart_uploads (
    id text NOT NULL,
    in_progress_size bigint DEFAULT 0 NOT NULL,
    upload_signature text NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    version text NOT NULL,
    owner_id text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    user_metadata jsonb,
    metadata jsonb
);


ALTER TABLE storage.s3_multipart_uploads OWNER TO supabase_storage_admin;

--
-- Name: s3_multipart_uploads_parts; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.s3_multipart_uploads_parts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    upload_id text NOT NULL,
    size bigint DEFAULT 0 NOT NULL,
    part_number integer NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    etag text NOT NULL,
    owner_id text,
    version text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE storage.s3_multipart_uploads_parts OWNER TO supabase_storage_admin;

--
-- Name: vector_indexes; Type: TABLE; Schema: storage; Owner: supabase_storage_admin
--

CREATE TABLE storage.vector_indexes (
    id text DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL COLLATE pg_catalog."C",
    bucket_id text NOT NULL,
    data_type text NOT NULL,
    dimension integer NOT NULL,
    distance_metric text NOT NULL,
    metadata_configuration jsonb,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE storage.vector_indexes OWNER TO supabase_storage_admin;

--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('auth.refresh_tokens_id_seq'::regclass);


--
-- Name: admin admin_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin ALTER COLUMN admin_id SET DEFAULT nextval('public.admin_admin_id_seq'::regclass);


--
-- Name: auditlog audit_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditlog ALTER COLUMN audit_id SET DEFAULT nextval('public.auditlog_audit_id_seq'::regclass);


--
-- Name: chathistory chat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chathistory ALTER COLUMN chat_id SET DEFAULT nextval('public.chathistory_chat_id_seq'::regclass);


--
-- Name: conducting_body body_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conducting_body ALTER COLUMN body_id SET DEFAULT nextval('public.conducting_body_body_id_seq'::regclass);


--
-- Name: education education_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education ALTER COLUMN education_id SET DEFAULT nextval('public.education_education_id_seq'::regclass);


--
-- Name: eligibilityattribute attribute_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityattribute ALTER COLUMN attribute_id SET DEFAULT nextval('public.eligibilityattribute_attrubute_id_seq'::regclass);


--
-- Name: eligibilityrule rule_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrule ALTER COLUMN rule_id SET DEFAULT nextval('public.eligibilityrule_rule_id_seq'::regclass);


--
-- Name: eligibilityrulegroup group_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrulegroup ALTER COLUMN group_id SET DEFAULT nextval('public.eligibilityrulegroup_group_id_seq'::regclass);


--
-- Name: exam exam_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam ALTER COLUMN exam_id SET DEFAULT nextval('public.exam_exam_id_seq'::regclass);


--
-- Name: examdate exam_date_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examdate ALTER COLUMN exam_date_id SET DEFAULT nextval('public.examdate_exam_date_id_seq'::regclass);


--
-- Name: extractionhistory extraction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extractionhistory ALTER COLUMN extraction_id SET DEFAULT nextval('public.extractionhistory_extraction_id_seq'::regclass);


--
-- Name: monitoringreview review_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitoringreview ALTER COLUMN review_id SET DEFAULT nextval('public.monitoringreview_review_id_seq'::regclass);


--
-- Name: notification notification_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification ALTER COLUMN notification_id SET DEFAULT nextval('public.notification_notification_id_seq'::regclass);


--
-- Name: officialnotification notification_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.officialnotification ALTER COLUMN notification_id SET DEFAULT nextval('public.officialnotification_notification_id_seq'::regclass);


--
-- Name: pending_signup pending_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pending_signup ALTER COLUMN pending_id SET DEFAULT nextval('public.pending_signup_pending_id_seq'::regclass);


--
-- Name: student student_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student ALTER COLUMN student_id SET DEFAULT nextval('public.student_student_id_seq'::regclass);


--
-- Name: studentexameligibility eligibility_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studentexameligibility ALTER COLUMN eligibility_id SET DEFAULT nextval('public.studentexameligibility_eligibility_id_seq'::regclass);


--
-- Name: trackedexam tracking_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trackedexam ALTER COLUMN tracking_id SET DEFAULT nextval('public.trackedexam_tracking_id_seq'::regclass);


--
-- Name: work_experience work_experience_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_experience ALTER COLUMN work_experience_id SET DEFAULT nextval('public.work_experience_work_experience_id_seq'::regclass);


--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.audit_log_entries (instance_id, id, payload, created_at, ip_address) FROM stdin;
\.


--
-- Data for Name: custom_oauth_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.custom_oauth_providers (id, provider_type, identifier, name, client_id, client_secret, acceptable_client_ids, scopes, pkce_enabled, attribute_mapping, authorization_params, enabled, email_optional, issuer, discovery_url, skip_nonce_check, cached_discovery, discovery_cached_at, authorization_url, token_url, userinfo_url, jwks_uri, created_at, updated_at, custom_claims_allowlist) FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.flow_state (id, user_id, auth_code, code_challenge_method, code_challenge, provider_type, provider_access_token, provider_refresh_token, created_at, updated_at, authentication_method, auth_code_issued_at, invite_token, referrer, oauth_client_state_id, linking_target_id, email_optional) FROM stdin;
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.identities (provider_id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at, id) FROM stdin;
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.instances (id, uuid, raw_base_config, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_amr_claims (session_id, created_at, updated_at, authentication_method, id) FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_challenges (id, factor_id, created_at, verified_at, ip_address, otp_code, web_authn_session_data) FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_factors (id, user_id, friendly_name, factor_type, status, created_at, updated_at, secret, phone, last_challenged_at, web_authn_credential, web_authn_aaguid, last_webauthn_challenge_data) FROM stdin;
\.


--
-- Data for Name: mfa_recovery_code_sets; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_recovery_code_sets (id, user_id, mfa_factor_id, failed_verification_count, verification_locked_until, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: mfa_recovery_codes; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.mfa_recovery_codes (id, mfa_recovery_code_set_id, code_hash, consumed_at, created_at) FROM stdin;
\.


--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_authorizations (id, authorization_id, client_id, user_id, redirect_uri, scope, state, resource, code_challenge, code_challenge_method, response_type, status, authorization_code, created_at, expires_at, approved_at, nonce) FROM stdin;
\.


--
-- Data for Name: oauth_client_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_client_states (id, provider_type, code_verifier, created_at) FROM stdin;
\.


--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_clients (id, client_secret_hash, registration_type, redirect_uris, grant_types, client_name, client_uri, logo_uri, created_at, updated_at, deleted_at, client_type, token_endpoint_auth_method) FROM stdin;
\.


--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.oauth_consents (id, user_id, client_id, scopes, granted_at, revoked_at) FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.one_time_tokens (id, user_id, token_type, token_hash, relates_to, created_at, updated_at, expires_at) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.refresh_tokens (instance_id, id, token, user_id, revoked, created_at, updated_at, parent, session_id) FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.saml_providers (id, sso_provider_id, entity_id, metadata_xml, metadata_url, attribute_mapping, created_at, updated_at, name_id_format) FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.saml_relay_states (id, sso_provider_id, request_id, for_email, redirect_to, created_at, updated_at, flow_state_id) FROM stdin;
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.schema_migrations (version) FROM stdin;
20171026211738
20171026211808
20171026211834
20180103212743
20180108183307
20180119214651
20180125194653
00
20210710035447
20210722035447
20210730183235
20210909172000
20210927181326
20211122151130
20211124214934
20211202183645
20220114185221
20220114185340
20220224000811
20220323170000
20220429102000
20220531120530
20220614074223
20220811173540
20221003041349
20221003041400
20221011041400
20221020193600
20221021073300
20221021082433
20221027105023
20221114143122
20221114143410
20221125140132
20221208132122
20221215195500
20221215195800
20221215195900
20230116124310
20230116124412
20230131181311
20230322519590
20230402418590
20230411005111
20230508135423
20230523124323
20230818113222
20230914180801
20231027141322
20231114161723
20231117164230
20240115144230
20240214120130
20240306115329
20240314092811
20240427152123
20240612123726
20240729123726
20240802193726
20240806073726
20241009103726
20250717082212
20250731150234
20250804100000
20250901200500
20250903112500
20250904133000
20250925093508
20251007112900
20251104100000
20251111201300
20251201000000
20260115000000
20260121000000
20260219120000
20260302000000
20260625000000
20260821000000
20260821010000
20260824000000
20260824000001
20260831180000
\.


--
-- Data for Name: scim_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.scim_tokens (id, sso_provider_id, token_hash, prefix, created_at, expires_at, revoked_at, last_used_at) FROM stdin;
\.


--
-- Data for Name: scim_users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.scim_users (id, sso_provider_id, user_id, resource, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sessions (id, user_id, created_at, updated_at, factor_id, aal, not_after, refreshed_at, user_agent, ip, tag, oauth_client_id, refresh_token_hmac_key, refresh_token_counter, scopes) FROM stdin;
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sso_domains (id, sso_provider_id, domain, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.sso_providers (id, resource_id, created_at, updated_at, disabled) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.users (instance_id, id, aud, role, email, encrypted_password, email_confirmed_at, invited_at, confirmation_token, confirmation_sent_at, recovery_token, recovery_sent_at, email_change_token_new, email_change, email_change_sent_at, last_sign_in_at, raw_app_meta_data, raw_user_meta_data, is_super_admin, created_at, updated_at, phone, phone_confirmed_at, phone_change, phone_change_token, phone_change_sent_at, email_change_token_current, email_change_confirm_status, banned_until, reauthentication_token, reauthentication_sent_at, is_sso_user, deleted_at, is_anonymous) FROM stdin;
\.


--
-- Data for Name: webauthn_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.webauthn_challenges (id, user_id, challenge_type, session_data, created_at, expires_at) FROM stdin;
\.


--
-- Data for Name: webauthn_credentials; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY auth.webauthn_credentials (id, user_id, credential_id, public_key, attestation_type, aaguid, sign_count, transports, backup_eligible, backed_up, friendly_name, created_at, updated_at, last_used_at) FROM stdin;
\.


--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin (admin_id, name, email, password_hash, account_status, updated_timestamp, created_timestamp, token_version) FROM stdin;
1	NexStep Admin	admin@nexstep.com	$2b$12$tTwaWxur8krUJsMVPAMLE.daiHAuPrYhs6/M62FuvzidZtzG.k3z.	active	2026-08-16 22:09:43.582676	2026-08-16 22:09:43.582676	309691674f604151a85af0959acd6839
496	Vivek	sparrowspidey	$2b$12$DX1Qrauc0vQ8Jogctv8jguLXHvqbuVD8JCPcjluWvzcG/wTPyq3Ca	active	\N	\N	\N
497	vivek	sparrowspidey@gmail.com	$2b$12$cO1JLS0NptzlZeyYK9gesu.kfgIW/O14ehTiPR.25UfXyxKm3cW5W	active	\N	\N	9b191ab246dc40d1bc6e439b8478372f
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
f4c8a92d71e3
\.


--
-- Data for Name: auditlog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auditlog (audit_id, admin_id, action_type, entity_type, entity_id, description, old_value, new_value, created_at) FROM stdin;
1	1	APPROVED	OfficialNotification	1	Admin approved the extracted notification information.	PENDING	APPROVED	2026-08-16 22:13:37.509603
\.


--
-- Data for Name: chathistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chathistory (chat_id, student_id, user_message, ai_response, created_at) FROM stdin;
1	1	Which exams am I eligible for?	Based on your current profile, NexStep has evaluated the supported examinations in your account.	2026-08-16 22:13:24.976511
2	2	When is the JEE Main application deadline?	The application deadline available in NexStep is November 30, 2025.	2026-08-16 22:13:24.976511
\.


--
-- Data for Name: conducting_body; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.conducting_body (body_id, name, main_website, description, logo_url) FROM stdin;
1	UPSC	https://www.upsc.gov.in/	UPSC stands for the Union Public Service Commission. It is the central agency in India that chooses officers for high-level government jobs, including the Indian Administrative Service (IAS), Indian Police Service (IPS), and Indian Foreign Service (IFS)	https://www.upsc.gov.in/sites/all/themes/upsc/images/logo.png
3	NTA	https://www.nta.ac.in/	National Testing Agency conducts entrance and eligibility examinations across India.	https://www.nta.ac.in/img/nta-logo.png
4	SSC	https://ssc.gov.in/	Staff Selection Commission conducts recruitment examinations for various posts in the Government of India.	https://ssc.gov.in/Site/Upload/SSCLogo.png
6	Phase 8 Body 9329f063c88943e9875b0865ceda48cb	https://example.com	Phase 8 test conducting body	\N
7	Phase 8 Body 9a30c1cfd68f46c9a2730bb98ceba80e	https://example.com	Phase 8 test conducting body	\N
8	Phase 8 Body 07c86ab934284d57aead3e35bc3a3aed	https://example.com	Phase 8 test conducting body	\N
9	Phase 8 Body 4ab8be2b88684f0bbe5b451be70b485d	https://example.com	Phase 8 test conducting body	\N
10	Phase 8 Body ad3fa0020da04548bd0f4219609d6c75	https://example.com	Phase 8 test conducting body	\N
11	Phase 8 Body 1b10ff1c702d49d89761382a9642168f	https://example.com	Phase 8 test conducting body	\N
12	Phase 8 Body 0e1d3f68cd7e47eba165ce496a864a39	https://example.com	Phase 8 test conducting body	\N
13	Phase 8 Body 70cc337804fb4c3e91d632b575112904	https://example.com	Phase 8 test conducting body	\N
15	Phase 8 Body db2e2c7a12ea467eb6710d4efec20f27	https://example.com	Phase 8 test conducting body	\N
16	Phase 8 Body 07046be438cb41ff97897555e1da6937	https://example.com	Phase 8 test conducting body	\N
17	Phase 8 Body 27124a7205a64f3b9a863dc64a720c40	https://example.com	Phase 8 test conducting body	\N
18	Phase 8 Body f5c45798040440a7a1959889ef8f4b21	https://example.com	Phase 8 test conducting body	\N
19	Phase 8 Body 2086ae1d7844457f837b546cfdb4acd6	https://example.com	Phase 8 test conducting body	\N
20	Phase 8 Body e02e08211c2146d09b97e4f56acf8fb6	https://example.com	Phase 8 test conducting body	\N
21	Phase 8 Body 47dfcc7b104943a982366af341495fc8	https://example.com	Phase 8 test conducting body	\N
23	Phase 8 Body a32d4795ecd74e7285769a9df2fd8236	https://example.com	Phase 8 test conducting body	\N
24	Phase 8 Body 9db0ecdb53164af7a433df9cbe0f2ce2	https://example.com	Phase 8 test conducting body	\N
25	Phase 8 Body e9449e7da64c462c83b6eec5e81015a4	https://example.com	Phase 8 test conducting body	\N
26	Phase 8 Body 76d599e383b34c5dbea095c327a9cbf6	https://example.com	Phase 8 test conducting body	\N
27	Phase 8 Body 1f5db53bdf29489486fd4920a43efd40	https://example.com	Phase 8 test conducting body	\N
28	Phase 8 Body 6d5bb3eda28c4df68d94e5a8b6ec4c92	https://example.com	Phase 8 test conducting body	\N
29	Phase 8 Body 938a21d18d7e40a8b61c4ffe6c9f1465	https://example.com	Phase 8 test conducting body	\N
30	Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)	https://gate2027ib.iitm.ac.in/	\N	\N
32	Staff Selection Commission	https://ssc.gov.in/	\N	\N
33	Indian Institutes of Management	https://cdn.digialm.com/	\N	\N
34	Union Public Service Commission	https://www.upsc.gov.in/	\N	\N
35	Railway Recruitment Board (RRB)	https://rrbsecunderabad.gov.in/	\N	\N
36	Union Public Service Commission (UPSC)	https://www.upsc.gov.in/	\N	\N
37	Indian Institute of Science and Indian Institutes of Technology	https://gate2027ib.iitm.ac.in/	\N	\N
\.


--
-- Data for Name: education; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.education (education_id, student_id, qualification, course, specialization, college, university, cgpa, percentage, year_of_passing, current_year, is_current, institution, year_of_study_label, is_higher_qualification) FROM stdin;
1	1	B.Tech	B.Tech	CSE	ABC Engineering College	JNTU Hyderabad	8.40	\N	\N	3	t	\N	\N	\N
2	1	12th	Intermediate	\N	ABC Junior College	Telangana Board	\N	89.00	2022	\N	f	\N	\N	\N
3	2	B.Tech	B.Tech	ECE	XYZ Engineering College	JNTU Kakinada	7.20	\N	\N	4	t	\N	\N	\N
4	2	12th	Intermediate	\N	XYZ Junior College	Andhra Pradesh Board	\N	91.00	2021	\N	f	\N	\N	\N
5	3	B.Tech	B.Tech	CSE	PQR Institute of Technology	VTU	6.40	\N	\N	2	t	\N	\N	\N
6	3	12th	Intermediate	\N	PQR Junior College	Karnataka Board	\N	86.00	2023	\N	f	\N	\N	\N
182	126	Bachelor's	\N	cse	\N	\N	5.30	\N	\N	3	t	iiitk	3rd Year	\N
183	126	12th / Senior Secondary	\N		\N	\N	\N	\N	\N	\N	f		\N	\N
126	125	Bachelor's	\N	CYBER	\N	\N	8.00	80.00	\N	3	t	IIT PALAKKAD	3rd Year	\N
127	125	12th / Senior Secondary	\N		\N	\N	\N	\N	\N	\N	f		\N	\N
15	54	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
16	57	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
17	58	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
18	59	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
19	60	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
20	61	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
21	62	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
22	63	BTech	\N	Computer Science	\N	\N	8.50	\N	2026	4	t	Test College	Final Year	f
23	64	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
24	65	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
25	66	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
26	67	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
27	68	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
28	69	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
29	70	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
30	71	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
31	72	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
32	73	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
33	74	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
34	75	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
35	76	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
36	77	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
37	78	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
38	79	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
39	80	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
40	81	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
41	82	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
42	83	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
43	84	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
44	85	B.Tech	\N	CSE	\N	\N	8.00	\N	\N	3	t	Phase 8 Test College	3rd Year	f
45	86	B.Tech	\N	CSE	\N	\N	8.40	\N	\N	3	t	\N	\N	\N
46	91	B.Tech	\N	CSE	\N	\N	8.40	\N	\N	3	t	\N	\N	\N
47	106	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
48	107	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
49	108	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
50	109	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
208	111	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
209	112	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
210	113	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
211	114	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
212	115	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
213	116	BTech	\N	CSE	\N	\N	8.00	\N	\N	3	t	\N	\N	\N
83	123	Bachelor's	\N	CSE	\N	\N	8.50	\N	\N	\N	t	Test College	3	\N
84	124	Bachelor's	\N	CSE	\N	\N	8.00	80.00	\N	3	t	IIIT KOTTAYAM	3rd Year	\N
85	124	12th / Senior Secondary	\N		\N	\N	\N	\N	\N	\N	f		\N	\N
214	127	Bachelor's	\N	Cyber Security 	\N	\N	6.02	\N	\N	3	t	IIITKottayam	3rd Year	\N
215	127	12th / Senior Secondary	\N		\N	\N	\N	\N	\N	\N	f		\N	\N
216	128	Bachelor's	\N	CSE	\N	\N	7.13	\N	\N	3	t	IIIT Kottayam	3rd Year	\N
217	128	12th / Senior Secondary	\N		\N	\N	\N	\N	\N	\N	f		\N	\N
218	129	Bachelor's	\N	CSE	\N	\N	5.54	\N	\N	3	t	IIIT Kottayam	3rd Year	\N
219	129	12th / Senior Secondary	\N		\N	\N	\N	\N	\N	\N	f		\N	\N
220	133	Bachelor's	\N	\N	\N	\N	\N	\N	\N	\N	t	iii	\N	\N
\.


--
-- Data for Name: eligibilityattribute; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eligibilityattribute (attribute_id, attribute_name, source_table, source_column, data_type, description) FROM stdin;
1	CGPA	education	cgpa	numeric	Student CGPA
2	Percentage	education	percentage	numeric	Student percentage
3	Specialization	education	specialization	text	Student branch or specialization
4	Date of Birth	student	date_of_birth	date	Student date of birth
5	Nationality	student	nationality	text	Student nationality
6	State	student	state	text	Student state
7	Educational Qualification	education	qualification	text	Student educational qualification or degree
8	Work Experience	student	work_experience	text	Student work experience requirement
\.


--
-- Data for Name: eligibilityrule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eligibilityrule (rule_id, group_id, attribute_id, operator, value) FROM stdin;
1026	653	5	=	India
1030	656	2	>=	45
1031	657	7	=	Bachelor's
1032	657	7	=	Other
1033	659	5	=	India
1049	671	5	=	India
1050	671	5	=	Nepal
1051	671	5	=	Bhutan
1052	671	5	=	Indian origin (from Pakistan, Burma, Sri Lanka, East African Countries of Kenya, Uganda, United Republic of Tanzania (Formerly Tanganyika and Zanzibar), Zambia, Malawi, Zaire, Ethiopia and Vietnam)
\.


--
-- Data for Name: eligibilityrulegroup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.eligibilityrulegroup (group_id, notification_id, group_number, logical_operator, parent_group_id) FROM stdin;
652	1076	1	AND	\N
653	1076	1	OR	652
656	1080	1	AND	\N
657	1080	1	OR	656
658	1081	1	AND	\N
659	1081	1	OR	658
670	1082	1	AND	\N
671	1082	1	OR	670
\.


--
-- Data for Name: exam; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exam (exam_id, body_id, name, type, description, off_exam_page, status) FROM stdin;
42	30	GATE 2027	Competitive	\N	https://gate2027ib.iitm.ac.in/GATE2027-IB.pdf	ACTIVE
46	33	Common Admission Test 2026 (CAT 2026)	Competitive	\N	https://cdn.digialm.com/per/g06/pub/32842/EForms/image/CAT2026/CAT_2026_Information_Bulletin_26-07-26.pdf	ACTIVE
47	34	Civil Services Examination 2026	Competitive	\N	https://www.upsc.gov.in/sites/default/files/Notif-CSP-2026-Engl-060226Rev.pdf	ACTIVE
48	32	SSC Combined Graduate Level (CGL) 2026	Competitive	\N	https://ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_cgl_2026.pdf	ACTIVE
49	35	CEN No. 07/2025 NTPC (Under Graduate)	Competitive	\N	https://rrbsecunderabad.gov.in	ACTIVE
50	36	Civil Services Examination 2025	Competitive	\N	https://www.upsc.gov.in/sites/default/files/Notif-CSP-2025-Engl-220125.pdf	ACTIVE
51	34	Engineering Services (Preliminary) Examination, 2025	Competitive	\N	https://www.upsc.gov.in/exams-related-info/exam-notification/archives	ACTIVE
\.


--
-- Data for Name: examdate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.examdate (exam_date_id, notification_id, start_date, end_date) FROM stdin;
322	1076	2027-02-06	2027-02-06
323	1076	2027-02-13	2027-02-13
324	1076	2027-02-20	2027-02-20
325	1076	2027-02-21	2027-02-21
327	1080	2026-11-29	2026-11-29
328	1081	2026-05-24	2026-05-24
330	1083	2026-05-07	2026-05-07
331	1083	2026-05-08	2026-05-08
332	1083	2026-05-09	2026-05-09
333	1083	2026-06-13	2026-06-13
334	1083	2026-06-14	2026-06-14
335	1083	2026-06-16	2026-06-16
336	1083	2026-06-17	2026-06-17
337	1083	2026-06-18	2026-06-18
338	1083	2026-06-19	2026-06-19
339	1083	2026-06-20	2026-06-20
340	1083	2026-06-21	2026-06-21
346	1082	2026-08-01	2026-08-01
347	1085	2025-01-11	2025-01-11
348	1085	2025-02-09	2025-02-09
349	1085	2025-04-27	2025-04-27
350	1085	2025-05-25	2025-05-25
351	1085	2025-06-08	2025-06-08
352	1085	2025-06-20	2025-06-20
353	1085	2025-07-20	2025-07-20
354	1085	2025-08-03	2025-08-03
355	1085	2025-08-10	2025-08-10
356	1086	2025-01-11	2025-01-11
357	1086	2025-02-09	2025-02-09
358	1086	2025-04-13	2025-04-13
359	1086	2025-04-27	2025-04-27
360	1086	2025-05-25	2025-05-25
361	1086	2025-06-08	2025-06-08
362	1086	2025-06-20	2025-06-20
363	1086	2025-07-20	2025-07-20
364	1086	2025-08-03	2025-08-03
365	1087	2027-02-06	2027-02-07
366	1087	2027-02-13	2027-02-14
367	1087	2027-02-20	2027-02-21
368	1088	2027-02-06	2027-02-06
369	1088	2027-02-07	2027-02-07
370	1088	2027-02-13	2027-02-13
371	1088	2027-02-14	2027-02-14
372	1089	2027-02-06	2027-02-07
373	1089	2027-02-13	2027-02-14
374	1089	2027-02-20	2027-02-21
375	1090	2027-02-06	2027-02-07
376	1090	2027-02-13	2027-02-14
377	1090	2027-02-20	2027-02-21
\.


--
-- Data for Name: extractionhistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extractionhistory (extraction_id, notification_id, extraction_type, source_pdf_path, extracted_content, ai_summary, change_detected, change_details, extraction_status, created_at) FROM stdin;
209	1076	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-09-27", "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-06"}, {"start_date": "2027-02-07", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-13"}, {"start_date": "2027-02-14", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-20"}, {"start_date": "2027-02-21", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "null", "work_experience": null, "other_requirements": ["Candidates must use only the on-screen virtual calculator provided for their calculations.", "Candidates are allowed to appear for one or two test papers only."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "null"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "warning", "code": "unverified-quote", "field": "Exam date", "message": "Exam date: the supporting quote could not be found in the document."}, {"severity": "info", "code": "start-tba", "field": "Application start date", "message": "The application start date is listed as 'to be announced' in the document."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 74.9, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 21, 25, 26, 32, 33, 36, 38], "context_tokens": 5733, "passages": 26}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6651, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 18.2}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 3814, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 30.2s for 3814 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='User Safety: safe', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6119, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 32.3s for 6119 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for EligibilityDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='We need to extract who m...nly through the GATE 20', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	GATE 2027 conducted by Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs). Exam: 2027-02-06, 2027-02-07, 2027-02-13, 2027-02-14, 2027-02-20, 2027-02-21. 1 eligibility rule(s) extracted.	f	Check again the nationality eligibility	REJECTED	2026-09-30 14:51:24.320061
210	1076	RETRY_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-09-27", "application_start_date": "2026-09-02", "application_end_date": "2026-10-05", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": ["Candidates must use only the on-screen virtual calculator provided for their calculations.", "Candidates are allowed to appear for one or two test papers only."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application start date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 12, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 1)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 2)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 3)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-12. Only the regular deadline is stored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": true, "seconds": 83.5, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 21, 25, 26, 32, 33, 36, 38], "context_tokens": 5733, "passages": 26}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6651, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 3814, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 24.8}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6148, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 48.9s for 6148 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	Retry after administrator feedback. GATE 2027 conducted by Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs). Applications: 2026-09-02 to 2026-10-05. Exam: 2027-02-06 to 2027-02-07, 2027-02-13 to 2027-02-14, 2027-02-20 to 2027-02-21. 1 eligibility rule(s) extracted.	f	\N	APPROVED	2026-09-30 14:54:09.385553
222	1083	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Citi-Intimation-Slip-Notice-CEN-07-2025-English.pdf	{"extraction": {"exam_information": {"exam_name": "CEN No. 07/2025 NTPC (Under Graduate)", "conducting_body": "Railway Recruitment Board (RRB)", "release_date": null, "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2026-05-07", "end_date": "2026-05-07"}, {"start_date": "2026-05-08", "end_date": "2026-05-08"}, {"start_date": "2026-05-09", "end_date": "2026-05-09"}, {"start_date": "2026-06-13", "end_date": "2026-06-13"}, {"start_date": "2026-06-14", "end_date": "2026-06-14"}, {"start_date": "2026-06-16", "end_date": "2026-06-16"}, {"start_date": "2026-06-17", "end_date": "2026-06-17"}, {"start_date": "2026-06-18", "end_date": "2026-06-18"}, {"start_date": "2026-06-19", "end_date": "2026-06-19"}, {"start_date": "2026-06-20", "end_date": "2026-06-20"}, {"start_date": "2026-06-21", "end_date": "2026-06-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": null, "work_experience": null, "other_requirements": ["Aadhaar biometric must be updated after attaining age 15 years if enrolled before age 15."]}}, "eligibility_rules": {"rule_groups": []}}, "evidence": [{"chunk_number": 1, "page_numbers": [1], "source_text": "CEN No. 07/2025 NTPC (Under Graduate)", "field": "Exam name", "verified": false, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Conducting body", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "1. The Link for viewing the Exam City & Date and downloading of Travel Authority for SC/ST candidates is live on the official websites of all RRBs. Candidates can view their exam city 10 days before the exam date which is scheduled on 07.05.2026, 08.05.2026, 09.05.2026, 13.06.2026, 14.06.2026, 16.06.2026, 17.06.2026, 18.06.2026, 19.06.2026, 20.06.2026 & 21.06.2026 respectively.\\n2. Downloading of E-call letters will start 4 days prior to exam dates mentioned in the Exam City & Date intimation Link.\\n3. Aadhaar Linked Biometric Authentication of Candidates will be done in the Exam Centre prior to entry in the Exam Hall. Candidates are required to bring their original Aadhaar Card or printout of", "field": "Exam date", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "5. Candidates should also comply with UIDAI instructions related to updation of Aadhaar, i.e., if enrolled before age 15, biometric should be updated after attaining age 15 years.\\n6. In case of any queries or clarification needed the Helpdesk contact No. 9513166169", "field": "Requirement: Aadhaar biometric must be updated after ", "verified": true, "section": "CBT-I of CEN No. 07/2025 NTPC (Under Graduate)"}], "conflicts": [], "issues": [{"severity": "error", "code": "validation", "field": null, "message": "Eligibility rules must contain at least one rule group."}, {"severity": "warning", "code": "unverified-quote", "field": "Exam name", "message": "Exam name: the supporting quote could not be found in the document."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 1, "characters": 2316, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 15.9, "topics": {"identity": {"pages": [1], "context_tokens": 601, "passages": 3}, "dates": {"pages": [1], "context_tokens": 374, "passages": 1}, "eligibility": {"pages": [1], "context_tokens": 472, "passages": 2}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 1599, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 2068, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "groq", "estimated_tokens": 2999, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 10.7}]}]}}	CEN No. 07/2025 NTPC (Under Graduate) conducted by Railway Recruitment Board (RRB). Exam: 2026-05-07, 2026-05-08, 2026-05-09, 2026-06-13, 2026-06-14, 2026-06-16, 2026-06-17, 2026-06-18, 2026-06-19, 2026-06-20, 2026-06-21. 0 eligibility rule(s) extracted. 1 issue(s) need review before approval.	f	\N	PENDING	2026-10-07 11:03:04.858032
221	1082	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Notice_of_adv_cgl_2026.pdf	{"extraction": {"exam_information": {"exam_name": "SSC Combined Graduate Level (CGL) 2026", "conducting_body": "Staff Selection Commission", "release_date": null, "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2026-08-01", "end_date": "2026-08-01"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India, Nepal, Bhutan, Indian origin (from Pakistan, Burma, Sri Lanka, East African Countries of Kenya, Uganda, United Republic of Tanzania (Formerly Tanganyika and Zanzibar), Zambia, Malawi, Zaire, Ethiopia and Vietnam)", "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}, {"attribute": "Nationality", "operator": "=", "value": "Nepal"}, {"attribute": "Nationality", "operator": "=", "value": "Bhutan"}, {"attribute": "Nationality", "operator": "=", "value": "Indian origin (from Pakistan, Burma, Sri Lanka, East African Countries of Kenya, Uganda, United Republic of Tanzania (Formerly Tanganyika and Zanzibar), Zambia, Malawi, Zaire, Ethiopia and Vietnam)"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 4, "page_numbers": [1], "source_text": "Training,\\nStaff Selection Commission,", "field": "Conducting body", "verified": true, "section": "Department of Personnel and"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Qualification: Bachelor's", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must have been born not earli", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must have been born not earli", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must have been born not earli", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must have been born not earli", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "warning", "code": "name-from-admin", "field": "Exam name", "message": "The exam name was not found in the document; the administrator's entry was used."}, {"severity": "warning", "code": "unverified-quote", "field": "Exam date", "message": "Exam date: the supporting quote could not be found in the document."}, {"severity": "warning", "code": "date-not-in-document", "field": "Exam date", "message": "Exam date: 2026-12-01, 2026-12-01 does not appear in the document; range dropped."}, {"severity": "warning", "code": "qualification-unverified", "field": "Qualification: Bachelor's", "message": "Qualification: Bachelor's: the supporting quote could not be located in the document; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Candidates must have been born not earli", "message": "Requirement: Candidates must have been born not earli: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 132, "characters": 213262, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 158.4, "topics": {"identity": {"pages": [1, 4, 5, 12, 16, 19, 24, 29, 36, 38, 40, 41, 48, 53, 81, 118, 119, 120], "context_tokens": 5736, "passages": 24}, "dates": {"pages": [1, 7, 8, 17, 19, 48, 49, 50, 51, 59, 64, 65, 66, 67, 71, 72, 73], "context_tokens": 5029, "passages": 21}, "eligibility": {"pages": [6, 7, 8, 9, 10, 16, 17, 37, 41, 50, 61, 71, 118], "context_tokens": 4192, "passages": 19}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6647, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 22.6}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 6644, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 54.2s for 6644 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6651, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Groq failed to generate a response: BadRequestError('Error code: 400 - {\\\\'error\\\\': {\\\\'message\\\\': \\"max completion tokens reached before generating a valid document: the output was truncated to fit max_completion_tokens and is missing required content. Increase max_completion_tokens. See \\\\'failed_gene", "waited_s": 24.7}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for EligibilityDraft\\n  Invalid JSON: EOF while parsing a string at line 7 column 53 [type=json_invalid, input_value='{\\\\n  \\"age_limits\\": [\\\\n  ...5. Age limit (As on 01-', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_in", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	SSC Combined Graduate Level (CGL) 2026 conducted by Staff Selection Commission. Exam: 2026-08-01. 4 eligibility rule(s) extracted.	f	\N	APPROVED	2026-10-07 11:02:01.101294
223	1084	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Notif-CSP-2025-Engl-220125.pdf	{"extraction": {"exam_information": {"exam_name": "Civil Services Examination 2025", "conducting_body": "Union Public Service Commission (UPSC)", "release_date": "2025-01-22", "application_start_date": null, "application_end_date": null, "exam_dates": [], "eligibility": {"minimum_age": 21, "maximum_age": 32, "educational_qualification": null, "nationality": "India, Nepal, Bhutan", "work_experience": null, "other_requirements": ["Age maximum 35 years for Defence Services Personnel disabled in operations (as on 2025-08-01)"]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [{"attribute": "Date of Birth", "operator": "<=", "value": "2004-08-01"}, {"attribute": "Date of Birth", "operator": ">=", "value": "1992-08-02"}], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}, {"attribute": "Nationality", "operator": "=", "value": "Nepal"}, {"attribute": "Nationality", "operator": "=", "value": "Bhutan"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE No 05/2025-CSP DATE: 22.01.2025\\n(LAST DATE FOR RECEIPT OF ONLINE APPLICATIONS: 11.02.2025 of CIVIL SERVICES EXAMINATION,\\n2025)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Exam name", "verified": true, "section": "Document"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE No 05/2025-CSP DATE: 22.01.2025\\n(LAST DATE FOR RECEIPT OF ONLINE APPLICATIONS: 11.02.2025 of CIVIL SERVICES EXAMINATION,\\n2025)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Conducting body", "verified": true, "section": "Document"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE No 05/2025-CSP DATE: 22.01.2025\\n(LAST DATE FOR RECEIPT OF ONLINE APPLICATIONS: 11.02.2025 of CIVIL SERVICES EXAMINATION,\\n2025)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 35, "page_numbers": [11], "source_text": "(1) A candidate must have attained the age of 21 years and must not have attained the age of 32\\nyears on the 1st of August, 2025 i.e., the candidate must have been born not earlier than 2nd August,\\n1993 and not later than 1st August, 2004.\\n(2) The upper age-limit prescribed above will be relaxable:\\n(a) up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled\\nTribe;\\n(b) up to a maximum of three years in the case of candidates belonging to Other Backward\\nClasses who are eligible to avail of reservation applicable to such candidates;\\n(c) up to a maximum of three years in the case of Defence Services Personnel, disabled in\\noperations during hostilities with any fo", "field": "Age limit (Defence Services Personnel disabled in operations)", "verified": true, "section": "Age Limits:"}, {"chunk_number": 35, "page_numbers": [11], "source_text": "(1) A candidate must have attained the age of 21 years and must not have attained the age of 32\\nyears on the 1st of August, 2025 i.e., the candidate must have been born not earlier than 2nd August,\\n1993 and not later than 1st August, 2004.\\n(2) The upper age-limit prescribed above will be relaxable:\\n(a) up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled\\nTribe;\\n(b) up to a maximum of three years in the case of candidates belonging to Other Backward\\nClasses who are eligible to avail of reservation applicable to such candidates;\\n(c) up to a maximum of three years in the case of Defence Services Personnel, disabled in\\noperations during hostilities with any fo", "field": "Age limit (minimum)", "verified": true, "section": "Age Limits:"}, {"chunk_number": 35, "page_numbers": [11], "source_text": "(1) A candidate must have attained the age of 21 years and must not have attained the age of 32\\nyears on the 1st of August, 2025 i.e., the candidate must have been born not earlier than 2nd August,\\n1993 and not later than 1st August, 2004.\\n(2) The upper age-limit prescribed above will be relaxable:\\n(a) up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled\\nTribe;\\n(b) up to a maximum of three years in the case of candidates belonging to Other Backward\\nClasses who are eligible to avail of reservation applicable to such candidates;\\n(c) up to a maximum of three years in the case of Defence Services Personnel, disabled in\\noperations during hostilities with any fo", "field": "Age limit (maximum)", "verified": true, "section": "Age Limits:"}, {"chunk_number": 39, "page_numbers": [12], "source_text": "A candidate must hold a Graduate degree of any of the Universities incorporated by an Act of the\\ncentral or State Legislature in India or other educational institutions established by an Act of Parliament or\\ndeclared to be deemed as a University under Section 3 of the University Grants Commission Act, 1956 or\\npossess an equivalent qualification.\\nNote-I: Candidates who have appeared at a qualifying examination the passing of which would render them\\neducationally qualified for the Commission’s Examination but have not been informed of the result as also\\nthe candidates who intend to appear at such a qualifying examination will also be eligible for admission to\\nthe written part of Civil Services", "field": "Qualification: Bachelor's", "verified": true, "section": "Minimum Educational Qualification:"}, {"chunk_number": 33, "page_numbers": [10], "source_text": "(1)\\nFor the Indian Administrative Service, the Indian Foreign Service and the Indian Police Service, a\\ncandidate must be a citizen of India.\\n(2)\\nFor other services, a candidate must be either:—\\n(a)\\na citizen of India, or\\n(b)\\na subject of Nepal, or\\n(c)\\na subject of Bhutan, or\\n(d)\\na Tibetan refugee who came over to India before 1st January, 1962 with the intention of permanently\\nsettling in India, or\\n(e)\\na person of Indian origin who has migrated from Pakistan, Burma, Sri Lanka, East African countries\\nof Kenya, Uganda, the United Republic of Tanzania, Zambia, Malawi, Zaire, Ethiopia and Vietnam\\nwith the intention of permanently settling in India.\\nProvided that a candidate belonging to categori", "field": "Nationality", "verified": true, "section": "Nationality"}, {"chunk_number": 29, "page_numbers": [9], "source_text": "The Commission shall also provide a window of 15 (Fifteen) days from the date of declaration of\\nresult of written part of Civil Services (Main) Examination to the candidates qualified for Personality\\nTest/Interview. The candidates as per Note 1 below Rule 6 of CSE, 2025 shall be required to update their\\ndetails/educational qualification status (whether appearing/appeared) and to produce/upload the proof of\\npassing of the requisite qualifying examination at the specified module/portal, failing which such candidates\\nwill not be allowed to appear in the Personality Test/Interview and his/her candidature will be liable to be\\ncancelled.\\nNote: In this period, all the candidates qualified for Perso", "field": "Requirement: Proof of passing the qualifying examinat", "verified": true, "section": "B.3."}], "conflicts": [{"field": "Age limit (maximum)", "options": [{"value": "32 years as on 2025-08-01", "source": "must not have attained the age of 32 years on the 1st of August, 2025", "pages": []}, {"value": "37 years as on 2025-08-01", "source": "up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled Tribe", "pages": []}, {"value": "35 years as on 2025-08-01", "source": "up to a maximum of three years in the case of candidates belonging to Other Backward Classes", "pages": []}, {"value": "37 years as on 2025-08-01", "source": "up to a maximum of five years in the case of ex‑servicemen ... who have rendered at least five years Military Service", "pages": []}], "chosen": "32 years", "reason": "Provisionally using the first general limit found; verify against the document."}], "issues": [{"severity": "warning", "code": "unverified-quote", "field": "Exam date", "message": "Exam date: the supporting quote could not be found in the document."}, {"severity": "warning", "code": "date-unverified", "field": "Exam date", "message": "Exam date: the supporting quote could not be located in the document; range dropped."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Qualification: Bachelor's", "message": "Qualification: Bachelor's: the extracted qualification is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Tibetan refugee (pre‑1 Jan 1962)' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Pakistan' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Burma' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Sri Lanka' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Kenya' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Uganda' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Tanzania' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Zambia' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Malawi' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Zaire' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Ethiopia' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Nationality", "message": "Nationality 'Indian origin from Vietnam' is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "value-quote-mismatch", "field": "Requirement: Proof of passing the qualifying examinat", "message": "Requirement: Proof of passing the qualifying examinat: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "1 struck-out (superseded) values in the document were ignored, e.g. '' (p.153)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 157, "characters": 369313, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 137.4, "topics": {"identity": {"pages": [1, 2, 3, 5, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 28, 34, 120, 121, 139, 141, 156], "context_tokens": 5735, "passages": 31}, "dates": {"pages": [1, 2, 3, 4, 11, 14, 15, 16, 18, 19, 21, 153], "context_tokens": 4736, "passages": 24}, "eligibility": {"pages": [1, 9, 10, 11, 12, 13, 16, 20, 21, 27, 28, 72, 157], "context_tokens": 4168, "passages": 17}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6640, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 6335, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 31.6s for 6335 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "groq", "estimated_tokens": 6633, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}]}}	Civil Services Examination 2025 conducted by Union Public Service Commission (UPSC). 5 eligibility rule(s) extracted.	f	\N	PENDING	2026-10-07 12:22:14.462617
224	1085	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\RevisedIIICalendar2025-Engl-160126.pdf	{"extraction": {"exam_information": {"exam_name": "Engineering Services (Preliminary) Examination, 2025", "conducting_body": "Union Public Service Commission", "release_date": "2024-09-18", "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2025-01-11", "end_date": "2025-01-11"}, {"start_date": "2025-02-09", "end_date": "2025-02-09"}, {"start_date": "2025-04-27", "end_date": "2025-04-27"}, {"start_date": "2025-05-25", "end_date": "2025-05-25"}, {"start_date": "2025-06-08", "end_date": "2025-06-08"}, {"start_date": "2025-06-20", "end_date": "2025-06-20"}, {"start_date": "2025-07-20", "end_date": "2025-07-20"}, {"start_date": "2025-08-03", "end_date": "2025-08-03"}, {"start_date": "2025-08-10", "end_date": "2025-08-10"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": null, "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": []}}, "evidence": [{"chunk_number": 2, "page_numbers": [1], "source_text": "04.2025; (Sunday) | 1 DAY\\n7.; 8. | Civil Services (Preliminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01.2025 | 21.02.2025 % | 25.05.2025; (Sunday) | 1 DAY\\n9. | Engineering Services (Preliminary) Examination, 2025 | 18.09.2024 | 22.11.2024* | 08.06.2025; (Sunday) | 1 DAY\\n10. | Reserved for UPSC RT/ Examination | 14.06.2025; (Saturday) | 2 DAYS\\n11. | I.E.S./I.S.S. Examination, 2025 | 12.02.2025 | 04.03.2025 | 20.06.2025; (Friday) | 3 DAYS\\n12. | Combined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical S", "field": "Exam name", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Conducting body", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "iminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01.2025 | 21.02.2025 % | 25.05.2025; (Sunday) | 1 DAY\\n9. | Engineering Services (Preliminary) Examination, 2025 | 18.09.2024 | 22.11.2024* | 08.06.2025; (Sunday) | 1 DAY\\n10. | Reserved for UPSC RT/ Examination | 14.06.2025; (Saturday) | 2 DAYS\\n11. | I.E.S./I.S.S. Examination, 2025 | 12.02.2025 | 04.03.2025 | 20.06.2025; (Friday) | 3 DAYS\\n12. | Combined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical Services Examination, 2025 | 19.02.2025 | 11.03.2025 | 2", "field": "Release date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "ECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | 13.04.2025; (Sunday) | 1 DAY\\n7.; 8. | Civil Services (Preli", "field": "Exam date (S.O. Grade-B LDCE, 2024)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "ions | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | 13.04.2025; (Sunday) | 1 DAY\\n7.; 8. | Civil Services (Preliminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01", "field": "Exam date (Combined Geo-Scientist (Preliminary) Examination, 2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "| 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | 13.04.2025; (Sunday) | 1 DAY\\n7.; 8. | Civil Services (Preliminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01.2025 | 21.02.2025 % | 25.05.2025; (Sunday) | 1 DAY\\n9. | Engineering Services (Prelim", "field": "Exam date (CISF AC(EXE) LDCE-2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "25 | 11.12.2024 | 31.12.2024 | 13.04.2025; (Sunday) | 1 DAY\\n7.; 8. | Civil Services (Preliminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01.2025 | 21.02.2025 % | 25.05.2025; (Sunday) | 1 DAY\\n9. | Engineering Services (Preliminary) Examination, 2025 | 18.09.2024 | 22.11.2024* | 08.06.2025; (Sunday) | 1 DAY\\n10. | Reserved for UPSC RT/ Examination | 14.06.2025; (Saturday) | 2 DAYS\\n11. | I.E.S./I.S.S. Examination, 2025 | 12.02.2025 | 04.03.2025 | 20.06.2025; (Friday) | 3 DAYS\\n12. | Combined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday)", "field": "Exam date (Civil Services (Preliminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": " Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01.2025 | 21.02.2025 % | 25.05.2025; (Sunday) | 1 DAY\\n9. | Engineering Services (Preliminary) Examination, 2025 | 18.09.2024 | 22.11.2024* | 08.06.2025; (Sunday) | 1 DAY\\n10. | Reserved for UPSC RT/ Examination | 14.06.2025; (Saturday) | 2 DAYS\\n11. | I.E.S./I.S.S. Examination, 2025 | 12.02.2025 | 04.03.2025 | 20.06.2025; (Friday) | 3 DAYS\\n12. | Combined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical Services Examination, 2025 | 19.02.2025 | 11.03.2025 | 20.07.2025; (Sunday) | 1 DAY", "field": "Exam date (Engineering Services (Preliminary) Examination, 2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "es (Preliminary) Examination, 2025 | 18.09.2024 | 22.11.2024* | 08.06.2025; (Sunday) | 1 DAY\\n10. | Reserved for UPSC RT/ Examination | 14.06.2025; (Saturday) | 2 DAYS\\n11. | I.E.S./I.S.S. Examination, 2025 | 12.02.2025 | 04.03.2025 | 20.06.2025; (Friday) | 3 DAYS\\n12. | Combined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical Services Examination, 2025 | 19.02.2025 | 11.03.2025 | 20.07.2025; (Sunday) | 1 DAY\\n15. | Central Armed Police Forces (ACs) Examination, 2025 | 05.03.2025 | 25.03.2025 | 03.08.2025; (Sunday) | 1 DAY\\n16. | Engineering Services (Main) Examination, 2025 |", "field": "Exam date (I.E.S./I.S.S. Examination, 2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "ombined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical Services Examination, 2025 | 19.02.2025 | 11.03.2025 | 20.07.2025; (Sunday) | 1 DAY\\n15. | Central Armed Police Forces (ACs) Examination, 2025 | 05.03.2025 | 25.03.2025 | 03.08.2025; (Sunday) | 1 DAY\\n16. | Engineering Services (Main) Examination, 2025 | 10.08.2025; (Sunday) | 1 DAY\\n17. | Civil Services (Main) Examination, 2025 | 22.08.2025; (Friday) | 5 DAYS\\n18.; 19. | N.D.A. & N.A. Examination (II), 2025; C.D.S. Examination (II), 2025 | 28.05.2025 | 17.06.2025 | 14.09.2025; (Sunday) | 1 DAY\\n20. | Reserved for UPSC RT", "field": "Exam date (Combined Medical Services Examination, 2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "ation | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical Services Examination, 2025 | 19.02.2025 | 11.03.2025 | 20.07.2025; (Sunday) | 1 DAY\\n15. | Central Armed Police Forces (ACs) Examination, 2025 | 05.03.2025 | 25.03.2025 | 03.08.2025; (Sunday) | 1 DAY\\n16. | Engineering Services (Main) Examination, 2025 | 10.08.2025; (Sunday) | 1 DAY\\n17. | Civil Services (Main) Examination, 2025 | 22.08.2025; (Friday) | 5 DAYS\\n18.; 19. | N.D.A. & N.A. Examination (II), 2025; C.D.S. Examination (II), 2025 | 28.05.2025 | 17.06.2025 | 14.09.2025; (Sunday) | 1 DAY\\n20. | Reserved for UPSC RT/ Examination | 04.10.2025; (Saturday) | 2 DAYS\\n21. | Reserved for UPSC RT/ Examination | 01.11.2025; (Saturday) | ", "field": "Exam date (Central Armed Police Forces (ACs) Examination, 2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": ", 2025 | 19.02.2025 | 11.03.2025 | 20.07.2025; (Sunday) | 1 DAY\\n15. | Central Armed Police Forces (ACs) Examination, 2025 | 05.03.2025 | 25.03.2025 | 03.08.2025; (Sunday) | 1 DAY\\n16. | Engineering Services (Main) Examination, 2025 | 10.08.2025; (Sunday) | 1 DAY\\n17. | Civil Services (Main) Examination, 2025 | 22.08.2025; (Friday) | 5 DAYS\\n18.; 19. | N.D.A. & N.A. Examination (II), 2025; C.D.S. Examination (II), 2025 | 28.05.2025 | 17.06.2025 | 14.09.2025; (Sunday) | 1 DAY\\n20. | Reserved for UPSC RT/ Examination | 04.10.2025; (Saturday) | 2 DAYS\\n21. | Reserved for UPSC RT/ Examination | 01.11.2025; (Saturday) | 2 DAYS\\n22. | Indian Forest Service (Main) Examination, 2025 | 16.11.2025; (Sunday) ", "field": "Exam date (Engineering Services (Main) Examination, 2025)", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Work experience", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Attempt limits", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Year of study", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Category conditions", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "error", "code": "validation", "field": null, "message": "Eligibility rules must contain at least one rule group."}, {"severity": "warning", "code": "unverified-quote", "field": "Nationality", "message": "Nationality: the supporting quote could not be found in the document."}, {"severity": "warning", "code": "work-experience-unverified", "field": "Work experience", "message": "Work experience: the extracted value is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Attempt limits", "message": "Requirement: Attempt limits: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Year of study", "message": "Requirement: Year of study: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Category conditions", "message": "Requirement: Category conditions: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 1, "characters": 3049, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 44.2, "topics": {"identity": {"pages": [1], "context_tokens": 1305, "passages": 2}, "dates": {"pages": [1], "context_tokens": 1305, "passages": 2}, "eligibility": {"pages": [1], "context_tokens": 1115, "passages": 1}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 2385, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 3505, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 16.7}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 3711, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 28.0s for 3711 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for EligibilityDraft\\nwork_experience\\n  Input should be an object [type=model_type, input_value=None, input_type=NoneType]\\n    For further information visit https://errors.pydantic.dev/2.13/v/model_type", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	Engineering Services (Preliminary) Examination, 2025 conducted by Union Public Service Commission. Exam: 2025-01-11, 2025-02-09, 2025-04-27, 2025-05-25, 2025-06-08, 2025-06-20, 2025-07-20, 2025-08-03, 2025-08-10. 0 eligibility rule(s) extracted. 1 issue(s) need review before approval.	f	\N	PENDING	2026-10-07 14:42:24.627495
225	1086	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\RevisedIIICalendar2025-Engl-160126.pdf	{"extraction": {"exam_information": {"exam_name": "Engineering Services (Preliminary) Examination, 2025", "conducting_body": "Union Public Service Commission", "release_date": "2024-09-18", "application_start_date": "2024-10-18", "application_end_date": "2024-11-22", "exam_dates": [{"start_date": "2025-01-11", "end_date": "2025-01-11"}, {"start_date": "2025-02-09", "end_date": "2025-02-09"}, {"start_date": "2025-04-13", "end_date": "2025-04-13"}, {"start_date": "2025-04-27", "end_date": "2025-04-27"}, {"start_date": "2025-05-25", "end_date": "2025-05-25"}, {"start_date": "2025-06-08", "end_date": "2025-06-08"}, {"start_date": "2025-06-20", "end_date": "2025-06-20"}, {"start_date": "2025-07-20", "end_date": "2025-07-20"}, {"start_date": "2025-08-03", "end_date": "2025-08-03"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": null, "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": []}}, "evidence": [{"chunk_number": 2, "page_numbers": [1], "source_text": "04.2025; (Sunday) | 1 DAY\\n7.; 8. | Civil Services (Preliminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01.2025 | 21.02.2025 % | 25.05.2025; (Sunday) | 1 DAY\\n9. | Engineering Services (Preliminary) Examination, 2025 | 18.09.2024 | 22.11.2024* | 08.06.2025; (Sunday) | 1 DAY\\n10. | Reserved for UPSC RT/ Examination | 14.06.2025; (Saturday) | 2 DAYS\\n11. | I.E.S./I.S.S. Examination, 2025 | 12.02.2025 | 04.03.2025 | 20.06.2025; (Friday) | 3 DAYS\\n12. | Combined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical S", "field": "Exam name", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Conducting body", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "iminary) Examination, 2025; Indian Forest Service (Preliminary) Examination, 2025; through CS(P) Examination 2025 | 22.01.2025 | 21.02.2025 % | 25.05.2025; (Sunday) | 1 DAY\\n9. | Engineering Services (Preliminary) Examination, 2025 | 18.09.2024 | 22.11.2024* | 08.06.2025; (Sunday) | 1 DAY\\n10. | Reserved for UPSC RT/ Examination | 14.06.2025; (Saturday) | 2 DAYS\\n11. | I.E.S./I.S.S. Examination, 2025 | 12.02.2025 | 04.03.2025 | 20.06.2025; (Friday) | 3 DAYS\\n12. | Combined Geo-Scientist (Main) Examination, 2025 | 21.06.2025; (Saturday) | 2 DAYS\\n13. | Reserved for UPSC RT/ Examination | 05.07.2025; (Saturday) | 2 DAYS\\n14. | Combined Medical Services Examination, 2025 | 19.02.2025 | 11.03.2025 | 2", "field": "Release date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "* Last date for receipt of Application was 08.10.2024. Application Window has been re-opened from 18.10.2024 to 22.11.2024 after inclusion of IRMS in ESE, 2025\\n\\\\# Date of commencement of Examination postponed from 09.03.2025 to 27.04.2025.\\n% Last date of receipt of application extended from 11.02.2025 to 18.02.2025 and subsequently extended further to 21.02.2025.\\n@ Last date for receipt of Application was 07.10.2025. Application Window re-opened from 08.10.2025 to 12.10.2025.", "field": "Application start date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "* Last date for receipt of Application was 08.10.2024. Application Window has been re-opened from 18.10.2024 to 22.11.2024 after inclusion of IRMS in ESE, 2025\\n\\\\# Date of commencement of Examination postponed from 09.03.2025 to 27.04.2025.\\n% Last date of receipt of application extended from 11.02.2025 to 18.02.2025 and subsequently extended further to 21.02.2025.\\n@ Last date for receipt of Application was 07.10.2025. Application Window re-opened from 08.10.2025 to 12.10.2025.", "field": "Application end date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "* Last date for receipt of Application was 08.10.2024. Application Window has been re-opened from 18.10.2024 to 22.11.2024 after inclusion of IRMS in ESE, 2025\\n\\\\# Date of commencement of Examination postponed from 09.03.2025 to 27.04.2025.\\n% Last date of receipt of application extended from 11.02.2025 to 18.02.2025 and subsequently extended further to 21.02.2025.\\n@ Last date for receipt of Application was 07.10.2025. Application Window re-opened from 08.10.2025 to 12.10.2025.", "field": "Late-fee application end date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "UNION PUBLIC SERVICE COMMISSION PROGRAMME OF EXAMINATIONS/RECRUITMENT TESTS (RTs) -2025\\nSl.; No. | Name of Examination | Date of; Notification | Last Date for receipt of; Applications | Date of; commencement of Exam | Duration of Exam\\n1. | S.O. Grade-B LDCE, 2024 | 13.11.2024 | 03.12.2024 | 11.01.2025; (Saturday) | 2 DAYS\\n2. | Combined Geo-Scientist (Preliminary) Examination, 2025 | 04.09.2024 | 24.09.2024 | 09.02.2025; (Sunday) | 1 DAY\\n3. | CISF AC(EXE) LDCE-2025 | 04.12.2024 | 24.12.2024 | 27.04.2025#; (Sunday) | 1 DAY\\n4. | Reserved for UPSC RT/ Examination | 23.03.2025; (Sunday) | 1 DAY\\n5.; 6. | N.D.A. & N.A. Examination (I), 2025; C.D.S. Examination (I), 2025 | 11.12.2024 | 31.12.2024 | ", "field": "Exam date", "verified": true, "section": "As on 15.01.2026"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Work experience", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Attempt limits", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Year of study", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Category conditions", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "error", "code": "validation", "field": null, "message": "Eligibility rules must contain at least one rule group."}, {"severity": "warning", "code": "unverified-quote", "field": "Nationality", "message": "Nationality: the supporting quote could not be found in the document."}, {"severity": "warning", "code": "work-experience-unverified", "field": "Work experience", "message": "Work experience: the extracted value is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Attempt limits", "message": "Requirement: Attempt limits: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Year of study", "message": "Requirement: Year of study: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Category conditions", "message": "Requirement: Category conditions: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2025-02-21. Only the regular deadline is stored."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 1, "characters": 3049, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 71.1, "topics": {"identity": {"pages": [1], "context_tokens": 1305, "passages": 2}, "dates": {"pages": [1], "context_tokens": 1305, "passages": 2}, "eligibility": {"pages": [1], "context_tokens": 1115, "passages": 1}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 2385, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 3505, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 11.7}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 3711, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 27.9s for 3711 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for EligibilityDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='Here\\\\'s a thinking proce...empty if not restricted', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	Engineering Services (Preliminary) Examination, 2025 conducted by Union Public Service Commission. Applications: 2024-10-18 to 2024-11-22. Exam: 2025-01-11, 2025-02-09, 2025-04-13, 2025-04-27, 2025-05-25, 2025-06-08, 2025-06-20, 2025-07-20, 2025-08-03. 0 eligibility rule(s) extracted. 1 issue(s) need review before approval.	f	\N	PENDING	2026-10-07 15:11:36.002642
217	1080	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\CAT_2026_Information_Bulletin_26-07-26.pdf	{"extraction": {"exam_information": {"exam_name": "Common Admission Test 2026 (CAT 2026)", "conducting_body": "Indian Institutes of Management", "release_date": null, "application_start_date": "2026-08-03", "application_end_date": "2026-09-15", "exam_dates": [], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": "required work experience, if any", "other_requirements": ["Candidates must declare and maintain a valid and unique email account and a mobile phone number throughout the selection process."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 2, "page_numbers": [1], "source_text": "The Indian Institutes of Management will conduct a computer-based Common Admission Test 2026 (CAT\\n2026) on Sunday, November 29, 2026 in three sessions. CAT 2026 will be conducted by IIMs as a prerequisite for admission to various management programmes of IIMs. These programmes are:\\nA.", "field": "Exam name", "verified": true, "section": "Indian Institutes of Management > Information Bulletin"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "The Indian Institutes of Management will conduct a computer-based Common Admission Test 2026 (CAT\\n2026) on Sunday, November 29, 2026 in three sessions. CAT 2026 will be conducted by IIMs as a prerequisite for admission to various management programmes of IIMs. These programmes are:\\nA.", "field": "Conducting body", "verified": true, "section": "Indian Institutes of Management > Information Bulletin"}, {"chunk_number": 17, "page_numbers": [5], "source_text": "The CAT 2026 registration window opens at 10:00 a.m. on August 3, 2026 and will close at 5:00 p.m. on September 15, 2026. The details will be available in the registration guide.\\nAt the time of registration, the candidates have to select any five test cities, as per their preference, from a drop-down menu. After the last date of registration, candidates will be allotted one among the five preferred cities, subject to availability. In the rare case that a candidate is not allotted any of the preferred cities, he/she will be allotted a nearby city. The candidates can download the admit cards from November 04, 2026 until November 29, 2026.", "field": "Application start date", "verified": true, "section": "Indian Institutes of Management > REGISTRATION FOR CAT"}, {"chunk_number": 17, "page_numbers": [5], "source_text": "The CAT 2026 registration window opens at 10:00 a.m. on August 3, 2026 and will close at 5:00 p.m. on September 15, 2026. The details will be available in the registration guide.\\nAt the time of registration, the candidates have to select any five test cities, as per their preference, from a drop-down menu. After the last date of registration, candidates will be allotted one among the five preferred cities, subject to availability. In the rare case that a candidate is not allotted any of the preferred cities, he/she will be allotted a nearby city. The candidates can download the admit cards from November 04, 2026 until November 29, 2026.", "field": "Application end date", "verified": true, "section": "Indian Institutes of Management > REGISTRATION FOR CAT"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Work experience", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must declare and maintain a v", "verified": false, "section": null}], "conflicts": [], "issues": [], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 6, "characters": 14563, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 53.0, "topics": {"identity": {"pages": [1, 3, 5], "context_tokens": 1026, "passages": 6}, "dates": {"pages": [4, 5, 6], "context_tokens": 928, "passages": 5}, "eligibility": {"pages": [3, 4, 5, 6], "context_tokens": 1197, "passages": 6}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 2011, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 2606, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 10.5}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 3706, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 29.5s for 3706 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	Common Admission Test 2026 (CAT 2026) conducted by Indian Institutes of Management. Applications: 2026-08-03 to 2026-09-15. 1 eligibility rule(s) extracted.	f	extract exam date which is on 29 November 2026	REJECTED	2026-10-01 15:40:47.242234
218	1080	RETRY_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\CAT_2026_Information_Bulletin_26-07-26.pdf	{"extraction": {"exam_information": {"exam_name": "Common Admission Test 2026 (CAT 2026)", "conducting_body": "Indian Institutes of Management", "release_date": null, "application_start_date": "2026-08-03", "application_end_date": "2026-09-15", "exam_dates": [{"start_date": "2026-11-29", "end_date": "2026-11-29"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": "Bachelor's, Other", "nationality": null, "work_experience": null, "other_requirements": ["No age limit", "NC-OBC certificates must be issued on or after April 1, 2026; EWS certificates must be valid for FY 2025‑26."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [{"attribute": "Percentage", "operator": ">=", "value": "45"}], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Educational Qualification", "operator": "=", "value": "Bachelor's"}, {"attribute": "Educational Qualification", "operator": "=", "value": "Other"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 2, "page_numbers": [1], "source_text": "The Indian Institutes of Management will conduct a computer-based Common Admission Test 2026 (CAT\\n2026) on Sunday, November 29, 2026 in three sessions. CAT 2026 will be conducted by IIMs as a prerequisite for admission to various management programmes of IIMs. These programmes are:\\nA.", "field": "Exam name", "verified": true, "section": "Indian Institutes of Management > Information Bulletin"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "The Indian Institutes of Management will conduct a computer-based Common Admission Test 2026 (CAT\\n2026) on Sunday, November 29, 2026 in three sessions. CAT 2026 will be conducted by IIMs as a prerequisite for admission to various management programmes of IIMs. These programmes are:\\nA.", "field": "Conducting body", "verified": true, "section": "Indian Institutes of Management > Information Bulletin"}, {"chunk_number": 17, "page_numbers": [5], "source_text": "The CAT 2026 registration window opens at 10:00 a.m. on August 3, 2026 and will close at 5:00 p.m. on September 15, 2026. The details will be available in the registration guide.\\nAt the time of registration, the candidates have to select any five test cities, as per their preference, from a drop-down menu. After the last date of registration, candidates will be allotted one among the five preferred cities, subject to availability. In the rare case that a candidate is not allotted any of the preferred cities, he/she will be allotted a nearby city. The candidates can download the admit cards from November 04, 2026 until November 29, 2026.", "field": "Application start date", "verified": true, "section": "Indian Institutes of Management > REGISTRATION FOR CAT"}, {"chunk_number": 17, "page_numbers": [5], "source_text": "The CAT 2026 registration window opens at 10:00 a.m. on August 3, 2026 and will close at 5:00 p.m. on September 15, 2026. The details will be available in the registration guide.\\nAt the time of registration, the candidates have to select any five test cities, as per their preference, from a drop-down menu. After the last date of registration, candidates will be allotted one among the five preferred cities, subject to availability. In the rare case that a candidate is not allotted any of the preferred cities, he/she will be allotted a nearby city. The candidates can download the admit cards from November 04, 2026 until November 29, 2026.", "field": "Application end date", "verified": true, "section": "Indian Institutes of Management > REGISTRATION FOR CAT"}, {"chunk_number": 2, "page_numbers": [1], "source_text": "The Indian Institutes of Management will conduct a computer-based Common Admission Test 2026 (CAT\\n2026) on Sunday, November 29, 2026 in three sessions. CAT 2026 will be conducted by IIMs as a prerequisite for admission to various management programmes of IIMs. These programmes are:\\nA.", "field": "Exam date (CAT 2026 exam)", "verified": true, "section": "Indian Institutes of Management > Information Bulletin"}, {"chunk_number": 9, "page_numbers": [3], "source_text": "• The candidate must hold a Bachelor’s Degree, with at least 50% marks or equivalent CGPA [45% in the case of candidates belonging to the Scheduled Caste (SC), Scheduled Tribe (ST) and Persons with Benchmark Disabilities (PwBD) categories], awarded by any University or educational institution as incorporated by an Act of Parliament or State legislature in India or declared to be deemed as an University under Section 3 of the UGC Act, 1956, or possess an equivalent qualification recognised by the Ministry of Education, Government of India.\\n• Candidates appearing for the final year of Bachelor’s degree/equivalent qualification examination and those who have completed degree requirements and ar", "field": "Qualification: Bachelor's", "verified": true, "section": "Indian Institutes of Management > Eligibility"}, {"chunk_number": 10, "page_numbers": [3], "source_text": "Completed professional degree (CA/CS/ICWA (CMA)/Fellow of the Institute of Actuaries of India (FIAI)) with required percentage*.\\nc)\\nShould be in the final year of Bachelor’s degree with required percentage*.\\n*SC/ST/PwBD candidates should have a minimum 45%. For General, EWS and NC-OBC candidates, the minimum is 50%.", "field": "Qualification: Other", "verified": true, "section": "Indian Institutes of Management > Eligibility"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Minimum score", "verified": false, "section": null}, {"chunk_number": 15, "page_numbers": [5], "source_text": "For CAT 2026, NC-OBC certificates must be issued on or after April 1, 2026. For EWS candidates, the certificate must be valid for the year 2026–27 and specifically assessed for the financial year 2025–26.\\nHowever, candidates who have applied for a valid NC-OBC/EWS certificate on or after April 1, 2026, but have not received it by the time of CAT 2026 registration, may still submit the CAT application by uploading, in a single PDF, the following documents:\\n1.\\nA properly filled-in \\"Undertaking for NC-OBC/EWS Certificate\\" (available on the CAT 2026 official website);\\n2.\\nThe older NC-OBC/EWS certificate issued prior to April 1, 2026; and\\n3.\\nA copy of the communication/acknowledgement/screenshot ", "field": "Requirement: NC-OBC certificates must be issued on or", "verified": true, "section": "Indian Institutes of Management > any subsequent selection process of the IIMs."}], "conflicts": [], "issues": [{"severity": "warning", "code": "unverified-quote", "field": "Minimum score", "message": "Minimum score: the supporting quote could not be found in the document."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 6, "characters": 14563, "request_budget_tokens": 7000, "feedback_used": true, "seconds": 13.5, "topics": {"identity": {"pages": [1, 3, 5], "context_tokens": 1026, "passages": 6}, "dates": {"pages": [1, 4, 5, 6], "context_tokens": 1023, "passages": 6}, "eligibility": {"pages": [3, 4, 5, 6], "context_tokens": 1197, "passages": 6}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 2011, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 2733, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "groq", "estimated_tokens": 3706, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 7.1}]}]}}	Retry after administrator feedback. Common Admission Test 2026 (CAT 2026) conducted by Indian Institutes of Management. Applications: 2026-08-03 to 2026-09-15. Exam: 2026-11-29. 3 eligibility rule(s) extracted.	f	\N	APPROVED	2026-10-01 15:43:59.299685
219	1081	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Notif-CSP-2026-Engl-060226Rev.pdf	{"extraction": {"exam_information": {"exam_name": "Civil Services Examination 2026", "conducting_body": "Union Public Service Commission", "release_date": "2026-02-04", "application_start_date": null, "application_end_date": null, "exam_dates": [], "eligibility": {"minimum_age": 21, "maximum_age": 32, "educational_qualification": "Bachelor's", "nationality": "India, Nepal, Bhutan, Pakistan, Burma, Sri Lanka, Kenya, Uganda, Tanzania, Zambia, Malawi, Zaire, Ethiopia, Vietnam", "work_experience": null, "other_requirements": ["Age maximum 35 years for Defence Services Personnel disabled in operations (as on 2026-08-01)", "Reservation benefits require relevant community certificates as per rules."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [{"attribute": "Date of Birth", "operator": "<=", "value": "2005-08-01"}, {"attribute": "Date of Birth", "operator": ">=", "value": "1993-08-02"}], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Educational Qualification", "operator": "=", "value": "Bachelor's"}], "child_groups": []}, {"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}, {"attribute": "Nationality", "operator": "=", "value": "Nepal"}, {"attribute": "Nationality", "operator": "=", "value": "Bhutan"}, {"attribute": "Nationality", "operator": "=", "value": "Pakistan"}, {"attribute": "Nationality", "operator": "=", "value": "Burma"}, {"attribute": "Nationality", "operator": "=", "value": "Sri Lanka"}, {"attribute": "Nationality", "operator": "=", "value": "Kenya"}, {"attribute": "Nationality", "operator": "=", "value": "Uganda"}, {"attribute": "Nationality", "operator": "=", "value": "Tanzania"}, {"attribute": "Nationality", "operator": "=", "value": "Zambia"}, {"attribute": "Nationality", "operator": "=", "value": "Malawi"}, {"attribute": "Nationality", "operator": "=", "value": "Zaire"}, {"attribute": "Nationality", "operator": "=", "value": "Ethiopia"}, {"attribute": "Nationality", "operator": "=", "value": "Vietnam"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE NO 05/2026-CSE DATE: 04.02.2026\\n(LAST DATE FOR SUBMISSION OF ONLINE APPLICATIONS: 24.02.2026 of CIVIL SERVICES\\nEXAMINATION, 2026)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Exam name", "verified": true, "section": "Document"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE NO 05/2026-CSE DATE: 04.02.2026\\n(LAST DATE FOR SUBMISSION OF ONLINE APPLICATIONS: 24.02.2026 of CIVIL SERVICES\\nEXAMINATION, 2026)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Conducting body", "verified": true, "section": "Document"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE NO 05/2026-CSE DATE: 04.02.2026\\n(LAST DATE FOR SUBMISSION OF ONLINE APPLICATIONS: 24.02.2026 of CIVIL SERVICES\\nEXAMINATION, 2026)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 42, "page_numbers": [12], "source_text": "(1) A candidate must have attained the age of 21 years and must not have attained the age of 32\\nyears on the 1st of August, 2026 i.e., the candidate must have been born not earlier than 2nd\\nAugust, 1994 and not later than 1st August, 2005.\\n(2) The upper age-limit prescribed above will be relaxable:\\n(a) up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled\\nTribe;\\n(b) up to a maximum of three years in the case of candidates belonging to Other Backward\\nClasses who are eligible to avail of reservation applicable to such candidates;\\n(c) up to a maximum of three years in the case of Defence Services Personnel, disabled in\\noperations during hostilities with any fo", "field": "Age limit (Defence Services Personnel disabled in operations)", "verified": true, "section": "11. Face Authentication for Candidates at the Examination Venue > Age Limits:"}, {"chunk_number": 42, "page_numbers": [12], "source_text": "(1) A candidate must have attained the age of 21 years and must not have attained the age of 32\\nyears on the 1st of August, 2026 i.e., the candidate must have been born not earlier than 2nd\\nAugust, 1994 and not later than 1st August, 2005.\\n(2) The upper age-limit prescribed above will be relaxable:\\n(a) up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled\\nTribe;\\n(b) up to a maximum of three years in the case of candidates belonging to Other Backward\\nClasses who are eligible to avail of reservation applicable to such candidates;\\n(c) up to a maximum of three years in the case of Defence Services Personnel, disabled in\\noperations during hostilities with any fo", "field": "Age limit (minimum)", "verified": true, "section": "11. Face Authentication for Candidates at the Examination Venue > Age Limits:"}, {"chunk_number": 42, "page_numbers": [12], "source_text": "(1) A candidate must have attained the age of 21 years and must not have attained the age of 32\\nyears on the 1st of August, 2026 i.e., the candidate must have been born not earlier than 2nd\\nAugust, 1994 and not later than 1st August, 2005.\\n(2) The upper age-limit prescribed above will be relaxable:\\n(a) up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled\\nTribe;\\n(b) up to a maximum of three years in the case of candidates belonging to Other Backward\\nClasses who are eligible to avail of reservation applicable to such candidates;\\n(c) up to a maximum of three years in the case of Defence Services Personnel, disabled in\\noperations during hostilities with any fo", "field": "Age limit (maximum)", "verified": true, "section": "11. Face Authentication for Candidates at the Examination Venue > Age Limits:"}, {"chunk_number": 48, "page_numbers": [14], "source_text": "A candidate must hold a Graduate degree of any of the Universities incorporated by an Act of the\\ncentral or State Legislature in India or other educational institutions established by an Act of Parliament or\\ndeclared to be deemed as a University under Section 3 of the University Grants Commission Act, 1956 or\\npossess an equivalent qualification.\\nNote-I: Candidates who have appeared at a qualifying examination the passing of which would render them\\neducationally qualified for the Commission’s Examination but have not been informed of the result as also\\nthe candidates who intend to appear at such a qualifying examination will also be eligible for admission to\\nthe written part of Civil Services", "field": "Qualification: Bachelor's", "verified": true, "section": "11. Face Authentication for Candidates at the Examination Venue > Minimum Educational Qualification:"}, {"chunk_number": 41, "page_numbers": [12], "source_text": "(1)\\nFor the Indian Administrative Service, the Indian Foreign Service and the Indian Police Service, a\\ncandidate must be a citizen of India.\\n(2)\\nFor other services, a candidate must be either:—\\n(a)\\na citizen of India, or\\n(b)\\na subject of Nepal, or\\n(c)\\na subject of Bhutan, or\\n(d)\\na Tibetan refugee who came over to India before 1st January, 1962 with the intention of permanently\\nsettling in India, or\\n(e)\\na person of Indian origin who has migrated from Pakistan, Burma, Sri Lanka, East African countries\\nof Kenya, Uganda, the United Republic of Tanzania, Zambia, Malawi, Zaire, Ethiopia and Vietnam\\nwith the intention of permanently settling in India.\\nProvided that a candidate belonging to categori", "field": "Nationality", "verified": true, "section": "11. Face Authentication for Candidates at the Examination Venue > Nationality"}, {"chunk_number": 85, "page_numbers": [22], "source_text": "(1) A candidate will be eligible to get the benefit of community reservation only in case the particular\\ncaste to which the candidate belongs is included in the list of reserved communities issued by the\\nCentral Government.\\n(2) The OBC candidates applying for CSE-2026 must produce OBC (Non-Creamy Layer) certificate\\nbased on the income for the Financial Year (FY) 2022-2023, 2023-2024 and 2024-2025 and issued", "field": "Requirement: Reservation benefits require relevant co", "verified": true, "section": "2026 nor takes exemption from joining training, his/her allocation of service on the basis of CSE-2026 > Eligibility for Availing Reservation:"}], "conflicts": [{"field": "Age limit (maximum)", "options": [{"value": "32 years as on 2026-08-01", "source": "must not have attained the age of 32 years on the 1st of August, 2026", "pages": [12]}, {"value": "37 years as on 2026-08-01", "source": "up to a maximum of five years if a candidate belongs to a Scheduled Caste or a Scheduled Tribe", "pages": [12]}, {"value": "35 years as on 2026-08-01", "source": "up to a maximum of three years in the case of candidates belonging to Other Backward Classes", "pages": [12]}, {"value": "37 years as on 2026-08-01", "source": "up to a maximum of five years in the case of ex‑servicemen ... who have rendered at least five years Military Service", "pages": [12]}], "chosen": "32 years", "reason": "Provisionally using the first general limit found; verify against the document."}], "issues": [], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 159, "characters": 375893, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 80.3, "topics": {"identity": {"pages": [1, 2, 3, 6, 11, 12, 14, 19, 21, 22, 23, 30, 122, 123, 141, 143, 155, 158], "context_tokens": 5725, "passages": 25}, "dates": {"pages": [1, 3, 4, 5, 6, 10, 12, 13, 14, 15, 20, 21, 23, 155], "context_tokens": 4992, "passages": 24}, "eligibility": {"pages": [1, 2, 12, 13, 14, 16, 18, 22, 23, 30, 32], "context_tokens": 4187, "passages": 19}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6641, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 17.9}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 6591, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 53.6s for 6591 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='User Safety: safe', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "groq", "estimated_tokens": 6644, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 18.3}]}]}}	Civil Services Examination 2026 conducted by Union Public Service Commission. 17 eligibility rule(s) extracted.	f	Extract the prelims exam date	REJECTED	2026-10-01 17:31:58.920975
220	1081	RETRY_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Notif-CSP-2026-Engl-060226Rev.pdf	{"extraction": {"exam_information": {"exam_name": "Civil Services Examination 2026", "conducting_body": "Union Public Service Commission", "release_date": "2026-02-04", "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2026-05-24", "end_date": "2026-05-24"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": ["Candidates must be a citizen of India for Indian Administrative Service, Indian Foreign Service, and Indian Police Service.", "Candidates from other services must be a citizen of India, or a subject of Nepal, Bhutan, or a Tibetan refugee who came to India before 1962, or a person of Indian origin who migrated to India with the intention of settling permanently."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE NO 05/2026-CSE DATE: 04.02.2026\\n(LAST DATE FOR SUBMISSION OF ONLINE APPLICATIONS: 24.02.2026 of CIVIL SERVICES\\nEXAMINATION, 2026)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Exam name", "verified": true, "section": "Document"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE NO 05/2026-CSE DATE: 04.02.2026\\n(LAST DATE FOR SUBMISSION OF ONLINE APPLICATIONS: 24.02.2026 of CIVIL SERVICES\\nEXAMINATION, 2026)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Conducting body", "verified": true, "section": "Document"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "EXAMINATION NOTICE NO 05/2026-CSE DATE: 04.02.2026\\n(LAST DATE FOR SUBMISSION OF ONLINE APPLICATIONS: 24.02.2026 of CIVIL SERVICES\\nEXAMINATION, 2026)\\n(The Commission’s Website: www.upsc.gov.in)", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must be a citizen of India fo", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates from other services must be a", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "warning", "code": "unverified-quote", "field": "Exam date", "message": "Exam date: the supporting quote could not be found in the document."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 159, "characters": 375893, "request_budget_tokens": 7000, "feedback_used": true, "seconds": 152.7, "topics": {"identity": {"pages": [1, 2, 3, 6, 11, 12, 14, 19, 21, 22, 23, 30, 122, 123, 141, 143, 155, 158], "context_tokens": 5725, "passages": 25}, "dates": {"pages": [1, 3, 4, 5, 6, 10, 12, 13, 14, 15, 20, 21, 23, 155], "context_tokens": 5042, "passages": 25}, "eligibility": {"pages": [1, 2, 12, 13, 14, 16, 18, 22, 23, 30, 32], "context_tokens": 4187, "passages": 19}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6641, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 6666, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 49.6s for 6666 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6644, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Groq failed to generate a response: BadRequestError('Error code: 400 - {\\\\'error\\\\': {\\\\'message\\\\': \\"Generated JSON does not match the expected schema. Please adjust your prompt. See \\\\'failed_generation\\\\' for more details. Error: jsonschema: \\\\'\\\\' does not validate with /required: missing properties: \\\\'", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	Retry after administrator feedback. Civil Services Examination 2026 conducted by Union Public Service Commission. Exam: 2026-05-24. 1 eligibility rule(s) extracted.	f	\N	APPROVED	2026-10-01 17:36:27.232771
226	1087	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-08-27", "application_start_date": null, "application_end_date": "2026-09-27", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": null, "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": []}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 17, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th August 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | To be Announced (TBA)\\nApplication Portal closing | Sunday, September 27, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 5, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 13, "page_numbers": [7], "source_text": ") | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a fee of ₹500 per test paper | TBA to December 31, 2027", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 13, "page_numbers": [7], "source_text": "ndidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a fee of ₹500 per test paper | TBA to December 31, 2027", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 13, "page_numbers": [7], "source_text": "nnounced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a fee of ₹500 per test paper | TBA to December 31, 2027", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Work experience", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "error", "code": "validation", "field": null, "message": "Eligibility rules must contain at least one rule group."}, {"severity": "warning", "code": "unverified-quote", "field": "Nationality", "message": "Nationality: the supporting quote could not be found in the document."}, {"severity": "warning", "code": "work-experience-unverified", "field": "Work experience", "message": "Work experience: the extracted value is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Candidates must use only the on-screen v", "message": "Requirement: Candidates must use only the on-screen v: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Candidates are allowed to appear for one", "message": "Requirement: Candidates are allowed to appear for one: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "info", "code": "start-tba", "field": "Application start date", "message": "The application start date is listed as 'to be announced' in the document."}, {"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-05. Only the regular deadline is stored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "14 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Wednesday, September 30, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 383964, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 106.5, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 25, 26, 32, 33, 36, 37, 38], "context_tokens": 5662, "passages": 25}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2361, "passages": 14}, "eligibility": {"pages": [6, 12, 13, 14, 19, 20], "context_tokens": 3971, "passages": 14}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6660, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 4515, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 31.5s for 4515 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='The user wants me to ext...start_date: 2027-02-20,', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: EOF while parsing an object at line 43 column 22 [type=json_invalid, input_value='{\\\\n  \\"application_start_...n      \\"passage\\": \\"P13\\"', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invali", "waited_s": 0.0}, {"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6513, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 34.4s for 6513 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	GATE 2027 conducted by Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs). Applications: start date not announced to 2026-09-27. Exam: 2027-02-06 to 2027-02-07, 2027-02-13 to 2027-02-14, 2027-02-20 to 2027-02-21. 0 eligibility rule(s) extracted. 1 issue(s) need review before approval.	f	\N	PENDING	2026-10-07 15:19:51.610477
227	1088	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-08-27", "application_start_date": null, "application_end_date": "2026-09-27", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-06"}, {"start_date": "2027-02-07", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-13"}, {"start_date": "2027-02-14", "end_date": "2027-02-14"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": null, "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": []}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 17, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th August 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | To be Announced (TBA)\\nApplication Portal closing | Sunday, September 27, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 5, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 13, "page_numbers": [7], "source_text": ") | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a fee of ₹500 per test paper | TBA to December 31, 2027", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 13, "page_numbers": [7], "source_text": "ion of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a fee of ₹500 per test paper | TBA to December 31, 2027", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 13, "page_numbers": [7], "source_text": "ndidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a fee of ₹500 per test paper | TBA to December 31, 2027", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 13, "page_numbers": [7], "source_text": "mit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a fee of ₹500 per test paper | TBA to December 31, 2027", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Work experience", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "error", "code": "validation", "field": null, "message": "Eligibility rules must contain at least one rule group."}, {"severity": "warning", "code": "unverified-quote", "field": "Nationality", "message": "Nationality: the supporting quote could not be found in the document."}, {"severity": "warning", "code": "work-experience-unverified", "field": "Work experience", "message": "Work experience: the extracted value is not supported by the quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Candidates must use only the on-screen v", "message": "Requirement: Candidates must use only the on-screen v: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Candidates are allowed to appear for one", "message": "Requirement: Candidates are allowed to appear for one: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "info", "code": "start-tba", "field": "Application start date", "message": "The application start date is listed as 'to be announced' in the document."}, {"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-05. Only the regular deadline is stored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "14 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Wednesday, September 30, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 383964, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 107.3, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 25, 26, 32, 33, 36, 37, 38], "context_tokens": 5662, "passages": 25}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2361, "passages": 14}, "eligibility": {"pages": [6, 12, 13, 14, 19, 20], "context_tokens": 3971, "passages": 14}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6660, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 4515, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 27.3s for 4515 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: EOF while parsing an object at line 43 column 22 [type=json_invalid, input_value='{\\\\n  \\"application_start_...n      \\"passage\\": \\"P13\\"', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invali", "waited_s": 0.0}, {"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6513, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 39.2s for 6513 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	GATE 2027 conducted by Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs). Applications: start date not announced to 2026-09-27. Exam: 2027-02-06, 2027-02-07, 2027-02-13, 2027-02-14. 0 eligibility rule(s) extracted. 1 issue(s) need review before approval.	f	\N	PENDING	2026-10-07 15:23:01.953886
228	1089	COMPLETE_EXTRACTION	/opt/render/project/src/backend/storage/notifications/GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-09-27", "application_start_date": "2026-09-02", "application_end_date": "2026-10-05", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": null, "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": []}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application start date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 12, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 1)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 2)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 3)", "verified": true, "section": "DATES* FOR EXAMINATION"}], "conflicts": [], "issues": [{"severity": "error", "code": "ai-failed", "field": null, "message": "AI extraction of 'eligibility' failed: All AI providers failed. Attempts: groq: Token budget: groq: would need to wait 43.8s for 6119 tokens (limit 25.0s).; openrouter: OpenRouter returned an empty response.; local: Local Ollama provider failed to generate a response: ConnectionError('Failed to connect to Ollama. Please check that Ollama"}, {"severity": "error", "code": "validation", "field": null, "message": "Eligibility rules must contain at least one rule group."}, {"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-12. Only the regular deadline is stored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 156.1, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 21, 25, 26, 32, 33, 36, 38], "context_tokens": 5733, "passages": 26}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6651, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 3814, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 25.6s for 3814 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='The user wants me to ext...day, September 2, 2026\\"', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": false, "error": "Local Ollama provider failed to generate a response: ConnectionError('Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible. https://ollama.com/download')", "waited_s": 0.0}, {"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": null, "error": "All AI providers failed. Attempts: groq: Token budget: groq: would need to wait 43.8s for 6119 tokens (limit 25.0s).; openrouter: OpenRouter returned an empty response.; local: Local Ollama provider failed to generate a response: ConnectionError('Failed to connect to Ollama. Please check that Ollama"}]}}	GATE 2027 conducted by Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs). Applications: 2026-09-02 to 2026-10-05. Exam: 2027-02-06 to 2027-02-07, 2027-02-13 to 2027-02-14, 2027-02-20 to 2027-02-21. 0 eligibility rule(s) extracted. 2 issue(s) need review before approval.	f	check for the eligibility	REJECTED	2026-10-07 10:04:42.986051
229	1089	RETRY_EXTRACTION	/opt/render/project/src/backend/storage/notifications/GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-09-27", "application_start_date": "2026-09-02", "application_end_date": "2026-10-05", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": null, "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": []}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application start date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 12, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 1)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 2)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 3)", "verified": true, "section": "DATES* FOR EXAMINATION"}], "conflicts": [], "issues": [{"severity": "error", "code": "ai-failed", "field": null, "message": "AI extraction of 'eligibility' failed: All AI providers failed. Attempts: groq: Token budget: groq: would need to wait 43.3s for 6147 tokens (limit 25.0s).; openrouter: OpenRouter returned an empty response.; local: Local Ollama provider failed to generate a response: ConnectionError('Failed to connect to Ollama. Please check that Ollama"}, {"severity": "error", "code": "validation", "field": null, "message": "Eligibility rules must contain at least one rule group."}, {"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-12. Only the regular deadline is stored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": true, "seconds": 154.1, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 21, 25, 26, 32, 33, 36, 38], "context_tokens": 5733, "passages": 26}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6651, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 3814, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 25.4s for 3814 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='Here\\\\'s a thinking proce... as separate entries or', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": false, "error": "Local Ollama provider failed to generate a response: ConnectionError('Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible. https://ollama.com/download')", "waited_s": 0.0}, {"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": null, "error": "All AI providers failed. Attempts: groq: Token budget: groq: would need to wait 43.3s for 6147 tokens (limit 25.0s).; openrouter: OpenRouter returned an empty response.; local: Local Ollama provider failed to generate a response: ConnectionError('Failed to connect to Ollama. Please check that Ollama"}]}}	Retry after administrator feedback. GATE 2027 conducted by Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs). Applications: 2026-09-02 to 2026-10-05. Exam: 2027-02-06 to 2027-02-07, 2027-02-13 to 2027-02-14, 2027-02-20 to 2027-02-21. 0 eligibility rule(s) extracted. 2 issue(s) need review before approval.	f	\N	PENDING	2026-10-07 10:12:35.630309
230	1090	COMPLETE_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science and Indian Institutes of Technology", "release_date": "2026-09-27", "application_start_date": "2026-09-02", "application_end_date": "2026-10-05", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application start date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 12, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 29, "page_numbers": [12], "source_text": "In the past, several Public Sector Undertakings (PSUs) have used candidate’s GATE score in their recruitment process. During the past few years, the PSUs that have used GATE scores in their recruitment process are: Airports Authority of India (AAI), Bharat Heavy Electricals Limited (BHEL), Bharat Sanchar Nigam Limited (BSNL), Coal India Limited (CIL), Centre for Railway Information Systems (CRIS), Chenab Valley Power Projects Limited (CVPPL), Damodar Valley Corporation (DVC), Electronics Corporation of India Limited (ECIL), Engineers India Limited (EIL), GAIL (India) Limited, GRID India, Indian Oil Corporation Limited (IOCL), Mazagon Dock Shipbuilders Limited (MDSL), National Aluminium Compa", "field": "Nationality", "verified": true, "section": "5. About GATE > 5.3 Opportunities with GATE Qualification > 5.3.2 Use of GATE Score for Employment"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are required to provide live facial…", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "error", "code": "validation", "field": null, "message": "Exam information: release_date cannot be after application_start_date."}, {"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Candidates are required to provide live facial…", "message": "Requirement: Candidates are required to provide live facial…: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-12. Only the regular deadline is stored."}, {"severity": "info", "code": "quote-recovered", "field": "Nationality", "message": "Nationality: the model gave no usable quote, so the matching sentence from the document was used."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 216.5, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 25, 26, 32, 33, 36, 37, 38], "context_tokens": 5662, "passages": 27}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6654, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 16.8}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 4323, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 33.4s for 4323 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='The user wants me to ext...t is \\"February 6 & 7, 2', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: EOF while parsing a string at line 3 column 1085 [type=json_invalid, input_value='{\\\\n  \\"application_start_...-02 2026-09-02 2026-09-', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invali", "waited_s": 0.0}, {"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6522, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 27.7s for 6522 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	GATE 2027 conducted by Indian Institute of Science and Indian Institutes of Technology. Applications: 2026-09-02 to 2026-10-05. Exam: 2027-02-06 to 2027-02-07, 2027-02-13 to 2027-02-14, 2027-02-20 to 2027-02-21. 1 eligibility rule(s) extracted. 1 issue(s) need review before approval.	f	check for the correct release date	REJECTED	2026-10-08 11:02:39.186653
231	1090	RETRY_EXTRACTION	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science and Indian Institutes of Technology", "release_date": "2026-09-27", "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-06"}, {"start_date": "2027-02-07", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-13"}, {"start_date": "2027-02-14", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-20"}, {"start_date": "2027-02-21", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": []}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 15, "page_numbers": [7], "source_text": " Adding a new test paper, and change of personal; details (additional fee may be applicable per change) | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a ", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 15, "page_numbers": [7], "source_text": " Adding a new test paper, and change of personal; details (additional fee may be applicable per change) | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a ", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 15, "page_numbers": [7], "source_text": " Adding a new test paper, and change of personal; details (additional fee may be applicable per change) | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a ", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 15, "page_numbers": [7], "source_text": " Adding a new test paper, and change of personal; details (additional fee may be applicable per change) | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a ", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 15, "page_numbers": [7], "source_text": " Adding a new test paper, and change of personal; details (additional fee may be applicable per change) | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a ", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 15, "page_numbers": [7], "source_text": " Adding a new test paper, and change of personal; details (additional fee may be applicable per change) | October 21, 2026\\nNotification of Exam cities to the Candidates | January 04, 2027\\nAdmit Cards download | To be Announced (TBA)\\nGATE 2027 Examination Dates; Sessions; Forenoon: 9:30 AM to 12:30 PM; Afternoon: 2:30 PM to 5:30 PM | February 06, 2027 (Saturday); February 07, 2027 (Sunday); February 13, 2027 (Saturday); February 14, 2027 (Sunday); February 20, 2027 (Saturday); February 21, 2027 (Sunday)\\nAnnouncement of results in the GATE Online Application; Processing System (GOAPS) | March 19, 2027\\nScore Cards available for free download | TBA\\nScore Cards available for download by paying a ", "field": "Exam date", "verified": true, "section": "3. Important Dates*"}, {"chunk_number": 29, "page_numbers": [12], "source_text": "In the past, several Public Sector Undertakings (PSUs) have used candidate’s GATE score in their recruitment process. During the past few years, the PSUs that have used GATE scores in their recruitment process are: Airports Authority of India (AAI), Bharat Heavy Electricals Limited (BHEL), Bharat Sanchar Nigam Limited (BSNL), Coal India Limited (CIL), Centre for Railway Information Systems (CRIS), Chenab Valley Power Projects Limited (CVPPL), Damodar Valley Corporation (DVC), Electronics Corporation of India Limited (ECIL), Engineers India Limited (EIL), GAIL (India) Limited, GRID India, Indian Oil Corporation Limited (IOCL), Mazagon Dock Shipbuilders Limited (MDSL), National Aluminium Compa", "field": "Nationality", "verified": true, "section": "5. About GATE > 5.3 Opportunities with GATE Qualification > 5.3.2 Use of GATE Score for Employment"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are required to provide live facial…", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "warning", "code": "requirement-unverified", "field": "Requirement: Candidates are required to provide live facial…", "message": "Requirement: Candidates are required to provide live facial…: the extracted requirement is not sufficiently supported by its quoted text; it was ignored."}, {"severity": "info", "code": "start-tba", "field": "Application start date", "message": "The application start date is listed as 'to be announced' in the document."}, {"severity": "info", "code": "quote-recovered", "field": "Nationality", "message": "Nationality: the model gave no usable quote, so the matching sentence from the document was used."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": true, "seconds": 173.3, "topics": {"identity": {"pages": [1, 2, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 21, 25, 32, 36, 37, 38], "context_tokens": 5643, "passages": 29}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6656, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 4353, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 30.1s for 4353 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6522, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Groq failed to generate a response: BadRequestError('Error code: 400 - {\\\\'error\\\\': {\\\\'message\\\\': \\"Generated JSON does not match the expected schema. Please adjust your prompt. See \\\\'failed_generation\\\\' for more details. Error: jsonschema: \\\\'/qualifications/6/level\\\\' does not validate with /propertie", "waited_s": 20.3}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	Retry after administrator feedback. GATE 2027 conducted by Indian Institute of Science and Indian Institutes of Technology. Exam: 2027-02-06, 2027-02-07, 2027-02-13, 2027-02-14, 2027-02-20, 2027-02-21. 1 eligibility rule(s) extracted.	f	\N	PENDING	2026-10-08 11:12:02.696325
\.


--
-- Data for Name: monitoringreview; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.monitoringreview (review_id, notification_id, old_document_hash, new_document_hash, old_extraction, new_extraction, structural_changes, semantic_analysis, impact_analysis, review_status, rejection_reason, reviewed_by, reviewed_at, created_at) FROM stdin;
620	1076	81A9E59B0493C3A882953549750D973490B14A65F29931DB818E7F37949865AA	991c8f31e58276a18da8ee52d58e1f3b8c353ace075fbbc44fb4d47ccef49002	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-09-27", "application_start_date": "2026-09-02", "application_end_date": "2026-10-05", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": ["Candidates must use only the on-screen virtual calculator provided for their calculations.", "Candidates are allowed to appear for one or two test papers only."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application start date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 12, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 1)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 2)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 3)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-12. Only the regular deadline is stored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": true, "seconds": 83.5, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 21, 25, 26, 32, 33, 36, 38], "context_tokens": 5733, "passages": 26}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6651, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 3814, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 24.8}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6148, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 48.9s for 6148 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-08-27", "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-06"}, {"start_date": "2027-02-13", "end_date": "2027-02-13"}, {"start_date": "2027-02-20", "end_date": "2027-02-20"}, {"start_date": "2027-02-21", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": ["Candidates must use only the on-screen virtual calculator provided for their calculations.", "Candidates are allowed to appear for one or two test papers only. The two test paper combinations must be chosen from the given list of combinations of test papers."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 17, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th August 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "warning", "code": "unverified-quote", "field": "Exam date", "message": "Exam date: the supporting quote could not be found in the document."}, {"severity": "info", "code": "start-tba", "field": "Application start date", "message": "The application start date is listed as 'to be announced' in the document."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "14 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Wednesday, September 30, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 383964, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 202.4, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 25, 26, 32, 33, 36, 38], "context_tokens": 5714, "passages": 25}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2361, "passages": 14}, "eligibility": {"pages": [6, 12, 13, 14, 19, 20], "context_tokens": 3971, "passages": 14}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6635, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 4006, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 26.9s for 4006 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for DatesDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='The user wants me to ext... quotes (max 25 words).', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6448, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Groq failed to generate a response: BadRequestError('Error code: 400 - {\\\\'error\\\\': {\\\\'message\\\\': \\"Generated JSON does not match the expected schema. Please adjust your prompt. See \\\\'failed_generation\\\\' for more details. Error: jsonschema: \\\\'/qualifications/5/level\\\\' does not validate with /propertie", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	"StructuralChangeReport(change_detected=True, changes=[StructuralChange(change_type='MODIFIED', path='exam_information.application_end_date', old_value='2026-10-05', new_value=None), StructuralChange(change_type='MODIFIED', path='exam_information.application_start_date', old_value='2026-09-02', new_value=None), StructuralChange(change_type='MODIFIED', path='exam_information.eligibility.other_requirements[1]', old_value='Candidates are allowed to appear for one or two test papers only.', new_value='Candidates are allowed to appear for one or two test papers only. The two test paper combinations must be chosen from the given list of combinations of test papers.'), StructuralChange(change_type='MODIFIED', path='exam_information.release_date', old_value='2026-09-27', new_value='2026-08-27'), StructuralChange(change_type='MODIFIED', path='exam_information.exam_dates[0]', old_value={'start_date': '2027-02-06', 'end_date': '2027-02-07'}, new_value={'start_date': '2027-02-06', 'end_date': '2027-02-06'}), StructuralChange(change_type='MODIFIED', path='exam_information.exam_dates[1]', old_value={'start_date': '2027-02-13', 'end_date': '2027-02-14'}, new_value={'start_date': '2027-02-13', 'end_date': '2027-02-13'}), StructuralChange(change_type='MODIFIED', path='exam_information.exam_dates[2]', old_value={'start_date': '2027-02-20', 'end_date': '2027-02-21'}, new_value={'start_date': '2027-02-20', 'end_date': '2027-02-20'}), StructuralChange(change_type='ADDED', path='exam_information.exam_dates[3]', old_value=None, new_value={'start_date': '2027-02-21', 'end_date': '2027-02-21'})])"	{"overall_summary": "The notification removed the application start and end dates, added a clarification to the test paper selection rule, moved the release date earlier, changed three exam sessions from two-day to single-day events, and added a fourth single-day exam session.", "changes": [{"change_index": 0, "summary": "The application end date was removed.", "affected_requirement": "Application deadline", "impact": "Applicants no longer have a published deadline, creating uncertainty about the latest date to submit applications.", "confidence": "MEDIUM", "requires_human_review": true, "explanation": "The field exam_information.application_end_date changed from \\"2026-10-05\\" to null, indicating the end date is no longer specified."}, {"change_index": 1, "summary": "The application start date was removed.", "affected_requirement": "Application opening date", "impact": "Potential applicants cannot determine when the application window opens, which may affect planning and eligibility timing.", "confidence": "MEDIUM", "requires_human_review": true, "explanation": "The field exam_information.application_start_date changed from \\"2026-09-02\\" to null, meaning the start date is no longer provided."}, {"change_index": 2, "summary": "Eligibility wording for test paper combinations was expanded.", "affected_requirement": "Test paper selection rule", "impact": "Adds a specific restriction on which combinations of test papers may be chosen, potentially narrowing eligible candidates.", "confidence": "HIGH", "requires_human_review": false, "explanation": "The entry exam_information.eligibility.other_requirements[1] was modified to add the sentence \\"The two test paper combinations must be chosen from the given list of combinations of test papers.\\""}, {"change_index": 3, "summary": "The release date was moved earlier by one month.", "affected_requirement": "Notification release date", "impact": "Information becomes available earlier; does not directly affect eligibility but may give candidates more time to prepare.", "confidence": "HIGH", "requires_human_review": false, "explanation": "The field exam_information.release_date changed from \\"2026-09-27\\" to \\"2026-08-27\\"."}, {"change_index": 4, "summary": "First exam session changed from a two‑day to a single‑day event.", "affected_requirement": "Exam schedule for session 1", "impact": "The exam will now be held only on 2027‑02‑06 instead of spanning two days, reducing the time allocated for the test.", "confidence": "HIGH", "requires_human_review": false, "explanation": "exam_information.exam_dates[0] end_date changed from \\"2027-02-07\\" to \\"2027-02-06\\", making start and end dates identical."}, {"change_index": 5, "summary": "Second exam session changed from a two‑day to a single‑day event.", "affected_requirement": "Exam schedule for session 2", "impact": "The exam will now be held only on 2027‑02‑13 instead of spanning two days.", "confidence": "HIGH", "requires_human_review": false, "explanation": "exam_information.exam_dates[1] end_date changed from \\"2027-02-14\\" to \\"2027-02-13\\", aligning start and end dates."}, {"change_index": 6, "summary": "Third exam session changed from a two‑day to a single‑day event.", "affected_requirement": "Exam schedule for session 3", "impact": "The exam will now be held only on 2027‑02‑20 instead of spanning two days.", "confidence": "HIGH", "requires_human_review": false, "explanation": "exam_information.exam_dates[2] end_date changed from \\"2027-02-21\\" to \\"2027-02-20\\", making start and end dates identical."}, {"change_index": 7, "summary": "A fourth exam session was added as a single‑day event.", "affected_requirement": "Additional exam date", "impact": "Provides an extra exam opportunity on 2027‑02‑21, potentially increasing flexibility for candidates.", "confidence": "HIGH", "requires_human_review": false, "explanation": "exam_information.exam_dates[3] was added with start_date and end_date both set to \\"2027-02-21\\"."}], "requires_human_review": true}	{"impacts": [{"change_index": 0, "impact_type": "APPLICATION_TIMELINE_CHANGED", "affects_eligibility": false, "affects_application_timeline": true, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": true, "reason": "The structural change affects the application timeline."}, {"change_index": 1, "impact_type": "APPLICATION_TIMELINE_CHANGED", "affects_eligibility": false, "affects_application_timeline": true, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": true, "reason": "The structural change affects the application timeline."}, {"change_index": 2, "impact_type": "EXAM_INFORMATION_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects exam information outside the known eligibility, application timeline, and exam schedule fields."}, {"change_index": 3, "impact_type": "EXAM_INFORMATION_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects exam information outside the known eligibility, application timeline, and exam schedule fields."}, {"change_index": 4, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}, {"change_index": 5, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}, {"change_index": 6, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}, {"change_index": 7, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}], "overall_requires_human_review": true, "overall_requires_eligibility_re_evaluation": false}	REJECTED	application dead line should be shown	497	2026-10-01 15:11:49.629173	2026-10-01 14:48:22.004969
621	1076	81A9E59B0493C3A882953549750D973490B14A65F29931DB818E7F37949865AA	991c8f31e58276a18da8ee52d58e1f3b8c353ace075fbbc44fb4d47ccef49002	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-09-27", "application_start_date": "2026-09-02", "application_end_date": "2026-10-05", "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-07"}, {"start_date": "2027-02-13", "end_date": "2027-02-14"}, {"start_date": "2027-02-20", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": ["Candidates must use only the on-screen virtual calculator provided for their calculations.", "Candidates are allowed to appear for one or two test papers only."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 19, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th September 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application start date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 3, "page_numbers": [2], "source_text": "Regular Period\\nApplication Portal opening | Wednesday, September 2, 2026\\nApplication Portal closing | Monday, October 5, 2026", "field": "Application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 4, "page_numbers": [2], "source_text": "Extended Period\\nApplication Portal closing with late fee | Monday, October 12, 2026", "field": "Late-fee application end date", "verified": true, "section": "DATES* FOR ONLINE REGISTRATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 1)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 2)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 2, "page_numbers": [2], "source_text": "Week 1 | Week 2 | Week 3\\nFebruary 6 & 7, 2027 | February 13 & 14, 2027 | February 20 & 21, 2027", "field": "Exam date (Week 3)", "verified": true, "section": "DATES* FOR EXAMINATION"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "info", "code": "late-fee-deadline", "field": "Application end date", "message": "Extended (late-fee) application deadline: 2026-10-12. Only the regular deadline is stored."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "17 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Sunday, September 27, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 384124, "request_budget_tokens": 7000, "feedback_used": true, "seconds": 83.5, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 21, 25, 26, 32, 33, 36, 38], "context_tokens": 5733, "passages": 26}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2175, "passages": 15}, "eligibility": {"pages": [6, 12, 13, 14, 15, 20], "context_tokens": 3639, "passages": 13}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6651, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "groq", "estimated_tokens": 3814, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 24.8}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6148, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 48.9s for 6148 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	{"extraction": {"exam_information": {"exam_name": "GATE 2027", "conducting_body": "Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs)", "release_date": "2026-08-27", "application_start_date": null, "application_end_date": null, "exam_dates": [{"start_date": "2027-02-06", "end_date": "2027-02-06"}, {"start_date": "2027-02-13", "end_date": "2027-02-13"}, {"start_date": "2027-02-20", "end_date": "2027-02-20"}, {"start_date": "2027-02-21", "end_date": "2027-02-21"}], "eligibility": {"minimum_age": null, "maximum_age": null, "educational_qualification": null, "nationality": "India", "work_experience": null, "other_requirements": ["Candidates must use only the on-screen virtual calculator provided for their calculations.", "Candidates are allowed to appear for one or two test papers only. The two test paper combinations must be chosen from the given list of combinations of test papers."]}}, "eligibility_rules": {"rule_groups": [{"logical_operator": "AND", "rules": [], "child_groups": [{"logical_operator": "OR", "rules": [{"attribute": "Nationality", "operator": "=", "value": "India"}], "child_groups": []}]}]}}, "evidence": [{"chunk_number": 9, "page_numbers": [6], "source_text": "• Indian Institute of Technology Madras (IITM) is the Organizing Institute (OI) for GATE 2027. The official website of GATE 2027 is https://gate2027.iitm.ac.in.\\n• GATE 2027 will be conducted for 30 test papers as Computer Based Test (CBT).\\n• Syllabus of GATE 2027 test papers has been revised. Candidates are advised to check the syllabus.\\n• A new test paper on Robotics & Automation (RA) has been introduced in GATE 2027. Candidates must note that Textile Engineering & Fibre Science (TF) paper will be a part of XE sectional paper (i.e., XE9: Textile Engineering & Fibre Science) from GATE 2027.\\n• Please note the changes in paper codes for sectional papers XE, XH, XL from GATE 2027.\\n• GATE 2027 t", "field": "Exam name", "verified": true, "section": "2. Highlights of GATE 2027"}, {"chunk_number": 17, "page_numbers": [9], "source_text": "Graduate Aptitude Test in Engineering (GATE) is a national examination conducted jointly by the Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs).\\nGATE is conducted as a Computer Based Test (CBT) and evaluates the comprehensive understanding of the candidates in various undergraduate subjects in Engineering, Technology, and Architecture; and both undergraduate and post-graduate level subjects in Science, Humanities, Commerce, and Arts. The GATE score reflects the relative performance level of the candidate in a particular test paper. GATE 2027 score will be valid for THREE YEARS from the date of announcement of results. No information on GATE 2027 score will be av", "field": "Conducting body", "verified": true, "section": "5. About GATE"}, {"chunk_number": 1, "page_numbers": [1], "source_text": "Revised version, Date: 27th August 2026", "field": "Release date", "verified": true, "section": "Document"}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Exam date", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Nationality", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates must use only the on-screen v", "verified": false, "section": null}, {"chunk_number": 0, "page_numbers": [], "source_text": "(no supporting quote provided)", "field": "Requirement: Candidates are allowed to appear for one", "verified": false, "section": null}], "conflicts": [], "issues": [{"severity": "warning", "code": "unverified-quote", "field": "Exam date", "message": "Exam date: the supporting quote could not be found in the document."}, {"severity": "info", "code": "start-tba", "field": "Application start date", "message": "The application start date is listed as 'to be announced' in the document."}, {"severity": "info", "code": "superseded-ignored", "field": null, "message": "14 struck-out (superseded) values in the document were ignored, e.g. 'Friday, August 14, 2026' (p.2); 'Thursday, August 27, 2026' (p.2); 'Monday, September 21, 2026' (p.2); 'Wednesday, September 30, 2026' (p.2)."}], "pipeline": {"version": "2.0", "parser": "nexstep-layout-v2", "pages": 143, "characters": 383964, "request_budget_tokens": 7000, "feedback_used": false, "seconds": 102.3, "topics": {"identity": {"pages": [1, 6, 7, 9, 10, 12, 13, 14, 15, 17, 25, 26, 32, 33, 36, 38], "context_tokens": 5714, "passages": 25}, "dates": {"pages": [2, 6, 7, 9, 10, 21, 25], "context_tokens": 2361, "passages": 14}, "eligibility": {"pages": [6, 12, 13, 14, 19, 20], "context_tokens": 3971, "passages": 14}}, "calls": [{"facet": "identity", "provider": "groq", "estimated_tokens": 6635, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "dates", "provider": "local", "estimated_tokens": 4006, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Token budget: groq: would need to wait 26.8s for 4006 tokens (limit 25.0s).", "waited_s": 0.0}, {"provider": "openrouter", "ok": false, "error": "OpenRouter returned an empty response.", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}, {"facet": "eligibility", "provider": "local", "estimated_tokens": 6448, "corrective_retry": false, "attempts": [{"provider": "groq", "ok": false, "error": "Groq failed to generate a response: BadRequestError('Error code: 400 - {\\\\'error\\\\': {\\\\'message\\\\': \\"Generated JSON does not match the expected schema. Please adjust your prompt. See \\\\'failed_generation\\\\' for more details. Error: jsonschema: \\\\'/qualifications/6/level\\\\' does not validate with /propertie", "waited_s": 15.1}, {"provider": "openrouter", "ok": false, "error": "Validation failed: 1 validation error for EligibilityDraft\\n  Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='The user wants me to ext...ribe guidelines (P68, P', input_type=str]\\n    For further information visit https://errors.pydantic.dev/2.13/v/json_invalid", "waited_s": 0.0}, {"provider": "local", "ok": true, "error": null, "waited_s": 0.0}]}]}}	"StructuralChangeReport(change_detected=True, changes=[StructuralChange(change_type='MODIFIED', path='exam_information.application_end_date', old_value='2026-10-05', new_value=None), StructuralChange(change_type='MODIFIED', path='exam_information.application_start_date', old_value='2026-09-02', new_value=None), StructuralChange(change_type='MODIFIED', path='exam_information.eligibility.other_requirements[1]', old_value='Candidates are allowed to appear for one or two test papers only.', new_value='Candidates are allowed to appear for one or two test papers only. The two test paper combinations must be chosen from the given list of combinations of test papers.'), StructuralChange(change_type='MODIFIED', path='exam_information.release_date', old_value='2026-09-27', new_value='2026-08-27'), StructuralChange(change_type='MODIFIED', path='exam_information.exam_dates[0]', old_value={'start_date': '2027-02-06', 'end_date': '2027-02-07'}, new_value={'start_date': '2027-02-06', 'end_date': '2027-02-06'}), StructuralChange(change_type='MODIFIED', path='exam_information.exam_dates[1]', old_value={'start_date': '2027-02-13', 'end_date': '2027-02-14'}, new_value={'start_date': '2027-02-13', 'end_date': '2027-02-13'}), StructuralChange(change_type='MODIFIED', path='exam_information.exam_dates[2]', old_value={'start_date': '2027-02-20', 'end_date': '2027-02-21'}, new_value={'start_date': '2027-02-20', 'end_date': '2027-02-20'}), StructuralChange(change_type='ADDED', path='exam_information.exam_dates[3]', old_value=None, new_value={'start_date': '2027-02-21', 'end_date': '2027-02-21'})])"	{"overall_summary": "The notification removed the application start and end dates, added a clarification to the test paper selection requirement, moved the release date earlier, changed all existing exam dates to single-day events, and added an additional exam day on 2027-02-21.", "changes": [{"change_index": 0, "summary": "The application end date was removed.", "affected_requirement": "Application deadline (end date)", "impact": "Applicants no longer have a published end date for submitting applications, creating uncertainty about the deadline.", "confidence": "MEDIUM", "requires_human_review": true, "explanation": "The old value was \\"2026-10-05\\" and the new value is null, indicating the field was cleared."}, {"change_index": 1, "summary": "The application start date was removed.", "affected_requirement": "Application opening date (start date)", "impact": "Applicants cannot determine when the application window opens, which may affect planning and eligibility timing.", "confidence": "MEDIUM", "requires_human_review": true, "explanation": "The old value was \\"2026-09-02\\" and the new value is null, showing the field was cleared."}, {"change_index": 2, "summary": "The eligibility requirement about test papers was expanded with an additional condition on allowed combinations.", "affected_requirement": "Eligibility – test paper selection rule", "impact": "Candidates must now choose test‑paper combinations from a specified list, adding a restriction to the previously broader allowance.", "confidence": "HIGH", "requires_human_review": false, "explanation": "The old text allowed \\"one or two test papers only\\"; the new text adds \\"The two test paper combinations must be chosen from the given list of combinations of test papers.\\""}, {"change_index": 3, "summary": "The release date was changed from 2026-09-27 to 2026-08-27.", "affected_requirement": "Notification release date", "impact": "The information becomes available one month earlier; no direct effect on eligibility but may affect applicant planning.", "confidence": "HIGH", "requires_human_review": false, "explanation": "The old value was \\"2026-09-27\\" and the new value is \\"2026-08-27\\"."}, {"change_index": 4, "summary": "Exam date 0 end date changed from 2027-02-07 to 2027-02-06, making the exam a single‑day event.", "affected_requirement": "Exam schedule for first session", "impact": "The first exam session is now one day instead of two, reducing the exam duration.", "confidence": "HIGH", "requires_human_review": false, "explanation": "Old end_date was \\"2027-02-07\\"; new end_date is \\"2027-02-06\\" matching the start_date."}, {"change_index": 5, "summary": "Exam date 1 end date changed from 2027-02-14 to 2027-02-13, making the exam a single‑day event.", "affected_requirement": "Exam schedule for second session", "impact": "The second exam session is now one day instead of two, reducing the exam duration.", "confidence": "HIGH", "requires_human_review": false, "explanation": "Old end_date was \\"2027-02-14\\"; new end_date is \\"2027-02-13\\" matching the start_date."}, {"change_index": 6, "summary": "Exam date 2 end date changed from 2027-02-21 to 2027-02-20, making the exam a single‑day event.", "affected_requirement": "Exam schedule for third session", "impact": "The third exam session is now one day instead of two, reducing the exam duration.", "confidence": "HIGH", "requires_human_review": false, "explanation": "Old end_date was \\"2027-02-21\\"; new end_date is \\"2027-02-20\\" matching the start_date."}, {"change_index": 7, "summary": "A new exam date (session 4) on 2027-02-21 was added as a single‑day exam.", "affected_requirement": "Additional exam session", "impact": "Provides an extra exam opportunity on 2027-02-21.", "confidence": "HIGH", "requires_human_review": false, "explanation": "The path previously had no entry (null) and now contains a date object with start_date and end_date both set to \\"2027-02-21\\"."}], "requires_human_review": true}	{"impacts": [{"change_index": 0, "impact_type": "APPLICATION_TIMELINE_CHANGED", "affects_eligibility": false, "affects_application_timeline": true, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": true, "reason": "The structural change affects the application timeline."}, {"change_index": 1, "impact_type": "APPLICATION_TIMELINE_CHANGED", "affects_eligibility": false, "affects_application_timeline": true, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": true, "reason": "The structural change affects the application timeline."}, {"change_index": 2, "impact_type": "EXAM_INFORMATION_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects exam information outside the known eligibility, application timeline, and exam schedule fields."}, {"change_index": 3, "impact_type": "EXAM_INFORMATION_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": false, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects exam information outside the known eligibility, application timeline, and exam schedule fields."}, {"change_index": 4, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}, {"change_index": 5, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}, {"change_index": 6, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}, {"change_index": 7, "impact_type": "EXAM_SCHEDULE_CHANGED", "affects_eligibility": false, "affects_application_timeline": false, "affects_exam_schedule": true, "requires_eligibility_re_evaluation": false, "requires_human_review": false, "reason": "The structural change affects the exam schedule."}], "overall_requires_human_review": true, "overall_requires_eligibility_re_evaluation": false}	APPROVED	\N	497	2026-10-01 15:15:50.229633	2026-10-01 15:14:46.62378
\.


--
-- Data for Name: notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification (notification_id, student_id, exam_id, notification_type, title, message, is_read, created_at, read_at, dedupe_key, email_status, email_sent_at, email_error) FROM stdin;
3	1	\N	EXAM_UPDATED	NexStep test	Test email from NexStep.	f	2026-10-04 19:04:47.470686	\N	\N	SENT	2026-10-04 19:04:52.702653	\N
\.


--
-- Data for Name: officialnotification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.officialnotification (notification_id, exam_id, title, notification_type, release_date, application_start_date, application_end_date, official_url, pdf_path, ai_summary, ai_change_summary, approval_status, rejection_reason, downloaded_on, document_url, document_hash) FROM stdin;
1076	42	GATE 2027	EXAM	2026-08-27	\N	\N	https://gate2027ib.iitm.ac.in/GATE2027-IB.pdf	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	Retry after administrator feedback. GATE 2027 conducted by Indian Institute of Science (IISc) and Indian Institutes of Technology (IITs). Applications: 2026-09-02 to 2026-10-05. Exam: 2027-02-06 to 2027-02-07, 2027-02-13 to 2027-02-14, 2027-02-20 to 2027-02-21. 1 eligibility rule(s) extracted.	The notification removed the application start and end dates, added a clarification to the test paper selection requirement, moved the release date earlier, changed all existing exam dates to single-day events, and added an additional exam day on 2027-02-21.	APPROVED	\N	2026-10-01 15:16:08.239774	https://gate2027.iitm.ac.in/static/doc/IB/GATE2027-IB.pdf	991c8f31e58276a18da8ee52d58e1f3b8c353ace075fbbc44fb4d47ccef49002
1085	51	Engineering Services (Preliminary) Examination, 2025	EXAM	2024-09-18	\N	\N	https://www.upsc.gov.in/exams-related-info/exam-notification/archives	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\RevisedIIICalendar2025-Engl-160126.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-07 14:42:24.470099	https://www.upsc.gov.in/sites/default/files/RevisedIIICalendar2025-Engl-160126.pdf	8eac12b70b7bb105000fa4f1a711d96a2c6b6bf467b69e91510cae964597e633
1081	47	Civil Services Examination 2026	EXAM	2026-02-04	\N	\N	https://www.upsc.gov.in/sites/default/files/Notif-CSP-2026-Engl-060226Rev.pdf	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Notif-CSP-2026-Engl-060226Rev.pdf	Retry after administrator feedback. Civil Services Examination 2026 conducted by Union Public Service Commission. Exam: 2026-05-24. 1 eligibility rule(s) extracted.	\N	APPROVED	\N	2026-10-01 17:31:58.733856	https://www.upsc.gov.in/sites/default/files/Notif-CSP-2026-Engl-060226Rev.pdf	f68a7de905ff05c6ab76c6bc03ddd5ee2b835e5150f46c8760fd6eb4df82dce2
1083	49	CEN No. 07/2025 NTPC (Under Graduate)	EXAM	\N	\N	\N	https://rrbsecunderabad.gov.in	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Citi-Intimation-Slip-Notice-CEN-07-2025-English.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-07 11:03:04.7176	https://rrbsecunderabad.gov.in/wp-content/uploads/2026/04/Citi-Intimation-Slip-Notice-CEN-07-2025-English.pdf	1c585fb05d8a72ab9ae013dfd21026e8287be658bc13d9755e1721a79a63be36
1086	51	Engineering Services (Preliminary) Examination, 2025	EXAM	2024-09-18	2024-10-18	2024-11-22	https://www.upsc.gov.in/exams-related-info/exam-notification/archives	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\RevisedIIICalendar2025-Engl-160126.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-07 15:11:35.320331	https://www.upsc.gov.in/sites/default/files/RevisedIIICalendar2025-Engl-160126.pdf	8eac12b70b7bb105000fa4f1a711d96a2c6b6bf467b69e91510cae964597e633
1087	42	GATE 2027	EXAM	2026-08-27	\N	2026-09-27	https://gate2027.iitm.ac.in	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-07 15:19:51.445389	https://gate2027.iitm.ac.in/static/doc/IB/GATE2027-IB.pdf	991c8f31e58276a18da8ee52d58e1f3b8c353ace075fbbc44fb4d47ccef49002
1088	42	GATE 2027	EXAM	2026-08-27	\N	2026-09-27	https://gate2027.iitm.ac.in	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-07 15:23:01.763826	https://gate2027.iitm.ac.in/static/doc/IB/GATE2027-IB.pdf	991c8f31e58276a18da8ee52d58e1f3b8c353ace075fbbc44fb4d47ccef49002
1082	48	SSC Combined Graduate Level (CGL) 2026	EXAM	\N	\N	\N	https://ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_cgl_2026.pdf	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Notice_of_adv_cgl_2026.pdf	SSC Combined Graduate Level (CGL) 2026 conducted by Staff Selection Commission. Exam: 2026-08-01. 4 eligibility rule(s) extracted.	\N	APPROVED	\N	2026-10-07 11:02:00.951199	https://ssc.gov.in/api/attachment/uploads/masterData/NoticeBoards/Notice_of_adv_cgl_2026.pdf	54a01dda220cb8836f19983908e1f3fd14ddba8286781765a02765728a89e070
1080	46	Common Admission Test 2026 (CAT 2026)	EXAM	\N	2026-08-03	2026-09-15	https://cdn.digialm.com/per/g06/pub/32842/EForms/image/CAT2026/CAT_2026_Information_Bulletin_26-07-26.pdf	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\CAT_2026_Information_Bulletin_26-07-26.pdf	Retry after administrator feedback. Common Admission Test 2026 (CAT 2026) conducted by Indian Institutes of Management. Applications: 2026-08-03 to 2026-09-15. Exam: 2026-11-29. 3 eligibility rule(s) extracted.	\N	APPROVED	\N	2026-10-01 15:40:47.086324	https://cdn.digialm.com/per/g06/pub/32842/EForms/image/CAT2026/CAT_2026_Information_Bulletin_26-07-26.pdf	d0e77066b8ddc81ffc93effd2a0378b2bd9c87a4e5cfebf3138b2d1d4b73242b
1089	42	GATE 2027	EXAM	2026-09-27	2026-09-02	2026-10-05	https://gate2027ib.iitm.ac.in/GATE2027-IB.pdf	/opt/render/project/src/backend/storage/notifications/GATE2027-IB.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-07 10:04:42.898003	https://gate2027ib.iitm.ac.in/GATE2027-IB.pdf	81a9e59b0493c3a882953549750d973490b14a65f29931db818e7f37949865aa
1084	50	Civil Services Examination 2025	EXAM	2025-01-22	\N	\N	https://www.upsc.gov.in/sites/default/files/Notif-CSP-2025-Engl-220125.pdf	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\Notif-CSP-2025-Engl-220125.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-07 12:22:14.304128	https://www.upsc.gov.in/sites/default/files/Notif-CSP-2025-Engl-220125.pdf	dcf6dcea428efee344472af3c8d0cb5622c4b07638dabcc586c3f2ec19fe6910
1090	42	GATE 2027	EXAM	2026-09-27	2026-09-02	2026-10-05	https://gate2027ib.iitm.ac.in/GATE2027-IB.pdf	C:\\Users\\VIVEK\\Documents\\Projects\\NexStep\\backend\\storage\\notifications\\GATE2027-IB.pdf	AI-discovered official examination notification. Awaiting administrator approval.	\N	PENDING	\N	2026-10-08 11:02:39.019389	https://gate2027ib.iitm.ac.in/GATE2027-IB.pdf	81a9e59b0493c3a882953549750d973490b14a65f29931db818e7f37949865aa
\.


--
-- Data for Name: pending_signup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pending_signup (pending_id, email, name, password_hash, code_hash, expires_at, attempts, send_count, last_sent_at, created_at) FROM stdin;
2	edigaviek@gmail.com	ediga vivek	$2b$12$HsRrdhAwnErY.z3oAaQqZOULfoB/XVVhUAPnZaLRkOFg.l/zWnfMS	8e9872b4f075bf2e:b127281ae9a93be936f258181cdb393d61f49602fc534531b20baeeb866b59d0	2026-10-05 12:42:46.265517	0	1	2026-10-05 12:32:46.265517	2026-10-05 12:32:46.265517
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (student_id, name, email, password_hash, phone_number, date_of_birth, gender, account_status, created_timestamp, updated_timestamp, nationality, state, token_version) FROM stdin;
1	Rahul Sharma	rahul.test@nexstep.com	test_hash_rahul	9876543210	2004-05-15	Male	active	2026-08-16 22:09:15.697302	2026-08-16 22:09:15.697302	Indian	Telangana	\N
2	Priya Reddy	priya.test@nexstep.com	test_hash_priya	9876543211	2003-08-21	Female	active	2026-08-16 22:09:15.697302	2026-08-16 22:09:15.697302	Indian	Andhra Pradesh	\N
3	Arjun Kumar	arjun.test@nexstep.com	test_hash_arjun	9876543212	2005-01-10	Male	active	2026-08-16 22:09:15.697302	2026-08-16 22:09:15.697302	Indian	Karnataka	\N
124	Hiranya Venkata Reddy Kurri	bobbyk2706@gmail.cm	$2b$12$pTotDytiKQtDDP6fCza1U.18h7k9udqmPNPqKKGgN088PnPk4/u8y	\N	2006-06-27	\N	active	2026-09-23 21:44:06.565865	2026-09-23 21:44:06.565865	India	Andhra Pradesh	41fc9d675cb641309a83bdf7d1352f75
126	vdbgb	hiranya.pytest@nexstep.example	$2b$12$eCkYommAZlyOZoLkqVzKgeTjGYfslQ88iQs9KDHgPygs8WCo756vW	\N	2008-07-11	\N	active	2026-09-28 13:38:13.392851	2026-09-28 13:38:13.392851	india	anfhra	5831b279e2ea4724920f46fc301a1bd0
54	Phase8 Student untracked	phase8_untracked@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:28:03.332407	2026-09-21 00:28:03.332407	Indian	Kerala	\N
57	Phase8 Student untracked	phase8_untracked_798398d825d743ca91c0943d5d1c8b72@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:32:48.606332	2026-09-21 00:32:48.606332	Indian	Kerala	\N
58	Phase8 Student untracked	phase8_untracked_24aca2d81bde438cb575c6d90274935e@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:33:01.543736	2026-09-21 00:33:01.543736	Indian	Kerala	\N
59	Phase8 Student untracked	phase8_untracked_4b8ed92bd6284f5e99959b42b17e3a45@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:33:55.240995	2026-09-21 00:33:55.240995	Indian	Kerala	\N
60	Phase8 Student untracked	phase8_untracked_6aba30973c5d42a1af7d3197440a4330@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:37:05.187767	2026-09-21 00:37:05.187767	Indian	Kerala	\N
61	Phase8 Student untracked	phase8_untracked_61b91dfe7db94ffe8c2af860ed00a805@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:42:07.583238	2026-09-21 00:42:07.583238	Indian	Kerala	\N
62	Phase8 Student untracked	phase8_untracked_0ecd6f6b1bfb4859ac038feea138f69f@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:44:05.129401	2026-09-21 00:44:05.129401	Indian	Kerala	\N
63	Phase8 Student untracked	phase8_untracked_2eac67d9028e4bd78a554697e15273e0@example.com	test-password	\N	2002-01-01	Male	active	2026-09-21 00:48:29.761415	2026-09-21 00:48:29.761415	Indian	Kerala	\N
64	Phase 8 Student untracked	phase8_untracked_77429dc3b2484fc384d821ad7e9d2b05@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:00:26.892251	2026-09-21 01:00:26.892251	Indian	Kerala	1
65	Phase 8 Student active	phase8_active_5804b56d7489455c98f8c39e11b521ad@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:00:26.975562	2026-09-21 01:00:26.975562	Indian	Kerala	1
66	Phase 8 Student history	phase8_history_14c47e951bc34d0983b4b70e15610302@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:00:27.069392	2026-09-21 01:00:27.069392	Indian	Kerala	1
67	Phase 8 Student changed	phase8_changed_c23aee48a6ff488ba5b42be4b0254619@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:00:29.39587	2026-09-21 01:00:29.39587	Indian	Kerala	1
68	Phase 8 Student unchanged	phase8_unchanged_39ffc284b70043e3ac837d6c37ac6a3c@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:00:30.247214	2026-09-21 01:00:30.247214	Indian	Kerala	1
69	Phase 8 Student inactive	phase8_inactive_6e4f4f1385bd48b187cf87f7dc1cf264@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:00:30.981124	2026-09-21 01:00:30.981124	Indian	Kerala	1
70	Phase 8 Student failure	phase8_failure_7e84e920a5f144f5aee1fa0b7464382e@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:00:31.003049	2026-09-21 01:00:31.003049	Indian	Kerala	1
71	Phase 8 Student history	phase8_history_9d7edf32e7d54dae908eee8fc136dc87@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:01:49.086452	2026-09-21 01:01:49.086452	Indian	Kerala	1
72	Phase 8 Student untracked	phase8_untracked_12647597673c47e4bb1403418b9cf499@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:03:36.13307	2026-09-21 01:03:36.13307	Indian	Kerala	1
73	Phase 8 Student active	phase8_active_96bb30fabb4f47acb331623e66de1a3f@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:03:36.180839	2026-09-21 01:03:36.180839	Indian	Kerala	1
74	Phase 8 Student history	phase8_history_2edb43d07c1343799c766402047c5e91@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:03:36.225687	2026-09-21 01:03:36.225687	Indian	Kerala	1
75	Phase 8 Student changed	phase8_changed_34502e3f56614118b635a23b6d3ae043@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:03:36.261125	2026-09-21 01:03:36.261125	Indian	Kerala	1
76	Phase 8 Student unchanged	phase8_unchanged_53997a4f1f034af6af155d8a95e3f339@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:03:36.997171	2026-09-21 01:03:36.997171	Indian	Kerala	1
77	Phase 8 Student inactive	phase8_inactive_72da5b9c5b6a4cb99e601b3b41e34479@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:03:37.028889	2026-09-21 01:03:37.028889	Indian	Kerala	1
78	Phase 8 Student failure	phase8_failure_c0484728a9184d78bcd825f85a3e4f57@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:03:37.045856	2026-09-21 01:03:37.045856	Indian	Kerala	1
79	Phase 8 Student untracked	phase8_untracked_f14b14ef2a5d4145bfba9750084f05b8@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:25:34.56614	2026-09-21 01:25:34.56614	Indian	Kerala	1
80	Phase 8 Student active	phase8_active_c04b9b0f5eea46d1b4bd5685ac671a29@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:25:34.616491	2026-09-21 01:25:34.616491	Indian	Kerala	1
81	Phase 8 Student history	phase8_history_5486139d655a453985a43be8e660fab8@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:25:34.680717	2026-09-21 01:25:34.680717	Indian	Kerala	1
82	Phase 8 Student changed	phase8_changed_1ac38eb170e34b489561e9fb0bbe92bb@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:25:34.711649	2026-09-21 01:25:34.711649	Indian	Kerala	1
83	Phase 8 Student unchanged	phase8_unchanged_19938416fef84622bace0fa101cf88e2@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:25:34.731108	2026-09-21 01:25:34.731108	Indian	Kerala	1
84	Phase 8 Student inactive	phase8_inactive_48e1a23889654a0581f5384a220cbd3c@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:25:34.762883	2026-09-21 01:25:34.762883	Indian	Kerala	1
85	Phase 8 Student failure	phase8_failure_164c5d5e5e7047c0902ca30507f4296e@example.com	test-password-hash	\N	2002-01-01	Male	active	2026-09-21 01:25:34.785831	2026-09-21 01:25:34.785831	Indian	Kerala	1
86	abc	abcnjsi@email.com	xnndonco	\N	2006-06-27	Male	active	2026-09-21 01:27:11.595696	2026-09-21 01:27:11.595696	India	AP	\N
91	abc	abcnjsi_crud_test@email.com	xnndonco	\N	2006-06-27	Male	active	2026-09-21 03:06:33.969012	2026-09-21 03:06:33.969012	India	AP	\N
92	Tracked Exam Test Student	tracked-get-test@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 21:32:18.010382	2026-09-21 21:32:18.010382	Indian	Kerala	\N
93	Tracked Exam Test Student	tracked-create-test@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 21:32:18.290751	2026-09-21 21:32:18.290751	Indian	Kerala	\N
94	Tracked Exam Test Student	tracked-duplicate-test@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 21:32:18.36041	2026-09-21 21:32:18.36041	Indian	Kerala	\N
95	Tracked Exam Test Student	tracked-untrack-test@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 21:32:18.748448	2026-09-21 21:32:18.748448	Indian	Kerala	\N
96	Tracked Exam Test Student	tracked-owner-test@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 21:32:19.441532	2026-09-21 21:32:19.441532	Indian	Kerala	\N
97	Tracked Exam Test Student	tracked-attacker-test@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 21:32:19.444717	2026-09-21 21:32:19.444717	Indian	Kerala	\N
98	Tracked Exam Test Student	tracked-not-found-test@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 21:32:20.021826	2026-09-21 21:32:20.021826	Indian	Kerala	\N
123	Test Student 2	teststudent2@example.com	$2b$12$wEQMklbB7CMxvZTHBUdiVOODBx/.qAp/fwNay5eTD3aaf0/t3wpHi	\N	2004-05-15	\N	active	2026-09-23 21:22:49.289495	2026-09-23 21:22:49.289495	Indian	Kerala	cf6ac6f0b1bc4067b0de773a4a1b8c57
105	Eligibility Router Test Student	eligibility-get-empty@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:02:18.847129	2026-09-21 22:02:18.847129	Indian	Kerala	\N
106	Eligibility Router Test Student	eligibility-evaluate@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:02:19.013285	2026-09-21 22:02:19.013285	Indian	Kerala	\N
107	Eligibility Router Test Student	eligibility-get@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:02:19.136063	2026-09-21 22:02:19.136063	Indian	Kerala	\N
108	Eligibility Router Test Student	eligibility-history@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:02:19.214292	2026-09-21 22:02:19.214292	Indian	Kerala	\N
109	Eligibility Router Test Student	eligibility-owner@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:02:19.289016	2026-09-21 22:02:19.289016	Indian	Kerala	\N
110	Eligibility Router Test Student	eligibility-attacker@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:02:19.293194	2026-09-21 22:02:19.293194	Indian	Kerala	\N
111	Eligibility Re-Evaluation Test Student	reeval-not-required@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:08:59.594715	2026-09-21 22:08:59.594715	Indian	Kerala	\N
112	Eligibility Re-Evaluation Test Student	reeval-new-record@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:09:00.137282	2026-09-21 22:09:00.137282	Indian	Kerala	\N
113	Eligibility Re-Evaluation Test Student	reeval-history@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:09:00.286163	2026-09-21 22:09:00.286163	Indian	Kerala	\N
114	Eligibility Re-Evaluation Test Student	reeval-multiple-one@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:09:00.45982	2026-09-21 22:09:00.45982	Indian	Kerala	\N
115	Eligibility Re-Evaluation Test Student	reeval-multiple-two@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:09:00.467615	2026-09-21 22:09:00.467615	Indian	Kerala	\N
116	Eligibility Re-Evaluation Test Student	reeval-inactive-tracking@example.com	test-password-hash	\N	2004-01-01	Male	active	2026-09-21 22:09:00.6585	2026-09-21 22:09:00.6585	Indian	Kerala	\N
125	Bobby	hiranyavenkatareddyk@gmail.com	$2b$12$30fGpEwDvkbWW/YpppXyFuXsq/zoDonZ527A.V3mzdOiBnaBxSyOC	\N	2006-06-27	\N	active	2026-09-23 22:02:58.119118	2026-09-23 22:02:58.119118	India	Andhra Pradesh	fb457f92731f403e8041722c24811000
127	Madapati jyothi radithya 	madapatijyothiradithya@gmail.com	$2b$12$nrwiAUW/90bRCubBhU0ptOEKObK045szrvkyQLa8KXf/D15D6v.1G	\N	2007-09-05	\N	active	2026-10-01 12:12:07.591137	2026-10-01 12:12:07.591137	indian	Andhra Pradesh	72bd148e24a64d8488df643bc0bbf7e9
128	Malapati Vivekananda	vivekananda1824@gmail.com	$2b$12$ij0sdGDInjcRI0ZNEHoNdugTVAZwgDW6aiEilZJ3y5sz7cvvflf2m	\N	2006-08-15	\N	active	2026-10-01 12:22:16.786663	2026-10-01 12:22:16.786663	Indian	Telangana	903ca61a0ae446d4bcdfb0355713afbd
130	Vivek Ediga	vivek772256l@gmail.com	$2b$12$5/u5jlEA66vn.759MfaF6OfD/mStCLV9tZO1Y56NWkfkHyVMQ93cq	\N	\N	\N	active	2026-10-04 13:46:27.587287	2026-10-04 13:46:27.587287	\N	\N	274516ed2fb24613b09f7639aa0fc59f
129	vivek ediga	sparrowspidey@gmail.com	$2b$12$WqP0BQG//pVhb2OdalHdA.K6zVWsn5vB9eHNvAjrb46sJKn2VfkSu	\N	2006-05-24	\N	active	2026-10-04 13:44:39.958969	2026-10-04 13:44:39.958969	indian	telangana	2480a8be2f074cf8a2acab216ace3062
131	vivek	vivekuesi@gmail.com	$2b$12$kDmtYZ8SiZUO8gqfrq6Gq.RqQSo3/kq8VIL0G2Vu77IoUX7jz7mAa	\N	2006-05-24	\N	active	2026-10-04 18:17:28.540359	2026-10-04 18:17:28.540359	indian	telangaana	437990da62fd420bb96e3f787efe2cfc
132	Vivek	edigavivek24bcs0229@iiitkottayam.ac.in	$2b$12$erPQIenpb6YxYXYfsKq/kuRjMvXICM64NazQ96qyKPqdzQXCmpqGu	\N	2006-05-24	\N	active	2026-10-05 03:40:56.414139	2026-10-05 03:40:56.414139	Indian	Telangana	4b44ef7c4b904b9e91edac274ccfb2d2
133	EDIGA vivek	hvrk27@gmail.com	$2b$12$GyVqxsFlK0vZciUQcfRTMuNK2JI/5za9SzYWykEUBsC66KAD2gr8m	\N	2005-11-09	\N	active	2026-10-05 07:05:54.87735	2026-10-05 07:05:54.87735	indian	keralam	8f386c4135414d7b9a3036713fe56dc4
134	Reshmitha	reshmithag09@gmail.com	$2b$12$.gaMsz7Q.H8vQNZ5LJrNgOjwN7PuP1wtFa02YlqLqu8.854/3T1jW	\N	2007-02-09	\N	active	2026-10-05 17:14:04.788687	2026-10-05 17:14:04.788687	Indian	AP	d2e2f9cea199427a87e19760b8cc3366
\.


--
-- Data for Name: studentexameligibility; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.studentexameligibility (eligibility_id, student_id, exam_id, eligibility_status, reason, evaluated_at) FROM stdin;
306	127	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:43:39.526869
307	127	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:43:39.590813
308	127	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:45:50.377719
309	127	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:45:50.435069
310	127	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:50:41.028111
311	127	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:50:41.093965
312	128	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:55:25.784648
313	128	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:55:25.921061
314	128	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:56:25.447173
315	128	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-01 17:56:25.454528
316	129	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-04 20:20:12.29489
317	129	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-04 20:20:13.23534
318	131	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-04 23:48:24.464315
319	131	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-04 23:48:25.67833
320	131	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-04 23:49:27.980635
321	131	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-04 23:49:28.766679
322	132	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-05 09:11:26.181172
323	132	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-05 09:11:26.228582
324	133	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-05 12:37:30.886007
325	133	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-05 12:37:31.016351
326	134	42	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-05 17:14:56.197016
327	134	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-05 17:14:56.19927
328	134	47	ELIGIBLE	All applicable eligibility requirements were satisfied.	2026-10-05 17:15:29.609014
\.


--
-- Data for Name: trackedexam; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trackedexam (tracking_id, student_id, exam_id, tracked_at, tracking_status) FROM stdin;
\.


--
-- Data for Name: work_experience; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.work_experience (work_experience_id, student_id, company, role, duration) FROM stdin;
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: realtime; Owner: supabase_admin
--

COPY realtime.schema_migrations (version, inserted_at) FROM stdin;
20211116024918	2026-09-30 06:32:52
20211116045059	2026-09-30 06:32:52
20211116050929	2026-09-30 06:32:52
20211116051442	2026-09-30 06:32:52
20211116212300	2026-09-30 06:32:52
20211116213355	2026-09-30 06:32:52
20211116213934	2026-09-30 06:32:52
20211116214523	2026-09-30 06:32:52
20211122062447	2026-09-30 06:32:52
20211124070109	2026-09-30 06:32:52
20211202204204	2026-09-30 06:32:52
20211202204605	2026-09-30 06:32:52
20211210212804	2026-09-30 06:32:52
20211228014915	2026-09-30 06:32:52
20220107221237	2026-09-30 06:32:52
20220228202821	2026-09-30 06:32:52
20220312004840	2026-09-30 06:32:52
20220603231003	2026-09-30 06:32:52
20220603232444	2026-09-30 06:32:52
20220615214548	2026-09-30 06:32:52
20220712093339	2026-09-30 06:32:52
20220908172859	2026-09-30 06:32:52
20220916233421	2026-09-30 06:32:52
20230119133233	2026-09-30 06:32:52
20230128025114	2026-09-30 06:32:52
20230128025212	2026-09-30 06:32:52
20230227211149	2026-09-30 06:32:52
20230228184745	2026-09-30 06:32:52
20230308225145	2026-09-30 06:32:52
20230328144023	2026-09-30 06:32:52
20231018144023	2026-09-30 06:32:52
20231204144023	2026-09-30 06:32:52
20231204144024	2026-09-30 06:32:52
20231204144025	2026-09-30 06:32:52
20240108234812	2026-09-30 06:32:52
20240109165339	2026-09-30 06:32:52
20240227174441	2026-09-30 06:32:52
20240311171622	2026-09-30 06:32:52
20240321100241	2026-09-30 06:32:52
20240401105812	2026-09-30 06:32:52
20240418121054	2026-09-30 06:32:52
20240523004032	2026-09-30 06:32:52
20240618124746	2026-09-30 06:32:52
20240801235015	2026-09-30 06:32:52
20240805133720	2026-09-30 06:32:52
20240827160934	2026-09-30 06:32:52
20240919163303	2026-09-30 06:32:52
20240919163305	2026-09-30 06:32:52
20241019105805	2026-09-30 06:32:52
20241030150047	2026-09-30 06:32:52
20241108114728	2026-09-30 06:32:52
20241121104152	2026-09-30 06:32:52
20241130184212	2026-09-30 06:32:52
20241220035512	2026-09-30 06:32:52
20241220123912	2026-09-30 06:32:52
20241224161212	2026-09-30 06:32:52
20250107150512	2026-09-30 06:32:52
20250110162412	2026-09-30 06:32:52
20250123174212	2026-09-30 06:32:52
20250128220012	2026-09-30 06:32:52
20250506224012	2026-09-30 06:32:52
20250523164012	2026-09-30 06:32:52
20250714121412	2026-09-30 06:32:52
20250905041441	2026-09-30 06:32:52
20251103001201	2026-09-30 06:32:52
20251120212548	2026-09-30 06:32:52
20251120215549	2026-09-30 06:32:52
20260218120000	2026-09-30 06:32:52
20260326120000	2026-09-30 06:32:52
20260514120000	2026-09-30 06:32:52
20260527120000	2026-09-30 06:32:52
20260528120000	2026-09-30 06:32:52
20260603120000	2026-09-30 06:32:52
20260605120000	2026-09-30 06:32:52
20260606110000	2026-09-30 06:32:52
20260616120000	2026-09-30 06:32:52
20260624120000	2026-09-30 06:32:52
20260626120000	2026-09-30 06:32:52
20260706120000	2026-09-30 06:32:52
20260707120000	2026-09-30 06:32:52
20260709120000	2026-09-30 06:32:52
20260714120000	2026-09-30 06:32:52
20260827120000	2026-09-30 06:32:52
20260914120000	2026-09-30 06:32:52
20260916120000	2026-09-30 06:32:52
20260922120000	2026-09-30 06:32:52
20260925120000	2026-09-30 06:32:52
20260928120000	2026-10-05 13:46:03
\.


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: realtime; Owner: supabase_realtime_admin
--

COPY realtime.subscription (id, subscription_id, entity, filters, claims, created_at, action_filter, selected_columns) FROM stdin;
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.buckets (id, name, owner, created_at, updated_at, public, avif_autodetection, file_size_limit, allowed_mime_types, owner_id, type, versioning_status, lifecycle_configuration, lifecycle_configuration_generation) FROM stdin;
\.


--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.buckets_analytics (name, type, format, created_at, updated_at, id, deleted_at) FROM stdin;
\.


--
-- Data for Name: buckets_vectors; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.buckets_vectors (id, type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: migrations; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.migrations (id, name, hash, executed_at) FROM stdin;
0	create-migrations-table	e18db593bcde2aca2a408c4d1100f6abba2195df	2026-09-30 06:32:51.157398
1	initialmigration	6ab16121fbaa08bbd11b712d05f358f9b555d777	2026-09-30 06:32:51.173814
2	storage-schema	f6a1fa2c93cbcd16d4e487b362e45fca157a8dbd	2026-09-30 06:32:51.176688
3	pathtoken-column	2cb1b0004b817b29d5b0a971af16bafeede4b70d	2026-09-30 06:32:51.204525
4	add-migrations-rls	427c5b63fe1c5937495d9c635c263ee7a5905058	2026-09-30 06:32:51.242959
5	add-size-functions	79e081a1455b63666c1294a440f8ad4b1e6a7f84	2026-09-30 06:32:51.247638
6	change-column-name-in-get-size	ded78e2f1b5d7e616117897e6443a925965b30d2	2026-09-30 06:32:51.25595
7	add-rls-to-buckets	e7e7f86adbc51049f341dfe8d30256c1abca17aa	2026-09-30 06:32:51.259506
8	add-public-to-buckets	fd670db39ed65f9d08b01db09d6202503ca2bab3	2026-09-30 06:32:51.26357
9	fix-search-function	af597a1b590c70519b464a4ab3be54490712796b	2026-09-30 06:32:51.267343
10	search-files-search-function	b595f05e92f7e91211af1bbfe9c6a13bb3391e16	2026-09-30 06:32:51.271301
11	add-trigger-to-auto-update-updated_at-column	7425bdb14366d1739fa8a18c83100636d74dcaa2	2026-09-30 06:32:51.275231
12	add-automatic-avif-detection-flag	8e92e1266eb29518b6a4c5313ab8f29dd0d08df9	2026-09-30 06:32:51.279832
13	add-bucket-custom-limits	cce962054138135cd9a8c4bcd531598684b25e7d	2026-09-30 06:32:51.283218
14	use-bytes-for-max-size	941c41b346f9802b411f06f30e972ad4744dad27	2026-09-30 06:32:51.286594
15	add-can-insert-object-function	934146bc38ead475f4ef4b555c524ee5d66799e5	2026-09-30 06:32:51.319727
16	add-version	76debf38d3fd07dcfc747ca49096457d95b1221b	2026-09-30 06:32:51.325908
17	drop-owner-foreign-key	f1cbb288f1b7a4c1eb8c38504b80ae2a0153d101	2026-09-30 06:32:51.330921
18	add_owner_id_column_deprecate_owner	e7a511b379110b08e2f214be852c35414749fe66	2026-09-30 06:32:51.333638
19	alter-default-value-objects-id	02e5e22a78626187e00d173dc45f58fa66a4f043	2026-09-30 06:32:51.340902
20	list-objects-with-delimiter	cd694ae708e51ba82bf012bba00caf4f3b6393b7	2026-09-30 06:32:51.343973
21	s3-multipart-uploads	8c804d4a566c40cd1e4cc5b3725a664a9303657f	2026-09-30 06:32:51.353343
22	s3-multipart-uploads-big-ints	9737dc258d2397953c9953d9b86920b8be0cdb73	2026-09-30 06:32:51.383916
23	optimize-search-function	9d7e604cddc4b56a5422dc68c9313f4a1b6f132c	2026-09-30 06:32:51.410294
24	operation-function	8312e37c2bf9e76bbe841aa5fda889206d2bf8aa	2026-09-30 06:32:51.415251
25	custom-metadata	d974c6057c3db1c1f847afa0e291e6165693b990	2026-09-30 06:32:51.419147
26	objects-prefixes	215cabcb7f78121892a5a2037a09fedf9a1ae322	2026-09-30 06:32:51.424188
27	search-v2	859ba38092ac96eb3964d83bf53ccc0b141663a6	2026-09-30 06:32:51.428901
28	object-bucket-name-sorting	c73a2b5b5d4041e39705814fd3a1b95502d38ce4	2026-09-30 06:32:51.431384
29	create-prefixes	ad2c1207f76703d11a9f9007f821620017a66c21	2026-09-30 06:32:51.434979
30	update-object-levels	2be814ff05c8252fdfdc7cfb4b7f5c7e17f0bed6	2026-09-30 06:32:51.437408
31	objects-level-index	b40367c14c3440ec75f19bbce2d71e914ddd3da0	2026-09-30 06:32:51.439839
32	backward-compatible-index-on-objects	e0c37182b0f7aee3efd823298fb3c76f1042c0f7	2026-09-30 06:32:51.442956
33	backward-compatible-index-on-prefixes	b480e99ed951e0900f033ec4eb34b5bdcb4e3d49	2026-09-30 06:32:51.445301
34	optimize-search-function-v1	ca80a3dc7bfef894df17108785ce29a7fc8ee456	2026-09-30 06:32:51.448793
35	add-insert-trigger-prefixes	458fe0ffd07ec53f5e3ce9df51bfdf4861929ccc	2026-09-30 06:32:51.451247
36	optimise-existing-functions	6ae5fca6af5c55abe95369cd4f93985d1814ca8f	2026-09-30 06:32:51.453557
37	add-bucket-name-length-trigger	3944135b4e3e8b22d6d4cbb568fe3b0b51df15c1	2026-09-30 06:32:51.456021
38	iceberg-catalog-flag-on-buckets	02716b81ceec9705aed84aa1501657095b32e5c5	2026-09-30 06:32:51.460447
39	add-search-v2-sort-support	6706c5f2928846abee18461279799ad12b279b78	2026-09-30 06:32:51.478014
40	fix-prefix-race-conditions-optimized	7ad69982ae2d372b21f48fc4829ae9752c518f6b	2026-09-30 06:32:51.48094
41	add-object-level-update-trigger	07fcf1a22165849b7a029deed059ffcde08d1ae0	2026-09-30 06:32:51.483571
42	rollback-prefix-triggers	771479077764adc09e2ea2043eb627503c034cd4	2026-09-30 06:32:51.488058
43	fix-object-level	84b35d6caca9d937478ad8a797491f38b8c2979f	2026-09-30 06:32:51.490533
44	vector-bucket-type	99c20c0ffd52bb1ff1f32fb992f3b351e3ef8fb3	2026-09-30 06:32:51.493984
45	vector-buckets	049e27196d77a7cb76497a85afae669d8b230953	2026-09-30 06:32:51.497568
46	buckets-objects-grants	fedeb96d60fefd8e02ab3ded9fbde05632f84aed	2026-09-30 06:32:51.508378
47	iceberg-table-metadata	649df56855c24d8b36dd4cc1aeb8251aa9ad42c2	2026-09-30 06:32:51.512274
48	iceberg-catalog-ids	e0e8b460c609b9999ccd0df9ad14294613eed939	2026-09-30 06:32:51.514767
49	buckets-objects-grants-postgres	072b1195d0d5a2f888af6b2302a1938dd94b8b3d	2026-09-30 06:32:51.530608
50	search-v2-optimised	6323ac4f850aa14e7387eb32102869578b5bd478	2026-09-30 06:32:51.534441
51	index-backward-compatible-search	2ee395d433f76e38bcd3856debaf6e0e5b674011	2026-09-30 06:32:51.907298
52	drop-not-used-indexes-and-functions	5cc44c8696749ac11dd0dc37f2a3802075f3a171	2026-09-30 06:32:51.909592
53	drop-index-lower-name	d0cb18777d9e2a98ebe0bc5cc7a42e57ebe41854	2026-09-30 06:32:51.920175
54	drop-index-object-level	6289e048b1472da17c31a7eba1ded625a6457e67	2026-09-30 06:32:51.922335
55	prevent-direct-deletes	262a4798d5e0f2e7c8970232e03ce8be695d5819	2026-09-30 06:32:51.923751
56	fix-optimized-search-function	b823ed1e418101032fa01374edc9a436e54e3ed4	2026-09-30 06:32:51.964999
57	s3-multipart-uploads-metadata	f127886e00d1b374fadbc7c6b31e09336aad5287	2026-09-30 06:32:51.969542
58	operation-ergonomics	00ca5d483b3fe0d522133d9002ccc5df98365120	2026-09-30 06:32:51.972528
59	drop-unused-functions	38456f13e39691c2bbb4b5151d0d1cdbabd4a8c4	2026-09-30 06:32:51.976233
60	optimize-existing-functions-again	db35e1c91a9201e59f4fef8d972c2f277d68b157	2026-09-30 06:32:51.979515
61	mark-filename-immutable	fe0096517ae9d60aaec1d110172ba9036dc66bb7	2026-09-30 06:32:51.982979
62	object-versioning-core	0b855f00ff3be0bfca91efee02a9858912491a9a	2026-09-30 06:32:51.986493
63	fix-search-name-relative-to-prefix	c7485e417624f795ce8bb2da21927f48e088904d	2026-09-30 06:32:51.992802
64	fix-search-by-timestamp-sqli	0af424ecd388a39bb1645184b222185a12149675	2026-09-30 06:32:51.997565
65	objects-key-version-index	da319c4b89ba800ce795d1b699f3a70675138058	2026-09-30 06:32:52.009545
66	objects-current-version-index	191466c93aa2c46a00e36505577c5fcab8d7cb4b	2026-09-30 06:32:52.018253
67	objects-null-version-index	15bfe8c35b66642b6c78ba60060fa8793bd2207a	2026-09-30 06:32:52.304978
68	bucket-lifecycle-configuration	3c08f6f889922f399519722a932b51007c11bebc	2026-09-30 06:32:52.30767
69	validate-bucket-lifecycle-constraints	4febacaaaa0e61e2b783bef081fe03a287e65eb3	2026-09-30 06:32:52.315536
70	list-objects-with-versions	5c17c3777616cd8d7b18b82835525fa3205af57b	2026-09-30 06:32:52.319008
71	objects-delete-marker-index	6d14858e66c66f8d6accf8a2630aefd1527fddba	2026-09-30 06:32:52.34315
72	drop-bucketid-objname-index	302beb09e1b469d7d4db19566f2389d280b64aa3	2026-09-30 06:32:52.348783
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.objects (id, bucket_id, name, owner, created_at, updated_at, last_accessed_at, metadata, version, owner_id, user_metadata, archived_at, is_delete_marker, is_versioned) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.s3_multipart_uploads (id, in_progress_size, upload_signature, bucket_id, key, version, owner_id, created_at, user_metadata, metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.s3_multipart_uploads_parts (id, upload_id, size, part_number, bucket_id, key, etag, owner_id, version, created_at) FROM stdin;
\.


--
-- Data for Name: vector_indexes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY storage.vector_indexes (id, name, bucket_id, data_type, dimension, distance_metric, metadata_configuration, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--

COPY vault.secrets (id, name, description, secret, key_id, nonce, created_at, updated_at) FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('auth.refresh_tokens_id_seq', 1, false);


--
-- Name: admin_admin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admin_admin_id_seq', 497, true);


--
-- Name: auditlog_audit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auditlog_audit_id_seq', 1, true);


--
-- Name: chathistory_chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chathistory_chat_id_seq', 2, true);


--
-- Name: conducting_body_body_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.conducting_body_body_id_seq', 37, true);


--
-- Name: education_education_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.education_education_id_seq', 220, true);


--
-- Name: eligibilityattribute_attrubute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.eligibilityattribute_attrubute_id_seq', 8, true);


--
-- Name: eligibilityrule_rule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.eligibilityrule_rule_id_seq', 1052, true);


--
-- Name: eligibilityrulegroup_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.eligibilityrulegroup_group_id_seq', 671, true);


--
-- Name: exam_exam_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exam_exam_id_seq', 51, true);


--
-- Name: examdate_exam_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.examdate_exam_date_id_seq', 377, true);


--
-- Name: extractionhistory_extraction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extractionhistory_extraction_id_seq', 231, true);


--
-- Name: monitoringreview_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.monitoringreview_review_id_seq', 621, true);


--
-- Name: notification_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notification_notification_id_seq', 3, true);


--
-- Name: officialnotification_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.officialnotification_notification_id_seq', 1090, true);


--
-- Name: pending_signup_pending_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pending_signup_pending_id_seq', 4, true);


--
-- Name: student_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_student_id_seq', 134, true);


--
-- Name: studentexameligibility_eligibility_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.studentexameligibility_eligibility_id_seq', 328, true);


--
-- Name: trackedexam_tracking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.trackedexam_tracking_id_seq', 290, true);


--
-- Name: work_experience_work_experience_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.work_experience_work_experience_id_seq', 1, false);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: realtime; Owner: supabase_realtime_admin
--

SELECT pg_catalog.setval('realtime.subscription_id_seq', 1, false);


--
-- Name: mfa_amr_claims amr_id_pk; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT amr_id_pk PRIMARY KEY (id);


--
-- Name: audit_log_entries audit_log_entries_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.audit_log_entries
    ADD CONSTRAINT audit_log_entries_pkey PRIMARY KEY (id);


--
-- Name: custom_oauth_providers custom_oauth_providers_identifier_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.custom_oauth_providers
    ADD CONSTRAINT custom_oauth_providers_identifier_key UNIQUE (identifier);


--
-- Name: custom_oauth_providers custom_oauth_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.custom_oauth_providers
    ADD CONSTRAINT custom_oauth_providers_pkey PRIMARY KEY (id);


--
-- Name: flow_state flow_state_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.flow_state
    ADD CONSTRAINT flow_state_pkey PRIMARY KEY (id);


--
-- Name: identities identities_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_pkey PRIMARY KEY (id);


--
-- Name: identities identities_provider_id_provider_unique; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_provider_id_provider_unique UNIQUE (provider_id, provider);


--
-- Name: instances instances_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.instances
    ADD CONSTRAINT instances_pkey PRIMARY KEY (id);


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_authentication_method_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_authentication_method_pkey UNIQUE (session_id, authentication_method);


--
-- Name: mfa_challenges mfa_challenges_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_pkey PRIMARY KEY (id);


--
-- Name: mfa_factors mfa_factors_last_challenged_at_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_last_challenged_at_key UNIQUE (last_challenged_at);


--
-- Name: mfa_factors mfa_factors_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_pkey PRIMARY KEY (id);


--
-- Name: mfa_recovery_code_sets mfa_recovery_code_sets_mfa_factor_id_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_recovery_code_sets
    ADD CONSTRAINT mfa_recovery_code_sets_mfa_factor_id_key UNIQUE (mfa_factor_id);


--
-- Name: mfa_recovery_code_sets mfa_recovery_code_sets_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_recovery_code_sets
    ADD CONSTRAINT mfa_recovery_code_sets_pkey PRIMARY KEY (id);


--
-- Name: mfa_recovery_code_sets mfa_recovery_code_sets_user_id_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_recovery_code_sets
    ADD CONSTRAINT mfa_recovery_code_sets_user_id_key UNIQUE (user_id);


--
-- Name: mfa_recovery_codes mfa_recovery_codes_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_recovery_codes
    ADD CONSTRAINT mfa_recovery_codes_pkey PRIMARY KEY (id);


--
-- Name: oauth_authorizations oauth_authorizations_authorization_code_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_authorization_code_key UNIQUE (authorization_code);


--
-- Name: oauth_authorizations oauth_authorizations_authorization_id_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_authorization_id_key UNIQUE (authorization_id);


--
-- Name: oauth_authorizations oauth_authorizations_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_pkey PRIMARY KEY (id);


--
-- Name: oauth_client_states oauth_client_states_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_client_states
    ADD CONSTRAINT oauth_client_states_pkey PRIMARY KEY (id);


--
-- Name: oauth_clients oauth_clients_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_clients
    ADD CONSTRAINT oauth_clients_pkey PRIMARY KEY (id);


--
-- Name: oauth_consents oauth_consents_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_pkey PRIMARY KEY (id);


--
-- Name: oauth_consents oauth_consents_user_client_unique; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_user_client_unique UNIQUE (user_id, client_id);


--
-- Name: one_time_tokens one_time_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_token_unique; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_unique UNIQUE (token);


--
-- Name: saml_providers saml_providers_entity_id_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_entity_id_key UNIQUE (entity_id);


--
-- Name: saml_providers saml_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_pkey PRIMARY KEY (id);


--
-- Name: saml_relay_states saml_relay_states_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: scim_tokens scim_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.scim_tokens
    ADD CONSTRAINT scim_tokens_pkey PRIMARY KEY (id);


--
-- Name: scim_users scim_users_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.scim_users
    ADD CONSTRAINT scim_users_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sso_domains sso_domains_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_pkey PRIMARY KEY (id);


--
-- Name: sso_providers sso_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sso_providers
    ADD CONSTRAINT sso_providers_pkey PRIMARY KEY (id);


--
-- Name: users users_phone_key; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: webauthn_challenges webauthn_challenges_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_challenges
    ADD CONSTRAINT webauthn_challenges_pkey PRIMARY KEY (id);


--
-- Name: webauthn_credentials webauthn_credentials_pkey; Type: CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_credentials
    ADD CONSTRAINT webauthn_credentials_pkey PRIMARY KEY (id);


--
-- Name: admin admin_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_email_key UNIQUE (email);


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (admin_id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: auditlog auditlog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditlog
    ADD CONSTRAINT auditlog_pkey PRIMARY KEY (audit_id);


--
-- Name: chathistory chathistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chathistory
    ADD CONSTRAINT chathistory_pkey PRIMARY KEY (chat_id);


--
-- Name: conducting_body conducting_body_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conducting_body
    ADD CONSTRAINT conducting_body_pkey PRIMARY KEY (body_id);


--
-- Name: education education_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT education_pkey PRIMARY KEY (education_id);


--
-- Name: eligibilityattribute eligibilityattribute_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityattribute
    ADD CONSTRAINT eligibilityattribute_pkey PRIMARY KEY (attribute_id);


--
-- Name: eligibilityrule eligibilityrule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrule
    ADD CONSTRAINT eligibilityrule_pkey PRIMARY KEY (rule_id);


--
-- Name: eligibilityrulegroup eligibilityrulegroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrulegroup
    ADD CONSTRAINT eligibilityrulegroup_pkey PRIMARY KEY (group_id);


--
-- Name: exam exam_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_name_key UNIQUE (name);


--
-- Name: exam exam_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_pkey PRIMARY KEY (exam_id);


--
-- Name: examdate examdate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examdate
    ADD CONSTRAINT examdate_pkey PRIMARY KEY (exam_date_id);


--
-- Name: extractionhistory extractionhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extractionhistory
    ADD CONSTRAINT extractionhistory_pkey PRIMARY KEY (extraction_id);


--
-- Name: monitoringreview monitoringreview_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitoringreview
    ADD CONSTRAINT monitoringreview_pkey PRIMARY KEY (review_id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (notification_id);


--
-- Name: officialnotification officialnotification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.officialnotification
    ADD CONSTRAINT officialnotification_pkey PRIMARY KEY (notification_id);


--
-- Name: pending_signup pending_signup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pending_signup
    ADD CONSTRAINT pending_signup_pkey PRIMARY KEY (pending_id);


--
-- Name: student student_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_email_key UNIQUE (email);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (student_id);


--
-- Name: studentexameligibility studentexameligibility_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studentexameligibility
    ADD CONSTRAINT studentexameligibility_pkey PRIMARY KEY (eligibility_id);


--
-- Name: trackedexam trackedexam_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trackedexam
    ADD CONSTRAINT trackedexam_pkey PRIMARY KEY (tracking_id);


--
-- Name: conducting_body uq_conducting_body_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conducting_body
    ADD CONSTRAINT uq_conducting_body_name UNIQUE (name);


--
-- Name: trackedexam uq_student_tracked_exam; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trackedexam
    ADD CONSTRAINT uq_student_tracked_exam UNIQUE (student_id, exam_id);


--
-- Name: work_experience work_experience_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_experience
    ADD CONSTRAINT work_experience_pkey PRIMARY KEY (work_experience_id);


--
-- Name: messages messages_payload_exclusive; Type: CHECK CONSTRAINT; Schema: realtime; Owner: supabase_realtime_admin
--

ALTER TABLE realtime.messages
    ADD CONSTRAINT messages_payload_exclusive CHECK (((payload IS NULL) OR (binary_payload IS NULL))) NOT VALID;


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: realtime; Owner: supabase_realtime_admin
--

ALTER TABLE ONLY realtime.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id, inserted_at);


--
-- Name: subscription pk_subscription; Type: CONSTRAINT; Schema: realtime; Owner: supabase_realtime_admin
--

ALTER TABLE ONLY realtime.subscription
    ADD CONSTRAINT pk_subscription PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: realtime; Owner: supabase_admin
--

ALTER TABLE ONLY realtime.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: buckets_analytics buckets_analytics_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.buckets_analytics
    ADD CONSTRAINT buckets_analytics_pkey PRIMARY KEY (id);


--
-- Name: buckets buckets_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.buckets
    ADD CONSTRAINT buckets_pkey PRIMARY KEY (id);


--
-- Name: buckets_vectors buckets_vectors_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.buckets_vectors
    ADD CONSTRAINT buckets_vectors_pkey PRIMARY KEY (id);


--
-- Name: migrations migrations_name_key; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_name_key UNIQUE (name);


--
-- Name: migrations migrations_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_pkey PRIMARY KEY (id);


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_pkey PRIMARY KEY (id);


--
-- Name: vector_indexes vector_indexes_pkey; Type: CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.vector_indexes
    ADD CONSTRAINT vector_indexes_pkey PRIMARY KEY (id);


--
-- Name: audit_logs_instance_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX audit_logs_instance_id_idx ON auth.audit_log_entries USING btree (instance_id);


--
-- Name: confirmation_token_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX confirmation_token_idx ON auth.users USING btree (confirmation_token) WHERE ((confirmation_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: custom_oauth_providers_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_created_at_idx ON auth.custom_oauth_providers USING btree (created_at);


--
-- Name: custom_oauth_providers_enabled_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_enabled_idx ON auth.custom_oauth_providers USING btree (enabled);


--
-- Name: custom_oauth_providers_identifier_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_identifier_idx ON auth.custom_oauth_providers USING btree (identifier);


--
-- Name: custom_oauth_providers_provider_type_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX custom_oauth_providers_provider_type_idx ON auth.custom_oauth_providers USING btree (provider_type);


--
-- Name: email_change_token_current_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX email_change_token_current_idx ON auth.users USING btree (email_change_token_current) WHERE ((email_change_token_current)::text !~ '^[0-9 ]*$'::text);


--
-- Name: email_change_token_new_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX email_change_token_new_idx ON auth.users USING btree (email_change_token_new) WHERE ((email_change_token_new)::text !~ '^[0-9 ]*$'::text);


--
-- Name: factor_id_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX factor_id_created_at_idx ON auth.mfa_factors USING btree (user_id, created_at);


--
-- Name: flow_state_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX flow_state_created_at_idx ON auth.flow_state USING btree (created_at DESC);


--
-- Name: identities_email_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX identities_email_idx ON auth.identities USING btree (email text_pattern_ops);


--
-- Name: INDEX identities_email_idx; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON INDEX auth.identities_email_idx IS 'Auth: Ensures indexed queries on the email column';


--
-- Name: identities_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX identities_user_id_idx ON auth.identities USING btree (user_id);


--
-- Name: idx_auth_code; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_auth_code ON auth.flow_state USING btree (auth_code);


--
-- Name: idx_oauth_client_states_created_at; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_oauth_client_states_created_at ON auth.oauth_client_states USING btree (created_at);


--
-- Name: idx_user_id_auth_method; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_user_id_auth_method ON auth.flow_state USING btree (user_id, authentication_method);


--
-- Name: idx_users_created_at_desc; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_created_at_desc ON auth.users USING btree (created_at DESC);


--
-- Name: idx_users_email; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_email ON auth.users USING btree (email);


--
-- Name: idx_users_last_sign_in_at_desc; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_last_sign_in_at_desc ON auth.users USING btree (last_sign_in_at DESC);


--
-- Name: idx_users_name; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX idx_users_name ON auth.users USING btree (((raw_user_meta_data ->> 'name'::text))) WHERE ((raw_user_meta_data ->> 'name'::text) IS NOT NULL);


--
-- Name: mfa_challenge_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX mfa_challenge_created_at_idx ON auth.mfa_challenges USING btree (created_at DESC);


--
-- Name: mfa_factors_user_friendly_name_unique; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX mfa_factors_user_friendly_name_unique ON auth.mfa_factors USING btree (friendly_name, user_id) WHERE (TRIM(BOTH FROM friendly_name) <> ''::text);


--
-- Name: mfa_factors_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX mfa_factors_user_id_idx ON auth.mfa_factors USING btree (user_id);


--
-- Name: mfa_recovery_codes_set_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX mfa_recovery_codes_set_id_idx ON auth.mfa_recovery_codes USING btree (mfa_recovery_code_set_id);


--
-- Name: oauth_auth_pending_exp_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_auth_pending_exp_idx ON auth.oauth_authorizations USING btree (expires_at) WHERE (status = 'pending'::auth.oauth_authorization_status);


--
-- Name: oauth_clients_deleted_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_clients_deleted_at_idx ON auth.oauth_clients USING btree (deleted_at);


--
-- Name: oauth_consents_active_client_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_consents_active_client_idx ON auth.oauth_consents USING btree (client_id) WHERE (revoked_at IS NULL);


--
-- Name: oauth_consents_active_user_client_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_consents_active_user_client_idx ON auth.oauth_consents USING btree (user_id, client_id) WHERE (revoked_at IS NULL);


--
-- Name: oauth_consents_user_order_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX oauth_consents_user_order_idx ON auth.oauth_consents USING btree (user_id, granted_at DESC);


--
-- Name: one_time_tokens_relates_to_hash_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX one_time_tokens_relates_to_hash_idx ON auth.one_time_tokens USING hash (relates_to);


--
-- Name: one_time_tokens_token_hash_hash_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX one_time_tokens_token_hash_hash_idx ON auth.one_time_tokens USING hash (token_hash);


--
-- Name: one_time_tokens_user_id_token_type_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX one_time_tokens_user_id_token_type_key ON auth.one_time_tokens USING btree (user_id, token_type);


--
-- Name: reauthentication_token_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX reauthentication_token_idx ON auth.users USING btree (reauthentication_token) WHERE ((reauthentication_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: recovery_token_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX recovery_token_idx ON auth.users USING btree (recovery_token) WHERE ((recovery_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: refresh_tokens_instance_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_instance_id_idx ON auth.refresh_tokens USING btree (instance_id);


--
-- Name: refresh_tokens_instance_id_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_instance_id_user_id_idx ON auth.refresh_tokens USING btree (instance_id, user_id);


--
-- Name: refresh_tokens_parent_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_parent_idx ON auth.refresh_tokens USING btree (parent);


--
-- Name: refresh_tokens_session_id_revoked_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_session_id_revoked_idx ON auth.refresh_tokens USING btree (session_id, revoked);


--
-- Name: refresh_tokens_updated_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX refresh_tokens_updated_at_idx ON auth.refresh_tokens USING btree (updated_at DESC);


--
-- Name: saml_providers_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_providers_sso_provider_id_idx ON auth.saml_providers USING btree (sso_provider_id);


--
-- Name: saml_relay_states_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_relay_states_created_at_idx ON auth.saml_relay_states USING btree (created_at DESC);


--
-- Name: saml_relay_states_for_email_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_relay_states_for_email_idx ON auth.saml_relay_states USING btree (for_email);


--
-- Name: saml_relay_states_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX saml_relay_states_sso_provider_id_idx ON auth.saml_relay_states USING btree (sso_provider_id);


--
-- Name: scim_tokens_expires_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_tokens_expires_at_idx ON auth.scim_tokens USING btree (expires_at);


--
-- Name: scim_tokens_revoked_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_tokens_revoked_at_idx ON auth.scim_tokens USING btree (revoked_at);


--
-- Name: scim_tokens_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_tokens_sso_provider_id_idx ON auth.scim_tokens USING btree (sso_provider_id);


--
-- Name: scim_tokens_token_hash_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX scim_tokens_token_hash_key ON auth.scim_tokens USING btree (token_hash);


--
-- Name: scim_users_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_users_created_at_idx ON auth.scim_users USING btree (sso_provider_id, created_at, id) WHERE (deleted_at IS NULL);


--
-- Name: scim_users_deleted_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_users_deleted_at_idx ON auth.scim_users USING btree (deleted_at);


--
-- Name: scim_users_external_id_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX scim_users_external_id_key ON auth.scim_users USING btree (sso_provider_id, external_id) WHERE ((external_id IS NOT NULL) AND (deleted_at IS NULL));


--
-- Name: scim_users_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_users_id_idx ON auth.scim_users USING btree (sso_provider_id, id) WHERE (deleted_at IS NULL);


--
-- Name: scim_users_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_users_sso_provider_id_idx ON auth.scim_users USING btree (sso_provider_id);


--
-- Name: scim_users_updated_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_users_updated_at_idx ON auth.scim_users USING btree (sso_provider_id, updated_at, id) WHERE (deleted_at IS NULL);


--
-- Name: scim_users_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_users_user_id_idx ON auth.scim_users USING btree (user_id);


--
-- Name: scim_users_user_name_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX scim_users_user_name_idx ON auth.scim_users USING btree (sso_provider_id, user_name COLLATE "C", id) WHERE (deleted_at IS NULL);


--
-- Name: scim_users_user_name_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX scim_users_user_name_key ON auth.scim_users USING btree (sso_provider_id, user_name) WHERE (deleted_at IS NULL);


--
-- Name: sessions_not_after_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sessions_not_after_idx ON auth.sessions USING btree (not_after DESC);


--
-- Name: sessions_oauth_client_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sessions_oauth_client_id_idx ON auth.sessions USING btree (oauth_client_id);


--
-- Name: sessions_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sessions_user_id_idx ON auth.sessions USING btree (user_id);


--
-- Name: sso_domains_domain_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX sso_domains_domain_idx ON auth.sso_domains USING btree (lower(domain));


--
-- Name: sso_domains_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sso_domains_sso_provider_id_idx ON auth.sso_domains USING btree (sso_provider_id);


--
-- Name: sso_providers_resource_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX sso_providers_resource_id_idx ON auth.sso_providers USING btree (lower(resource_id));


--
-- Name: sso_providers_resource_id_pattern_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX sso_providers_resource_id_pattern_idx ON auth.sso_providers USING btree (resource_id text_pattern_ops);


--
-- Name: unique_phone_factor_per_user; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX unique_phone_factor_per_user ON auth.mfa_factors USING btree (user_id, phone);


--
-- Name: user_id_created_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX user_id_created_at_idx ON auth.sessions USING btree (user_id, created_at);


--
-- Name: users_email_partial_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX users_email_partial_key ON auth.users USING btree (email) WHERE (is_sso_user = false);


--
-- Name: INDEX users_email_partial_key; Type: COMMENT; Schema: auth; Owner: supabase_auth_admin
--

COMMENT ON INDEX auth.users_email_partial_key IS 'Auth: A partial unique index that applies only when is_sso_user is false';


--
-- Name: users_instance_id_email_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX users_instance_id_email_idx ON auth.users USING btree (instance_id, lower((email)::text));


--
-- Name: users_instance_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX users_instance_id_idx ON auth.users USING btree (instance_id);


--
-- Name: users_is_anonymous_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX users_is_anonymous_idx ON auth.users USING btree (is_anonymous);


--
-- Name: webauthn_challenges_expires_at_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX webauthn_challenges_expires_at_idx ON auth.webauthn_challenges USING btree (expires_at);


--
-- Name: webauthn_challenges_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX webauthn_challenges_user_id_idx ON auth.webauthn_challenges USING btree (user_id);


--
-- Name: webauthn_credentials_credential_id_key; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE UNIQUE INDEX webauthn_credentials_credential_id_key ON auth.webauthn_credentials USING btree (credential_id);


--
-- Name: webauthn_credentials_user_id_idx; Type: INDEX; Schema: auth; Owner: supabase_auth_admin
--

CREATE INDEX webauthn_credentials_user_id_idx ON auth.webauthn_credentials USING btree (user_id);


--
-- Name: ix_notification_dedupe_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_notification_dedupe_key ON public.notification USING btree (dedupe_key);


--
-- Name: ix_pending_signup_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_pending_signup_email ON public.pending_signup USING btree (email);


--
-- Name: uq_one_current_education; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX uq_one_current_education ON public.education USING btree (student_id) WHERE (is_current = true);


--
-- Name: ix_realtime_subscription_entity; Type: INDEX; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE INDEX ix_realtime_subscription_entity ON realtime.subscription USING btree (entity);


--
-- Name: messages_inserted_at_topic_index; Type: INDEX; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE INDEX messages_inserted_at_topic_index ON ONLY realtime.messages USING btree (inserted_at DESC, topic) WHERE ((extension = 'broadcast'::text) AND (private IS TRUE));


--
-- Name: subscription_subscription_id_entity_filters_action_filter_selec; Type: INDEX; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE UNIQUE INDEX subscription_subscription_id_entity_filters_action_filter_selec ON realtime.subscription USING btree (subscription_id, entity, filters, action_filter, COALESCE(selected_columns, '{}'::text[]));


--
-- Name: bname; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX bname ON storage.buckets USING btree (name);


--
-- Name: buckets_analytics_unique_name_idx; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX buckets_analytics_unique_name_idx ON storage.buckets_analytics USING btree (name) WHERE (deleted_at IS NULL);


--
-- Name: idx_multipart_uploads_list; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX idx_multipart_uploads_list ON storage.s3_multipart_uploads USING btree (bucket_id, key, created_at);


--
-- Name: idx_objects_bucket_id_name; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX idx_objects_bucket_id_name ON storage.objects USING btree (bucket_id, name COLLATE "C");


--
-- Name: idx_objects_bucket_id_name_lower; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX idx_objects_bucket_id_name_lower ON storage.objects USING btree (bucket_id, lower(name) COLLATE "C");


--
-- Name: idx_objects_current_version; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX idx_objects_current_version ON storage.objects USING btree (bucket_id, name COLLATE "C") WHERE (archived_at IS NULL);


--
-- Name: idx_objects_delete_markers; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX idx_objects_delete_markers ON storage.objects USING btree (bucket_id, name COLLATE "C") WHERE is_delete_marker;


--
-- Name: idx_objects_null_version; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX idx_objects_null_version ON storage.objects USING btree (bucket_id, name COLLATE "C") WHERE (NOT is_versioned);


--
-- Name: name_prefix_search; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE INDEX name_prefix_search ON storage.objects USING btree (name text_pattern_ops);


--
-- Name: objects_bucket_id_name_version_key; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX objects_bucket_id_name_version_key ON storage.objects USING btree (bucket_id, name COLLATE "C", version) NULLS NOT DISTINCT;


--
-- Name: vector_indexes_name_bucket_id_idx; Type: INDEX; Schema: storage; Owner: supabase_storage_admin
--

CREATE UNIQUE INDEX vector_indexes_name_bucket_id_idx ON storage.vector_indexes USING btree (name, bucket_id);


--
-- Name: subscription tr_check_filters; Type: TRIGGER; Schema: realtime; Owner: supabase_realtime_admin
--

CREATE TRIGGER tr_check_filters BEFORE INSERT OR UPDATE ON realtime.subscription FOR EACH ROW EXECUTE FUNCTION realtime.subscription_check_filters();


--
-- Name: buckets enforce_bucket_name_length_trigger; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER enforce_bucket_name_length_trigger BEFORE INSERT OR UPDATE OF name ON storage.buckets FOR EACH ROW EXECUTE FUNCTION storage.enforce_bucket_name_length();


--
-- Name: buckets protect_bucket_control_insert; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER protect_bucket_control_insert BEFORE INSERT ON storage.buckets FOR EACH ROW EXECUTE FUNCTION storage.protect_bucket_control_columns('service_role');


--
-- Name: buckets protect_bucket_control_update; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER protect_bucket_control_update BEFORE UPDATE OF lifecycle_configuration, lifecycle_configuration_generation ON storage.buckets FOR EACH ROW EXECUTE FUNCTION storage.protect_bucket_control_columns();


--
-- Name: buckets protect_bucket_control_update_role; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER protect_bucket_control_update_role AFTER UPDATE OF lifecycle_configuration, lifecycle_configuration_generation ON storage.buckets FOR EACH ROW EXECUTE FUNCTION storage.enforce_bucket_lifecycle_service_role('service_role');


--
-- Name: buckets protect_buckets_delete; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER protect_buckets_delete BEFORE DELETE ON storage.buckets FOR EACH STATEMENT EXECUTE FUNCTION storage.protect_delete();


--
-- Name: objects protect_objects_delete; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER protect_objects_delete BEFORE DELETE ON storage.objects FOR EACH STATEMENT EXECUTE FUNCTION storage.protect_delete();


--
-- Name: objects update_objects_updated_at; Type: TRIGGER; Schema: storage; Owner: supabase_storage_admin
--

CREATE TRIGGER update_objects_updated_at BEFORE UPDATE ON storage.objects FOR EACH ROW EXECUTE FUNCTION storage.update_updated_at_column();


--
-- Name: identities identities_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: mfa_challenges mfa_challenges_auth_factor_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_auth_factor_id_fkey FOREIGN KEY (factor_id) REFERENCES auth.mfa_factors(id) ON DELETE CASCADE;


--
-- Name: mfa_factors mfa_factors_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: mfa_recovery_code_sets mfa_recovery_code_sets_mfa_factor_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_recovery_code_sets
    ADD CONSTRAINT mfa_recovery_code_sets_mfa_factor_id_fkey FOREIGN KEY (mfa_factor_id) REFERENCES auth.mfa_factors(id) ON DELETE CASCADE;


--
-- Name: mfa_recovery_code_sets mfa_recovery_code_sets_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_recovery_code_sets
    ADD CONSTRAINT mfa_recovery_code_sets_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: mfa_recovery_codes mfa_recovery_codes_mfa_recovery_code_set_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.mfa_recovery_codes
    ADD CONSTRAINT mfa_recovery_codes_mfa_recovery_code_set_id_fkey FOREIGN KEY (mfa_recovery_code_set_id) REFERENCES auth.mfa_recovery_code_sets(id) ON DELETE CASCADE;


--
-- Name: oauth_authorizations oauth_authorizations_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_client_id_fkey FOREIGN KEY (client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: oauth_authorizations oauth_authorizations_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: oauth_consents oauth_consents_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_client_id_fkey FOREIGN KEY (client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: oauth_consents oauth_consents_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: one_time_tokens one_time_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: refresh_tokens refresh_tokens_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: saml_providers saml_providers_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_flow_state_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_flow_state_id_fkey FOREIGN KEY (flow_state_id) REFERENCES auth.flow_state(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: scim_tokens scim_tokens_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.scim_tokens
    ADD CONSTRAINT scim_tokens_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: scim_users scim_users_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.scim_users
    ADD CONSTRAINT scim_users_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: scim_users scim_users_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.scim_users
    ADD CONSTRAINT scim_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE SET NULL;


--
-- Name: sessions sessions_oauth_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_oauth_client_id_fkey FOREIGN KEY (oauth_client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: sso_domains sso_domains_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: webauthn_challenges webauthn_challenges_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_challenges
    ADD CONSTRAINT webauthn_challenges_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: webauthn_credentials webauthn_credentials_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE ONLY auth.webauthn_credentials
    ADD CONSTRAINT webauthn_credentials_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: exam exam_body_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_body_id_fkey FOREIGN KEY (body_id) REFERENCES public.conducting_body(body_id);


--
-- Name: auditlog fk_auditlog_admin; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditlog
    ADD CONSTRAINT fk_auditlog_admin FOREIGN KEY (admin_id) REFERENCES public.admin(admin_id);


--
-- Name: chathistory fk_chathistory_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chathistory
    ADD CONSTRAINT fk_chathistory_student FOREIGN KEY (student_id) REFERENCES public.student(student_id);


--
-- Name: education fk_education_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT fk_education_student FOREIGN KEY (student_id) REFERENCES public.student(student_id);


--
-- Name: studentexameligibility fk_eligibility_exam; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studentexameligibility
    ADD CONSTRAINT fk_eligibility_exam FOREIGN KEY (exam_id) REFERENCES public.exam(exam_id);


--
-- Name: studentexameligibility fk_eligibility_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.studentexameligibility
    ADD CONSTRAINT fk_eligibility_student FOREIGN KEY (student_id) REFERENCES public.student(student_id);


--
-- Name: examdate fk_examdate_notification; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examdate
    ADD CONSTRAINT fk_examdate_notification FOREIGN KEY (notification_id) REFERENCES public.officialnotification(notification_id) ON DELETE CASCADE;


--
-- Name: extractionhistory fk_extraction_notification; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extractionhistory
    ADD CONSTRAINT fk_extraction_notification FOREIGN KEY (notification_id) REFERENCES public.officialnotification(notification_id);


--
-- Name: eligibilityrulegroup fk_notification; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrulegroup
    ADD CONSTRAINT fk_notification FOREIGN KEY (notification_id) REFERENCES public.officialnotification(notification_id);


--
-- Name: notification fk_notification_exam; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT fk_notification_exam FOREIGN KEY (exam_id) REFERENCES public.exam(exam_id);


--
-- Name: notification fk_notification_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT fk_notification_student FOREIGN KEY (student_id) REFERENCES public.student(student_id);


--
-- Name: officialnotification fk_officialnotification_exam; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.officialnotification
    ADD CONSTRAINT fk_officialnotification_exam FOREIGN KEY (exam_id) REFERENCES public.exam(exam_id);


--
-- Name: eligibilityrulegroup fk_parent_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrulegroup
    ADD CONSTRAINT fk_parent_group FOREIGN KEY (parent_group_id) REFERENCES public.eligibilityrulegroup(group_id);


--
-- Name: eligibilityrule fk_rule_attribute; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrule
    ADD CONSTRAINT fk_rule_attribute FOREIGN KEY (attribute_id) REFERENCES public.eligibilityattribute(attribute_id);


--
-- Name: eligibilityrule fk_rule_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eligibilityrule
    ADD CONSTRAINT fk_rule_group FOREIGN KEY (group_id) REFERENCES public.eligibilityrulegroup(group_id);


--
-- Name: trackedexam fk_trackedexam_exam; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trackedexam
    ADD CONSTRAINT fk_trackedexam_exam FOREIGN KEY (exam_id) REFERENCES public.exam(exam_id);


--
-- Name: trackedexam fk_trackedexam_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trackedexam
    ADD CONSTRAINT fk_trackedexam_student FOREIGN KEY (student_id) REFERENCES public.student(student_id);


--
-- Name: work_experience fk_work_experience_student; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_experience
    ADD CONSTRAINT fk_work_experience_student FOREIGN KEY (student_id) REFERENCES public.student(student_id) ON DELETE CASCADE;


--
-- Name: monitoringreview monitoringreview_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitoringreview
    ADD CONSTRAINT monitoringreview_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.officialnotification(notification_id);


--
-- Name: monitoringreview monitoringreview_reviewed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitoringreview
    ADD CONSTRAINT monitoringreview_reviewed_by_fkey FOREIGN KEY (reviewed_by) REFERENCES public.admin(admin_id);


--
-- Name: objects objects_bucketId_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT "objects_bucketId_fkey" FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_upload_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_upload_id_fkey FOREIGN KEY (upload_id) REFERENCES storage.s3_multipart_uploads(id) ON DELETE CASCADE;


--
-- Name: vector_indexes vector_indexes_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE ONLY storage.vector_indexes
    ADD CONSTRAINT vector_indexes_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets_vectors(id);


--
-- Name: audit_log_entries; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.audit_log_entries ENABLE ROW LEVEL SECURITY;

--
-- Name: flow_state; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.flow_state ENABLE ROW LEVEL SECURITY;

--
-- Name: identities; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.identities ENABLE ROW LEVEL SECURITY;

--
-- Name: instances; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.instances ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_amr_claims; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.mfa_amr_claims ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_challenges; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.mfa_challenges ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_factors; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.mfa_factors ENABLE ROW LEVEL SECURITY;

--
-- Name: one_time_tokens; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.one_time_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: refresh_tokens; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.refresh_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_providers; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.saml_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_relay_states; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.saml_relay_states ENABLE ROW LEVEL SECURITY;

--
-- Name: schema_migrations; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.schema_migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: sessions; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.sessions ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_domains; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.sso_domains ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_providers; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.sso_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: users; Type: ROW SECURITY; Schema: auth; Owner: supabase_auth_admin
--

ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

--
-- Name: messages; Type: ROW SECURITY; Schema: realtime; Owner: supabase_realtime_admin
--

ALTER TABLE realtime.messages ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.buckets ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets_analytics; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.buckets_analytics ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets_vectors; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.buckets_vectors ENABLE ROW LEVEL SECURITY;

--
-- Name: migrations; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: objects; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.s3_multipart_uploads ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads_parts; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.s3_multipart_uploads_parts ENABLE ROW LEVEL SECURITY;

--
-- Name: vector_indexes; Type: ROW SECURITY; Schema: storage; Owner: supabase_storage_admin
--

ALTER TABLE storage.vector_indexes ENABLE ROW LEVEL SECURITY;

--
-- Name: supabase_realtime; Type: PUBLICATION; Schema: -; Owner: postgres
--

CREATE PUBLICATION supabase_realtime WITH (publish = 'insert, update, delete, truncate');


ALTER PUBLICATION supabase_realtime OWNER TO postgres;

--
-- Name: SCHEMA auth; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA auth TO anon;
GRANT USAGE ON SCHEMA auth TO authenticated;
GRANT USAGE ON SCHEMA auth TO service_role;
GRANT ALL ON SCHEMA auth TO supabase_auth_admin;
GRANT ALL ON SCHEMA auth TO dashboard_user;
GRANT USAGE ON SCHEMA auth TO postgres;


--
-- Name: SCHEMA extensions; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA extensions TO anon;
GRANT USAGE ON SCHEMA extensions TO authenticated;
GRANT USAGE ON SCHEMA extensions TO service_role;
GRANT ALL ON SCHEMA extensions TO dashboard_user;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO postgres;
GRANT USAGE ON SCHEMA public TO anon;
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO service_role;


--
-- Name: SCHEMA realtime; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA realtime TO postgres WITH GRANT OPTION;
GRANT USAGE ON SCHEMA realtime TO anon;
GRANT USAGE ON SCHEMA realtime TO service_role;
GRANT ALL ON SCHEMA realtime TO supabase_realtime_admin;
GRANT USAGE ON SCHEMA realtime TO authenticated;


--
-- Name: SCHEMA storage; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA storage TO postgres WITH GRANT OPTION;
GRANT USAGE ON SCHEMA storage TO anon;
GRANT USAGE ON SCHEMA storage TO authenticated;
GRANT USAGE ON SCHEMA storage TO service_role;
GRANT ALL ON SCHEMA storage TO supabase_storage_admin WITH GRANT OPTION;
GRANT ALL ON SCHEMA storage TO dashboard_user;


--
-- Name: SCHEMA vault; Type: ACL; Schema: -; Owner: supabase_admin
--

GRANT USAGE ON SCHEMA vault TO postgres WITH GRANT OPTION;
GRANT USAGE ON SCHEMA vault TO service_role;


--
-- Name: FUNCTION email(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.email() TO dashboard_user;


--
-- Name: FUNCTION jwt(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.jwt() TO postgres;
GRANT ALL ON FUNCTION auth.jwt() TO dashboard_user;


--
-- Name: FUNCTION role(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.role() TO dashboard_user;


--
-- Name: FUNCTION uid(); Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON FUNCTION auth.uid() TO dashboard_user;


--
-- Name: FUNCTION armor(bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.armor(bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.armor(bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.armor(bytea) TO dashboard_user;


--
-- Name: FUNCTION armor(bytea, text[], text[]); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.armor(bytea, text[], text[]) FROM postgres;
GRANT ALL ON FUNCTION extensions.armor(bytea, text[], text[]) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.armor(bytea, text[], text[]) TO dashboard_user;


--
-- Name: FUNCTION crypt(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.crypt(text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.crypt(text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.crypt(text, text) TO dashboard_user;


--
-- Name: FUNCTION dearmor(text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.dearmor(text) FROM postgres;
GRANT ALL ON FUNCTION extensions.dearmor(text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.dearmor(text) TO dashboard_user;


--
-- Name: FUNCTION decrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.decrypt(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.decrypt(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.decrypt(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION decrypt_iv(bytea, bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.decrypt_iv(bytea, bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.decrypt_iv(bytea, bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.decrypt_iv(bytea, bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION digest(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.digest(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.digest(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.digest(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION digest(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.digest(text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.digest(text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.digest(text, text) TO dashboard_user;


--
-- Name: FUNCTION encrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.encrypt(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.encrypt(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.encrypt(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION encrypt_iv(bytea, bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.encrypt_iv(bytea, bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.encrypt_iv(bytea, bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.encrypt_iv(bytea, bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION gen_random_bytes(integer); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_random_bytes(integer) FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_random_bytes(integer) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_random_bytes(integer) TO dashboard_user;


--
-- Name: FUNCTION gen_random_uuid(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_random_uuid() FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_random_uuid() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_random_uuid() TO dashboard_user;


--
-- Name: FUNCTION gen_salt(text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_salt(text) FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_salt(text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_salt(text) TO dashboard_user;


--
-- Name: FUNCTION gen_salt(text, integer); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.gen_salt(text, integer) FROM postgres;
GRANT ALL ON FUNCTION extensions.gen_salt(text, integer) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.gen_salt(text, integer) TO dashboard_user;


--
-- Name: FUNCTION grant_pg_cron_access(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

REVOKE ALL ON FUNCTION extensions.grant_pg_cron_access() FROM supabase_admin;
GRANT ALL ON FUNCTION extensions.grant_pg_cron_access() TO supabase_admin WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.grant_pg_cron_access() TO dashboard_user;


--
-- Name: FUNCTION grant_pg_graphql_access(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.grant_pg_graphql_access() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION grant_pg_net_access(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

REVOKE ALL ON FUNCTION extensions.grant_pg_net_access() FROM supabase_admin;
GRANT ALL ON FUNCTION extensions.grant_pg_net_access() TO supabase_admin WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.grant_pg_net_access() TO dashboard_user;


--
-- Name: FUNCTION hmac(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.hmac(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.hmac(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.hmac(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION hmac(text, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.hmac(text, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.hmac(text, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.hmac(text, text, text) TO dashboard_user;


--
-- Name: FUNCTION pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) FROM postgres;
GRANT ALL ON FUNCTION extensions.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pg_stat_statements(showtext boolean, OUT userid oid, OUT dbid oid, OUT toplevel boolean, OUT queryid bigint, OUT query text, OUT plans bigint, OUT total_plan_time double precision, OUT min_plan_time double precision, OUT max_plan_time double precision, OUT mean_plan_time double precision, OUT stddev_plan_time double precision, OUT calls bigint, OUT total_exec_time double precision, OUT min_exec_time double precision, OUT max_exec_time double precision, OUT mean_exec_time double precision, OUT stddev_exec_time double precision, OUT rows bigint, OUT shared_blks_hit bigint, OUT shared_blks_read bigint, OUT shared_blks_dirtied bigint, OUT shared_blks_written bigint, OUT local_blks_hit bigint, OUT local_blks_read bigint, OUT local_blks_dirtied bigint, OUT local_blks_written bigint, OUT temp_blks_read bigint, OUT temp_blks_written bigint, OUT shared_blk_read_time double precision, OUT shared_blk_write_time double precision, OUT local_blk_read_time double precision, OUT local_blk_write_time double precision, OUT temp_blk_read_time double precision, OUT temp_blk_write_time double precision, OUT wal_records bigint, OUT wal_fpi bigint, OUT wal_bytes numeric, OUT jit_functions bigint, OUT jit_generation_time double precision, OUT jit_inlining_count bigint, OUT jit_inlining_time double precision, OUT jit_optimization_count bigint, OUT jit_optimization_time double precision, OUT jit_emission_count bigint, OUT jit_emission_time double precision, OUT jit_deform_count bigint, OUT jit_deform_time double precision, OUT stats_since timestamp with time zone, OUT minmax_stats_since timestamp with time zone) TO dashboard_user;


--
-- Name: FUNCTION pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) FROM postgres;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_info(OUT dealloc bigint, OUT stats_reset timestamp with time zone) TO dashboard_user;


--
-- Name: FUNCTION pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean) FROM postgres;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pg_stat_statements_reset(userid oid, dbid oid, queryid bigint, minmax_only boolean) TO dashboard_user;


--
-- Name: FUNCTION pgp_armor_headers(text, OUT key text, OUT value text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_armor_headers(text, OUT key text, OUT value text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_armor_headers(text, OUT key text, OUT value text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_armor_headers(text, OUT key text, OUT value text) TO dashboard_user;


--
-- Name: FUNCTION pgp_key_id(bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_key_id(bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_key_id(bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_key_id(bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt(bytea, bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt(bytea, bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_decrypt_bytea(bytea, bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_decrypt_bytea(bytea, bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt(text, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt(text, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt(text, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt_bytea(bytea, bytea); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea) TO dashboard_user;


--
-- Name: FUNCTION pgp_pub_encrypt_bytea(bytea, bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_pub_encrypt_bytea(bytea, bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt(bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt_bytea(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_decrypt_bytea(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_decrypt_bytea(bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt(text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt(text, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt(text, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt_bytea(bytea, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text) TO dashboard_user;


--
-- Name: FUNCTION pgp_sym_encrypt_bytea(bytea, text, text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text, text) FROM postgres;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text, text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.pgp_sym_encrypt_bytea(bytea, text, text) TO dashboard_user;


--
-- Name: FUNCTION pgrst_ddl_watch(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.pgrst_ddl_watch() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION pgrst_drop_watch(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.pgrst_drop_watch() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION set_graphql_placeholder(); Type: ACL; Schema: extensions; Owner: supabase_admin
--

GRANT ALL ON FUNCTION extensions.set_graphql_placeholder() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION uuid_generate_v1(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v1() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1() TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v1mc(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v1mc() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1mc() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v1mc() TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v3(namespace uuid, name text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v3(namespace uuid, name text) FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v3(namespace uuid, name text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v3(namespace uuid, name text) TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v4(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v4() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v4() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v4() TO dashboard_user;


--
-- Name: FUNCTION uuid_generate_v5(namespace uuid, name text); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_generate_v5(namespace uuid, name text) FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_generate_v5(namespace uuid, name text) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_generate_v5(namespace uuid, name text) TO dashboard_user;


--
-- Name: FUNCTION uuid_nil(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_nil() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_nil() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_nil() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_dns(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_dns() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_dns() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_dns() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_oid(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_oid() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_oid() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_oid() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_url(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_url() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_url() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_url() TO dashboard_user;


--
-- Name: FUNCTION uuid_ns_x500(); Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON FUNCTION extensions.uuid_ns_x500() FROM postgres;
GRANT ALL ON FUNCTION extensions.uuid_ns_x500() TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION extensions.uuid_ns_x500() TO dashboard_user;


--
-- Name: FUNCTION graphql("operationName" text, query text, variables jsonb, extensions jsonb); Type: ACL; Schema: graphql_public; Owner: supabase_admin
--

GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO postgres;
GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO anon;
GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO authenticated;
GRANT ALL ON FUNCTION graphql_public.graphql("operationName" text, query text, variables jsonb, extensions jsonb) TO service_role;


--
-- Name: FUNCTION pg_reload_conf(); Type: ACL; Schema: pg_catalog; Owner: supabase_admin
--

GRANT ALL ON FUNCTION pg_catalog.pg_reload_conf() TO postgres WITH GRANT OPTION;


--
-- Name: FUNCTION get_auth(p_usename text); Type: ACL; Schema: pgbouncer; Owner: supabase_admin
--

REVOKE ALL ON FUNCTION pgbouncer.get_auth(p_usename text) FROM PUBLIC;
GRANT ALL ON FUNCTION pgbouncer.get_auth(p_usename text) TO pgbouncer;


--
-- Name: FUNCTION apply_rls(wal jsonb, max_record_bytes integer); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO postgres;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO anon;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO authenticated;
GRANT ALL ON FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer) TO service_role;


--
-- Name: FUNCTION broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text) TO postgres;
GRANT ALL ON FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text) TO dashboard_user;


--
-- Name: FUNCTION build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO postgres;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO anon;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO authenticated;
GRANT ALL ON FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) TO service_role;


--
-- Name: FUNCTION "cast"(val text, type_ regtype); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO postgres;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO dashboard_user;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO anon;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO authenticated;
GRANT ALL ON FUNCTION realtime."cast"(val text, type_ regtype) TO service_role;


--
-- Name: FUNCTION check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO postgres;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO anon;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO authenticated;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) TO service_role;


--
-- Name: FUNCTION check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean) TO postgres;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean) TO anon;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean) TO authenticated;
GRANT ALL ON FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text, negate boolean) TO service_role;


--
-- Name: FUNCTION is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO postgres;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO anon;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO authenticated;
GRANT ALL ON FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) TO service_role;


--
-- Name: FUNCTION list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) TO postgres;
GRANT ALL ON FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) TO dashboard_user;


--
-- Name: FUNCTION list_changes_sync(publication name, slot_name name, max_changes integer, max_record_bytes integer); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.list_changes_sync(publication name, slot_name name, max_changes integer, max_record_bytes integer) TO postgres;
GRANT ALL ON FUNCTION realtime.list_changes_sync(publication name, slot_name name, max_changes integer, max_record_bytes integer) TO dashboard_user;


--
-- Name: FUNCTION quote_wal2json(entity regclass); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO postgres;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO anon;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO authenticated;
GRANT ALL ON FUNCTION realtime.quote_wal2json(entity regclass) TO service_role;


--
-- Name: FUNCTION send(payload jsonb, event text, topic text, private boolean); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean) TO postgres;
GRANT ALL ON FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean) TO dashboard_user;


--
-- Name: FUNCTION send_binary(payload bytea, event text, topic text, private boolean); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.send_binary(payload bytea, event text, topic text, private boolean) TO postgres;
GRANT ALL ON FUNCTION realtime.send_binary(payload bytea, event text, topic text, private boolean) TO dashboard_user;


--
-- Name: FUNCTION settled_changes(slot_name name, max_changes integer, VARIADIC opts text[]); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.settled_changes(slot_name name, max_changes integer, VARIADIC opts text[]) TO postgres;
GRANT ALL ON FUNCTION realtime.settled_changes(slot_name name, max_changes integer, VARIADIC opts text[]) TO dashboard_user;


--
-- Name: FUNCTION subscription_check_filters(); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO postgres;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO dashboard_user;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO anon;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO authenticated;
GRANT ALL ON FUNCTION realtime.subscription_check_filters() TO service_role;


--
-- Name: FUNCTION to_regrole(role_name text); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO postgres;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO dashboard_user;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO anon;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO authenticated;
GRANT ALL ON FUNCTION realtime.to_regrole(role_name text) TO service_role;


--
-- Name: FUNCTION topic(); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.topic() TO postgres;
GRANT ALL ON FUNCTION realtime.topic() TO dashboard_user;


--
-- Name: FUNCTION wal2json_escape_identifier(name text); Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON FUNCTION realtime.wal2json_escape_identifier(name text) TO postgres;
GRANT ALL ON FUNCTION realtime.wal2json_escape_identifier(name text) TO dashboard_user;


--
-- Name: FUNCTION _crypto_aead_det_decrypt(message bytea, additional bytea, key_id bigint, context bytea, nonce bytea); Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT ALL ON FUNCTION vault._crypto_aead_det_decrypt(message bytea, additional bytea, key_id bigint, context bytea, nonce bytea) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION vault._crypto_aead_det_decrypt(message bytea, additional bytea, key_id bigint, context bytea, nonce bytea) TO service_role;


--
-- Name: FUNCTION create_secret(new_secret text, new_name text, new_description text, new_key_id uuid); Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT ALL ON FUNCTION vault.create_secret(new_secret text, new_name text, new_description text, new_key_id uuid) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION vault.create_secret(new_secret text, new_name text, new_description text, new_key_id uuid) TO service_role;


--
-- Name: FUNCTION update_secret(secret_id uuid, new_secret text, new_name text, new_description text, new_key_id uuid); Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT ALL ON FUNCTION vault.update_secret(secret_id uuid, new_secret text, new_name text, new_description text, new_key_id uuid) TO postgres WITH GRANT OPTION;
GRANT ALL ON FUNCTION vault.update_secret(secret_id uuid, new_secret text, new_name text, new_description text, new_key_id uuid) TO service_role;


--
-- Name: TABLE audit_log_entries; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.audit_log_entries TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.audit_log_entries TO postgres;
GRANT SELECT ON TABLE auth.audit_log_entries TO postgres WITH GRANT OPTION;


--
-- Name: TABLE custom_oauth_providers; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.custom_oauth_providers TO postgres;
GRANT ALL ON TABLE auth.custom_oauth_providers TO dashboard_user;


--
-- Name: TABLE flow_state; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.flow_state TO postgres;
GRANT SELECT ON TABLE auth.flow_state TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.flow_state TO dashboard_user;


--
-- Name: TABLE identities; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.identities TO postgres;
GRANT SELECT ON TABLE auth.identities TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.identities TO dashboard_user;


--
-- Name: TABLE instances; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.instances TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.instances TO postgres;
GRANT SELECT ON TABLE auth.instances TO postgres WITH GRANT OPTION;


--
-- Name: TABLE mfa_amr_claims; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.mfa_amr_claims TO postgres;
GRANT SELECT ON TABLE auth.mfa_amr_claims TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.mfa_amr_claims TO dashboard_user;


--
-- Name: TABLE mfa_challenges; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.mfa_challenges TO postgres;
GRANT SELECT ON TABLE auth.mfa_challenges TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.mfa_challenges TO dashboard_user;


--
-- Name: TABLE mfa_factors; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.mfa_factors TO postgres;
GRANT SELECT ON TABLE auth.mfa_factors TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.mfa_factors TO dashboard_user;


--
-- Name: TABLE mfa_recovery_code_sets; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.mfa_recovery_code_sets TO postgres;
GRANT ALL ON TABLE auth.mfa_recovery_code_sets TO dashboard_user;


--
-- Name: TABLE mfa_recovery_codes; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.mfa_recovery_codes TO postgres;
GRANT ALL ON TABLE auth.mfa_recovery_codes TO dashboard_user;


--
-- Name: TABLE oauth_authorizations; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_authorizations TO postgres;
GRANT ALL ON TABLE auth.oauth_authorizations TO dashboard_user;


--
-- Name: TABLE oauth_client_states; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_client_states TO postgres;
GRANT ALL ON TABLE auth.oauth_client_states TO dashboard_user;


--
-- Name: TABLE oauth_clients; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_clients TO postgres;
GRANT ALL ON TABLE auth.oauth_clients TO dashboard_user;


--
-- Name: TABLE oauth_consents; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.oauth_consents TO postgres;
GRANT ALL ON TABLE auth.oauth_consents TO dashboard_user;


--
-- Name: TABLE one_time_tokens; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.one_time_tokens TO postgres;
GRANT SELECT ON TABLE auth.one_time_tokens TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.one_time_tokens TO dashboard_user;


--
-- Name: TABLE refresh_tokens; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.refresh_tokens TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.refresh_tokens TO postgres;
GRANT SELECT ON TABLE auth.refresh_tokens TO postgres WITH GRANT OPTION;


--
-- Name: SEQUENCE refresh_tokens_id_seq; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON SEQUENCE auth.refresh_tokens_id_seq TO dashboard_user;
GRANT ALL ON SEQUENCE auth.refresh_tokens_id_seq TO postgres;


--
-- Name: TABLE saml_providers; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.saml_providers TO postgres;
GRANT SELECT ON TABLE auth.saml_providers TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.saml_providers TO dashboard_user;


--
-- Name: TABLE saml_relay_states; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.saml_relay_states TO postgres;
GRANT SELECT ON TABLE auth.saml_relay_states TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.saml_relay_states TO dashboard_user;


--
-- Name: TABLE schema_migrations; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT SELECT ON TABLE auth.schema_migrations TO postgres WITH GRANT OPTION;


--
-- Name: TABLE scim_tokens; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.scim_tokens TO postgres;
GRANT ALL ON TABLE auth.scim_tokens TO dashboard_user;


--
-- Name: TABLE scim_users; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.scim_users TO postgres;
GRANT ALL ON TABLE auth.scim_users TO dashboard_user;


--
-- Name: TABLE sessions; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.sessions TO postgres;
GRANT SELECT ON TABLE auth.sessions TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.sessions TO dashboard_user;


--
-- Name: TABLE sso_domains; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.sso_domains TO postgres;
GRANT SELECT ON TABLE auth.sso_domains TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.sso_domains TO dashboard_user;


--
-- Name: TABLE sso_providers; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.sso_providers TO postgres;
GRANT SELECT ON TABLE auth.sso_providers TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE auth.sso_providers TO dashboard_user;


--
-- Name: TABLE users; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.users TO dashboard_user;
GRANT INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE auth.users TO postgres;
GRANT SELECT ON TABLE auth.users TO postgres WITH GRANT OPTION;


--
-- Name: TABLE webauthn_challenges; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.webauthn_challenges TO postgres;
GRANT ALL ON TABLE auth.webauthn_challenges TO dashboard_user;


--
-- Name: TABLE webauthn_credentials; Type: ACL; Schema: auth; Owner: supabase_auth_admin
--

GRANT ALL ON TABLE auth.webauthn_credentials TO postgres;
GRANT ALL ON TABLE auth.webauthn_credentials TO dashboard_user;


--
-- Name: TABLE pg_stat_statements; Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON TABLE extensions.pg_stat_statements FROM postgres;
GRANT ALL ON TABLE extensions.pg_stat_statements TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE extensions.pg_stat_statements TO dashboard_user;


--
-- Name: TABLE pg_stat_statements_info; Type: ACL; Schema: extensions; Owner: postgres
--

REVOKE ALL ON TABLE extensions.pg_stat_statements_info FROM postgres;
GRANT ALL ON TABLE extensions.pg_stat_statements_info TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE extensions.pg_stat_statements_info TO dashboard_user;


--
-- Name: TABLE admin; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.admin TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.admin TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.admin TO service_role;


--
-- Name: TABLE alembic_version; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.alembic_version TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.alembic_version TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.alembic_version TO service_role;


--
-- Name: TABLE auditlog; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.auditlog TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.auditlog TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.auditlog TO service_role;


--
-- Name: TABLE chathistory; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.chathistory TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.chathistory TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.chathistory TO service_role;


--
-- Name: TABLE conducting_body; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.conducting_body TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.conducting_body TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.conducting_body TO service_role;


--
-- Name: TABLE education; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.education TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.education TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.education TO service_role;


--
-- Name: TABLE eligibilityattribute; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityattribute TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityattribute TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityattribute TO service_role;


--
-- Name: TABLE eligibilityrule; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityrule TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityrule TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityrule TO service_role;


--
-- Name: TABLE eligibilityrulegroup; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityrulegroup TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityrulegroup TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.eligibilityrulegroup TO service_role;


--
-- Name: TABLE exam; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.exam TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.exam TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.exam TO service_role;


--
-- Name: TABLE examdate; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.examdate TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.examdate TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.examdate TO service_role;


--
-- Name: TABLE extractionhistory; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.extractionhistory TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.extractionhistory TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.extractionhistory TO service_role;


--
-- Name: TABLE monitoringreview; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.monitoringreview TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.monitoringreview TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.monitoringreview TO service_role;


--
-- Name: TABLE notification; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.notification TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.notification TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.notification TO service_role;


--
-- Name: TABLE officialnotification; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.officialnotification TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.officialnotification TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.officialnotification TO service_role;


--
-- Name: TABLE pending_signup; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.pending_signup TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.pending_signup TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.pending_signup TO service_role;


--
-- Name: TABLE student; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.student TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.student TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.student TO service_role;


--
-- Name: TABLE studentexameligibility; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.studentexameligibility TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.studentexameligibility TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.studentexameligibility TO service_role;


--
-- Name: TABLE trackedexam; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.trackedexam TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.trackedexam TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.trackedexam TO service_role;


--
-- Name: TABLE work_experience; Type: ACL; Schema: public; Owner: postgres
--

GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.work_experience TO anon;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.work_experience TO authenticated;
GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLE public.work_experience TO service_role;


--
-- Name: TABLE messages; Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLE realtime.messages TO postgres;
GRANT SELECT,INSERT ON TABLE realtime.messages TO postgres WITH GRANT OPTION;
GRANT ALL ON TABLE realtime.messages TO dashboard_user;
GRANT SELECT,INSERT,UPDATE ON TABLE realtime.messages TO anon;
GRANT SELECT,INSERT,UPDATE ON TABLE realtime.messages TO authenticated;
GRANT SELECT,INSERT,UPDATE ON TABLE realtime.messages TO service_role;


--
-- Name: TABLE schema_migrations; Type: ACL; Schema: realtime; Owner: supabase_admin
--

GRANT ALL ON TABLE realtime.schema_migrations TO postgres;
GRANT ALL ON TABLE realtime.schema_migrations TO dashboard_user;


--
-- Name: TABLE subscription; Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON TABLE realtime.subscription TO postgres;
GRANT ALL ON TABLE realtime.subscription TO dashboard_user;
GRANT SELECT ON TABLE realtime.subscription TO anon;
GRANT SELECT ON TABLE realtime.subscription TO authenticated;
GRANT SELECT ON TABLE realtime.subscription TO service_role;


--
-- Name: SEQUENCE subscription_id_seq; Type: ACL; Schema: realtime; Owner: supabase_realtime_admin
--

GRANT ALL ON SEQUENCE realtime.subscription_id_seq TO postgres;
GRANT ALL ON SEQUENCE realtime.subscription_id_seq TO dashboard_user;
GRANT USAGE ON SEQUENCE realtime.subscription_id_seq TO anon;
GRANT USAGE ON SEQUENCE realtime.subscription_id_seq TO authenticated;
GRANT USAGE ON SEQUENCE realtime.subscription_id_seq TO service_role;


--
-- Name: TABLE buckets; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

REVOKE ALL ON TABLE storage.buckets FROM supabase_storage_admin;
GRANT ALL ON TABLE storage.buckets TO supabase_storage_admin WITH GRANT OPTION;
GRANT ALL ON TABLE storage.buckets TO service_role;
GRANT ALL ON TABLE storage.buckets TO authenticated;
GRANT ALL ON TABLE storage.buckets TO anon;
GRANT ALL ON TABLE storage.buckets TO postgres WITH GRANT OPTION;


--
-- Name: TABLE buckets_analytics; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT ALL ON TABLE storage.buckets_analytics TO service_role;
GRANT ALL ON TABLE storage.buckets_analytics TO authenticated;
GRANT ALL ON TABLE storage.buckets_analytics TO anon;


--
-- Name: TABLE buckets_vectors; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT SELECT ON TABLE storage.buckets_vectors TO service_role;
GRANT SELECT ON TABLE storage.buckets_vectors TO authenticated;
GRANT SELECT ON TABLE storage.buckets_vectors TO anon;


--
-- Name: TABLE objects; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

REVOKE ALL ON TABLE storage.objects FROM supabase_storage_admin;
GRANT ALL ON TABLE storage.objects TO supabase_storage_admin WITH GRANT OPTION;
GRANT ALL ON TABLE storage.objects TO service_role;
GRANT ALL ON TABLE storage.objects TO authenticated;
GRANT ALL ON TABLE storage.objects TO anon;
GRANT ALL ON TABLE storage.objects TO postgres WITH GRANT OPTION;


--
-- Name: TABLE s3_multipart_uploads; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT ALL ON TABLE storage.s3_multipart_uploads TO service_role;
GRANT SELECT ON TABLE storage.s3_multipart_uploads TO authenticated;
GRANT SELECT ON TABLE storage.s3_multipart_uploads TO anon;


--
-- Name: TABLE s3_multipart_uploads_parts; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT ALL ON TABLE storage.s3_multipart_uploads_parts TO service_role;
GRANT SELECT ON TABLE storage.s3_multipart_uploads_parts TO authenticated;
GRANT SELECT ON TABLE storage.s3_multipart_uploads_parts TO anon;


--
-- Name: TABLE vector_indexes; Type: ACL; Schema: storage; Owner: supabase_storage_admin
--

GRANT SELECT ON TABLE storage.vector_indexes TO service_role;
GRANT SELECT ON TABLE storage.vector_indexes TO authenticated;
GRANT SELECT ON TABLE storage.vector_indexes TO anon;


--
-- Name: TABLE secrets; Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT SELECT,REFERENCES,DELETE,TRUNCATE ON TABLE vault.secrets TO postgres WITH GRANT OPTION;
GRANT SELECT,DELETE ON TABLE vault.secrets TO service_role;


--
-- Name: TABLE decrypted_secrets; Type: ACL; Schema: vault; Owner: supabase_admin
--

GRANT SELECT,REFERENCES,DELETE,TRUNCATE ON TABLE vault.decrypted_secrets TO postgres WITH GRANT OPTION;
GRANT SELECT,DELETE ON TABLE vault.decrypted_secrets TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: auth; Owner: supabase_auth_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON SEQUENCES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: auth; Owner: supabase_auth_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON FUNCTIONS TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: auth; Owner: supabase_auth_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_auth_admin IN SCHEMA auth GRANT ALL ON TABLES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: extensions; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA extensions GRANT ALL ON SEQUENCES TO postgres WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: extensions; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA extensions GRANT ALL ON FUNCTIONS TO postgres WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: extensions; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA extensions GRANT ALL ON TABLES TO postgres WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: graphql; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: graphql; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: graphql; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql GRANT ALL ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: graphql_public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: graphql_public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: graphql_public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA graphql_public GRANT ALL ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON FUNCTIONS TO postgres;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT REFERENCES,TRIGGER,TRUNCATE,MAINTAIN ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA public GRANT ALL ON TABLES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: realtime; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON SEQUENCES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: realtime; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON FUNCTIONS TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: realtime; Owner: supabase_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT REFERENCES,DELETE,TRIGGER,TRUNCATE,MAINTAIN,UPDATE ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT SELECT,INSERT ON TABLES TO postgres WITH GRANT OPTION;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON TABLES TO dashboard_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: storage; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON SEQUENCES TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: storage; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON FUNCTIONS TO service_role;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: storage; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO anon;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO authenticated;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA storage GRANT ALL ON TABLES TO service_role;


--
-- Name: issue_graphql_placeholder; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_graphql_placeholder ON sql_drop
         WHEN TAG IN ('DROP EXTENSION')
   EXECUTE FUNCTION extensions.set_graphql_placeholder();


ALTER EVENT TRIGGER issue_graphql_placeholder OWNER TO supabase_admin;

--
-- Name: issue_pg_cron_access; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_pg_cron_access ON ddl_command_end
         WHEN TAG IN ('CREATE EXTENSION')
   EXECUTE FUNCTION extensions.grant_pg_cron_access();


ALTER EVENT TRIGGER issue_pg_cron_access OWNER TO supabase_admin;

--
-- Name: issue_pg_graphql_access; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_pg_graphql_access ON ddl_command_end
         WHEN TAG IN ('CREATE EXTENSION')
   EXECUTE FUNCTION extensions.grant_pg_graphql_access();


ALTER EVENT TRIGGER issue_pg_graphql_access OWNER TO supabase_admin;

--
-- Name: issue_pg_net_access; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER issue_pg_net_access ON ddl_command_end
         WHEN TAG IN ('CREATE EXTENSION')
   EXECUTE FUNCTION extensions.grant_pg_net_access();


ALTER EVENT TRIGGER issue_pg_net_access OWNER TO supabase_admin;

--
-- Name: pgrst_ddl_watch; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER pgrst_ddl_watch ON ddl_command_end
   EXECUTE FUNCTION extensions.pgrst_ddl_watch();


ALTER EVENT TRIGGER pgrst_ddl_watch OWNER TO supabase_admin;

--
-- Name: pgrst_drop_watch; Type: EVENT TRIGGER; Schema: -; Owner: supabase_admin
--

CREATE EVENT TRIGGER pgrst_drop_watch ON sql_drop
   EXECUTE FUNCTION extensions.pgrst_drop_watch();


ALTER EVENT TRIGGER pgrst_drop_watch OWNER TO supabase_admin;

--
-- PostgreSQL database dump complete
--

\unrestrict WKVq8s8q1VDx5dp9IyWccvw5tvwF4tLWdH2zDofUCz5RVfhbqhCaNegioUdOO75

