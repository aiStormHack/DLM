CONSULTANT_INSTRUCTION = """
You are a Business‑Consultant agent.

**Data you receive**
• Order counts, revenue, traffic, conversion‑rate, and landing‑page KPIs
  for the *current week* and the *previous week*.
• Additional `business_data` such as last month's revenue.

**Your job**

1. Write a concise weekly **summary_report** (≤ 120 words) that compares
   *this* week with *last* week in plain language.

2. Produce a **recommendations** list:
   • Each bullet must be a *precise* action the merchant can take
     (e.g. *“Add a ‘Selling fast — only 12 left’ banner to landing‑page
     `/best‑sellers`”* or *“Lower SKU `hoodie‑blue` price from 3900 dzd  → 3400 dzd”*).
   • Use concrete numbers, page‑slugs, product handles, stock counts, etc.
   • Prioritise quick wins that improve revenue or conversion.

3. **For every bullet**, add a line that starts with `TASK:` followed by
   a single‑line JSON object describing the action.

   • Keys MUST be lowercase snake_case.  
   • Allowed keys: `action`, `entity_type`, `target`, `parameters`.  
   • `action` examples: `"update_price"`, `"add_banner"`,
     `"pause_campaign"`, `"clone_section"`.  
   • `entity_type` examples: `"product"`, `"landing_page"`,
     `"collection"`, `"announcement_bar"`.  
   • Put additional details inside `"parameters"` (from, to, currency,
     banner_text, deadline, priority, etc.).

**Output format (strict JSON)**
{
  "summary_report": "<your 1‑paragraph summary>",
  "recommendations": [
    "<bullet 1>",
    "TASK: { ... }",
    "<bullet 2>",
    "TASK: { ... }",
    ...
  ]
}
Do NOT wrap the entire response in markdown back‑ticks.
"""
EMAIL_SUBJECT = " Your Monthly Store Insights & Quick‑Win Actions"

EXECUTOR_INSTRUCTION = """"""


EMAIL_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{subject}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body style="margin:0;padding:0;background:#f4f6fb;font-family:Arial,Helvetica,sans-serif;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f4f6fb;">
    <tr>
      <td align="center" style="padding:32px 12px;">
        <!-- card -->
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.06);">
          <tr><td style="padding:32px;">
            <!-- greeting -->
            <h2 style="margin:0 0 16px;font-size:22px;color:#1e2251;">Hi {first_name},</h2>
            <p style="margin:0 0 24px;font-size:15px;line-height:1.6;color:#444;">
              I’ve finished analysing last month’s numbers and spotted a few <strong>quick wins</strong> you can act on right away:
            </p>

            <!-- insight table -->
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;margin-bottom:28px;">
              <thead>
                <tr>
                  <th align="left" style="padding:10px 12px;background:#eef2ff;color:#1e2251;font-size:14px;">Insight</th>
                  <th align="left" style="padding:10px 12px;background:#eef2ff;color:#1e2251;font-size:14px;">Action</th>
                </tr>
              </thead>
              <tbody>
                {insight_rows}
              </tbody>
            </table>

            <!-- recommendations -->
            <h3 style="margin:0 0 12px;font-size:18px;color:#1e2251;"> Top Recommendations</h3>
            <ol style="margin:0 0 32px;padding-left:20px;color:#444;font-size:15px;line-height:1.6;">
              {recommendation_items}
            </ol>

            <!-- CTA -->
            <p style="margin:0 0 32px;font-size:15px;color:#444;">
              These changes are already queued in your dashboard.
            </p>
            <p style="text-align:center;margin:0 0 40px;">
              <a href="{dashboard_url}" style="background:#5964ff;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:4px;font-weight:600;display:inline-block;">
                Apply All
              </a>
            </p>

            <!-- footer -->
            <p style="margin:0 0 8px;font-size:15px;color:#444;line-height:1.6;">
              Have questions? Just reply to this email and I’ll be right on it.
            </p>
            <p style="margin:0;font-size:15px;color:#444;">Talk soon and happy selling!</p>

            <p style="margin:28px 0 0;font-size:15px;color:#1e2251;font-weight:600;">
              {your_name}<br>
              <span style="font-weight:400;">Your AI Business Consultant</span><br>
              ayor.AI · 0770 123 456
            </p>
          </td></tr>
        </table>
        <!-- /card -->
      </td>
    </tr>
  </table>
</body>
</html>
"""

EMAIL_TEXT = """\
{subject}

Hi {first_name},

I’ve finished analysing last month’s numbers and spotted a few quick wins you can act on right away.

INSIGHTS
--------
{plain_insight}

TOP RECOMMENDATIONS
-------------------
{plain_recommendations}

Apply them all here → {dashboard_url}

Talk soon and happy selling!
{your_name} — ayor.AI  ·  0770 123 456
"""
