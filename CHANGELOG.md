## [v0.1.1] - 20-07-2025

### Added
- User authentication and authorization:
  - `/users` endpoint for registration with hashed passwords.
  - `/token` endpoint for user login and JWT issuance.
- JWT protection enforced on all sensitive endpoints.
- `/upload` endpoint for authenticated file uploads (any format).
- `/ingest` endpoint for authenticated event/JSON ingestion.
- `/webhook/{client_id}` endpoint (accepts any JSON, stores to Postgres, JWT-protected).
- PostgreSQL audit logging:
  - `audit_logs` table tracking user, action, resource, status, details, timestamp.
  - Audit log entries for login, file uploads, event ingest, and webhook calls.
- Access token (JWT) tracking in database for audit/compliance (not for session reuse).
- Scaffolded FTP (`ingestors/ftp_ingest.py`) and SFTP (`ingestors/sftp_ingest.py`) ingestion workers to forward files to `/upload` (currently blocked for testing—pending credentials).
- Modular code structure: `app/` (API, models), `ingestors/`, `tests/`.
- Consistent environment variable/config handling and error message improvement.

## [v0.1.0] - 19-07-2025

### Added
- Added initial Docker Compose setup in `/infra/docker-compose.yml` for developer infra.
- Included Kafka, Zookeeper, and MinIO images for local event streaming and object storage.
- Scaffolded infrastructure directory for infra scripts and future service configs.
- Provided sample volumes and environment variable configuration for development.
