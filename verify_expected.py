"""Independent pandas calculation of the monthly numbers the DAX measures should return.
Compare this output with your Power BI matrix (Month on rows) to validate the model.
"""
import pandas as pd

t = pd.read_csv("data/tickets.csv", parse_dates=["CreatedDate", "ResolvedDate"])
months = pd.period_range(t["CreatedDate"].min(), t["CreatedDate"].max(), freq="M")
rows = []
for m in months:
    end = m.end_time.normalize()
    created = (t["CreatedDate"].dt.to_period("M") == m).sum()
    res_m = t[t["ResolvedDate"].dt.to_period("M") == m]
    backlog = ((t["CreatedDate"] <= end) & (t["ResolvedDate"].isna() | (t["ResolvedDate"] > end))).sum()
    sla = (res_m["ResolutionHours"] <= res_m["SLATargetHours"]).mean() * 100 if len(res_m) else float("nan")
    rows.append([str(m), created, len(res_m), created - len(res_m), backlog, round(sla, 1), round(res_m["ResolutionHours"].median(), 1)])
out = pd.DataFrame(rows, columns=["Month", "Created", "Resolved", "Net_Flow", "Backlog_EOP", "SLA_Met_Pct", "Median_Hrs"])
print(out.to_string(index=False))
out.to_csv("data/expected_monthly.csv", index=False)

# Created by Avash Mohanty, 2026
