import React, { useEffect, useRef, useState } from 'react';
import { Message, Sender } from '../types';
import { streamGeminiResponse } from '../services/geminiService';

interface ChatProps {
  onCodeReceived: (code: string) => void;
  onClose: () => void;
}

export const Chat: React.FC<ChatProps> = ({ onCodeReceived, onClose }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      text: 'Hello! I am your Godot AI Architect. Ask me how to integrate AI into VS Code or request GDScript code.',
      sender: Sender.AI,
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: Sender.User,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Prepare history for API
    const history = messages.map(m => ({
      role: m.sender === Sender.User ? 'user' as const : 'model' as const,
      parts: [{ text: m.text }]
    }));

    const aiMessageId = (Date.now() + 1).toString();
    let fullResponseText = '';

    try {
      // Add placeholder AI message
      setMessages(prev => [...prev, {
        id: aiMessageId,
        text: '',
        sender: Sender.AI,
        timestamp: new Date(),
        isStreaming: true
      }]);

      const stream = await streamGeminiResponse(userMessage.text, history);

      for await (const chunk of stream) {
        const chunkText = chunk.text();
        fullResponseText += chunkText;
        
        setMessages(prev => prev.map(msg => 
          msg.id === aiMessageId ? { ...msg, text: fullResponseText } : msg
        ));
      }

      // Finish streaming
      setMessages(prev => prev.map(msg => 
        msg.id === aiMessageId ? { ...msg, isStreaming: false } : msg
      ));

      // Check for code blocks to update editor
      const codeBlockRegex = /```gdscript([\s\S]*?)```/;
      const match = fullResponseText.match(codeBlockRegex);
      if (match && match[1]) {
        onCodeReceived(match[1].trim());
      }

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        text: "Sorry, I encountered an error communicating with the AI.",
        sender: Sender.AI,
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-vscode-sidebar border-l border-black w-96 shadow-xl z-20">
      {/* Header */}
      <div className="h-10 flex items-center justify-between px-4 bg-vscode-bg border-b border-black">
        <span className="text-xs font-bold uppercase tracking-wider text-white">Godot Copilot Chat</span>
        <button onClick={onClose} className="text-gray-400 hover:text-white" title="Close Chat">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(msg => (
          <div key={msg.id} className={`flex flex-col ${msg.sender === Sender.User ? 'items-end' : 'items-start'}`}>
            <div className={`max-w-[90%] rounded px-3 py-2 text-sm whitespace-pre-wrap ${
              msg.sender === Sender.User 
                ? 'bg-godot-accent text-white' 
                : 'bg-gray-700 text-gray-200'
            }`}>
              {msg.text}
              {msg.isStreaming && <span className="inline-block w-1 h-4 ml-1 bg-white animate-pulse align-middle"></span>}
            </div>
            <span className="text-[10px] text-gray-500 mt-1">
              {msg.sender === Sender.AI ? 'Godot Agent' : 'You'}
            </span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-vscode-bg border-t border-black">
        <div className="relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about GDScript or VS Code setup..."
            className="w-full bg-gray-800 text-gray-200 text-sm rounded border border-gray-700 p-3 focus:outline-none focus:border-godot-accent resize-none h-24 scrollbar-thin"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="absolute bottom-2 right-2 p-1 rounded hover:bg-gray-700 disabled:opacity-50 text-godot-accent"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
        <div className="text-[10px] text-gray-500 mt-2 text-center">
          Powered by Gemini 2.5 Flash
        </div>
      </div>
    </div>
  );
};