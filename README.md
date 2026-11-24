# cdnet-dup-repro — QD-16773

Reproduces the backend/frontend problem-count mismatch from
[QD-16773](https://youtrack.jetbrains.com/issue/QD-16773) with the production
Qodana Community for .NET linter (`jetbrains/qodana-cdnet:2026.2`) and an unmodified SARIF.

## Cause

qodana-cdnet gives the same `equalIndicator/v1` hash to different inspections that report on
the same code range:

| Code | Inspections sharing one hash |
|---|---|
| `public class Program` (`Program.cs:3`) | `ClassNeverInstantiated.Global`, `ConvertToStaticClass` |
| `private int unusedField;` (`Program.cs:5`) | `InconsistentNaming`, `UnusedField.Compiler` |

- Backend counts every result → timeline shows **5**.
- Frontend `filterValidProblems` (`Frontend/src/helpers/convertProblems.ts`) keeps one problem
  per hash → "Current problems" shows **3**.

## Run

```bash
export QODANA_ENDPOINT=https://web.cloud.sssa-qa.aws.intellij.net
export QODANA_TOKEN=<QA project token>
qodana scan --solution cdnet-dup.sln
```

Open the report link printed at the end and compare the timeline bar with "Current problems".

## Notes

- The git remote `origin` is a placeholder. Without any remote the upload fails with
  `400 {"name":"validation_failed","details":"projectUrl: Must be valid"}`.
- The first report of a new project goes to baseline, so the gap then shows under the baseline
  tab. Scan twice, or look at the second report.
