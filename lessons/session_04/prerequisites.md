# Session 04: Mandatory pre-delivery setup

**Audience:** Customer Azure/Fabric administrators, lab facilitator, and presenter  
**Deadline:** Complete and verify this setup **before the day of delivery**.  
**Default source:** ADLS Gen2, with raw files copied into Lakehouse Files.

This is preparation, not a delivery-day exercise. Participants should arrive
with working access, approved connections, the correct data already landed, and
training targets ready. During delivery, the presenter can explain or rerun the
prepared ingestion; the session must not depend on first-time provisioning.

> **Presenter action: Check in with the customer 3-5 business days before
> delivery.** Confirm the prerequisites have actually been completed, review the
> evidence below, and assign an owner/deadline to each gap. Sending this guide
> without following up is not sufficient. Reconfirm readiness on the preceding
> business day; do not discover missing access or data at the start of class.

## 1. Agree responsibilities and timing

| When | Responsible role | Required action |
| --- | --- | --- |
| At least one week before delivery, earlier if approvals require it | Presenter and customer coordinator | Send this guide and the matching Session 04 materials; assign Azure, Fabric, data-upload, and access owners |
| Before the readiness check-in | Customer administrators and lab facilitator | Complete sections 2-6 and provide actual resource/path/connection details |
| 3-5 business days before delivery | Presenter with customer owners | Check completion, review successful runs and access evidence, identify blockers, and agree remediation |
| Before delivery day; reconfirm on the preceding business day | Presenter and customer coordinator | Complete the rehearsal and participant checks; record a ready/not-ready decision or an explicitly approved modified delivery |
| Delivery day | Presenter | Perform a brief visibility/access check only; use the prepared environment |

Use the customer's actual cloud, tenant, region, networking rules, and approved
identity model. Commercial Fabric documentation is **not proof of GCC High
availability**. If the required ADLS endpoint/authentication/network path is not
supported in the target environment, escalate during preparation.

## 2. Obtain the correct teaching data

The presenter supplies a fixed snapshot of the current Session 04 materials,
including:

- [Scenario inputs and answer keys](artifacts/data/scenario/).
- [Main notebook lab](09_realistic_data_lab.md).
- [Notebook 101 handout](00_notebook_101.md), [survival guide](notebook_survival_guide.md), and [eight importable starter/solution notebooks](notebooks/README.md).
- [Independent challenge](10_independent_challenge.md), [Git lesson](11_git_and_fabric_notebooks.md), and [VS Code lesson](12_vscode_connected_authoring.md).
- [Scenario Warehouse setup](artifacts/sql/scenario_warehouse_setup.sql) and the two publication scripts linked from the lab.

**The v1.0.0 customer release contains Session 03, not these Session 04 assets.**
Do not use it as the Session 04 setup package. Record which repository
commit/package snapshot the presenter supplied and use that same snapshot for
sources, manifest, expected results, notebook cells, and SQL.

The dataset version is `s04-scenario-v1`. The files are already materialized;
participants do not need Python or the generator on their laptops. A maintainer
with Python can check the package before distribution:

```bash
python lessons/session_04/artifacts/validate_examples.py
```

Run this from the supplied repository root. It checks local source hashes,
independent expected results, and reproducibility; it does **not** verify Azure
uploads, tenant permissions, Spark, Data Wrangler, SQL, or live copy activities.
Do not regenerate or change the dataset after readiness sign-off.

## 3. Prepare the ADLS Gen2 source

**Owner:** Customer Azure/storage administrator and data-upload owner.

1. Select an approved training subscription/resource group and storage account,
   or create a dedicated training account under customer policy. The account
   must support **ADLS Gen2 with hierarchical namespace enabled**. Record its
   actual DFS endpoint from the customer's environment; do not substitute a
   commercial-cloud hostname.
2. Create or approve a private container/file system, for example
   `fabric-training`. Record ownership, permitted access, and the agreed
   post-training retention/cleanup date. Do not enable anonymous access.
3. Use Azure Storage Explorer or another approved upload method to upload
   **only the contents of the scenario `devices` and `orders` folders** into
   the following paths. Preserve filenames, bytes, and folder structure.
4. Confirm fourteen CSV files and fourteen JSON Lines files, covering
   October 1-14, 2026. Do not combine, re-save, clean, rename, or decompress
   individual records. There are intentional bad values for the exercises.
5. Keep this versioned source unchanged through delivery. A new copy of a file
   with a suffix is an extra source file, not a correction to the same batch.

```text
<approved-ADLS-DFS-endpoint>
  fabric-training/
    session_04/scenario-v1/
      devices/
        readings_2026-10-01.csv
        ... through readings_2026-10-14.csv
      orders/
        orders_2026-10-01.jsonl
        ... through orders_2026-10-14.jsonl
```

The container and source prefix are examples; record the actual values.
Do **not** upload the micro fixtures, `expected/`, or `manifest.json` into these
source folders. The answer keys are separate teaching assets, staged in step 5.

Grant the upload operator the required scoped data-write permission and the
approved pipeline connection identity **read/list** access to the source.
For example, `Storage Blob Data Reader` at the container scope can provide
source data access; management-plane `Contributor` alone is not data-read
permission. If using ACL-based authorization instead, configure the required
directory traversal and file/directory permissions with the storage owner.
Do not grant all participants storage-administrator access.

Verify firewall/private-endpoint/gateway requirements and the identity that will
actually execute the copy. A successful upload from an administrator's laptop
does not prove that Fabric can read the same files. Keep credentials in approved
managed connections, never notebook cells, documents, screenshots, or the repo.
Do not weaken the customer's network controls to make the lab work.

## 4. Prepare Fabric resources and access

**Owner:** Customer Fabric administrator and lab facilitator.

Create or allocate an approved training workspace/capacity and a separate
Lakehouse and Warehouse **per participant/pair**, plus a presenter rehearsal
environment. Source ADLS files can be shared read-only; fixed `s04_lab_` output
tables must not have competing writers.

Before delivery, verify:

- The assigned users can sign in, open their workspace, run a PySpark notebook,
  and write the intended Lakehouse training tables.
- The correct Lakehouse is attached as the notebook's **default Lakehouse**;
  its table/schema naming behavior matches the notebook and copy selections.
- The actual runtime starts and supports the lab's Spark expressions; Data
  Wrangler and notebook chart controls are available for the intended users.
- The source ADLS connection is configured with an approved supported identity,
  and the operators can use the connection without receiving its secrets.
- The Lakehouse and Warehouse connections, any required copy staging, and
  network routes work under the intended identities, not just an administrator.
- The intended SQL operator can create the isolated training objects and
  execute the publication scripts; intended consumers can query the result.
  If semantic-model consumption is included, also preflight its permissions
  and freshness behavior.

Run [scenario Warehouse setup](artifacts/sql/scenario_warehouse_setup.sql)
**once, before delivery**, in each fresh isolated training **Warehouse**.
It creates `stg.s04_lab_order_line`, `gold.s04_lab_order_line`,
`stg.s04_lab_device_daily`, and `gold.s04_lab_device_daily`.
Do not run it in the Lakehouse SQL analytics endpoint, use the micro-fixture
DDL, or automatically drop/alter existing objects. Stop and use an approved
fresh target if the names already contain unknown data or incompatible schemas.

Direct Spark-to-Warehouse writing is not required for this setup. Use the
verified copy route; do not assume that optional connector identity/runtime
support is the same as ADLS pipeline support.

Import the starter notebooks into each assigned environment **before class**,
following [the notebook import guide](notebooks/README.md). Confirm PySpark and
the correct default Lakehouse; no resource/environment binding is embedded in
the files. Give each learner/pair its own notebook items and a lowercase learner
ID for the optional `s04_101_<id>_demo` table. Keep solutions as separate
presenter/recovery items; never overwrite participant edits.

### Git and VS Code module preparation

If these follow-on modules are in the agreed delivery scope, verify their
additional prerequisites **before class**, at the same 3-5-business-day check-in:

- Customer-approved **private practice repository**, supported provider, feature
  branch/review target, and isolated practice workspace per pair. Do not connect
  customer workspaces to the public training-material repository.
- Actual-cloud Git support, tenant/provider switches, capacity, network rules,
  repository/workspace permissions, and an admin-prepared connection to the
  intended branch/folder. Do not replace an existing shared workspace connection.
- A separately imported read-only troubleshooting solution named per pair, with
  the correct default Lakehouse and sources; no main-lab writes are needed.
- If VS Code is included: approved VS Code, Fabric Data Engineering
  (`SynapseVSCode.synapse`) and Jupyter (`ms-toolsai.jupyter`) extensions, approved
  local working folder, correct-cloud/tenant sign-in, workspace discovery, and
  verified **Microsoft Fabric Runtime** remote execution.
- Actual Git commit/update/PR and extension download/Publish/Update Notebook
  rehearsal under the intended identities, with customer-approved evidence.

Browser access is not proof of Git/provider or extension Government-cloud
support. If a module cannot be used in the approved environment, agree a
labeled conceptual demonstration or omission in advance; do not bypass cloud,
identity, network, or branch protections. This does not block the separately
verified browser notebook path.

## 5. Land the raw files and stage the answer keys

**Owner:** Lab facilitator, using the approved connections.

Create a Fabric pipeline, for example `s04_prepare_raw_inputs`, with two copy
activities. Configure **file-to-file Binary copy** on both ends so the notebook,
not the ingestion pipeline, parses CSV/JSON and applies cleaning rules.

| Setting | Device copy | Order copy |
| --- | --- | --- |
| Source connection | Approved ADLS Gen2 connection | Same approved source connection |
| File system | Actual training container | Actual training container |
| Source folder | `session_04/scenario-v1/devices` | `session_04/scenario-v1/orders` |
| Wildcard filename | `*.csv` | `*.jsonl` |
| Recursive reading | Off; these folders have no nested inputs | Off |
| Source and destination format | Binary | Binary |
| Destination item/root | Assigned training Lakehouse / **Files** | Assigned training Lakehouse / **Files** |
| Destination folder, relative to Files | `session_04/scenario/devices` | `session_04/scenario/orders` |
| Destination filenames | Preserve original names; do not merge | Preserve original names; do not merge |
| Copy behavior | Preserve hierarchy relative to the selected source folder | Same |

Use actual tenant UI names if they differ. Leave last-modified filters unset,
disable source deletion after copy, and do not add transformations or column
mappings. Select **Files**, not Tables. Do not use a shortcut for the default
lab: a shortcut is a reference to the source, not a retained landing copy.

Run the pipeline **before delivery** into every assigned Lakehouse. Verify
successful activity runs, fourteen files per destination folder, unchanged
filenames/file sizes, and the exact final paths below. Adjust the copy root if
it adds an unexpected extra source-folder level. Do not change the notebook
path to conceal an incorrectly prepared folder tree.

Using the Lakehouse's approved upload interface, separately upload
`scenario/manifest.json` to `Files/session_04/scenario/manifest.json` and the two
`scenario/expected/*.csv` files to `Files/session_04/scenario/expected/`.
These are notebook answer keys, not raw source data. The final structure in
**each** participant/pair Lakehouse must be:

```text
Files/session_04/scenario/
  devices/              14 copied source CSV files
  orders/               14 copied source JSON Lines files
  expected/
    device_daily.csv
    order_lines.csv
  manifest.json
```

Do not place another `scenario` folder inside this path. Do not read the entire
tree as one dataset: the notebook's explicit source globs exclude answer keys.
Do not rerun preparation while a notebook/copy is using the inputs, and do not
delete or overwrite unrelated files. Review any unexpected destination files
with the owner rather than performing a broad cleanup.

If the presenter plans to use the optional micro examples, also pre-stage
`orders.jsonl` at `Files/session_04/orders/batch-001/orders.jsonl` and
`device_readings.csv` at `Files/session_04/devices/batch-001/device_readings.csv`.
Keep them outside the scenario source folders. Prepare their separate
[micro-fixture Warehouse objects](04_warehouse_gold.md#1-prepare-fixed-contracts-in-an-isolated-warehouse)
before delivery if that publication will be shown; never substitute their DDL
or expected counts for the main lab.

## 6. Rehearse and verify readiness

**Owner:** Presenter and lab facilitator, with the customer's resource owners.

Rehearse [Notebook 101](00_notebook_101.md) and the troubleshooting pair first.
Confirm the three starter practice stops and three intentional repair errors
match the handouts, and that solutions run in order. If demonstrating
persistence, approve a fresh learner-named target and test the optional write
plus restart/read-back; keep the write flag off for the read-back rerun.
Never switch to overwrite to bypass a rehearsal table. Record skipped optional
writes explicitly.

In the presenter rehearsal environment, run the **complete main lab** using the
prepared source scope and intended identities. After proving ADLS-to-Files copy,
run notebook sections 1-8, including Wrangler/chart steps, to create and verify
the transfer tables. Then configure and test the two Gold-staging copy
activities from [main lab section 9](09_realistic_data_lab.md#9-copy-validate-and-publish-warehouse-gold),
including explicit mappings and reviewed batch-only staging cleanup. Complete
SQL publication and consumer checks. Leave the copy activities configured for
delivery; participants should not create their connections for the first time
in class. Do not perform setup by copying data straight into live Gold.

Both main-lab variants intentionally stop at `RUN_TRAINING_LAB=False` until
the approved Lakehouse/write scope is verified. Complete the three additional
starter checkpoints when rehearsing the participant path. Warehouse SQL remains
Markdown in the imported notebook and must run in the actual Warehouse.
After the main notebook succeeds, rehearse the read-only
[independent challenge](10_independent_challenge.md) in a fresh session.
Verify both D032 daily summaries and the explicit zero-rejection-day explanation.
Use the [full live-testing sequence](notebooks/README.md#first-real-workspace-test)
to include Git/VS Code if those modules are in scope.

| Evidence | Required result for scenario v1 |
| --- | --- |
| ADLS source and Lakehouse landing | 14 device files and 14 order files; matching names/sizes; successful raw-copy runs |
| Device Bronze | 201,579 source rows, excluding CSV headers |
| Orders Bronze | 5,000 JSON documents |
| Device acceptance | 194,545 accepted events; 7,034 quarantined rows |
| Order acceptance | 14,391 accepted lines; 663 quarantined evidence rows |
| Complete expected-row comparisons | Both notebook comparisons succeed, including every transfer business row |
| Device Warehouse Gold | 700 device/day rows representing 194,545 accepted readings |
| Order Warehouse Gold | 14,391 accepted lines; accepted-line amount 5,643,227.95 |
| User experience | Intended identities can perform their assigned actions; Wrangler/charts and SQL/consumer access are verified |
| Beginner notebook assets | Starters imported, PySpark/default attachment verified, practice/repair stops understood, solutions rehearsed, optional restart/read-back demonstrated or explicitly skipped |
| Independent analysis | Challenge runs from persisted main tables in a fresh session; accepted coverage and source/quarantine populations explained |
| Git / VS Code, if included | Actual private branch/sync/PR and approved-cloud remote-runtime/publish/update operations verified, or blocked/modified scope agreed |

The amount includes multiple order statuses and is not recognized revenue.
Review all individual rejection counts against the manifest, not just totals.
Keep screenshots/run IDs and SQL results in an approved customer location;
record failures honestly. Do not put credentials in the evidence.

For **every participant/pair environment**, verify access with the assigned user,
default Lakehouse, manifest/answer-key visibility, source file counts, actual
Spark source row counts, Warehouse objects, and usable connections. A presenter
rehearsal alone does not establish participant readiness. Run approved notebook
landing checks from the main lab in the isolated targets as needed; preserve
the raw inputs and record whether rehearsal outputs remain. No automatic
reset/drop of training tables is required.

## 7. Presenter check-in and go/no-go

At the **3-5-business-day customer check-in**, review the evidence above together.
Record the following in the customer's approved coordination channel:

| Item | Record |
| --- | --- |
| Delivery date and customer setup owner | Agreed date and responsible role/contact |
| Materials | Supplied package snapshot and `s04-scenario-v1` |
| Actual environment | Cloud/tenant, workspace, capacity, per-pair Lakehouse/Warehouse assignments |
| Source | ADLS DFS endpoint, container, prefix; no credentials |
| Execution | Connection names, intended identities, successful raw-copy and rehearsal run references |
| Participant readiness | Access and landing checks completed for each participant/pair |
| Development modules | Git/VS Code included or excluded; actual provider/extension versions, connectivity, remote execution, and sync evidence if included |
| Exceptions | Blocked step, owner, remediation deadline, and agreed impact |
| Decision | Ready, not ready, or approved modified delivery; who approved and when |

If work is incomplete, assign owners and resolve it **before delivery day**.
Reconfirm on the preceding business day. No confirmation means prerequisites
are **not verified**; silence is not approval.

If ADLS/copy or another required feature remains blocked, tell the customer
before delivery and agree whether to reschedule or use an explicitly modified
demonstration. An approved manual upload of the scenario folder can preserve
the notebook exercises, but bypasses the ADLS ingestion objective and must be
labeled as such. A SharePoint source is a separately agreed ingestion variant,
not a drop-in replacement for this pipeline configuration. Prepared screenshots
or a successful administrator session must not be reported as participant
completion.

## References

Microsoft configuration references, checked October 29, 2026; validate actual
Government-cloud support and identity/network behavior during preparation:

- [ADLS Gen2 connector capabilities](https://learn.microsoft.com/en-us/fabric/data-factory/connector-azure-data-lake-storage-gen2-overview)
- [ADLS Gen2 copy activity configuration](https://learn.microsoft.com/en-us/fabric/data-factory/connector-azure-data-lake-storage-gen2-copy-activity)
- [Lakehouse copy activity configuration](https://learn.microsoft.com/en-us/fabric/data-factory/connector-lakehouse-copy-activity)

**Delivery starts only after this readiness gate.**
Continue with [Notebook 101](00_notebook_101.md) for first-time users, then
[the main notebook lab](09_realistic_data_lab.md).
