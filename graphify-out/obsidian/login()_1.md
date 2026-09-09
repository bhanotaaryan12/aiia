---
source_file: "backend/app/api/v1/auth.py"
type: "code"
community: "User Authentication and Access Control"
location: "L13"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/User_Authentication_and_Access_Control
---

# login()

## Connections
- [[AsyncSession_11]] - `references` [EXTRACTED]
- [[LoginRequest]] - `uses` [INFERRED]
- [[Role]] - `uses` [INFERRED]
- [[TokenResponse]] - `uses` [INFERRED]
- [[User]] - `uses` [INFERRED]
- [[UserRole]] - `uses` [INFERRED]
- [[create_access_token()]] - `calls` [EXTRACTED]
- [[create_refresh_token()]] - `calls` [EXTRACTED]
- [[post_8]] - `references` [EXTRACTED]
- [[v1auth.py]] - `contains` [EXTRACTED]
- [[verify_password()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/User_Authentication_and_Access_Control