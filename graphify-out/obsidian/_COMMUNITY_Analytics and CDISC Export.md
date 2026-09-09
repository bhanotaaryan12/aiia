---
type: community
members: 76
---

# Analytics and CDISC Export

**Members:** 76 nodes

## Members
- [[AdverseEvent]] - code - backend/app/models/pharmacovigilance.py
- [[AsyncSession]] - code
- [[AsyncSession_1]] - code
- [[AsyncSession_2]] - code
- [[BaseModel]] - code - backend/app/models/base.py
- [[CDISCExportRequest]] - code - backend/app/schemas/cdisc.py
- [[CDISCMapping]] - code - backend/app/models/cdisc.py
- [[CDISCMappingOut]] - code - backend/app/schemas/cdisc.py
- [[CausalityAssessment]] - code - backend/app/models/pharmacovigilance.py
- [[ChartData]] - code - backend/app/schemas/analytics.py
- [[Comprehensive seed data for AIIA CTMS demo.]] - rationale - backend/app/seed.py
- [[Config]] - code - backend/app/schemas/cdisc.py
- [[Consent]] - code - backend/app/models/participant.py
- [[DashboardData]] - code - backend/app/schemas/analytics.py
- [[DashboardKPIs]] - code - backend/app/schemas/analytics.py
- [[DataPoint]] - code - backend/app/models/form.py
- [[DataQuery]] - code - backend/app/models/form.py
- [[Document]] - code - backend/app/models/document.py
- [[Enrollment]] - code - backend/app/models/participant.py
- [[EthicsApproval]] - code - backend/app/models/ethics.py
- [[EthicsCommittee]] - code - backend/app/models/ethics.py
- [[EthicsReview]] - code - backend/app/models/ethics.py
- [[EthicsSubmission]] - code - backend/app/models/ethics.py
- [[Form]] - code - backend/app/models/form.py
- [[FormField]] - code - backend/app/models/form.py
- [[FormSubmission]] - code - backend/app/models/form.py
- [[Intervention]] - code - backend/app/models/trial.py
- [[Investigator]] - code - backend/app/models/site.py
- [[Notification]] - code - backend/app/models/notification.py
- [[ParticipantVisit]] - code - backend/app/models/visit.py
- [[Permission]] - code - backend/app/models/user.py
- [[Protocol]] - code - backend/app/models/trial.py
- [[ProtocolAmendment]] - code - backend/app/models/ethics.py
- [[Randomization]] - code - backend/app/models/participant.py
- [[RegulatoryRecord]] - code - backend/app/models/regulatory.py
- [[RolePermission]] - code - backend/app/models/user.py
- [[SafetySignal]] - code - backend/app/models/pharmacovigilance.py
- [[Screening]] - code - backend/app/models/participant.py
- [[SeriousAdverseEvent]] - code - backend/app/models/pharmacovigilance.py
- [[Site]] - code - backend/app/models/site.py
- [[SiteAssignment]] - code - backend/app/models/site.py
- [[StudyArm]] - code - backend/app/models/trial.py
- [[Trial]] - code - backend/app/models/trial.py
- [[TrialMilestone]] - code - backend/app/models/trial.py
- [[VisitDefinition]] - code - backend/app/models/visit.py
- [[Withdrawal]] - code - backend/app/models/participant.py
- [[base.py]] - code - backend/app/models/base.py
- [[export_cdisc()]] - code - backend/app/api/v1/cdisc.py
- [[get]] - code
- [[get_1]] - code
- [[get_2]] - code
- [[get_dashboard()]] - code - backend/app/api/v1/analytics.py
- [[global_search()]] - code - backend/app/api/v1/search.py
- [[list_mappings()]] - code - backend/app/api/v1/cdisc.py
- [[models__init__.py]] - code - backend/app/models/__init__.py
- [[modelscdisc.py]] - code - backend/app/models/cdisc.py
- [[modelsdocument.py]] - code - backend/app/models/document.py
- [[modelsethics.py]] - code - backend/app/models/ethics.py
- [[modelsform.py]] - code - backend/app/models/form.py
- [[modelsnotification.py]] - code - backend/app/models/notification.py
- [[modelsparticipant.py]] - code - backend/app/models/participant.py
- [[modelspharmacovigilance.py]] - code - backend/app/models/pharmacovigilance.py
- [[modelsregulatory.py]] - code - backend/app/models/regulatory.py
- [[modelssite.py]] - code - backend/app/models/site.py
- [[modelstrial.py]] - code - backend/app/models/trial.py
- [[modelsuser.py]] - code - backend/app/models/user.py
- [[modelsvisit.py]] - code - backend/app/models/visit.py
- [[post]] - code
- [[rand_id()]] - code - backend/app/seed.py
- [[schemasanalytics.py]] - code - backend/app/schemas/analytics.py
- [[schemascdisc.py]] - code - backend/app/schemas/cdisc.py
- [[seed.py]] - code - backend/app/seed.py
- [[seed_data()]] - code - backend/app/seed.py
- [[v1analytics.py]] - code - backend/app/api/v1/analytics.py
- [[v1cdisc.py]] - code - backend/app/api/v1/cdisc.py
- [[v1search.py]] - code - backend/app/api/v1/search.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Analytics_and_CDISC_Export
SORT file.name ASC
```

## Connections to other communities
- 59 edges to [[_COMMUNITY_Audit Logs and Document Management]]
- 39 edges to [[_COMMUNITY_FHIR R4 Interoperability Routes]]
- 35 edges to [[_COMMUNITY_User Authentication and Access Control]]
- 25 edges to [[_COMMUNITY_eCRF Forms and Data Queries]]
- 23 edges to [[_COMMUNITY_Pharmacovigilance and Safety Management]]
- 23 edges to [[_COMMUNITY_Clinical Trials and Study Arms]]
- 21 edges to [[_COMMUNITY_Ethics Committees and Approvals]]
- 16 edges to [[_COMMUNITY_Regulatory Compliance and Tracking]]
- 13 edges to [[_COMMUNITY_Visit Schedules and Tracking]]
- 4 edges to [[_COMMUNITY_Context Memory API Routes]]
- 4 edges to [[_COMMUNITY_Graphify Memory Extraction Pipeline]]
- 2 edges to [[_COMMUNITY_Tenant Graph Storage Backend]]
- 1 edge to [[_COMMUNITY_Context Builder and Ranking Engine]]
- 1 edge to [[_COMMUNITY_FHIR Pydantic Data Schemas]]

## Top bridge nodes
- [[BaseModel]] - degree 140, connects to 14 communities
- [[seed.py]] - degree 58, connects to 4 communities
- [[models__init__.py]] - degree 56, connects to 4 communities
- [[seed_data()]] - degree 39, connects to 4 communities
- [[v1analytics.py]] - degree 32, connects to 3 communities