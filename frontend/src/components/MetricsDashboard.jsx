import { useQuery } from '@tanstack/react-query';
import { Activity, Clock, DollarSign, TrendingUp } from 'lucide-react';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

export const MetricsDashboard = () => {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: async () => {
      const response = await api.get('/metrics/summary');
      return response.data;
    },
    refetchInterval: 30000,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const stats = [
    { name: 'Total Queries', value: metrics?.total_queries || 0, icon: Activity, color: 'bg-blue-500' },
    { name: 'Avg Response Time', value: `${metrics?.avg_response_time?.toFixed(2) || 0}s`, icon: Clock, color: 'bg-green-500' },
    { name: 'Total Cost', value: `$${metrics?.total_cost?.toFixed(4) || 0}`, icon: DollarSign, color: 'bg-purple-500' },
    { name: 'Success Rate', value: `${metrics?.success_rate?.toFixed(1) || 0}%`, icon: TrendingUp, color: 'bg-emerald-500' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">System Metrics</h2>
        <p className="text-gray-600 mt-1">Real-time performance and usage statistics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Research Agent</h3>
          <p className="text-3xl font-bold text-blue-600">{metrics?.agent_usage?.research || 0}</p>
          <p className="text-sm text-gray-600 mt-1">queries handled</p>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Financial Agent</h3>
          <p className="text-3xl font-bold text-green-600">{metrics?.agent_usage?.financial || 0}</p>
          <p className="text-sm text-gray-600 mt-1">queries handled</p>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Summary Agent</h3>
          <p className="text-3xl font-bold text-purple-600">{metrics?.agent_usage?.summary || 0}</p>
          <p className="text-sm text-gray-600 mt-1">queries handled</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance</h3>
          <div className="space-y-3">
            <div className="flex justify-between"><span className="text-sm text-gray-600">Fastest Query</span><span className="text-sm font-semibold">{metrics?.fastest_query?.toFixed(2) || 0}s</span></div>
            <div className="flex justify-between"><span className="text-sm text-gray-600">Slowest Query</span><span className="text-sm font-semibold">{metrics?.slowest_query?.toFixed(2) || 0}s</span></div>
            <div className="flex justify-between"><span className="text-sm text-gray-600">Documents</span><span className="text-sm font-semibold">{metrics?.total_documents || 0}</span></div>
            <div className="flex justify-between"><span className="text-sm text-gray-600">Total Chunks</span><span className="text-sm font-semibold">{metrics?.total_chunks || 0}</span></div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Cost Analysis</h3>
          <div className="space-y-3">
            <div className="flex justify-between"><span className="text-sm text-gray-600">Cost per Query</span><span className="text-sm font-semibold">${metrics?.cost_per_query?.toFixed(4) || 0}</span></div>
            <div className="flex justify-between"><span className="text-sm text-gray-600">Est. Monthly</span><span className="text-sm font-semibold">${((metrics?.cost_per_query || 0) * (metrics?.total_queries || 0) * 30).toFixed(2)}</span></div>
            <div className="flex justify-between"><span className="text-sm text-gray-600">Input Tokens</span><span className="text-sm font-semibold">{metrics?.total_input_tokens?.toLocaleString() || 0}</span></div>
            <div className="flex justify-between"><span className="text-sm text-gray-600">Output Tokens</span><span className="text-sm font-semibold">{metrics?.total_output_tokens?.toLocaleString() || 0}</span></div>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Detailed Analytics</h3>
            <p className="text-sm text-gray-600 mt-1">View traces in Langfuse</p>
          </div>
          <a href="https://cloud.langfuse.com" target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Open Langfuse</a>
        </div>
      </div>
    </div>
  );
};
