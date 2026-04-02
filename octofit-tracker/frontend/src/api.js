// API utility for making authenticated requests to the backend

const BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.REACT_APP_CODESPACE_NAME 
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev`
    : 'http://localhost:8000');

const API_BASE = `${BASE_URL}/api`;

// Get the auth token from localStorage
export const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

// Save the auth token to localStorage
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('authToken', token);
  }
};

// Remove the auth token from localStorage
export const removeAuthToken = () => {
  localStorage.removeItem('authToken');
};

// Make an authenticated API request
export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE}${endpoint}`;
  const token = getAuthToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    if (response.status === 401) {
      // Token expired or invalid
      removeAuthToken();
      window.location.href = '/login';
    }
    const error = await response.json();
    throw new Error(error.detail || error.error || 'API Error');
  }

  return await response.json();
};

// Login user with username and password
export const login = async (username, password) => {
  const response = await fetch(`${API_BASE}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      password,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.non_field_errors?.[0] || error.detail || 'Login failed');
  }

  const data = await response.json();
  setAuthToken(data.key);
  return data;
};

// Logout user
export const logout = async () => {
  try {
    const token = getAuthToken();
    if (token) {
      await fetch(`${API_BASE}/auth/logout/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });
    }
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    removeAuthToken();
  }
};

// Get current user info
export const getCurrentUser = async () => {
  return apiCall('/users/profiles/my_profile/');
};
