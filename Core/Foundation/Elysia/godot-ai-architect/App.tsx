
import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { CodeEditor } from './components/CodeEditor';
import { Chat } from './components/Chat';
import { FileNode } from './types';

// Initial dummy file structure with West Continent Theme
const initialFiles: FileNode[] = [
  {
    id: 'root',
    name: 'res://',
    type: 'folder',
    children: [
      {
        id: 'core',
        name: 'Core',
        type: 'folder',
        children: [
           { id: 'elysia_gd', name: 'Elysia.gd', type: 'file', content: 'extends Node\n\nclass_name ElysiaCore\n\n# The Z-Axis intention vector\nvar intention_z = 1.0\nvar current_theme = "West Continent"\n\nfunc _ready():\n\tprint("Elysia Core Initialized. Loading Fantasy Protocols.")\n' }
        ]
      },
      {
        id: 'maps',
        name: 'Maps',
        type: 'folder',
        children: [
          { id: 'west_continent_gd', name: 'WestContinent.gd', type: 'file', content: 'extends Node2D\n\n# PROJECTION LAYER: Kingdom of Silvercrest\n# Purpose: Visualize Metabolic Flows & Structural Integrity\n\nconst GRID_SIZE = 20\n\n# Entities are data points in the CellWorld simulation\n# Resources: Iron (Structure), Fruit (Energy)\n# Units: Man/Woman (Reproduction/Labor)\n\nfunc generate_world():\n\tprint("Materializing resources for metabolic analysis...")\n\t# See CodeEditor.tsx for procedural generation logic\n\tpass\n' }
        ]
      },
      { id: 'main_gd', name: 'Main.gd', type: 'file', content: 'extends Node\n\nvar score = 0\nvar level_name = "Level 1"\n\nfunc _ready():\n\tpass\n' }
    ]
  }
];

const App: React.FC = () => {
  const [files, setFiles] = useState<FileNode[]>(initialFiles);
  const [activeFileId, setActiveFileId] = useState<string | null>('west_continent_gd');
  const [activeFileContent, setActiveFileContent] = useState<string>('');
  const [activeFileName, setActiveFileName] = useState<string>('');
  const [isPlaying, setIsPlaying] = useState(false);

  // Layout State
  const [showSidebar, setShowSidebar] = useState(true);
  const [showChat, setShowChat] = useState(true);

  // Helper to find file by ID recursively
  const findFile = (nodes: FileNode[], id: string): FileNode | null => {
    for (const node of nodes) {
      if (node.id === id) return node;
      if (node.children) {
        const found = findFile(node.children, id);
        if (found) return found;
      }
    }
    return null;
  };

  // Helper to update file content
  const updateFileContent = (nodes: FileNode[], id: string, newContent: string): FileNode[] => {
    return nodes.map(node => {
      if (node.id === id) {
        return { ...node, content: newContent };
      }
      if (node.children) {
        return { ...node, children: updateFileContent(node.children, id, newContent) };
      }
      return node;
    });
  };

  useEffect(() => {
    if (activeFileId) {
      const file = findFile(files, activeFileId);
      if (file && file.type === 'file') {
        setActiveFileContent(file.content || '');
        setActiveFileName(file.name);
      }
    }
  }, [activeFileId, files]);

  const handleFileSelect = (id: string) => {
    setActiveFileId(id);
  };

  // When AI generates code, update the active file or create a temp one
  const handleCodeReceived = (code: string) => {
    if (activeFileId) {
      setFiles(prev => updateFileContent(prev, activeFileId, code));
    } else {
      // Create a new scratchpad if no file open
      const scratchpadId = 'generated_code';
      const newFile: FileNode = { id: scratchpadId, name: 'generated.gd', type: 'file', content: code };
      setFiles(prev => [...prev, newFile]);
      setActiveFileId(scratchpadId);
    }
  };

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-[#1e1e1e] text-[#d4d4d4] font-sans overflow-hidden">
      {/* Top Status Bar */}
      <div className="h-8 bg-[#333333] flex items-center px-4 justify-between text-xs select-none border-b border-black shrink-0">
        <div className="flex items-center space-x-4">
          <span className="text-blue-400 font-bold">Godot Engine</span>
          <span>Project</span>
          <span>Debug</span>
          <span>Editor</span>
          <span>Help</span>
        </div>
        
        {/* Godot Play Toolbar */}
        <div className="flex items-center space-x-2 bg-[#252526] rounded px-2 py-0.5 border border-gray-700">
          <button 
            onClick={togglePlay}
            className={`p-1 rounded hover:bg-gray-700 ${isPlaying ? 'text-red-500' : 'text-green-500'}`} 
            title={isPlaying ? "Stop (F8)" : "Play Project (F5)"}
          >
            {isPlaying ? (
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="4" y="4" width="16" height="16"/></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            )}
          </button>
          <button className="p-1 rounded hover:bg-gray-700 text-gray-400" title="Pause (F7)">
             <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
          </button>
          <button className="p-1 rounded hover:bg-gray-700 text-gray-400" title="Play Scene (F6)">
             <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M6 4v16l14-8z"/></svg>
          </button>
        </div>

        <div className="flex items-center space-x-4">
           <div className="text-godot-accent">GLES3 / Vulkan</div>
           <button 
             onClick={() => setShowChat(!showChat)} 
             className={`p-1 rounded hover:bg-gray-700 ${showChat ? 'text-white bg-gray-700' : 'text-gray-400'}`}
             title="Toggle Chat"
           >
             <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
           </button>
        </div>
      </div>

      {/* Main Layout */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Activity Bar */}
        <div className="w-12 bg-[#333333] flex flex-col items-center py-2 space-y-4 border-r border-black z-10 shrink-0">
          <div 
            className={`w-8 h-8 flex items-center justify-center rounded cursor-pointer hover:bg-gray-700 ${showSidebar ? 'border-l-2 border-white bg-[#252526]' : 'opacity-50'}`} 
            title="Explorer"
            onClick={() => setShowSidebar(!showSidebar)}
          >
             <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-white"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          </div>
          <div className="w-6 h-6 opacity-50 cursor-pointer hover:opacity-100" title="Search">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-white"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          </div>
          <div className="w-6 h-6 opacity-50 cursor-pointer hover:opacity-100" title="Source Control">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-white"><circle cx="12" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><path d="M6 9v3a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V9"/></svg>
          </div>
           <div className="w-6 h-6 text-amber-500 cursor-pointer hover:text-amber-300" title="Elysia Protocol">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          </div>
        </div>

        {/* Sidebar (Collapsible) */}
        {showSidebar && <Sidebar files={files} activeFileId={activeFileId} onFileSelect={handleFileSelect} />}

        {/* Central Workspace (Editor + Visualizer) */}
        <CodeEditor fileName={activeFileName} content={activeFileContent} />

        {/* Chat Panel (Collapsible) */}
        {showChat && <Chat onCodeReceived={handleCodeReceived} onClose={() => setShowChat(false)} />}
      </div>

      {/* Bottom Status Bar */}
      <div className="h-6 bg-[#3d4b5d] text-white text-xs flex items-center px-2 justify-between border-t border-[#202531] shrink-0">
        <div className="flex items-center space-x-4">
          <span className="flex items-center gap-1 font-bold">
             Output
          </span>
          <span>Debugger</span>
          <span>Audio</span>
          <span>Animation</span>
        </div>
        <div className="flex items-center space-x-4">
          {isPlaying && <span className="text-green-300 animate-pulse">● Running</span>}
          <span className="text-amber-300">Z-AXIS: ALIGNED</span>
          <span>Mem: 256MB</span>
        </div>
      </div>
    </div>
  );
};

export default App;
