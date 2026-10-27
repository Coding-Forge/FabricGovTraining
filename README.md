# Fabric Government Training

Microsoft Fabric training for SQL, Power Query, and Power BI practitioners, with a focus on low-code data engineering and GCC High readiness.

**Session 03 is the developed training package:** six lessons, six labs, a PowerPoint presentation, printable handbooks, and a presenter delivery guide. Sessions 01 and 02 are not yet developed.

## Customer downloads

Download the [v1.0.0 release](https://github.com/Coding-Forge/FabricGovTraining/releases/tag/v1.0.0), or get the [complete customer package ZIP](https://github.com/Coding-Forge/FabricGovTraining/releases/download/v1.0.0/FabricGovTraining-v1.0.0.zip).

Extract the ZIP before opening the materials so relative links and lab paths work. It includes this README, the Session 03 blueprint, lessons, labs, presentation, PDFs, synthetic data, scripts, and build tools. Internal program planning and the superseded facilitator draft are excluded.

The release also provides the PowerPoint and three PDFs as individual downloads, plus `SHA256SUMS.txt` for integrity checks. GitHub's automatic **Source code** archives contain the full repository, not the curated customer package.

## Start here

| Your role | Start with |
| --- | --- |
| Presenter | [Session 03 delivery guide](lessons/session_03/delivery_guide.md) for timing, demo/lab handoffs, and recovery plans |
| Participant | [Lab workbook PDF](lessons/session_03/pdf/session_03_lab_workbook.pdf) for exercises and [teaching handbook PDF](lessons/session_03/pdf/session_03_teaching_handbook.pdf) for explanations |
| Lab facilitator | [Setup and reset runbook](lessons/session_03/labs/README.md) for environment preparation, script order, safety, and completion checks |
| Content maintainer | [Session 03 blueprint](session_3_blueprint.md) and the lesson sources linked below |

Use the [54-slide PowerPoint](lessons/session_03/presentation/session_03_low_code_fabric_data_engineering.pptx) as the delivery spine. Keep the delivery guide alongside it: explicit demo switches, lab timing, and break instructions are not consistently visible in the deck.

The [printable delivery guide](lessons/session_03/pdf/session_03_delivery_guide.pdf) is also available.

## Session 03: Low-code Fabric Data Engineering

The three-hour session follows one synthetic reconciliation workload:

```text
SharePoint extracts
  -> Dataflow Gen2
  -> Warehouse Bronze landing tables
  -> SQL Silver normalization and quality checks
  -> Gold reconciliation results
  -> Shared semantic model
  -> Power BI
```

Participants compare two complete extracts, investigate exceptions, rerun the process, and document operating responsibilities. Warehouse is selected for this relational, SQL-first scenario; it is not prescribed for every Fabric workload.

| Module | Allocation | Teaching content | Exercise |
| --- | --- | --- | --- |
| 1. Architecture decision framework | 25 minutes | [Lesson 1](lessons/session_03/01_architecture_decision_framework.md) | [Lab 1](lessons/session_03/labs/01_architecture_lab.md) |
| 2. Repeatable ingestion | 35 minutes | [Lesson 2](lessons/session_03/02_repeatable_ingestion.md) | [Lab 2](lessons/session_03/labs/02_ingestion_lab.md) |
| 3. Curated SQL engineering | 50 minutes | [Lesson 3](lessons/session_03/03_curated_sql_engineering.md) | [Lab 3](lessons/session_03/labs/03_sql_engineering_lab.md) |
| 4. Consumption architecture | 35 minutes | [Lesson 4](lessons/session_03/04_consumption_architecture.md) | [Lab 4](lessons/session_03/labs/04_consumption_lab.md) |
| 5. Operations and GCC High findings | 25 minutes | [Lesson 5](lessons/session_03/05_operations_and_gcc_high_findings.md) | [Lab 5](lessons/session_03/labs/05_operations_lab.md) |
| 6. Exit review | 10 minutes | [Lesson 6](lessons/session_03/06_exit_review.md) | [Lab 6](lessons/session_03/labs/06_exit_review_lab.md) |

The 180-minute agenda includes 96 minutes of practice and a five-minute break, not additional time after the lessons.

## Lab assets and safety

The package includes [baseline, corrected, and expected-result CSVs](lessons/session_03/artifacts/data/), [Warehouse SQL scripts](lessons/session_03/artifacts/sql/), and [DAX measure definitions](lessons/session_03/artifacts/dax/reconciliation_measures.dax).

Use an approved, isolated training Warehouse and synthetic data only. Assign separate Warehouses and source folders to participants or pairs; the scripts use fixed object names. Follow the setup runbook rather than executing every SQL file as one batch. Reset and SQL-only seed scripts require explicit confirmation and must not target production.

The baseline produces six reconciled keys: one match and five exceptions. The corrected input changes A002, producing two matches and four exceptions.

**Tenant execution is not yet verified.** Offline checks do not establish SharePoint authentication, Fabric SQL compatibility, scheduled execution, Direct Lake availability, or consumer permissions. Preflight the actual environment and record whether work was participant-completed, presenter-demonstrated, reviewed as prepared evidence, or blocked. Commercial Fabric documentation is not proof of GCC High availability.

## Repository layout

```text
lesson_plan.md                    Original program context and planning
session_3_blueprint.md             Session 03 outcomes and module outline
session_3_facilitator_guide.md     Earlier planning draft; use delivery_guide.md instead
lessons/
  build_pdfs.py                   Teaching handbook generator
  session_03/
    01_...md through 06_...md      Lesson sources
    delivery_guide.md             Integrated presenter run of show
    labs/                         Setup/reset runbook and six lab guides
    artifacts/
      data/                       Synthetic inputs and expected results
      sql/                        Warehouse setup, publication, checks, and reset
      dax/                        Semantic-model measures
      build_*.py                  Presentation, workbook, and guide generators
      validate_lab_assets.py      Offline lab checks
    presentation/                 Generated PowerPoint
    pdf/                          Generated handbook, workbook, and delivery guide
```

## Rebuild and maintain

Ready-to-use PowerPoint and PDF files are included; Python is needed only to regenerate them or run the offline checks.

Generators require Python 3 with `python-pptx`, `Pillow`, `WeasyPrint`, `markdown-it-py`, and `Pygments`. WeasyPrint also needs its platform-specific system libraries. The current styles and text measurements reference DejaVu fonts under `/usr/share/fonts/truetype/dejavu/`; provide those fonts or update the generator paths for another environment.

Run from the repository root:

```bash
# Check fixtures, source alignment, and lab packaging; no Fabric connection required.
python lessons/session_03/artifacts/validate_lab_assets.py

# Regenerate the presentation and PDFs.
python lessons/session_03/artifacts/build_presentation.py
python lessons/build_pdfs.py
python lessons/session_03/artifacts/build_lab_workbook.py
python lessons/session_03/artifacts/build_delivery_guide.py
```

Edit Markdown lesson/lab sources and the presentation generator rather than only modifying generated files. After rebuilding, check slide and PDF page references in the delivery guide, along with layout and pagination, before sharing the package.
