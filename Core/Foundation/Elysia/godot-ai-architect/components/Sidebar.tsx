import React from 'react';
import { FileNode } from '../types';

// Simple icons as SVG components to avoid external deps issues in this environment
const FolderIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400 mr-1"><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 2H4a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2Z"/></svg>
);
const FileIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-godot-accent mr-1"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
);
const GodotIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="text-blue-400 mr-1"><circle cx="12" cy="12" r="10" opacity="0.2"/><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 14a1.5 1.5 0 1 1 1.5-1.5A1.5 1.5 0 0 1 12 16zm3.5-4h-7a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1z"/></svg>
);

interface SidebarProps {
  files: FileNode[];
  activeFileId: string | null;
  onFileSelect: (id: string) => void;
}

const FileTreeItem: React.FC<{ node: FileNode; activeId: string | null; onSelect: (id: string) => void; level: number }> = ({ node, activeId, onSelect, level }) => {
  const indent = level * 12;
  
  if (node.type === 'folder') {
    return (
      <div>
        <div className="flex items-center py-1 px-2 hover:bg-gray-700 cursor-pointer text-sm" style={{ paddingLeft: `${indent + 8}px` }}>
          <FolderIcon />
          <span className="truncate">{node.name}</span>
        </div>
        {node.children?.map(child => (
          <FileTreeItem key={child.id} node={child} activeId={activeId} onSelect={onSelect} level={level + 1} />
        ))}
      </div>
    );
  }

  return (
    <div 
      onClick={() => onSelect(node.id)}
      className={`flex items-center py-1 px-2 cursor-pointer text-sm ${activeId === node.id ? 'bg-godot-base text-white' : 'hover:bg-gray-700 text-gray-400'}`}
      style={{ paddingLeft: `${indent + 8}px` }}
    >
      {node.name.endsWith('.gd') ? <GodotIcon /> : <FileIcon />}
      <span className="truncate">{node.name}</span>
    </div>
  );
};

export const Sidebar: React.FC<SidebarProps> = ({ files, activeFileId, onFileSelect }) => {
  return (
    <div className="w-64 bg-vscode-sidebar flex flex-col border-r border-black h-full">
      <div className="h-10 flex items-center px-4 text-xs font-bold uppercase tracking-wider text-gray-500">
        Explorer
      </div>
      <div className="flex-1 overflow-y-auto">
        <div className="mb-2">
          <div className="px-4 py-1 text-xs font-bold text-blue-400 uppercase mb-1">Project: MyGodotGame</div>
          {files.map(file => (
            <FileTreeItem key={file.id} node={file} activeId={activeFileId} onSelect={onFileSelect} level={0} />
          ))}
        </div>
      </div>
    </div>
  );
};