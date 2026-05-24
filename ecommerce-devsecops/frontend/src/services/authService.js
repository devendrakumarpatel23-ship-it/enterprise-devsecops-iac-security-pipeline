import apiClient from './api';

export const authService = {
  register: async (email, password, firstName, lastName) => {
    const response = await apiClient.post('/auth/register', {
      email,
      password,
      first_name: firstName,
      last_name: lastName
    });
    return response.data;
  },

  login: async (email, password) => {
    const response = await apiClient.post('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  verifyToken: async () => {
    const response = await apiClient.get('/auth/verify');
    return response.data;
  },

  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    const response = await apiClient.post('/auth/refresh', {}, {
      headers: { Authorization: `Bearer ${refreshToken}` }
    });
    localStorage.setItem('access_token', response.data.access_token);
    return response.data;
  }
};

export const productService = {
  getProducts: async (page = 1, limit = 10, category = '') => {
    const response = await apiClient.get('/products', {
      params: { page, limit, category }
    });
    return response.data;
  },

  getProduct: async (id) => {
    const response = await apiClient.get(`/products/${id}`);
    return response.data;
  },

  createProduct: async (product) => {
    const response = await apiClient.post('/products', product);
    return response.data;
  },

  updateProduct: async (id, product) => {
    const response = await apiClient.put(`/products/${id}`, product);
    return response.data;
  },

  deleteProduct: async (id) => {
    const response = await apiClient.delete(`/products/${id}`);
    return response.data;
  }
};

export const orderService = {
  getOrders: async () => {
    const response = await apiClient.get('/orders');
    return response.data;
  },

  getOrder: async (id) => {
    const response = await apiClient.get(`/orders/${id}`);
    return response.data;
  },

  createOrder: async (order) => {
    const response = await apiClient.post('/orders', order);
    return response.data;
  },

  cancelOrder: async (id) => {
    const response = await apiClient.post(`/orders/${id}/cancel`);
    return response.data;
  }
};

export const userService = {
  getProfile: async () => {
    const response = await apiClient.get('/users/profile');
    return response.data;
  },

  updateProfile: async (profile) => {
    const response = await apiClient.put('/users/profile', profile);
    return response.data;
  },

  changePassword: async (currentPassword, newPassword) => {
    const response = await apiClient.put('/users/password', {
      current_password: currentPassword,
      new_password: newPassword
    });
    return response.data;
  }
};
