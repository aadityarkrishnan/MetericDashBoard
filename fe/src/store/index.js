// frontend/src/store/index.js

import { configureStore } from '@reduxjs/toolkit';
import metricsReducer from './metricsSlice';

const store = configureStore({
  reducer: {
    metrics: metricsReducer,
  },
});

export default store;
