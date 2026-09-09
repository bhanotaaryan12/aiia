# Security Architecture

## Authentication

### JWT-Based Authentication
- Access tokens (60-minute expiry) for API requests
- Refresh tokens (7-day expiry) for token renewal
- Tokens contain: user ID, email, roles
- bcrypt password hashing (cost factor 12)

### Login Flow
```
Client → POST /api/v1/auth/login {email, password}
Server → Verify credentials → Issue JWT pair
Client → Store tokens → Include in Authorization header
```

### MFA-Ready Architecture
- `mfa_enabled` field on User model
- Architecture supports TOTP integration
- Not implemented in MVP

## Authorization (RBAC)

### Role Hierarchy
| Role | Access Level |
|------|-------------|
| SUPER_ADMIN | Full system access |
| TRIAL_ADMIN | Trial, site, user management |
| PRINCIPAL_INVESTIGATOR | Clinical operations |
| STUDY_COORDINATOR | Enrollment, visits, forms |
| DATA_MANAGER | Data quality, validation, CDISC |
| ETHICS_COMMITTEE | Ethics workflow |
| PHARMACOVIGILANCE_OFFICER | Safety management |
| REGULATORY_OFFICER | Regulatory compliance |
| AUDITOR | Read-only + audit trails |
| VIEWER | Read-only dashboards |

### Enforcement
- **Backend**: Every API route checks permissions via `require_roles()` dependency
- **Frontend**: Role-based UI rendering (hide/disable unauthorized features)
- Authorization is NEVER frontend-only

## Data Protection

### Participant Privacy
- Pseudonymous participant IDs (format: AIIA-{trial#}-{random})
- No PII stored in clinical data tables
- Identity and clinical data architecturally separated

### Password Security
- bcrypt hashing with salt
- No plaintext passwords stored
- Password validated server-side only

## API Security

### CORS
- Configured origins (localhost:3000 for development)
- Credentials supported
- All methods and headers allowed in development

### Request Validation
- All input validated with Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- File upload validation (executable files blocked)

### Rate Limiting
- Architecture ready for rate limiting middleware
- Configurable via environment variables

## Audit Trail

### Append-Only Logging
- All mutations create audit records
- AuditLog table does not support UPDATE or DELETE
- Records include: user, action, entity, old/new values, timestamp, IP

### Tracked Actions
- Authentication events
- CRUD operations on all entities
- Status transitions
- File uploads
- Data exports

## Infrastructure Security

### Environment-Based Secrets
- SECRET_KEY, DATABASE_URL via environment variables
- `.env.example` provided, `.env` in `.gitignore`
- GCP Secret Manager ready for production

### Secure Headers
- CORS middleware configured
- Content-Type validation on all requests

## Compliance Disclaimer
This security architecture supports GCP-aligned clinical research workflows. It does not constitute regulatory certification. Organizations must validate security controls per their regulatory requirements.
