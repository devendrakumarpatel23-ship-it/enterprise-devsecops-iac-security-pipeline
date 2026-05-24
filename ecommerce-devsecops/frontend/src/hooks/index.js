import { useState, useCallback, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { jwtDecode } from 'jwt-decode';

/**
 * Custom hook for authentication management
 * Handles login, logout, token refresh, and user state
 */
export const useAuth = () => {
  const dispatch = useDispatch();
  const { user, token, loading, error } = useSelector(state => state.auth);
  const [isTokenExpired, setIsTokenExpired] = useState(false);

  // Check if token is expired
  const checkTokenExpiry = useCallback(() => {
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const expiryTime = decoded.exp * 1000; // Convert to milliseconds
        const currentTime = Date.now();
        const timeUntilExpiry = expiryTime - currentTime;

        if (timeUntilExpiry < 0) {
          setIsTokenExpired(true);
          return true;
        }

        // Set timer to refresh token before expiry
        if (timeUntilExpiry > 0) {
          const refreshTimer = setTimeout(() => {
            setIsTokenExpired(true);
          }, timeUntilExpiry - 60000); // Refresh 1 min before expiry

          return () => clearTimeout(refreshTimer);
        }
      } catch (err) {
        console.error('Token decode error:', err);
        setIsTokenExpired(true);
      }
    }
  }, [token]);

  // Check token expiry on mount and when token changes
  useEffect(() => {
    const cleanup = checkTokenExpiry();
    return cleanup;
  }, [checkTokenExpiry]);

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated: !!token && !isTokenExpired,
    isTokenExpired
  };
};

/**
 * Custom hook for managing form state and validation
 */
export const useForm = (initialValues, onSubmit) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = useCallback((e) => {
    const { name, value, type, checked } = e.target;
    setValues(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  }, []);

  const handleBlur = useCallback((e) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));
  }, []);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await onSubmit(values);
    } catch (err) {
      console.error('Form submission error:', err);
      if (err.validationErrors) {
        setErrors(err.validationErrors);
      }
    } finally {
      setIsSubmitting(false);
    }
  }, [values, onSubmit]);

  const resetForm = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  }, [initialValues]);

  const setFieldValue = useCallback((name, value) => {
    setValues(prev => ({
      ...prev,
      [name]: value
    }));
  }, []);

  const setFieldError = useCallback((name, error) => {
    setErrors(prev => ({
      ...prev,
      [name]: error
    }));
  }, []);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    resetForm,
    setFieldValue,
    setFieldError
  };
};

/**
 * Custom hook for API data fetching
 */
export const useFetch = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem('token');
        
        const headers = {
          'Content-Type': 'application/json',
          ...options.headers
        };

        if (token) {
          headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, {
          ...options,
          headers
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err.message);
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    if (url) {
      fetchData();
    }
  }, [url, options]);

  const refetch = useCallback(() => {
    setLoading(true);
    // Re-fetch logic
  }, [url, options]);

  return { data, loading, error, refetch };
};

/**
 * Custom hook for pagination
 */
export const usePagination = (items = [], itemsPerPage = 10) => {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(items.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentItems = items.slice(startIndex, endIndex);

  const goToPage = useCallback((page) => {
    const pageNumber = Math.max(1, Math.min(page, totalPages));
    setCurrentPage(pageNumber);
  }, [totalPages]);

  const nextPage = useCallback(() => {
    goToPage(currentPage + 1);
  }, [currentPage, goToPage]);

  const prevPage = useCallback(() => {
    goToPage(currentPage - 1);
  }, [currentPage, goToPage]);

  return {
    currentPage,
    totalPages,
    currentItems,
    goToPage,
    nextPage,
    prevPage,
    hasNextPage: currentPage < totalPages,
    hasPrevPage: currentPage > 1
  };
};

/**
 * Custom hook for debounced values
 */
export const useDebounce = (value, delay = 500) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
};

/**
 * Custom hook for local storage
 */
export const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  });

  const setValue = useCallback((value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  }, [key, storedValue]);

  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.error('Error removing from localStorage:', error);
    }
  }, [key, initialValue]);

  return [storedValue, setValue, removeValue];
};

/**
 * Custom hook for managing async operations
 */
export const useAsync = (asyncFunction, immediate = true) => {
  const [status, setStatus] = useState('idle');
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setStatus('pending');
    setData(null);
    setError(null);

    try {
      const response = await asyncFunction(...args);
      setData(response);
      setStatus('success');
      return response;
    } catch (err) {
      setError(err);
      setStatus('error');
      throw err;
    }
  }, [asyncFunction]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { execute, status, data, error };
};

/**
 * Custom hook for previous value
 */
export const usePrevious = (value) => {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
};

export default {
  useAuth,
  useForm,
  useFetch,
  usePagination,
  useDebounce,
  useLocalStorage,
  useAsync,
  usePrevious
};
