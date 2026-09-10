import httpx

BASE = 'http://127.0.0.1:8000/api/v1'
client = httpx.Client(timeout=30, follow_redirects=True)

# 1. Login
print('=== AUTH ===')
r = client.post(f'{BASE}/auth/login', json={'email': 'admin@aiia.gov.in', 'password': 'Demo@12345'})
assert r.status_code == 200, f'Login failed: {r.status_code}'
token = r.json()['access_token']
csrf = r.cookies.get('csrf_token', '')
h = {'Authorization': f'Bearer {token}', 'X-CSRF-Token': csrf}
print('Login OK')

me = client.get(f'{BASE}/auth/me', headers=h).json()
print(f"Me: {me['full_name']} ({me['roles']})")

# 2. Trials
print('\n=== TRIALS ===')
trials = client.get(f'{BASE}/trials/', headers=h).json()
print(f'Trials: {len(trials)}')
for t in trials:
    print(f"  - {t['short_title']}: {t['status']} ({t['participant_count']} participants)")

# 3. Sites
print('\n=== SITES ===')
sites = client.get(f'{BASE}/sites/', headers=h).json()
print(f'Sites: {len(sites)}')

# 4. Participants
print('\n=== PARTICIPANTS ===')
parts = client.get(f'{BASE}/participants/?limit=5', headers=h).json()
print(f'Participants (first 5): {len(parts)}')

# 5. Pharmacovigilance
print('\n=== PHARMACOVIGILANCE ===')
s = client.get(f'{BASE}/pharmacovigilance/summary', headers=h).json()
print(f"AEs: {s['total_aes']}, SAEs: {s['total_saes']}, Open SAEs: {s['open_saes']}")

# 6. Ethics
print('\n=== ETHICS ===')
ethics = client.get(f'{BASE}/ethics/submissions', headers=h).json()
print(f'Ethics submissions: {len(ethics)}')

# 7. Regulatory
print('\n=== REGULATORY ===')
regs = client.get(f'{BASE}/regulatory/records', headers=h).json()
print(f'Regulatory records: {len(regs)}')
checklists = client.get(f'{BASE}/regulatory/checklists', headers=h).json()
print(f'NDCT checklist items: {len(checklists)}')

# 8. Analytics
print('\n=== ANALYTICS ===')
k = client.get(f'{BASE}/analytics/dashboard', headers=h).json()['kpis']
print(f"Active trials: {k['active_trials']}, Participants: {k['total_participants']}, Sites: {k['active_sites']}")
print(f"Enrollment rate: {k['enrollment_rate']}%, Visit compliance: {k['visit_compliance']}%")

# 9. CDISC Export
print('\n=== CDISC ===')
trial_id = trials[0]['id']
cdisc = client.post(f'{BASE}/cdisc/export', headers=h, json={'trial_id': trial_id, 'domains': ['DM', 'AE']}).json()
print(f"CDISC DM records: {len(cdisc.get('DM', []))}")
print(f"CDISC AE records: {len(cdisc.get('AE', []))}")

# 10. FHIR
print('\n=== FHIR ===')
fhir = client.get(f'{BASE}/fhir/ResearchStudy/{trial_id}', headers=h).json()
print(f"FHIR ResearchStudy: {fhir['title'][:50]}")

# 11. Search
print('\n=== SEARCH ===')
sr = client.get(f'{BASE}/search/?q=Ashwagandha', headers=h).json()
print(f"Search results for 'Ashwagandha': {len(sr['results'])}")

# 12. Audit
print('\n=== AUDIT ===')
audit = client.get(f'{BASE}/audit/', headers=h).json()
print(f'Audit log entries: {len(audit)}')

# 13. Notifications
print('\n=== NOTIFICATIONS ===')
nr = client.get(f'{BASE}/notifications/unread-count', headers=h).json()
print(f"Unread notifications: {nr['count']}")

# 14. Documents
print('\n=== DOCUMENTS ===')
docs = client.get(f'{BASE}/documents/', headers=h).json()
print(f'Documents: {len(docs)}')

# 15. Forms
print('\n=== FORMS ===')
forms = client.get(f'{BASE}/forms/', headers=h).json()
print(f'Forms: {len(forms)}')
subs = client.get(f'{BASE}/forms/submissions', headers=h).json()
print(f'Submissions: {len(subs)}')

# 16. RBAC test
print('\n=== RBAC TEST ===')
vr = client.post(f'{BASE}/auth/login', json={'email': 'viewer@aiia.gov.in', 'password': 'Demo@12345'})
vcsrf = vr.cookies.get('csrf_token', '')
vh = {'Authorization': f"Bearer {vr.json()['access_token']}", 'X-CSRF-Token': vcsrf}
r1 = client.get(f'{BASE}/trials/', headers=vh)
print(f'Viewer can read trials: {r1.status_code == 200}')
r2 = client.post(f'{BASE}/trials/', headers=vh, json={'title': 'Test'})
print(f'Viewer blocked from creating trials: {r2.status_code == 403}')

# 17. Demo Records (Demo Account Exclusive)
print('\n=== DEMO RECORDS (EXCLUSIVE TO ADMIN DEMO ACCOUNT) ===')
demo_res = client.get(f'{BASE}/demo/records', headers=h)
assert demo_res.status_code == 200, f'Demo records failed: {demo_res.status_code}'
demo_data = demo_res.json()['records']
print(f"Protocol Review: {demo_data['protocol_review']['title']} ({len(demo_data['protocol_review']['items'])} items)")
print(f"Operational Handoff: {demo_data['operational_handoff']['title']} ({len(demo_data['operational_handoff']['items'])} items)")
print(f"Data Safeguards: {demo_data['data_safeguards']['title']} ({len(demo_data['data_safeguards']['items'])} items)")

# Ensure viewer is blocked from demo records
viewer_demo = client.get(f'{BASE}/demo/records', headers=vh)
print(f"Non-demo account access blocked (HTTP 403): {viewer_demo.status_code == 403}")
assert viewer_demo.status_code == 403

print('\n=== ALL TESTS PASSED ===')
