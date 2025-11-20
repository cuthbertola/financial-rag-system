import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Chat } from './components/Chat';
import { DocumentUpload } from './components/DocumentUpload';
import { MetricsDashboard } from './components/MetricsDashboard';
import { FileText, MessageSquare, BarChart3, Sparkles } from 'lucide-react';

const queryClient = new QueryClient();

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
        <div className="container mx-auto px-4 py-8 h-screen flex flex-col">
          {/* Header */}
          <header className="mb-8">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-xl shadow-lg">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Financial RAG System
                </h1>
                <p className="text-blue-200 text-sm mt-1">
                  AI-Powered Multi-Agent Financial Document Analysis
                </p>
              </div>
            </div>
          </header>

          {/* Navigation Tabs */}
          <div className="flex gap-3 mb-6">
            <button
              onClick={() => setActiveTab('chat')}
              className={`group flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                activeTab === 'chat'
                  ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/50 scale-105'
                  : 'bg-white/10 text-blue-200 hover:bg-white/20 backdrop-blur-sm'
              }`}
            >
              <MessageSquare className={`w-5 h-5 ${activeTab === 'chat' ? 'animate-pulse' : ''}`} />
              Chat
            </button>
            <button
              onClick={() => setActiveTab('documents')}
              className={`group flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                activeTab === 'documents'
                  ? 'bg-gradient-to-r from-purple-600 to-purple-500 text-white shadow-lg shadow-purple-500/50 scale-105'
                  : 'bg-white/10 text-blue-200 hover:bg-white/20 backdrop-blur-sm'
              }`}
            >
              <FileText className={`w-5 h-5 ${activeTab === 'documents' ? 'animate-pulse' : ''}`} />
              Documents
            </button>
            <button
              onClick={() => setActiveTab('metrics')}
              className={`group flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                activeTab === 'metrics'
                  ? 'bg-gradient-to-r from-emerald-600 to-emerald-500 text-white shadow-lg shadow-emerald-500/50 scale-105'
                  : 'bg-white/10 text-blue-200 hover:bg-white/20 backdrop-blur-sm'
              }`}
            >
              <BarChart3 className={`w-5 h-5 ${activeTab === 'metrics' ? 'animate-pulse' : ''}`} />
              Metrics
            </button>
          </div>

          {/* Content Area */}
          <div className="flex-1 overflow-hidden">
            {activeTab === 'chat' ? (
              <Chat />
            ) : activeTab === 'documents' ? (
              <div className="h-full overflow-y-auto">
                <DocumentUpload />
              </div>
            ) : (
              <div className="h-full overflow-y-auto">
                <MetricsDashboard />
              </div>
            )}
          </div>

          {/* Footer */}
          <footer className="mt-6 text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10">
              <span className="text-sm text-blue-300">Built with</span>
              <span className="text-sm font-semibold text-white">FastAPI • LangChain • LangGraph • Langfuse • React</span>
            </div>
          </footer>
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
