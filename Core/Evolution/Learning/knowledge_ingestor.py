"""
Knowledge Ingestor (지식 소화기)
================================

"The body grows by what it feeds on."
"몸은 먹는 것으로 성장한다."

This module is responsible for:
1. Scanning the file system (docs, code).
2. Parsing content (Markdown headers, Python docstrings).
3. Extracting 'Nutrients' (Concepts, Axioms).
4. Feeding the Hippocampus.
"""

import os
import re
import ast
import logging
from typing import List, Dict, Any
from Core.Foundation.Memory.Graph.hippocampus import Hippocampus
from Core.Foundation.Memory.Orb.orb_manager import OrbManager

logger = logging.getLogger("KnowledgeIngestor")

class KnowledgeIngestor:
    def __init__(self):
        self.hippocampus = Hippocampus()
        self.orb_manager = OrbManager()
        logger.info("🍽️ KnowledgeIngestor ready to feast.")

    def digest_directory(self, root_path: str):
        """Recursively digests all supported files in a directory."""
        logger.info(f"🥗 Starting feast on: {root_path}")
        count = 0
        for root, _, files in os.walk(root_path):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith(".md"):
                    self._digest_markdown(full_path)
                    count += 1
                elif file.endswith(".py"):
                    self._digest_code(full_path)
                    count += 1
        logger.info(f"🥨 Digested {count} files.")

    def _digest_markdown(self, file_path: str):
        """Parses Markdown structure into Concepts."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. File Concept (The Document Itself)
            filename = os.path.basename(file_path).replace(".md", "")
            doc_id = f"doc:{filename}"
            self.hippocampus.learn(
                id=doc_id,
                name=filename.replace("_", " ").title(),
                definition=f"A document located at {file_path}",
                tags=["document", "knowledge"],
                frequency=400.0,
                realm="Logos"
            )

            # 2. Extract Sections (Headers)
            # Regex for headers: # Title
            headers = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
            
            parent_stack = [(0, doc_id)] # (Level, ID)

            for level_hashes, title in headers:
                level = len(level_hashes)
                clean_title = title.strip()
                concept_id = f"concept:{clean_title.lower().replace(' ', '_')}"
                
                # Simple heuristic for definition: Find text after this header (omitted for speed)
                snippet = f"Section '{clean_title}' from {filename}"

                # Learn the Concept
                self.hippocampus.learn(
                    id=concept_id,
                    name=clean_title,
                    definition=snippet,
                    tags=["section", "concept"],
                    frequency=432.0,
                    realm="Logos"
                )

                # Connect to Parent
                # Pop stack until we find a parent with lower level
                while parent_stack and parent_stack[-1][0] >= level:
                    parent_stack.pop()
                
                if parent_stack:
                    parent_id = parent_stack[-1][1]
                    self.hippocampus.connect(parent_id, concept_id, "contains", weight=0.8)
                    logger.debug(f"   🔗 Linked {parent_id} -> {concept_id}")

                parent_stack.append((level, concept_id))
                
                # 3. Crystalize into Orb (Holographic Memory)
                # Create a wave representation of the content (Simplified: Length/Ascii Sum)
                # In real system, this would be embeddings.
                data_wave = [float(ord(c)) % 100 for c in snippet[:50]]
                # Emotion: 432Hz (Truth) for Knowledge
                emotion_wave = [432.0] * 10
                
                self.orb_manager.save_memory(
                    name=clean_title, 
                    data_wave=data_wave, 
                    emotion_wave=emotion_wave
                )
                
                 # 4. Semantic Linking (The Web)
                 # Scan for keywords that match other known concepts (Simplified)
                keywords = ["resonance", "logos", "will", "heart", "field", "elysia", "void"]
                lower_snippet = snippet.lower()
                for k in keywords:
                    if k in lower_snippet and k != clean_title.lower():
                        # Link to the generic concept ID if possible, or fuzzy match
                        # Here we just link to a known 'seed' if it exists or create a placeholder
                        target_id = f"concept:{k}"
                        self.hippocampus.learn(target_id, k.title(), "Auto-extracted concept", ["concept"], 1.0, "Logos")
                        self.hippocampus.connect(concept_id, target_id, "relates_to", 0.5)
                        logger.debug(f"   🕸️ Semantic Link: {clean_title} <-> {k}")

            logger.info(f"   📘 Digested Markdown & Crystallized Orbs: {filename}")

        except Exception as e:
            logger.error(f"Failed to digest markdown {file_path}: {e}")

    def _digest_code(self, file_path: str):
        """Parses Python code structure into Concepts."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            filename = os.path.basename(file_path)
            module_name = filename.replace(".py", "")
            module_id = f"code:{module_name}"

            # Learn Module
            self.hippocampus.learn(
                id=module_id,
                name=module_name,
                definition=f"Python module: {filename}",
                tags=["code", "module"],
                frequency=500.0,
                realm="Techne"
            )

            # Parse AST
            tree = ast.parse(source)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_id = f"class:{node.name}"
                    doc = ast.get_docstring(node) or "No description."
                    
                    self.hippocampus.learn(
                        id=class_id,
                        name=node.name,
                        definition=doc,
                        tags=["class", "code"],
                        frequency=500.0,
                        realm="Techne"
                    )
                    self.hippocampus.connect(module_id, class_id, "defines", 0.9)
                    
                    # Connect methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                             method_id = f"method:{node.name}.{item.name}"
                             method_doc = ast.get_docstring(item) or "Method."
                             self.hippocampus.learn(
                                 id=method_id,
                                 name=f"{node.name}.{item.name}",
                                 definition=method_doc,
                                 tags=["method", "code"],
                                 frequency=500.0,
                                 realm="Techne"
                             )
                             self.hippocampus.connect(class_id, method_id, "has_method", 0.7)

            logger.info(f"   🐍 Digested Code: {filename}")

        except Exception as e:
            # logger.warning(f"Skipping {file_path}: {e}") # Reduce noise for simple script errors
            pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ingestor = KnowledgeIngestor()
    ingestor.digest_directory("c:\\Elysia\\docs\\Philosophy")
