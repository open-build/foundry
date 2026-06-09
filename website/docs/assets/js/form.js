// Join the Index form handling and local ForgeWeb submission.
document.addEventListener("DOMContentLoaded", function() {
  const CONFIG = {
    INDEX_API_PATH: "/marketing/api/index-submissions",
    MARKETING_API_BASE: "https://market.firstcityfoundry.com",
    GOOGLE_SCRIPT_URL: "https://script.google.com/macros/s/AKfycbzaXn82jf98akTlphk00Ao0luuM9lDQF6kN2ZN73lWGdSblLsdKtBjxLSfobnlknSvG/exec",
    REQUIRE_TURNSTILE: false
  };

  const form = document.getElementById("startupApplicationForm");
  if (!form) return;

  const surveyRoot = document.getElementById("indexSurveySteps");
  if (surveyRoot && !surveyRoot.querySelector(".step") && window.renderIndexSurvey) {
    window.renderIndexSurvey(surveyRoot);
  }

  let currentStep = 1;
  let steps = Array.from(document.querySelectorAll(".step"));
  const totalSteps = steps.length || 1;
  const stepIndicators = Array.from(document.querySelectorAll(".step-indicator"));
  const progressBar = document.querySelector(".progress-bar");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const submitBtn = document.getElementById("submitBtn");
  const draftKey = "foundryIndexSurveyDraft";
  const pageLoadedAt = Date.now();
  let formReadyAt = pageLoadedAt;
  formReadyAt = Date.now();

  showStep(currentStep);
  loadFormData();
  attachAutosave();

  nextBtn.addEventListener("click", function() {
    if (!validateCurrentStep()) return;
    if (currentStep < totalSteps) {
      currentStep += 1;
      showStep(currentStep);
    }
  });

  prevBtn.addEventListener("click", function() {
    if (currentStep > 1) {
      currentStep -= 1;
      showStep(currentStep);
    }
  });

  form.addEventListener("submit", async function(event) {
    event.preventDefault();
    if (!validateCurrentStep()) return;

    const turnstileToken = window.turnstile ? window.turnstile.getResponse() : "";
    if (CONFIG.REQUIRE_TURNSTILE && !turnstileToken) {
      showMessage("Please complete the verification before submitting.", "error");
      return;
    }

    const originalText = showLoading(submitBtn);

    try {
      const data = getFormDataObject();
      if (turnstileToken) data.turnstile_token = turnstileToken;
      data.submitted_page = window.location.pathname;
      data.source = "first_city_foundry_index";
      data.reporting = buildReportingMetadata();

      await submitIndexSurvey(data);
      localStorage.removeItem(draftKey);

      showMessage("Your Index response has been recorded. Thank you for contributing to the benchmark.", "success");
      setTimeout(function() {
        window.location.href = "success.html?submitted=index";
      }, 1200);
    } catch (error) {
      console.error("Submission error:", error);
      if (window.turnstile) window.turnstile.reset();
      showMessage(error.userMessage || "There was an error submitting your response. Please try again.", "error");
    } finally {
      hideLoading(submitBtn, originalText);
    }
  });

  function showStep(step) {
    steps = Array.from(document.querySelectorAll(".step"));
    steps.forEach(section => section.classList.remove("active"));
    stepIndicators.forEach(indicator => {
      indicator.classList.remove("active");
      indicator.classList.remove("completed");
    });

    const currentStepElement = document.querySelector(`.step[data-step="${step}"]`);
    const currentIndicator = document.querySelector(`.step-indicator[data-step="${step}"]`);

    if (currentStepElement) currentStepElement.classList.add("active");
    if (currentIndicator) currentIndicator.classList.add("active");

    for (let i = 1; i < step; i += 1) {
      const indicator = document.querySelector(`.step-indicator[data-step="${i}"]`);
      if (indicator) indicator.classList.add("completed");
    }

    if (progressBar) {
      const progress = Math.max(1, Math.round((step / totalSteps) * 100));
      progressBar.style.width = `${progress}%`;
    }

    prevBtn.style.display = step === 1 ? "none" : "inline-flex";
    nextBtn.style.display = step === totalSteps ? "none" : "inline-flex";
    submitBtn.style.display = step === totalSteps ? "inline-flex" : "none";

    const turnstileWidget = document.getElementById("turnstileWidget");
    if (turnstileWidget) {
      turnstileWidget.style.display = step === totalSteps && CONFIG.REQUIRE_TURNSTILE ? "block" : "none";
    }

    const formTop = document.querySelector(".index-form-shell");
    if (formTop) formTop.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function validateCurrentStep() {
    const currentStepElement = document.querySelector(`.step[data-step="${currentStep}"]`);
    if (!currentStepElement) return false;

    let isValid = true;
    currentStepElement.querySelectorAll(".error-message").forEach(error => error.remove());
    currentStepElement.querySelectorAll(".border-red-500").forEach(field => field.classList.remove("border-red-500"));

    currentStepElement.querySelectorAll("input[required], textarea[required], select[required]").forEach(field => {
      if (!String(field.value || "").trim()) {
        isValid = false;
        showFieldError(field, "This field is required");
      }
    });

    currentStepElement.querySelectorAll("[data-required-group='true']").forEach(group => {
      const fieldName = group.dataset.fieldName;
      const checked = group.querySelectorAll(`input[name="${cssEscape(fieldName)}"]:checked`);
      if (!checked.length) {
        isValid = false;
        showFieldError(group, "Please choose at least one option");
      }
    });

    currentStepElement.querySelectorAll("input[type='email']").forEach(field => {
      if (field.value && !isValidEmail(field.value)) {
        isValid = false;
        showFieldError(field, "Please enter a valid email address");
      }
    });

    if (!isValid) {
      const firstError = currentStepElement.querySelector(".border-red-500, .error-message");
      if (firstError) firstError.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    return isValid;
  }

  function showFieldError(field, message) {
    field.classList.add("border-red-500");
    const error = document.createElement("div");
    error.className = "error-message text-sm mt-2";
    error.textContent = message;

    const slot = field.querySelector ? field.querySelector(".field-error-slot") : null;
    if (slot) {
      slot.innerHTML = "";
      slot.appendChild(error);
    } else if (field.parentNode) {
      field.parentNode.appendChild(error);
    }
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  function cssEscape(value) {
    if (window.CSS && window.CSS.escape) return window.CSS.escape(value);
    return String(value).replace(/"/g, '\\"');
  }

  function getFormDataObject() {
    const formData = new FormData(form);
    const data = {};

    formData.forEach((value, key) => {
      if (Object.prototype.hasOwnProperty.call(data, key)) {
        if (!Array.isArray(data[key])) data[key] = [data[key]];
        data[key].push(value);
      } else {
        data[key] = value;
      }
    });

    const questions = (window.INDEX_SURVEY && window.INDEX_SURVEY.questions) || [];
    questions.forEach(question => {
      if (question.type === "multi" || question.type === "checkbox") {
        data[question.name] = formData.getAll(question.name);
      }
    });

    return data;
  }

  async function submitIndexSurvey(data) {
    const endpoint = buildMarketingApiUrl(CONFIG.INDEX_API_PATH);
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        try {
          return await response.json();
        } catch (_) {
          return { ok: true };
        }
      }

      if (shouldFallbackToGoogleScript(response.status)) {
        return submitIndexSurveyToGoogleScript(data);
      }

      let errorBody = {};
      try {
        errorBody = await response.json();
      } catch (_) {}

      const err = new Error(`Submission failed: HTTP ${response.status}`);
      err.userMessage = errorBody.error || "The response could not be saved. Please try again.";
      throw err;
    } catch (error) {
      if (error && error.name === "TypeError") {
        return submitIndexSurveyToGoogleScript(data);
      }
      throw error;
    }
  }

  function shouldFallbackToGoogleScript(status) {
    return status === 404 || status === 405 || status === 501;
  }

  function buildMarketingApiUrl(path) {
    const cleanPath = path.startsWith("/") ? path : `/${path}`;
    return `${CONFIG.MARKETING_API_BASE}${cleanPath}`;
  }

  function getDefaultMarketingApiBase() {
    if (window.FOUNDRY_MARKETING_API_BASE) {
      return String(window.FOUNDRY_MARKETING_API_BASE).replace(/\/$/, "");
    }
    const host = window.location.hostname;
    const port = window.location.port;
    if ((host === "localhost" || host === "127.0.0.1") && (port === "3000" || port === "3001")) {
      return `${window.location.protocol}//${host}:4000`;
    }
    return "";
  }

  function buildReportingMetadata() {
    const params = new URLSearchParams(window.location.search);
    return {
      submitted_page: window.location.pathname,
      referrer: document.referrer || "",
      user_agent: navigator.userAgent || "",
      language: navigator.language || "",
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "",
      screen: {
        width: window.screen && window.screen.width ? window.screen.width : null,
        height: window.screen && window.screen.height ? window.screen.height : null,
      },
      viewport: {
        width: window.innerWidth || null,
        height: window.innerHeight || null,
      },
      utm: {
        source: params.get("utm_source") || "",
        medium: params.get("utm_medium") || "",
        campaign: params.get("utm_campaign") || "",
        term: params.get("utm_term") || "",
        content: params.get("utm_content") || "",
      },
      timing: {
        ms_since_page_load: Date.now() - pageLoadedAt,
        ms_since_form_ready: Date.now() - formReadyAt,
      },
    };
  }

  async function submitIndexSurveyToGoogleScript(data) {
    const params = new URLSearchParams();
    Object.keys(data).forEach(key => {
      const value = data[key];
      if (Array.isArray(value)) {
        value.forEach(item => params.append(key, String(item)));
      } else if (value !== null && typeof value !== "undefined") {
        params.append(key, String(value));
      }
    });

    const response = await fetch(CONFIG.GOOGLE_SCRIPT_URL, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params
    });

    if (!response.ok) {
      const err = new Error(`Fallback submission failed: HTTP ${response.status}`);
      err.userMessage = "The response could not be saved right now. Please try again in a moment.";
      throw err;
    }

    try {
      return await response.json();
    } catch (_) {
      return { ok: true };
    }
  }

  function showLoading(button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="spinner mr-2"></span>Submitting...';
    return originalText;
  }

  function hideLoading(button, originalText) {
    button.disabled = false;
    button.textContent = originalText;
  }

  function showMessage(message, type) {
    const messageContainer = document.querySelector(".message-container");
    const messageElement = document.createElement("div");
    messageElement.className = `alert-${type || "success"}`;
    messageElement.textContent = message;

    messageContainer.innerHTML = "";
    messageContainer.appendChild(messageElement);
    messageContainer.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function attachAutosave() {
    let autoSaveTimeout;
    form.addEventListener("input", queueSave);
    form.addEventListener("change", queueSave);

    function queueSave() {
      clearTimeout(autoSaveTimeout);
      autoSaveTimeout = setTimeout(saveFormData, 600);
    }
  }

  function saveFormData() {
    localStorage.setItem(draftKey, JSON.stringify(getFormDataObject()));
  }

  function loadFormData() {
    const savedData = localStorage.getItem(draftKey);
    if (!savedData) return;

    try {
      const data = JSON.parse(savedData);
      Object.keys(data).forEach(key => {
        const values = Array.isArray(data[key]) ? data[key] : [data[key]];
        const fields = form.querySelectorAll(`[name="${cssEscape(key)}"]`);
        fields.forEach(field => {
          if (field.type === "radio" || field.type === "checkbox") {
            field.checked = values.includes(field.value);
          } else {
            field.value = data[key] || "";
          }
        });
      });
    } catch (error) {
      console.error("Error loading saved Index response:", error);
    }
  }
});
