import axios from 'axios';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create Axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Authentication Endpoints
 */
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => api.post('/auth/login', { email, password }),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me'),
};

/**
 * Requirements Endpoints
 */
export const requirementsAPI = {
  create: (data) => api.post('/requirements', data),
  getAll: () => api.get('/requirements'),
  getById: (id) => api.get(`/requirements/${id}`),
  update: (id, data) => api.put(`/requirements/${id}`, data),
  delete: (id) => api.delete(`/requirements/${id}`),
};

/**
 * User Stories Endpoints
 */
export const storiesAPI = {
  generate: (requirementId, features) => 
    api.post('/stories', { requirement_id: requirementId, features }),
  getAll: () => api.get('/stories'),
  getById: (id) => api.get(`/stories/${id}`),
  update: (id, data) => api.put(`/stories/${id}`, data),
  delete: (id) => api.delete(`/stories/${id}`),
};

/**
 * Estimates Endpoints
 */
export const estimatesAPI = {
  generate: (requirementId, features) => 
    api.post('/estimates', { requirement_id: requirementId, features }),
  getAll: () => api.get('/estimates'),
  getById: (id) => api.get(`/estimates/${id}`),
};

/**
 * Test Cases Endpoints
 */
export const testCasesAPI = {
  generate: (functionName, description) => 
    api.post('/test-cases', { function_name: functionName, description }),
  getAll: () => api.get('/test-cases'),
  getById: (id) => api.get(`/test-cases/${id}`),
  update: (id, data) => api.put(`/test-cases/${id}`, data),
  delete: (id) => api.delete(`/test-cases/${id}`),
};

/**
 * Design Suggestions Endpoints
 */
export const designSuggestionsAPI = {
  generate: (requirementId, features) => 
    api.post('/design-suggestions', { requirement_id: requirementId, features }),
  getAll: () => api.get('/design-suggestions'),
  getById: (id) => api.get(`/design-suggestions/${id}`),
};

/**
 * Resource Gaps Endpoints
 */
export const resourceGapsAPI = {
  detect: (requirementId, features) => 
    api.post('/resource-gaps', { requirement_id: requirementId, features }),
  getAll: () => api.get('/resource-gaps'),
};

/**
 * Analytics Endpoints
 */
export const analyticsAPI = {
  getBurndown: (sprintId) => api.get(`/analytics/burndown?${sprintId ? `sprint=${sprintId}` : ''}`),
  getVelocity: () => api.get('/analytics/velocity'),
  getCompletion: () => api.get('/analytics/completion'),
};

/**
 * WebSocket Connection
 */
export const connectWebSocket = (onMessage, onError) => {
  const wsUrl = `${API_BASE_URL.replace('http', 'ws')}/ws/connect`;
  
  const socket = new WebSocket(wsUrl);
  
  socket.onopen = () => {
    console.log('✅ WebSocket connected');
  };
  
  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (e) {
      console.error('Error parsing WebSocket message:', e);
    }
  };
  
  socket.onerror = (error) => {
    onError(error);
  };
  
  socket.onclose = () => {
    console.log('❌ WebSocket disconnected');
  };
  
  return socket;
};

export default api;
