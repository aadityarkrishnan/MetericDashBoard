

import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updateMetrics } from '../store/metricsSlice';
import axiosInstance from '../utils/axios';
import { createWebSocket } from '../utils/websocket';

const MetricsDashboard = () => {
  const dispatch = useDispatch();
  const metrics = useSelector((state) => state.metrics);

  useEffect(() => {
    // Fetch initial metrics using Axios
    const fetchInitialMetrics = async () => {
      try {
        const response = await axiosInstance.get('/api/metrics/');
        dispatch(updateMetrics(response.data));
      } catch (error) {
        console.error('Error fetching initial metrics:', error);
      }
    };

    fetchInitialMetrics();

    // Establish WebSocket connection
    const socket = createWebSocket((data) => {
      dispatch(updateMetrics(data));
    });

    // Cleanup on unmount
    return () => {
      socket.close();
    };
  }, [dispatch]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-6">EC2 Real-Time Metrics Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
        {/* CPU Usage */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-2">CPU Usage</h2>
          <p className="text-4xl font-bold text-blue-500">{metrics.cpu}%</p>
        </div>
        {/* Memory Usage */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-2">Memory Usage</h2>
          <p className="text-4xl font-bold text-green-500">{metrics.memory}%</p>
        </div>
        {/* Storage Usage */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-2">Storage Usage</h2>
          <p className="text-4xl font-bold text-red-500">{metrics.storage}%</p>
        </div>
      </div>
      {metrics.timestamp && (
        <p className="mt-6 text-gray-600">
          Last updated: {new Date(metrics.timestamp * 1000).toLocaleTimeString()}
        </p>
      )}
    </div>
  );
};

export default MetricsDashboard;
