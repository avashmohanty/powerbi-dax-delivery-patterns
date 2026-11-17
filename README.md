# Power BI DAX Patterns for Delivery Reporting

A reusable measure set for ticket-based delivery dashboards: created vs. resolved, end-of-period backlog, SLA compliance, rolling averages, and backlog months-of-work.

## Problem
Created-vs-resolved reporting is where most delivery dashboards go wrong. Both counts come from the same ticket table but need different dates, and backlog is a point-in-time stock that cannot be computed with a simple filter on one date column. Wrong DAX here produces a dashboard that looks fine while the backlog quietly grows.

## Approach
- One ticket fact table, one calendar table, **two relationships**: Calendar to `CreatedDate` (active) and Calendar to `ResolvedDate` (inactive, activated per measure with `USERELATIONSHIP`).
- `Backlog EOP` is computed as "created on or before the period end AND (unresolved OR resolved after the period end)". This is the part most people get wrong.
- `verify_expected.py` recomputes the monthly figures independently in pandas, so you can check the Power BI matrix against `data/expected_monthly.csv` instead of trusting your own DAX.

Measures in `delivery_measures.dax`: `Created`, `Resolved`, `Net Flow`, `Backlog EOP`, `SLA Met %`, `Median Resolution Hrs`, `Resolved 3M Avg`, `Resolved MoM %`, `Backlog Months of Work`.

## Use it
1. Load `data/tickets.csv` (synthetic) and create a `Calendar` table covering the full date range.
2. Create the two relationships described in the header of `delivery_measures.dax`.
3. Paste the measures, build a matrix with Month on rows, and compare with `data/expected_monthly.csv`.

## Measured result (synthetic data, pandas cross-check)
- Net flow was positive in **8 of 9 months**; backlog grew from **5 to 30 open tickets**.
- SLA compliance stayed between **90% and 98%** every month.
- The insight: an SLA-only dashboard would have shown green all year while the backlog grew six-fold. `Backlog EOP` and `Backlog Months of Work` are what expose it.

**Your real-world result (fill in):**
| Metric | Value |
|---|---|
| Dashboard defects found vs. previous manual report | _ |

## Status and limitations
- The DAX has **not** been executed in Power BI Desktop by the author of this repo's first commit: validate against `expected_monthly.csv` before relying on it, and fix any syntax differences for your model.
- The Calendar table is assumed contiguous. `DATEADD` and `DATESINPERIOD` break on gaps.
- Ticket data is synthetic.

Created by Avash Mohanty, 2026
