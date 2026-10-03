const form = document.querySelector("#idea-form");
const status = document.querySelector("#status");
const submitButton = document.querySelector("#submit-button");
const buttonText = document.querySelector(".button-text");
const buttonLoading = document.querySelector(".button-loading");
const result = document.querySelector("#result");
const resetButton = document.querySelector("#reset-button");
const goal = document.querySelector("#goal");
const coreLoop = document.querySelector("#core-loop");
const recommendedSystems = document.querySelector("#recommended-systems");
const developmentOrder = document.querySelector("#development-order");
const nextStep = document.querySelector("#next-step");

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  buttonText.hidden = isLoading;
  buttonLoading.hidden = !isLoading;
}

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("error", isError);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isPlan(plan) {
  return (
    plan &&
    isNonEmptyString(plan.goal) &&
    isNonEmptyString(plan.core_loop) &&
    Array.isArray(plan.recommended_systems) &&
    plan.recommended_systems.length > 0 &&
    Array.isArray(plan.development_order) &&
    plan.development_order.length > 0 &&
    isNonEmptyString(plan.next_step) &&
    plan.recommended_systems.every(isNonEmptyString) &&
    plan.development_order.every(isNonEmptyString)
  );
}

function renderList(element, items) {
  element.replaceChildren(...items.map((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    return listItem;
  }));
}

function renderPlan(plan) {
  goal.textContent = plan.goal;
  coreLoop.textContent = plan.core_loop;
  renderList(recommendedSystems, plan.recommended_systems);
  renderList(developmentOrder, plan.development_order);
  nextStep.textContent = plan.next_step;
  result.hidden = false;
  result.scrollIntoView({ behavior: "smooth", block: "start" });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (submitButton.disabled || !form.reportValidity()) {
    return;
  }

  const formData = new FormData(form);
  const payload = {
    game_idea: formData.get("game_idea").trim(),
    engine: formData.get("engine").trim(),
    experience_level: formData.get("experience_level").trim(),
    biggest_problem: formData.get("biggest_problem").trim(),
  };

  setLoading(true);
  setStatus("Gemma is building your MVP plan.");

  try {
    const response = await fetch("/api/generate-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const message = data?.detail || "Could not generate a plan. Try again.";
      throw new Error(message);
    }
    if (!isPlan(data)) {
      throw new Error("Received an unexpected plan. Please try again.");
    }

    renderPlan(data);
    setStatus("Plan ready.");
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not reach GameDev Buddy.";
    setStatus(message === "Ollama is unavailable" ? "Ollama is unavailable. Start Ollama, then try again." : message, true);
  } finally {
    setLoading(false);
  }
});

resetButton.addEventListener("click", () => {
  result.hidden = true;
  setStatus("");
  form.reset();
  document.querySelector("#game-idea").focus();
});
