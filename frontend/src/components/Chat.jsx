import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

export const Chat = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Welcome to the Financial RAG System! Upload documents and ask me anything about your financial data.',
      agent: 'system'
    }
  ]);
  const queryClient = useQueryClient();

  const sendMessage = useMutation({
    mutationFn: async (msg) => {
      const response = await api.post('/chat/', {
        message: msg,
        session_id: 'default'
      });
      return response.data;
    },
    onSuccess: (data) => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        agent: data.sources[0]?.replace('Agent used: ', '') || 'unknown'
      }]);
    }
  });

  const handleSend = () => {
    if (!message.trim()) return;
    
    setMessages(prev => [...prev, { role: 'user', content: message }]);
    sendMessage.mutate(message);
    setMessage('');
  };

  const getAgentColor = (agent) => {
    if (agent === 'research') return 'from-blue-500 to-blue-600';
    if (agent === 'financial') return 'from-green-500 to-green-600';
    if (agent === 'summary') return 'from-purple-500 to-purple-600';
    return 'from-gray-500 to-gray-600';
  };

  return (
    <div className="h-full flex flex-col bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 shadow-2xl">
      {/* Header */}
      <div className="px-6 py-4 border-b border-white/10 bg-gradient-to-r from-blue-600/20 to-purple-600/20">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Bot className="w-6 h-6" />
          Multi-Agent Financial Assistant
        </h2>
        <p className="text-sm text-blue-200 mt-1">Ask questions about your financial documents</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                <Bot className="w-5 h-5 text-white" />
              </div>
            )}
            <div className={`max-w-[70%] ${msg.role === 'user' ? 'order-first' : ''}`}>
              <div className={`rounded-2xl px-4 py-3 ${
                msg.role === 'user' 
                  ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white ml-auto'
                  : 'bg-white/10 backdrop-blur-sm text-white border border-white/10'
              }`}>
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              </div>
              {msg.agent && msg.agent !== 'system' && (
                <span className={`inline-block mt-2 px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${getAgentColor(msg.agent)} text-white`}>
                  {msg.agent} agent
                </span>
              )}
            </div>
            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-emerald-600 flex items-center justify-center flex-shrink-0">
                <User className="w-5 h-5 text-white" />
              </div>
            )}
          </div>
        ))}
        {sendMessage.isPending && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl px-4 py-3 border border-white/10">
              <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-white/10 bg-white/5">
        <div className="flex gap-3">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask a question about your financial documents..."
            className="flex-1 px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={handleSend}
            disabled={!message.trim() || sendMessage.isPending}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-xl hover:from-blue-500 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg shadow-blue-500/50 flex items-center gap-2 font-medium"
          >
            <Send className="w-5 h-5" />
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
