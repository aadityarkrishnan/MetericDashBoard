// frontend/src/store/metricsSlice.js

import { createSlice } from '@reduxjs/toolkit';

const metricsSlice = createSlice({
  name: 'metrics',
  initialState: {
    cpu: 0,
    memory: 0,
    storage: 0,
    timestamp: null,
  },
  reducers: {
    updateMetrics: (state, action) => {
      state.cpu = action.payload.cpu;
      state.memory = action.payload.memory;
      state.storage = action.payload.storage;
      state.timestamp = action.payload.timestamp;
    },
  },
});

export const { updateMetrics } = metricsSlice.actions;
export default metricsSlice.reducer;
