(function() {
  const sections = [
    {
      title: "Basics",
      eyebrow: "Step 1",
      description: "Tell us who is contributing to the Portland Operations & AI Index.",
      questions: [
        {
          name: "company_name",
          label: "Company Name",
          type: "text",
          required: true,
          autocomplete: "organization",
          placeholder: "Company or organization"
        },
        {
          name: "contact_name_role",
          label: "Your Name & Role",
          type: "text",
          required: true,
          autocomplete: "name",
          placeholder: "Name, title, founder role, or operator role"
        },
        {
          name: "contact_email",
          label: "Email Address",
          type: "email",
          required: true,
          autocomplete: "email",
          placeholder: "you@company.com"
        }
      ]
    },
    {
      title: "Company Profile",
      eyebrow: "Step 2",
      description: "These answers let the benchmark compare companies by stage, capital model, team size, and revenue band.",
      questions: [
        {
          name: "operating_years",
          label: "How long has your business been operating?",
          type: "single",
          required: true,
          options: [
            { value: "0_2_years", label: "0-2 years (Early Startup)" },
            { value: "3_5_years", label: "3-5 years (Growth Stage)" },
            { value: "6_10_years", label: "6-10 years (Established)" },
            { value: "10_plus_years", label: "10+ years (Legacy/Mature)" }
          ]
        },
        {
          name: "funding_pathway",
          label: "What is your primary funding pathway?",
          type: "single",
          required: true,
          options: [
            { value: "bootstrapped", label: "100% Bootstrapped / Self-funded" },
            { value: "angel_seed", label: "Angel / Seed backed" },
            { value: "vc_series_a_plus", label: "VC backed (Series A+)" },
            { value: "traditional_debt", label: "Traditional debt / Bank loans" },
            { value: "private_equity", label: "Private Equity owned" }
          ]
        },
        {
          name: "team_size",
          label: "What is your current team size?",
          type: "single",
          required: true,
          options: [
            { value: "1_5", label: "1-5" },
            { value: "6_15", label: "6-15" },
            { value: "16_50", label: "16-50" },
            { value: "51_150", label: "51-150" },
            { value: "150_plus", label: "150+" }
          ]
        },
        {
          name: "annual_revenue_band",
          label: "What is your current annual revenue?",
          type: "single",
          required: true,
          options: [
            { value: "under_500k", label: "Under $500K" },
            { value: "500k_1m", label: "$500K - $1M" },
            { value: "1m_3m", label: "$1M - $3M" },
            { value: "3m_5m", label: "$3M - $5M" },
            { value: "5m_10m", label: "$5M - $10M" },
            { value: "10m_plus", label: "$10M+" },
            { value: "prefer_not_to_say", label: "Prefer not to say" }
          ]
        }
      ]
    },
    {
      title: "Operations & AI",
      eyebrow: "Step 3",
      description: "This section looks at the visibility layer: tools, dashboards, automation, and how decisions are made.",
      questions: [
        {
          name: "backend_operations_state",
          label: "When it comes to your core backend operations, how would you describe your current state?",
          type: "single",
          required: true,
          options: [
            { value: "manual_heavy", label: "Manual Heavy: Mostly spreadsheets, manual data entry, and human-dependent workflows" },
            { value: "siloed_tech", label: "Siloed Tech: We use software, but systems don't talk to each other" },
            { value: "automated_integrated", label: "Automated/Integrated: Systems are connected, minimizing manual data entry" },
            { value: "ai_native", label: "AI-Native: AI agents, LLMs, and predictive models are baked directly into our daily workflows" }
          ]
        },
        {
          name: "ai_budget_allocation",
          label: "How much of your monthly operating budget is currently allocated to AI/automation tools and implementation?",
          type: "single",
          required: true,
          options: [
            { value: "none", label: "0% - We're not investing in AI yet" },
            { value: "testing", label: "1-5% - Testing/experimenting" },
            { value: "active", label: "6-10% - Active implementation" },
            { value: "significant", label: "11-20% - Significant investment" },
            { value: "ai_first", label: "20%+ - AI-first operations" }
          ]
        },
        {
          name: "decision_process",
          label: "How do you primarily make critical business decisions (hiring, spending, pivoting)?",
          type: "single",
          required: true,
          options: [
            { value: "gut_instinct", label: "Mostly gut instinct and market feel" },
            { value: "old_reports", label: "Reviewing 30-day-old financial reports" },
            { value: "real_time_dashboards", label: "Reviewing real-time operational and financial dashboards" },
            { value: "predictive_analytics", label: "Using predictive analytics and leading indicators" }
          ]
        },
        {
          name: "profitability_report_time",
          label: "If you needed to pull a comprehensive report on your company's profitability by client/product, how long would it take?",
          type: "single",
          required: true,
          options: [
            { value: "minutes", label: "Minutes (It's on a live dashboard)" },
            { value: "hours", label: "Hours (Needs some manual compiling)" },
            { value: "days", label: "Days (Requires deep spreadsheet work)" },
            { value: "cannot_track", label: "We currently cannot accurately track this" }
          ]
        },
        {
          name: "metrics_tracking",
          label: "Which statement best describes how you currently track your most important business metrics?",
          type: "single",
          required: true,
          options: [
            { value: "manual_spreadsheets", label: "I manually compile data from multiple sources into spreadsheets weekly/monthly" },
            { value: "automated_rarely_used", label: "I have automated reports, but I rarely look at them" },
            { value: "daily_dashboard", label: "I have a live dashboard I check daily" },
            { value: "predictive_alerts", label: "I have predictive alerts that notify me when metrics hit thresholds" },
            { value: "not_systematic", label: "I don't currently track metrics systematically" }
          ]
        },
        {
          name: "ai_visibility_usage",
          label: "How are you currently using AI to improve your business visibility?",
          type: "textarea",
          required: true,
          placeholder: "Share tools, agents, dashboards, alerts, reporting workflows, or experiments."
        }
      ]
    },
    {
      title: "Margins & Leverage",
      eyebrow: "Step 4",
      description: "These questions map where scale is creating leverage and where manual work is still absorbing growth.",
      questions: [
        {
          name: "first_scale_investment",
          label: "When you secure new funding or generate surplus cash, where is the very first place you invest it to scale?",
          type: "single",
          required: true,
          options: [
            { value: "hiring", label: "Hiring more people (Sales, Delivery, etc.)" },
            { value: "marketing", label: "Marketing and Lead Gen" },
            { value: "operational_architecture", label: "Operational architecture (Tools, Systems, Integrations)" },
            { value: "product_development", label: "Product Development / R&D" }
          ]
        },
        {
          name: "margin_trend",
          label: "As your revenue has grown over the last 12 months, what has happened to your profit margins?",
          type: "single",
          required: true,
          options: [
            { value: "margins_shrank", label: "Margins shrank (Scaling is getting more expensive)" },
            { value: "margins_flat", label: "Margins stayed flat (Costs grew at the exact same rate as revenue)" },
            { value: "margins_expanded", label: "Margins expanded (We achieved operational leverage)" },
            { value: "revenue_not_grown", label: "Revenue hasn't grown in the last 12 months" }
          ]
        },
        {
          name: "manual_effort_area",
          label: "Which area of your business is currently consuming the most unnecessary human capital or manual effort?",
          type: "single",
          required: true,
          options: [
            { value: "lead_gen_sales", label: "Lead generation & Sales follow-up" },
            { value: "client_onboarding_project_management", label: "Client onboarding & Project management" },
            { value: "fulfillment_service_delivery", label: "Fulfillment / Service delivery" },
            { value: "back_office_admin_invoicing", label: "Back-office admin & Invoicing" },
            { value: "mostly_automated", label: "None - we've automated most manual work" }
          ]
        },
        {
          name: "ai_margin_uses",
          label: "Where have you successfully used AI or automation to increase margins or reduce costs?",
          type: "multi",
          required: true,
          hasOther: true,
          options: [
            { value: "customer_acquisition", label: "Customer acquisition / Marketing automation" },
            { value: "sales_pipeline", label: "Sales pipeline management / CRM automation" },
            { value: "customer_onboarding", label: "Customer onboarding / Implementation" },
            { value: "service_delivery", label: "Service delivery / Fulfillment" },
            { value: "invoicing_payments", label: "Invoicing / Payment processing" },
            { value: "customer_support", label: "Customer support / FAQ handling" },
            { value: "reporting_data_analysis", label: "Reporting / Data analysis" },
            { value: "not_yet", label: "We haven't successfully implemented AI for margin expansion yet" },
            { value: "other", label: "Other" }
          ]
        }
      ]
    },
    {
      title: "Independence & Exit Readiness",
      eyebrow: "Step 5",
      description: "This section measures whether the company can operate beyond the founder and whether value is visible.",
      questions: [
        {
          name: "founder_absence_resilience",
          label: "The Hit by a Bus Test: If the founder/CEO had to disconnect completely for 60 days, what would happen?",
          type: "single",
          required: true,
          options: [
            { value: "halt", label: "The business would completely halt" },
            { value: "run_but_growth_stops", label: "Things would run, but growth would stop and major issues would arise" },
            { value: "run_smoothly", label: "The business would run smoothly; the team has the systems they need" },
            { value: "continue_growing", label: "The business would continue to grow independently" }
          ]
        },
        {
          name: "knowledge_systematization",
          label: "How systematized is your institutional knowledge?",
          type: "single",
          required: true,
          options: [
            { value: "in_heads", label: "It mostly lives in the founder's or key employees' heads" },
            { value: "scattered_docs", label: "We have scattered Google Docs and informal training" },
            { value: "documented_sops", label: "We have strict, documented SOPs for most critical functions" },
            { value: "integrated_ai_workflows", label: "Our SOPs are integrated directly into our tools/AI workflows" }
          ]
        },
        {
          name: "valuation_awareness",
          label: "Have you ever had a formal business valuation, or do you know what your business would be worth if you sold it today?",
          type: "single",
          required: true,
          options: [
            { value: "formal_12_months", label: "Yes, I've had a formal valuation in the last 12 months" },
            { value: "formal_older", label: "Yes, but it was more than 12 months ago" },
            { value: "rough_idea", label: "No, but I have a rough idea based on industry multiples" },
            { value: "no_idea", label: "No, and I have no idea what it's worth" },
            { value: "not_interested", label: "I'm not interested in selling, so I haven't thought about it" }
          ]
        },
        {
          name: "strategic_goal",
          label: "What is the ultimate strategic goal for this business?",
          type: "single",
          required: true,
          options: [
            { value: "build_to_sell", label: "Build to sell / Exit within 3-5 years" },
            { value: "pass_down", label: "Pass down to family/employees" },
            { value: "lifestyle_business", label: "Run as a highly profitable lifestyle business indefinitely" },
            { value: "public_vc_scale", label: "Go public / massive VC-backed scale" }
          ]
        },
        {
          name: "operational_bottleneck",
          label: "What is the single biggest operational bottleneck preventing your business from running independently of its founders today?",
          type: "textarea",
          required: true,
          placeholder: "Describe the system, workflow, decision, or role that still depends too heavily on a founder."
        }
      ]
    },
    {
      title: "Podcast & Report",
      eyebrow: "Step 6",
      description: "Help us shape the community conversation and choose whether to receive the benchmark report.",
      questions: [
        {
          name: "podcast_interest",
          label: "We're looking for founders to share their operational journey on the Startup Grind Portland podcast. Are you interested?",
          type: "single",
          required: true,
          options: [
            { value: "yes_guest", label: "Yes, I'd love to be a guest" },
            { value: "maybe", label: "Maybe, depending on timing and topic" },
            { value: "ask_again", label: "Not right now, but ask me again in 6 months" },
            { value: "no_thanks", label: "No thanks" }
          ]
        },
        {
          name: "podcast_topics",
          label: "What operational topic would you be most excited to hear on the podcast?",
          type: "multi",
          required: true,
          hasOther: true,
          options: [
            { value: "ai_operations", label: "How we implemented AI in our operations" },
            { value: "scaling_1m_5m", label: "Scaling from $1M to $5M without breaking" },
            { value: "founder_extraction", label: "Extracting myself from daily operations" },
            { value: "valuation_systems", label: "Building systems that increased our valuation" },
            { value: "bootstrapped_vs_vc", label: "Bootstrapped vs. VC-backed operational differences" },
            { value: "other", label: "Other" }
          ]
        },
        {
          name: "biggest_operational_challenge",
          label: "One last thing: What's the single biggest operational challenge you're facing right now that you wish you had a solution for?",
          type: "textarea",
          required: true,
          placeholder: "Share the challenge you wish the ecosystem could help solve."
        },
        {
          name: "report_opt_in",
          label: "Opt-in: Send me the State of Portland Operations & AI report based on this data",
          type: "checkbox",
          required: true,
          options: [
            { value: "yes_send_report", label: "Yes, send me the report (recommended)" }
          ]
        }
      ]
    }
  ];

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function renderTextQuestion(question) {
    const type = question.type === "email" ? "email" : "text";
    return `
      <label class="block" data-question="${escapeHtml(question.name)}">
        <span class="mb-2 block text-sm font-bold text-ink">${escapeHtml(question.label)}${question.required ? " *" : ""}</span>
        <input
          class="form-input"
          type="${type}"
          name="${escapeHtml(question.name)}"
          ${question.required ? "required" : ""}
          ${question.autocomplete ? `autocomplete="${escapeHtml(question.autocomplete)}"` : ""}
          placeholder="${escapeHtml(question.placeholder || "")}">
        <span class="field-error-slot"></span>
      </label>`;
  }

  function renderTextareaQuestion(question) {
    return `
      <label class="block" data-question="${escapeHtml(question.name)}">
        <span class="mb-2 block text-sm font-bold text-ink">${escapeHtml(question.label)}${question.required ? " *" : ""}</span>
        <textarea
          class="form-textarea"
          name="${escapeHtml(question.name)}"
          ${question.required ? "required" : ""}
          placeholder="${escapeHtml(question.placeholder || "")}"></textarea>
        <span class="field-error-slot"></span>
      </label>`;
  }

  function renderChoiceQuestion(question) {
    const inputType = question.type === "single" ? "radio" : "checkbox";
    const choices = question.options.map(option => {
      const id = `${question.name}_${option.value}`;
      return `
        <label class="index-choice" for="${escapeHtml(id)}">
          <input id="${escapeHtml(id)}" type="${inputType}" name="${escapeHtml(question.name)}" value="${escapeHtml(option.value)}">
          <span>${escapeHtml(option.label)}</span>
        </label>`;
    }).join("");
    const otherInput = question.hasOther ? `
      <label class="mt-3 block">
        <span class="mb-2 block text-xs font-bold uppercase tracking-[0.14em] text-slatebrand">Other details</span>
        <input class="form-input" type="text" name="${escapeHtml(question.name)}_other" placeholder="Add context if you chose Other">
      </label>` : "";

    return `
      <fieldset class="index-question-group" data-required-group="${question.required ? "true" : "false"}" data-field-name="${escapeHtml(question.name)}" data-field-label="${escapeHtml(question.label)}">
        <legend class="mb-3 block text-sm font-bold text-ink">${escapeHtml(question.label)}${question.required ? " *" : ""}</legend>
        <div class="grid gap-3">${choices}</div>
        ${otherInput}
        <span class="field-error-slot"></span>
      </fieldset>`;
  }

  function renderQuestion(question) {
    if (question.type === "textarea") return renderTextareaQuestion(question);
    if (question.type === "single" || question.type === "multi" || question.type === "checkbox") return renderChoiceQuestion(question);
    return renderTextQuestion(question);
  }

  function renderIndexSurvey(target) {
    const root = typeof target === "string" ? document.querySelector(target) : target;
    if (!root) return;

    root.innerHTML = sections.map((section, index) => `
      <section class="step ${index === 0 ? "active" : ""}" data-step="${index + 1}">
        <div class="mb-8 border-b border-ink/10 pb-5">
          <span class="foundry-page-badge">${escapeHtml(section.eyebrow)}</span>
          <h2 class="font-display mt-4 text-2xl font-bold text-ink">${escapeHtml(section.title)}</h2>
          <p class="mt-2 text-sm leading-6 text-slatebrand">${escapeHtml(section.description)}</p>
        </div>
        <div class="grid gap-6">
          ${section.questions.map(renderQuestion).join("")}
        </div>
      </section>`).join("");
  }

  window.INDEX_SURVEY = {
    title: "The Startup Grind Portland Operations & AI Index",
    sections,
    questions: sections.flatMap(section => section.questions)
  };
  window.renderIndexSurvey = renderIndexSurvey;

  document.addEventListener("DOMContentLoaded", function() {
    renderIndexSurvey("#indexSurveySteps");
  });
})();
