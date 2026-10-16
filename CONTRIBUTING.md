# Contributing

Issues and pull requests are welcome. This is a small scientific package, so the bar is
less about process and more about keeping the measurements honest.

## Reporting a problem

Open an issue. The most useful report contains the plate or palette involved, what number
you expected, what number you got, and how you ran it. If the input is a plate you cannot
share, the declared fills alone are usually enough to reproduce.

## Running the tests

```
pip install -e ".[fast,test]"
python -m pytest tests/
```

One test skips unless `PLATEAUDIT_SVG_DIR` points at a directory of plate SVGs. Those
images are not redistributed, so the skip is expected.

## The rule that matters most

**Every check must be able to fail.**

Each module carries a self-test with a positive control: a colour group known to lie off
the confusion axis that must be reported off axis. If you add a check, add the input that
proves it can detect the defect it exists to catch. A check that has only ever passed has
not been tested.

The suite enforces this on itself. `test_positive_control_is_actually_present` asserts the
known-broken palette is still present and still measured off axis, so a control cannot be
quietly removed.

## Changing a constant

Do not substitute a copunctal point from a table. The constants here are determined by the
cone fundamentals, and values belonging to a different set produce a plausible-looking angle
that is quietly wrong. Two such errors were caught by the controls during development. If a
constant needs to change, show the property that forces the new value.

## Style

Match the surrounding code. Keep the comments that explain why a thing is done a particular
way, especially where they record a defect that was found the hard way.
