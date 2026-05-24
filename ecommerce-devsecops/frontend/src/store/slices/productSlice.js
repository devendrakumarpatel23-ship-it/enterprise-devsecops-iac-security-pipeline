import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  products: [],
  loading: false,
  error: null,
  pagination: {
    page: 1,
    limit: 10,
    total: 0
  }
};

const productSlice = createSlice({
  name: 'products',
  initialState,
  reducers: {
    fetchStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchSuccess: (state, action) => {
      state.loading = false;
      state.products = action.payload.data;
      state.pagination = action.payload.pagination;
    },
    fetchFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    }
  }
});

export const { fetchStart, fetchSuccess, fetchFailure } = productSlice.actions;
export default productSlice.reducer;
