# patchwarden-demo

Seeded checkout service used as the target repository for
[PatchWarden](https://github.com/AIForge10/patchwarden), an evidence-gated incident-response agent.

**This app contains deliberate, disclosed defects.** See
[`demo_app/seed_variants/README.md`](demo_app/seed_variants/README.md) for the full list,
including one hidden defect that no alert or test points to.

```sh
pip install fastapi==0.143.0 httpx==0.28.1 pydantic==2.14.0 pytest==9.1.1
python -m pytest demo_app/tests/test_baseline.py      # original suite: green
python -m pytest demo_app/tests/test_incident.py      # incident demo-001: red on purpose
```

Branches:

- `master`: the seeded baseline that the evaluation alerts pin by SHA.
- `known-good`: the same commit with the hidden double charge fixed (negative control).

Pull requests on this repo are opened by PatchWarden for human review. They are never merged
automatically.
