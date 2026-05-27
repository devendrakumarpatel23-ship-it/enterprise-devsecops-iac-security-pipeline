import React, { createContext, useContext, useCallback, useState, useEffect } from 'react';

/**
 * Theme Context - Manage light/dark mode and theme settings
 */
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(() => {
    try {
      const saved = localStorage.getItem('theme');
      return saved ? JSON.parse(saved) : false;
    } catch (err) {
      return false;
    }
  });

  const toggleTheme = useCallback(() => {
    setIsDark(prev => {
      const newValue = !prev;
      localStorage.setItem('theme', JSON.stringify(newValue));
      return newValue;
    });
  }, []);

  useEffect(() => {
    if (isDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
      document.body.classList.add('dark-mode');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
      document.body.classList.remove('dark-mode');
    }
  }, [isDark]);

  const value = {
    isDark,
    toggleTheme,
    theme: isDark ? 'dark' : 'light'
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};

/**
 * Notification Context - Manage app-wide notifications
 */
const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);

  const addNotification = useCallback((message, type = 'info', duration = 5000) => {
    const id = Date.now();
    const notification = { id, message, type, timestamp: new Date() };
    
    setNotifications(prev => [...prev, notification]);

    if (duration) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }

    return id;
  }, []);

  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const addSuccess = useCallback((message, duration) => 
    addNotification(message, 'success', duration), [addNotification]);

  const addError = useCallback((message, duration) => 
    addNotification(message, 'error', duration), [addNotification]);

  const addWarning = useCallback((message, duration) => 
    addNotification(message, 'warning', duration), [addNotification]);

  const addInfo = useCallback((message, duration) => 
    addNotification(message, 'info', duration), [addNotification]);

  const value = {
    notifications,
    addNotification,
    removeNotification,
    addSuccess,
    addError,
    addWarning,
    addInfo
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within NotificationProvider');
  }
  return context;
};

/**
 * Loading Context - Manage global loading state
 */
const LoadingContext = createContext();

export const LoadingProvider = ({ children }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');

  const startLoading = useCallback((message = 'Loading...') => {
    setLoadingMessage(message);
    setIsLoading(true);
  }, []);

  const stopLoading = useCallback(() => {
    setIsLoading(false);
    setLoadingMessage('');
  }, []);

  const value = {
    isLoading,
    loadingMessage,
    startLoading,
    stopLoading
  };

  return (
    <LoadingContext.Provider value={value}>
      {children}
    </LoadingContext.Provider>
  );
};

export const useLoading = () => {
  const context = useContext(LoadingContext);
  if (!context) {
    throw new Error('useLoading must be used within LoadingProvider');
  }
  return context;
};

/**
 * Modal Context - Manage modals globally
 */
const ModalContext = createContext();

export const ModalProvider = ({ children }) => {
  const [modals, setModals] = useState([]);

  const openModal = useCallback((id, data = null) => {
    setModals(prev => [...prev, { id, data, isOpen: true }]);
  }, []);

  const closeModal = useCallback((id) => {
    setModals(prev => prev.filter(m => m.id !== id));
  }, []);

  const closeAllModals = useCallback(() => {
    setModals([]);
  }, []);

  const isModalOpen = useCallback((id) => {
    return modals.some(m => m.id === id);
  }, [modals]);

  const getModalData = useCallback((id) => {
    const modal = modals.find(m => m.id === id);
    return modal?.data || null;
  }, [modals]);

  const value = {
    modals,
    openModal,
    closeModal,
    closeAllModals,
    isModalOpen,
    getModalData
  };

  return (
    <ModalContext.Provider value={value}>
      {children}
    </ModalContext.Provider>
  );
};

export const useModal = () => {
  const context = useContext(ModalContext);
  if (!context) {
    throw new Error('useModal must be used within ModalProvider');
  }
  return context;
};

/**
 * Filter Context - Manage product filters and search
 */
const FilterContext = createContext();

export const FilterProvider = ({ children }) => {
  const [filters, setFilters] = useState({
    search: '',
    category: '',
    minPrice: 0,
    maxPrice: 10000,
    sortBy: 'latest',
    inStock: true
  });

  const updateFilter = useCallback((key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  }, []);

  const updateFilters = useCallback((newFilters) => {
    setFilters(prev => ({
      ...prev,
      ...newFilters
    }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      search: '',
      category: '',
      minPrice: 0,
      maxPrice: 10000,
      sortBy: 'latest',
      inStock: true
    });
  }, []);

  const value = {
    filters,
    updateFilter,
    updateFilters,
    resetFilters
  };

  return (
    <FilterContext.Provider value={value}>
      {children}
    </FilterContext.Provider>
  );
};

export const useFilters = () => {
  const context = useContext(FilterContext);
  if (!context) {
    throw new Error('useFilters must be used within FilterProvider');
  }
  return context;
};

/**
 * Cart Context - Manage shopping cart state
 */
const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    try {
      const saved = localStorage.getItem('cart');
      return saved ? JSON.parse(saved) : [];
    } catch (err) {
      return [];
    }
  });

  const addToCart = useCallback((product, quantity = 1) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      let newCart;

      if (existing) {
        newCart = prev.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      } else {
        newCart = [...prev, { ...product, quantity }];
      }

      localStorage.setItem('cart', JSON.stringify(newCart));
      return newCart;
    });
  }, []);

  const removeFromCart = useCallback((productId) => {
    setCart(prev => {
      const newCart = prev.filter(item => item.id !== productId);
      localStorage.setItem('cart', JSON.stringify(newCart));
      return newCart;
    });
  }, []);

  const updateQuantity = useCallback((productId, quantity) => {
    setCart(prev => {
      const newCart = quantity <= 0
        ? prev.filter(item => item.id !== productId)
        : prev.map(item =>
            item.id === productId
              ? { ...item, quantity }
              : item
          );
      localStorage.setItem('cart', JSON.stringify(newCart));
      return newCart;
    });
  }, []);

  const clearCart = useCallback(() => {
    setCart([]);
    localStorage.removeItem('cart');
  }, []);

  const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  const value = {
    cart,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    total,
    itemCount
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};

export default {
  ThemeProvider,
  useTheme,
  NotificationProvider,
  useNotification,
  LoadingProvider,
  useLoading,
  ModalProvider,
  useModal,
  FilterProvider,
  useFilters,
  CartProvider,
  useCart
};
