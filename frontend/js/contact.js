/* ============================================================
   KLYRIVEN — CONTACT FORM
   Client-side validation, API submission, states
   ============================================================ */

(function () {
  'use strict';

  const form = document.getElementById('enquiry-form');
  if (!form) return;

  const submitBtn = form.querySelector('[type="submit"]');
  const btnText = submitBtn ? submitBtn.querySelector('.btn-text') : null;
  const btnSpinner = submitBtn ? submitBtn.querySelector('.spinner') : null;
  const successMsg = form.querySelector('.form__success');
  const failureMsg = form.querySelector('.form__failure');

  // ── Field validation rules ─────────────────────────────────

  const RULES = {
    name: {
      required: true,
      minLength: 2,
      maxLength: 100,
      messages: {
        required: 'Your name is required.',
        minLength: 'Name must be at least 2 characters.',
        maxLength: 'Name must not exceed 100 characters.',
      },
    },
    email: {
      required: true,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      messages: {
        required: 'Your email address is required.',
        pattern: 'Please enter a valid email address.',
      },
    },
    service_interest: {
      required: true,
      messages: {
        required: 'Please select a service.',
      },
    },
    description: {
      required: true,
      minLength: 20,
      maxLength: 5000,
      messages: {
        required: 'Please describe your project.',
        minLength: 'Please tell us a little more — at least 20 characters.',
        maxLength: 'Description is too long (max 5000 characters).',
      },
    },
    consent_given: {
      required: true,
      messages: {
        required: 'You must agree to the privacy terms to proceed.',
      },
    },
  };

  // ── Show/hide error ────────────────────────────────────────

  function showError(field, message) {
    const group = field.closest('.form__group') || field.closest('.form__checkbox-group');
    if (!group) return;
    const error = group.querySelector('.form__error');
    if (!error) return;
    error.textContent = message;
    error.classList.add('is-visible');
    field.classList.add('is-error');
    field.setAttribute('aria-invalid', 'true');
    field.setAttribute('aria-describedby', error.id || '');
  }

  function clearError(field) {
    const group = field.closest('.form__group') || field.closest('.form__checkbox-group');
    if (!group) return;
    const error = group.querySelector('.form__error');
    if (!error) return;
    error.classList.remove('is-visible');
    error.textContent = '';
    field.classList.remove('is-error');
    field.removeAttribute('aria-invalid');
  }

  // ── Validate single field ──────────────────────────────────

  function validateField(field) {
    const name = field.name;
    const rules = RULES[name];
    if (!rules) return true;

    const value = field.type === 'checkbox' ? field.checked : field.value.trim();

    if (rules.required) {
      if (field.type === 'checkbox' && !field.checked) {
        showError(field, rules.messages.required);
        return false;
      }
      if (field.type !== 'checkbox' && !value) {
        showError(field, rules.messages.required);
        return false;
      }
    }

    if (rules.minLength && typeof value === 'string' && value.length < rules.minLength) {
      showError(field, rules.messages.minLength);
      return false;
    }

    if (rules.maxLength && typeof value === 'string' && value.length > rules.maxLength) {
      showError(field, rules.messages.maxLength);
      return false;
    }

    if (rules.pattern && typeof value === 'string' && !rules.pattern.test(value)) {
      showError(field, rules.messages.pattern);
      return false;
    }

    clearError(field);
    return true;
  }

  // ── Validate all fields ────────────────────────────────────

  function validateAll() {
    const fields = form.querySelectorAll('input, select, textarea');
    let valid = true;
    fields.forEach(field => {
      if (!validateField(field)) valid = false;
    });
    return valid;
  }

  // ── Live validation on blur ────────────────────────────────

  form.querySelectorAll('input, select, textarea').forEach(field => {
    field.addEventListener('blur', () => validateField(field));
    field.addEventListener('input', () => {
      if (field.classList.contains('is-error')) validateField(field);
    });
  });

  // ── Loading state ──────────────────────────────────────────

  function setLoading(loading) {
    if (!submitBtn) return;
    submitBtn.disabled = loading;
    if (btnText) btnText.style.display = loading ? 'none' : '';
    if (btnSpinner) btnSpinner.style.display = loading ? 'flex' : 'none';
  }

  // ── Collect form data ──────────────────────────────────────

  function getFormData() {
    const data = {};
    const fd = new FormData(form);
    fd.forEach((value, key) => {
      data[key] = value;
    });
    // Checkbox needs special handling
    const consent = form.querySelector('[name="consent_given"]');
    data.consent_given = consent ? consent.checked : false;
    return data;
  }

  // ── Show messages ──────────────────────────────────────────

  function showSuccess(message) {
    if (!successMsg) return;
    successMsg.innerHTML = `
      <strong>Message sent.</strong><br>
      ${message || 'Thank you for reaching out. We\'ll be in touch within 1 business day.'}
    `;
    successMsg.classList.add('is-visible');
    successMsg.focus();
    if (failureMsg) failureMsg.classList.remove('is-visible');
  }

  function showFailure(message) {
    if (!failureMsg) return;
    failureMsg.textContent = message || 'Something went wrong. Please try again.';
    failureMsg.classList.add('is-visible');
    if (successMsg) successMsg.classList.remove('is-visible');
  }

  function clearMessages() {
    if (successMsg) successMsg.classList.remove('is-visible');
    if (failureMsg) failureMsg.classList.remove('is-visible');
  }

  // ── Handle server field errors ─────────────────────────────

  function applyServerErrors(errors) {
    Object.entries(errors).forEach(([fieldName, message]) => {
      const field = form.querySelector(`[name="${fieldName}"]`);
      if (field) showError(field, message);
    });
  }

  // ── Submit handler ─────────────────────────────────────────

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessages();

    if (!validateAll()) {
      // Scroll to first error
      const firstError = form.querySelector('.is-error');
      if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
      }
      return;
    }

    setLoading(true);

    const data = getFormData();

    const apiClient = window.KlyrivenAPI || window.AddWorkAPI;
    const result = apiClient ? await apiClient.submitEnquiry(data) : { ok: false, message: 'API unavailable' };

    setLoading(false);

    if (result.ok) {
      form.reset();
      showSuccess(result.data && result.data.message);
      // Scroll to success message
      if (successMsg) successMsg.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      if (result.errors && Object.keys(result.errors).length) {
        applyServerErrors(result.errors);
        showFailure('Please correct the highlighted fields and try again.');
      } else {
        showFailure(result.message);
      }
    }
  });

})();

