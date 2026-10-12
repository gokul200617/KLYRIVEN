/* ============================================================
   KLYRIVEN — API CLIENT
   Communicates with the FastAPI backend.
   All API calls go through this module.
   ============================================================ */

const API_BASE = (() => {
  // In production, served from same origin.
  // In development, backend may be on a different port.
  const hostname = window.location.hostname;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return window.location.origin; // same port when served via FastAPI
  }
  return window.location.origin;
})();

const api = {
  /**
   * POST /api/enquiries
   * @param {Object} data - Enquiry payload
   * @returns {Promise<{ok: boolean, data?: Object, errors?: Object, message?: string}>}
   */
  async submitEnquiry(data) {
    try {
      const response = await fetch(`${API_BASE}/api/enquiries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const json = await response.json();

      if (response.ok) {
        return { ok: true, data: json };
      }

      // Handle validation errors (422)
      if (response.status === 422) {
        const fieldErrors = {};
        if (json.detail && Array.isArray(json.detail)) {
          json.detail.forEach(err => {
            const field = err.loc && err.loc[err.loc.length - 1];
            if (field) fieldErrors[field] = err.msg;
          });
        }
        return { ok: false, errors: fieldErrors, message: json.message || 'Please correct the errors below.' };
      }

      // Rate limited (429)
      if (response.status === 429) {
        return { ok: false, message: (json && json.detail) || 'Too many submissions. Please wait a moment before trying again.' };
      }

      // Server error
      return {
        ok: false,
        message: json.message || 'Something went wrong on our end. Please try again or email us directly.',
      };

    } catch (err) {
      console.error('API error:', err);
      return {
        ok: false,
        message: 'Unable to connect. Please check your connection and try again, or email us at hello@klyriven.com.',
      };
    }
  },

  /**
   * GET /api/projects
   * @param {string} [category] - Optional category filter
   * @returns {Promise<Array>}
   */
  async getProjects(category = null) {
    try {
      const url = new URL(`${API_BASE}/api/projects`);
      if (category && category !== 'all') {
        url.searchParams.set('category', category);
      }

      const response = await fetch(url.toString(), {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
      });

      if (response.ok) {
        return await response.json();
      }
      return [];
    } catch (err) {
      console.error('Failed to fetch projects:', err);
      return [];
    }
  },

  /**
   * GET /api/health
   * @returns {Promise<Object>}
   */
  async getHealth() {
    try {
      const response = await fetch(`${API_BASE}/api/health`);
      return await response.json();
    } catch {
      return { status: 'unavailable' };
    }
  },
};

window.KlyrivenAPI = api;
window.AddWorkAPI = api;

