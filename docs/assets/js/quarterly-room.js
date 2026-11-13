document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("quarterlyRoomForm");
  if (!form) return;

  const API_BASE = "https://market.firstcityfoundry.com";
  const API_PATH = "/marketing/api/matching-intakes";
  const steps = Array.from(form.querySelectorAll(".step"));
  const indicators = Array.from(document.querySelectorAll(".step-indicator"));
  const progress = document.querySelector(".progress-bar");
  const status = document.getElementById("step-status");
  const prevButton = document.getElementById("prevBtn");
  const nextButton = document.getElementById("nextBtn");
  const submitButton = document.getElementById("submitBtn");
  const messageContainer = document.querySelector(".message-container");
  let currentStep = 1;

  const problemDetails = {
    problem_owner: `
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">Right now the problem is *</span><textarea class="form-textarea" name="problem_statement" rows="3" required></textarea><span class="field-error-slot"></span></label>
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">In the last 90 days this has cost (a decision, hours, or money) *</span><textarea class="form-textarea" name="problem_cost" rows="2" required></textarea><span class="field-error-slot"></span></label>
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">I have already tried (one line; “Nothing” is an answer) *</span><input class="form-input" name="tried_so_far" required><span class="field-error-slot"></span></label>`,
    problem_solver: `
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">The problem I take is *</span><textarea class="form-textarea" name="problem_taken" rows="3" required></textarea><span class="field-error-slot"></span></label>
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">The last company I did this for (what they do, and which size band)</span><textarea class="form-textarea" name="last_client" rows="2"></textarea><span class="field-error-slot"></span></label>
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">What changed?</span><textarea class="form-textarea" name="result_proof" rows="2"></textarea><span class="field-error-slot"></span></label>
      <p class="text-xs leading-5 text-slatebrand sm:col-span-2">Leave the last two lines blank if you have no proof yet; that means no match this quarter. General service descriptions do not create a match.</p>`,
    connector: `
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">I can put these people in a room *</span><textarea class="form-textarea" name="people_to_connect" rows="2" required></textarea><span class="field-error-slot"></span></label>
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">The problem they usually carry *</span><textarea class="form-textarea" name="connected_problem" rows="2" required></textarea><span class="field-error-slot"></span></label>
      <label class="block sm:col-span-2"><span class="mb-2 block text-sm font-bold text-ink">The last introduction that turned into work (who, to whom)</span><textarea class="form-textarea" name="introduction_proof" rows="2"></textarea><span class="field-error-slot"></span></label>
      <p class="text-xs leading-5 text-slatebrand sm:col-span-2">An introduction that already led to work is the evidence for a potential connector match.</p>`,
    room_builder: `
      <label class="block"><span class="mb-2 block text-sm font-bold text-ink">The room I already gather *</span><textarea class="form-textarea" name="room_description" rows="2" required></textarea><span class="field-error-slot"></span></label>
      <fieldset data-required-group="true" data-field-name="room_mix" data-field-label="Who was in your last room" class="space-y-3"><legend class="mb-3 text-sm font-bold text-ink">Last time that room was mostly *</legend>
        <label class="index-choice"><input type="radio" name="room_mix" value="problem_owners"><span>People with a problem in their own company</span></label>
        <label class="index-choice"><input type="radio" name="room_mix" value="sellers"><span>People selling</span></label>
        <label class="index-choice"><input type="radio" name="room_mix" value="even"><span>About even</span></label><span class="field-error-slot"></span></fieldset>
      <label class="block sm:col-span-2"><span class="mb-2 block text-sm font-bold text-ink">The problem that room keeps failing to solve *</span><textarea class="form-textarea" name="room_problem" rows="2" required></textarea><span class="field-error-slot"></span></label>`
  };

  function renderSeatDetails() {
    const seat = form.querySelector("input[name='seat']:checked")?.value;
    document.getElementById("seat-problem-fields").innerHTML = seat ? problemDetails[seat] : "";
    const sizeHint = seat === "problem_owner"
      ? "Choose one for your company."
      : "Choose all size bands for companies you work with.";
    form.querySelectorAll("[data-size-hint]").forEach(hint => { hint.textContent = sizeHint; });
  }

  function selectedValues(name) {
    return Array.from(form.querySelectorAll(`input[name="${name}"]:checked`), input => input.value);
  }

  function setStep(step) {
    currentStep = step;
    steps.forEach(section => {
      const active = Number(section.dataset.step) === step;
      section.classList.toggle("active", active);
      section.hidden = !active;
    });
    indicators.forEach((indicator, index) => {
      indicator.classList.toggle("active", index + 1 === step);
      indicator.classList.toggle("completed", index + 1 < step);
    });
    progress.style.width = `${(step / steps.length) * 100}%`;
    status.textContent = `Screen ${step} of ${steps.length}`;
    prevButton.hidden = step === 1;
    nextButton.hidden = step === steps.length;
    submitButton.hidden = step !== steps.length;
    prevButton.style.display = step === 1 ? "none" : "";
    nextButton.style.display = step === steps.length ? "none" : "";
    submitButton.style.display = step !== steps.length ? "none" : "";
    form.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function clearErrors(section) {
    section.querySelectorAll(".error-message").forEach(error => error.remove());
    section.querySelectorAll(".border-red-500").forEach(field => field.classList.remove("border-red-500"));
  }

  function showError(element, message) {
    element.classList.add("border-red-500");
    const error = document.createElement("span");
    error.className = "error-message mt-2 block text-sm text-red-700";
    error.textContent = message;
    const slot = element.querySelector(".field-error-slot");
    (slot || element).appendChild(error);
  }

  function validateStep() {
    const section = steps[currentStep - 1];
    clearErrors(section);
    let valid = true;
    section.querySelectorAll("input[required], textarea[required]").forEach(field => {
      if (!field.checkValidity()) {
        showError(field, field.type === "email" ? "Enter a valid email address." : "This field is required.");
        valid = false;
      }
    });
    section.querySelectorAll("[data-required-group='true']").forEach(group => {
      const fieldName = group.dataset.fieldName;
      const chosen = selectedValues(fieldName);
      const maxOne = fieldName === "seat" || fieldName === "problem_category" || fieldName === "last_event_skew" || fieldName === "room_mix" || fieldName === "contact_permission";
      const empty = chosen.length === 0;
      const tooMany = maxOne && chosen.length > 1;
      if (empty || tooMany) {
        showError(group, empty ? "Please choose an option." : "Choose one option.");
        valid = false;
      }
    });
    if (currentStep === 2) {
      ["revenue_bands", "people_bands"].forEach(name => {
        const count = selectedValues(name).length;
        const founder = selectedValues("seat")[0] === "problem_owner";
        if (count === 0 || (founder && count !== 1)) {
          const group = section.querySelector(`[data-field-name="${name}"]`);
          showError(group, founder ? "Choose exactly one size band." : "Choose at least one size band.");
          valid = false;
        }
      });
    }
    if (!valid) {
      const firstError = section.querySelector(".error-message");
      firstError?.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    return valid;
  }

  function formDataObject() {
    const data = Object.fromEntries(new FormData(form).entries());
    data.revenue_bands = selectedValues("revenue_bands");
    data.people_bands = selectedValues("people_bands");
    data.quarter_commitments = selectedValues("quarter_commitments");
    return data;
  }

  function buildPayload(fields) {
    const params = new URLSearchParams(window.location.search);
    return {
      schema_version: 1,
      intake_type: "quarterly_problem_solution_matching",
      seat: fields.seat,
      person: {
        name: fields.name,
        email: fields.email,
        city: fields.city,
        company: fields.company,
        role: fields.role,
        company_url: fields.company_url || "",
        company_description: fields.company_description,
        company_size: { revenue_bands: fields.revenue_bands, people_bands: fields.people_bands }
      },
      problem: {
        category: fields.problem_category,
        event_skew: fields.last_event_skew,
        details: Object.fromEntries(Object.entries(fields).filter(([key]) => ["problem_statement", "problem_cost", "tried_so_far", "problem_taken", "last_client", "result_proof", "people_to_connect", "connected_problem", "introduction_proof", "room_description", "room_mix", "room_problem"].includes(key)))
      },
      quarter: {
        commitments: fields.quarter_commitments,
        no_pitch_acknowledged: fields.no_pitch_acknowledged === "true",
        contact_permission: fields.contact_permission
      },
      source: "first_city_foundry_quarterly_room",
      submitted_page: window.location.pathname,
      reporting: {
        referrer: document.referrer || "",
        language: navigator.language || "",
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "",
        utm: Object.fromEntries(["source", "medium", "campaign", "term", "content"].map(key => [key, params.get(`utm_${key}`) || ""]))
      }
    };
  }

  form.addEventListener("change", event => {
    if (event.target.name === "seat") renderSeatDetails();
    if (event.target.name === "quarter_commitments" && event.target.value === "hold" && event.target.checked) {
      form.querySelectorAll("input[name='quarter_commitments']:not([value='hold'])").forEach(input => { input.checked = false; });
    } else if (event.target.name === "quarter_commitments" && event.target.value !== "hold" && event.target.checked) {
      form.querySelector("input[name='quarter_commitments'][value='hold']").checked = false;
    }
    if (event.target.name === "revenue_bands" || event.target.name === "people_bands") {
      const founder = selectedValues("seat")[0] === "problem_owner";
      const group = event.target.closest("fieldset");
      if (founder && event.target.checked) group.querySelectorAll("input[type='checkbox']").forEach(input => { if (input !== event.target) input.checked = false; });
    }
  });

  nextButton.addEventListener("click", () => {
    if (validateStep()) setStep(Math.min(currentStep + 1, steps.length));
  });
  prevButton.addEventListener("click", () => setStep(Math.max(currentStep - 1, 1)));

  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (!validateStep()) return;
    submitButton.disabled = true;
    submitButton.textContent = "Sending...";
    messageContainer.textContent = "";
    try {
      const response = await fetch(`${API_BASE}${API_PATH}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildPayload(formDataObject()))
      });
      if (!response.ok) throw new Error(response.status === 404 ? "This intake is not connected yet. Please contact hello@firstcityfoundry.com to share your response." : "We couldn't save your response. Please try again or email hello@firstcityfoundry.com.");
      window.location.href = "quarterly-room-success.html";
    } catch (error) {
      messageContainer.className = "message-container mb-5 alert-error";
      messageContainer.textContent = error.message || "We couldn't send your response. Please try again.";
      submitButton.disabled = false;
      submitButton.textContent = "Send my response";
    }
  });

  setStep(1);
});
