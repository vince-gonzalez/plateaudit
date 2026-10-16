# plateaudit

Measuring pseudoisochromatic colour-vision plates from the stimulus a browser actually
delivers.

[![tests](https://github.com/vince-gonzalez/plateaudit/actions/workflows/tests.yml/badge.svg)](https://github.com/vince-gonzalez/plateaudit/actions/workflows/tests.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23422998.svg)](https://doi.org/10.5281/zenodo.23422998)
[![method](https://img.shields.io/badge/method-10.5281%2Fzenodo.21310578-blue)](https://doi.org/10.5281/zenodo.21310578)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Pseudoisochromatic plates, the dot patterns in which a numeral is hidden from observers with
red-green or blue-yellow colour vision deficiency, are assessed colorimetrically by measuring
the chromaticities of figure and ground dots and comparing the direction in which they are
separated against the dichromatic confusion lines. That has been done for four decades
without shared tooling: each study builds its own extraction, and the chain from delivered
stimulus to reported angle is described in prose rather than executed from code.

`plateaudit` performs that analysis on plates as a browser receives them. It recovers each
dot's position, radius and declared fill from SVG path data, assigns figure and ground by the
spatial compactness of each colour class, pairs figure dots with the ground dots that
physically border them, and reports the distribution of confusion-line deviations across that
boundary.

**The colorimetry is not new.** It is Dain's procedure over Smith and Pokorny fundamentals,
and the paper says so. The contribution is that the chain is executable and checkable.

## Install

```
pip install plateaudit
```

From a checkout, with the test extra:

```
pip install -e ".[test]"
```

Requires Python 3.9 or newer. Add the `raster` extra if you want to measure rendered plate
images rather than SVG markup: `pip install -e ".[raster,test]"`. That path reads images
with OpenCV; everything else works without it.

## A worked example that runs end to end

The repository ships the deposited data, so this works immediately after a clone with no
plate images and no network:

```
python -m plateaudit.audit_delivered_plates
```

```
Deviation from the confusion axis the plate claims, in degrees.
Figure and ground as the site declares them. Dain (2004) form. Uncertainty +/- 3.6 deg.

A. PLATES WHERE THE CRITERION APPLIES (transformation, vanishing)

  site          plate  type            answer    protan  deutan  tritan   xy_sep
  ZEISS         2      transformation  8           25.6    39.0       -   0.0909
  ZEISS         3      transformation  29          37.0    26.1       -   0.0945
  ZEISS         4      transformation  5            0.9    13.5       -   0.0447
```

`data/` holds `delivered-plates.json` (the colours read from delivered markup),
`designs.csv` (one row per design) and `local-pairing.json` (the border-pair statistics
behind Table 1 of the accompanying paper). Point the tools at a different copy with
`PLATEAUDIT_DATA_DIR`.

## The verification discipline

Every module carries a self-test that must pass before the module will run, and each
self-test includes a **positive control**: a colour group known to lie off the confusion axis
is required to be reported off axis. The purpose is that a check which cannot detect the
defect it exists to catch should fail rather than pass.

Several defects in this software were found by those controls rather than by inspection,
including two incorrect copunctal constants and a figure/ground rule that mislabelled six of
eleven plates.

```
python -m pytest tests/
```

The suite also **guards the guard**: one test asserts that the deliberately broken pre-fix
palette is still present and still measured off axis, so that deleting or defeating the
control fails the build rather than quietly passing it.

The figure builder is gated the same way. `make_figures` recomputes dot counts, radii of
gyration, alignment fractions, rank correlations and threshold-sweep magnitudes, compares
each against the value printed in the article, and exits without writing anything if a
single comparison fails.

## What this does not do

- **It is not a clinical instrument.** It measures a stimulus; it does not screen a person,
  and nothing here is a diagnosis.
- **It does not redistribute plate images.** The ZEISS SVGs analysed during development are
  not included. Tests that need them skip unless `PLATEAUDIT_SVG_DIR` is set.
- **It does not rasterise for you.** The SVG path is exact because the colours are declared
  in markup. A plate whose dots overlap with per-dot opacity cannot be measured that way and
  is excluded on evidence rather than assumed sound.
- **It does not invent colorimetry.** Confusion directions are constructed by perturbing the
  missing cone's excitation and projecting back, rather than retrieved from a tabulated
  copunctal point, specifically so the analysis does not depend on a constant that circulates
  in several incompatible variants.

## Citing

This release is archived at **https://doi.org/10.5281/zenodo.23422998**

The method it implements is published open access at **https://doi.org/10.5281/zenodo.21310578**

See `CITATION.cff`, and `paper/paper.md` for the software paper.

## Provenance

These modules were developed inside the repository that serves opticquiz.com and were
extracted here so the software can be read, run and reviewed on its own terms. The website
tooling that lived alongside them, including a palette audit that scans HTML pages, was
deliberately left behind: it is site maintenance, not instrumentation.

## Licence

MIT. See [LICENSE](LICENSE).
