"""Print results that share an equalIndicator/v1 hash in a Qodana SARIF."""
import collections
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "out/qodana.sarif.json"
results = json.load(open(path))["runs"][0]["results"]
hashes = collections.Counter(r["partialFingerprints"]["equalIndicator/v1"] for r in results)
print(f"results {len(results)}, unique hashes {len(hashes)}")
for r in results:
    h = r["partialFingerprints"]["equalIndicator/v1"]
    if hashes[h] > 1:
        line = r["locations"][0]["physicalLocation"]["region"]["startLine"]
        print(h, r["ruleId"], f"line {line}")
