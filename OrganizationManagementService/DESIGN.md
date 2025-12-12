# Design Choices & Trade-offs

## Architecture
We chose a **Multi-tenant Database Architecture** using "Shared Database, Separate Collections".
- **Master Database**: Holds metadata and routing information.
- **Dynamic Collections**: `org_<name>` stores tenant-specific data.

### Why this approach?
- **Isolation**: logical separation of data.
- **Scalability**: Easier to shard collections or move specific collections to different DB servers in the future compared to a single huge table.
- **Simplicity**: Easier to manage than "Database per Tenant" (too much overhead) but safer than "Shared Schema" (row-level security risks).

### Tech Stack
- **FastAPI**: High performance, async, auto-documentation.
- **MongoDB (Motor)**: Schema-less flexibility fits the "dynamic collection" requirement perfectly.
- **JWT**: Stateless authentication standard.

## Trade-offs & Challenges
1.  **Renaming Organizations**:
    - *Challenge*: Renaming an organization requires renaming the underlying collection (`org_Old` -> `org_New`).
    - *Solution*: We implemented a migration step in `PUT /org/update` that renames the collection.
    - *Trade-off*: This is a heavy operation. In a distributed MongoDB cluster, `renameCollection` can be expensive or restricted. A better design might be using an immutable `org_id` for the collection name (`org_uuid123`) and mapping it to a display name. However, the requirements suggested `org_<organization_name>`.

2.  **Scalability**:
    - *Good*: MongoDB handles many collections well.
    - *Risk*: If we have 100k organizations, 100k collections might strain the namespace limit or metadata server. "Database per Tenant" might be better for that scale, or "Shared Collection with TenantID" (Sharding).

## Additional Questions Answered
**Q: Do you think this is a good architecture with a scalable design?**
A: It is scalable up to a mid-to-large size. For massive scale (SaaS like Salesforce), "Shared Schema" with Sharding (based on TenantID) is often preferred over "Collection per Tenant" because of database file overhead and namespace limits. However, for an internal tool or moderate SaaS, "Collection per Tenant" offers great isolation and backup/restore flexibility.

**Q: Design better?**
A: Use **Immutable IDs** for collection names (e.g., `org_8f7d2a...`). This decouples the "Display Name" from the "Storage Name". Renaming the organization would then be a simple metadata update (O(1)) instead of moving/renaming the entire data collection.
