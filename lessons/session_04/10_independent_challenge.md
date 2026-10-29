# Independent challenge: Explain a device's daily readings

**Session 04 | Read-only exit exercise**  
**Output:** A small, reproducible analysis and an evidence-backed explanation, without step-by-step transformation code.

Complete [Notebook 101](00_notebook_101.md) and the successful
[main scenario notebook](09_realistic_data_lab.md) first. Use the same approved
default Lakehouse and batch `s04-lab-devices-001`. Warehouse publication is not
required for this Lakehouse analysis and must not be inferred from its success.

Import [the challenge starter](notebooks/03_independent_challenge_starter.ipynb).
It supplies context/table reads, two code-task placeholders, and a Markdown
answer area. Replace the labeled `NotImplementedError` stops with your analysis.
Do not open [the presenter solution](notebooks/03_independent_challenge_solution.ipynb)
until the learner has submitted an attempt or requested recovery.

## The business question

Operations asks:

> For **D032 on October 10, 2026 (UTC)**, what were the accepted reading count,
> minimum, maximum, and average temperature? How does the reported daily average
> compare with **October 6**? Were all scheduled observations accepted, and what
> can we legitimately conclude about device health?

These are different device/date selections from the guided coverage checkpoint.
The source contract schedules one observation every five minutes: **288 per
device/day**. That is a known teaching denominator, not something inferred from
the number of records that arrived.

## Constraints

- Read existing `s04_lab_device_silver`, `s04_lab_device_bronze`, and
  `s04_lab_device_rejected`, filtered to the intended batch.
- Use typed **accepted Silver events** for temperature metrics; do not re-clean
  Bronze or quietly change the acceptance policy.
- Preserve the device/day grain and useful site/type context. Filter to the two
  requested UTC dates before presenting results.
- Do not write, append, overwrite, publish, install packages, change permissions,
  or edit source files. Keep driver-side output small.
- Use [the survival guide](notebook_survival_guide.md) and
  [PySpark reference](08_pyspark_function_reference.md) as lookup aids, not a
  copied worked transformation.

## Task 1: Produce the daily summary

Return one row per requested device/day with:

| Required field | Meaning |
| --- | --- |
| UTC date, device, site, device type | Scope and grain |
| Accepted reading count | Not the raw source count |
| Minimum, maximum, average temperature | Accepted events only; show the mean to two decimal places |
| Scheduled readings and accepted-slot shortfall | 288 and its difference from accepted count |
| Accepted percentage | Accepted count / scheduled readings, labeled clearly |

Compare the two **reported rounded daily means** without calling the difference
statistically significant or treating their average as an overall event mean.

## Task 2: Explain the source and quarantine evidence

Count raw source rows and primary quarantine reasons for D032 from each of the
two daily **source exports**. Include a zero-rejection day in your explanation,
even if the grouped quarantine result has no row for it.

Use `source_file` to identify the relevant `readings_YYYY-MM-DD.csv` export.
A record with an invalid timestamp cannot reliably be assigned an event day by
parsing that timestamp; an export filename supplies source-scope evidence, not
a repaired business timestamp.

Explain why raw row count, quarantine row count, accepted count, and scheduled
slots are different populations. Both occurrences of an ambiguous duplicated
event were rejected under the existing policy.

## Task 3: Write the interpretation

In the notebook's Markdown answer area, state:

1. The input tables, batch, device, dates, and output grain.
2. The two summaries and the direction/magnitude of the reported-mean change.
3. Whether accepted coverage is complete on the requested date and the evidence.
4. What zero quarantine rows does **not** prove, and why shortfall is not
   automatically device downtime.
5. Why two daily summaries do not establish device health, a trend, statistical
   significance, or a firmware-related cause.
6. Where the computation ran, whether anything was persisted, and which outputs
   this exercise does not prove (for example Warehouse Gold/model freshness).

Add a short Markdown title/question and scope above your analysis. Use
autocomplete/API help when useful. Preserve any error and explain its correction
rather than suppressing it.

## Completion rubric

| Evidence | Accept when |
| --- | --- |
| Scope/context | Correct default Lakehouse, batch, device, two UTC dates, and existing approved tables |
| Computation | Both device/day rows, correct accepted-only metrics, explicit denominator and no unintended grain change |
| Quality reasoning | Raw/export/quarantine/accepted populations distinguished, including an explicit zero-rejection case |
| Interpretation | Numerical comparison and honest completeness/causality limitations |
| Reproducibility/safety | Fresh-session run succeeds; no writes, secrets, unbounded collections, or bypassed controls |

The presenter compares results with the separate solution/answer key and checks
the learner's explanation, not just cell status. Restart your own session and
rerun the completed challenge from the top; the setup reads persisted main-lab
tables, so it must not depend on variables left in another notebook.

**Presenter:** Rehearse this after the main notebook and record actual Fabric
results in the [live-workspace test sequence](notebooks/README.md#first-real-workspace-test).
Offline checks do not prove tenant import, execution, access, or UI behavior.
