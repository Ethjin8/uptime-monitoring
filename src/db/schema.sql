-- targets table, storing each website --
CREATE TABLE IF NOT EXISTS targets (
  id                     BIGSERIAL    PRIMARY KEY,
  url                    TEXT         UNIQUE NOT NULL,
  owner_label            TEXT         NOT NULL,
  discord_webhook        TEXT,
  slack_webhook          TEXT,
  removal_token          TEXT         NOT NULL,
  created_at             TIMESTAMPTZ  NOT NULL DEFAULT now(),
  active                 BOOLEAN      NOT NULL DEFAULT true,
  interval_seconds       INT          NOT NULL DEFAULT 30 CHECK (interval_seconds IN (30, 60, 300)),
  next_due_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
  consecutive_failures   INT          NOT NULL DEFAULT 0,
  consecutive_successes  INT          NOT NULL DEFAULT 0,
  alert_state            TEXT         NOT NULL DEFAULT 'ok' CHECK (alert_state IN ('ok', 'alerting')),
  state_changed_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
  last_alert_at          TIMESTAMPTZ,
  open_alert_sent        BOOLEAN      NOT NULL DEFAULT false
);

CREATE INDEX IF NOT EXISTS probe_now ON targets (active, next_due_at);


-- probe_results table, storing the result when we query each website --
CREATE TABLE IF NOT EXISTS probe_results (
  id           BIGSERIAL    PRIMARY KEY,
  target_id    BIGINT       NOT NULL REFERENCES targets (id),
  probed_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
  status_code  INT,        
  latency_ms   INT,
  error        TEXT         CHECK (error IN ('TIMEOUT', 'CONN_REFUSED', 'DNS', 'TLS_ERROR')),
  CHECK (status_code IS NOT NULL OR error IS NOT NULL)  
);

CREATE INDEX IF NOT EXISTS past_probe ON probe_results (target_id, probed_at);


-- daily_rollups table, a per-day summary for each website --
CREATE TABLE IF NOT EXISTS daily_rollups (
  target_id        BIGINT       NOT NULL REFERENCES targets (id),
  day              TIMESTAMPTZ  NOT NULL,
  probe_count      INT          NOT NULL DEFAULT 0,
  success_count    INT          NOT NULL DEFAULT 0,
  latency_buckets  INT[]        NOT NULL,    -- counts per range: [under 100ms, 100-300, 300-1000, 1000+]
  PRIMARY KEY (target_id, day)
);
