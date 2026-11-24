# cdnet-dup-repro — QD-16773

Reproduces the backend/frontend problem-count mismatch from
[QD-16773](https://youtrack.jetbrains.com/issue/QD-16773) with the production
`jetbrains/qodana-cdnet:2026.2` linter and an unmodified SARIF.

## Cause

qodana-cdnet gives the same `equalIndicator/v1` hash to different inspections
that report on the same code range:

| Code | Inspections sharing one hash |
|---|---|
| `public class Program` (`Program.cs:8`) | `ClassNeverInstantiated.Global`, `ConvertToStaticClass` |
| `private int unusedField;` (`Program.cs:10`) | `InconsistentNaming`, `UnusedField.Compiler` |

- Backend counts every result → timeline shows **12**.
- Frontend `filterValidProblems` (`Frontend/src/helpers/convertProblems.ts`) keeps one
  problem per hash → "Current problems" shows **10**.

## Run

```bash
export QODANA_ENDPOINT=https://web.cloud.sssa-qa.aws.intellij.net
export QODANA_TOKEN=<QA project token>
qodana scan --solution cdnet-dup.sln --results-dir ./out
python3 check_dups.py out/qodana.sarif.json
```

Expected `check_dups.py` output:

```
results 12, unique hashes 10
8A28FF1EEF4BA3F3 ClassNeverInstantiated.Global line 8
8A28FF1EEF4BA3F3 ConvertToStaticClass line 8
1AAD898379A0EF48 InconsistentNaming line 10
1AAD898379A0EF48 UnusedField.Compiler line 10
```

Example report: https://web.cloud.sssa-qa.aws.intellij.net/projects/VPp9A/reports/PD7vY

## Notes

- The git remote `origin` is a placeholder. Without any remote the upload fails with
  `400 {"name":"validation_failed","details":"projectUrl: Must be valid"}`.
- The first report of a new project goes to baseline, so the 12 vs 10 gap then shows under the
  baseline tab. Scan twice, or look at the second report.
