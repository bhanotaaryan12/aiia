---
type: community
members: 71
---

# Audit Logs and Document Management

**Members:** 71 nodes

## Members
- [[Append-only audit log - no updates or deletes.]] - rationale - backend/app/models/audit.py
- [[AsyncSession_3]] - code
- [[AsyncSession_4]] - code
- [[AsyncSession_5]] - code
- [[AsyncSession_6]] - code
- [[AuditLog]] - code - backend/app/models/audit.py
- [[AuditLogOut]] - code - backend/app/schemas/audit.py
- [[Base]] - code - backend/app/core/database.py
- [[BaseSettings]] - code
- [[Config_1]] - code - backend/app/schemas/audit.py
- [[Config_2]] - code - backend/app/schemas/document.py
- [[Config_3]] - code - backend/app/schemas/notification.py
- [[Config_4]] - code - backend/app/schemas/site.py
- [[DeclarativeBase]] - code
- [[DocumentCreate]] - code - backend/app/schemas/document.py
- [[DocumentOut]] - code - backend/app/schemas/document.py
- [[FastAPI]] - code
- [[InvestigatorCreate]] - code - backend/app/schemas/site.py
- [[InvestigatorOut]] - code - backend/app/schemas/site.py
- [[NotificationOut]] - code - backend/app/schemas/notification.py
- [[Request]] - code
- [[Settings]] - code - backend/app/core/config.py
- [[SiteAssignmentCreate]] - code - backend/app/schemas/site.py
- [[SiteCreate]] - code - backend/app/schemas/site.py
- [[SiteOut]] - code - backend/app/schemas/site.py
- [[SiteUpdate]] - code - backend/app/schemas/site.py
- [[UploadFile]] - code
- [[config.py]] - code - backend/app/core/config.py
- [[create_investigator()]] - code - backend/app/api/v1/sites.py
- [[create_site()]] - code - backend/app/api/v1/sites.py
- [[create_site_assignment()]] - code - backend/app/api/v1/sites.py
- [[database.py]] - code - backend/app/core/database.py
- [[documents.py]] - code - backend/app/api/v1/documents.py
- [[get_3]] - code
- [[get_4]] - code
- [[get_5]] - code
- [[get_6]] - code
- [[get_7]] - code
- [[get_db()]] - code - backend/app/core/database.py
- [[get_site()]] - code - backend/app/api/v1/sites.py
- [[health_check()]] - code - backend/app/main.py
- [[lifespan()]] - code - backend/app/main.py
- [[list_audit_logs()]] - code - backend/app/api/v1/audit.py
- [[list_documents()]] - code - backend/app/api/v1/documents.py
- [[list_investigators()]] - code - backend/app/api/v1/sites.py
- [[list_notifications()]] - code - backend/app/api/v1/notifications.py
- [[list_sites()]] - code - backend/app/api/v1/sites.py
- [[log_requests()]] - code - backend/app/main.py
- [[main.py]] - code - backend/app/main.py
- [[mark_all_read()]] - code - backend/app/api/v1/notifications.py
- [[mark_as_read()]] - code - backend/app/api/v1/notifications.py
- [[middleware]] - code
- [[modelsaudit.py]] - code - backend/app/models/audit.py
- [[notifications.py]] - code - backend/app/api/v1/notifications.py
- [[post_1]] - code
- [[post_2]] - code
- [[put]] - code
- [[put_1]] - code
- [[readiness_check()]] - code - backend/app/main.py
- [[require_roles()]] - code - backend/app/core/security.py
- [[router.py]] - code - backend/app/api/v1/router.py
- [[schemasaudit.py]] - code - backend/app/schemas/audit.py
- [[schemasdocument.py]] - code - backend/app/schemas/document.py
- [[schemasnotification.py]] - code - backend/app/schemas/notification.py
- [[schemassite.py]] - code - backend/app/schemas/site.py
- [[sites.py]] - code - backend/app/api/v1/sites.py
- [[unread_count()]] - code - backend/app/api/v1/notifications.py
- [[update_site()]] - code - backend/app/api/v1/sites.py
- [[upload_document()]] - code - backend/app/api/v1/documents.py
- [[v1__init__.py]] - code - backend/app/api/v1/__init__.py
- [[v1audit.py]] - code - backend/app/api/v1/audit.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Audit_Logs_and_Document_Management
SORT file.name ASC
```

## Connections to other communities
- 59 edges to [[_COMMUNITY_Analytics and CDISC Export]]
- 22 edges to [[_COMMUNITY_User Authentication and Access Control]]
- 12 edges to [[_COMMUNITY_FHIR R4 Interoperability Routes]]
- 5 edges to [[_COMMUNITY_Ethics Committees and Approvals]]
- 5 edges to [[_COMMUNITY_eCRF Forms and Data Queries]]
- 5 edges to [[_COMMUNITY_Pharmacovigilance and Safety Management]]
- 5 edges to [[_COMMUNITY_Regulatory Compliance and Tracking]]
- 5 edges to [[_COMMUNITY_Clinical Trials and Study Arms]]
- 5 edges to [[_COMMUNITY_Visit Schedules and Tracking]]
- 2 edges to [[_COMMUNITY_Context Memory API Routes]]

## Top bridge nodes
- [[FastAPI]] - degree 22, connects to 10 communities
- [[router.py]] - degree 21, connects to 10 communities
- [[database.py]] - degree 25, connects to 9 communities
- [[get_db()]] - degree 19, connects to 9 communities
- [[require_roles()]] - degree 13, connects to 9 communities