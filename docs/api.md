# API Documentation

## Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.aiia-ctms.example.com/api/v1
```

## Authentication
All endpoints (except login) require JWT authentication via Bearer token:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/login | Login with email/password |
| GET | /auth/me | Get current user info |
| POST | /auth/refresh | Refresh access token |

### Users
| Method | Path | Roles | Description |
|--------|------|-------|-------------|
| GET | /users/ | SUPER_ADMIN, TRIAL_ADMIN | List users |
| POST | /users/ | SUPER_ADMIN, TRIAL_ADMIN | Create user |
| GET | /users/{id} | Any authenticated | Get user |
| GET | /users/roles | Any authenticated | List roles |

### Trials
| Method | Path | Roles | Description |
|--------|------|-------|-------------|
| GET | /trials/ | Any authenticated | List trials (filterable) |
| POST | /trials/ | SUPER_ADMIN, TRIAL_ADMIN, PI | Create trial |
| GET | /trials/{id} | Any authenticated | Get trial detail |
| PUT | /trials/{id} | SUPER_ADMIN, TRIAL_ADMIN, PI | Update trial |
| GET | /trials/{id}/arms | Any authenticated | Get study arms |
| POST | /trials/{id}/arms | SUPER_ADMIN, TRIAL_ADMIN | Create study arm |

### Sites
| Method | Path | Roles | Description |
|--------|------|-------|-------------|
| GET | /sites/ | Any authenticated | List sites |
| POST | /sites/ | SUPER_ADMIN, TRIAL_ADMIN | Create site |
| GET | /sites/{id} | Any authenticated | Get site |
| PUT | /sites/{id} | SUPER_ADMIN, TRIAL_ADMIN | Update site |
| POST | /sites/assignments | SUPER_ADMIN, TRIAL_ADMIN | Assign site to trial |
| GET | /sites/investigators/all | Any authenticated | List investigators |

### Participants
| Method | Path | Roles | Description |
|--------|------|-------|-------------|
| GET | /participants/ | Any authenticated | List participants (filterable) |
| POST | /participants/ | SUPER_ADMIN, TRIAL_ADMIN, PI, SC | Create participant |
| GET | /participants/{id} | Any authenticated | Get participant |
| PUT | /participants/{id} | SUPER_ADMIN, PI, SC | Update participant |
| POST | /participants/{id}/consent | SUPER_ADMIN, PI, SC | Record consent |
| POST | /participants/{id}/enroll | SUPER_ADMIN, PI, SC | Enroll participant |
| POST | /participants/{id}/randomize | SUPER_ADMIN, PI, SC | Randomize participant |

### Visits
| Method | Path | Description |
|--------|------|-------------|
| GET | /visits/definitions | List visit definitions |
| POST | /visits/definitions | Create visit definition |
| GET | /visits/ | List participant visits |
| POST | /visits/ | Create participant visit |
| PUT | /visits/{id} | Update visit |

### Forms (eCRF)
| Method | Path | Description |
|--------|------|-------------|
| GET | /forms/ | List forms |
| POST | /forms/ | Create form |
| GET | /forms/{id}/fields | Get form fields |
| POST | /forms/fields | Create form field |
| GET | /forms/submissions | List submissions |
| POST | /forms/submissions | Submit form data |
| PUT | /forms/submissions/{id} | Update submission |
| GET | /forms/queries | List data queries |
| POST | /forms/queries | Create data query |
| PUT | /forms/queries/{id} | Update data query |

### Ethics
| Method | Path | Description |
|--------|------|-------------|
| GET | /ethics/committees | List ethics committees |
| POST | /ethics/committees | Create committee |
| GET | /ethics/submissions | List submissions |
| POST | /ethics/submissions | Create submission |
| PUT | /ethics/submissions/{id} | Update submission |
| POST | /ethics/approvals | Create approval |
| GET | /ethics/approvals | List approvals |

### Regulatory
| Method | Path | Description |
|--------|------|-------------|
| GET | /regulatory/records | List records |
| POST | /regulatory/records | Create record |
| PUT | /regulatory/records/{id} | Update record |
| GET | /regulatory/checklists | List checklist items |
| POST | /regulatory/checklists | Create checklist item |
| PUT | /regulatory/checklists/{id} | Update checklist item |

### Pharmacovigilance
| Method | Path | Description |
|--------|------|-------------|
| GET | /pharmacovigilance/adverse-events | List AEs |
| POST | /pharmacovigilance/adverse-events | Report AE |
| PUT | /pharmacovigilance/adverse-events/{id} | Update AE |
| GET | /pharmacovigilance/serious-adverse-events | List SAEs |
| POST | /pharmacovigilance/serious-adverse-events | Report SAE |
| PUT | /pharmacovigilance/serious-adverse-events/{id} | Update SAE |
| GET | /pharmacovigilance/safety-signals | List safety signals |
| GET | /pharmacovigilance/summary | Safety summary statistics |

### CDISC
| Method | Path | Description |
|--------|------|-------------|
| GET | /cdisc/mappings | List CDISC mappings |
| POST | /cdisc/export | Export SDTM data (DM, SV, AE) |

### FHIR R4
| Method | Path | Description |
|--------|------|-------------|
| GET | /fhir/Patient/{id} | FHIR Patient resource |
| GET | /fhir/ResearchStudy/{id} | FHIR ResearchStudy |
| GET | /fhir/ResearchSubject/{id} | FHIR ResearchSubject |
| GET | /fhir/Observation/{id} | FHIR Observation |
| GET | /fhir/AdverseEvent/{id} | FHIR AdverseEvent |

### Analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | /analytics/dashboard | Dashboard KPIs and chart data |

### Search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search/?q={query} | Global search across entities |

### Other
| Method | Path | Description |
|--------|------|-------------|
| GET | /audit/ | Audit log entries |
| GET | /notifications/ | User notifications |
| PUT | /notifications/{id}/read | Mark notification read |
| GET | /notifications/unread-count | Unread count |
| GET | /documents/ | List documents |
| POST | /documents/upload | Upload document |

## Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
