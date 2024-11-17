// frontend/src/pages/index.js

import Head from 'next/head';
import MetricsDashboard from '../components/MetricsDashboard';

export default function Home() {
  return (
    <div>
      <Head>
        <title>EC2 Real-Time Metrics Dashboard</title>
        <meta name="description" content="Real-time EC2 metrics using Django and Next.js" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <MetricsDashboard />
    </div>
  );
}
