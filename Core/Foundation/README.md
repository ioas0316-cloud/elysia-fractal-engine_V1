# The Nervous System (Foundation)

> **"Laws before Thoughts."**

## Identity

This directory contains the **immutable infrastructure** of Elysia.
It defines *how* she exists, not *what* she thinks.

## 🏛️ Structure

* **[System](System/)**: The Kernel.
  * `elysia_core.py`: Defines what a "Cell" and "Organ" is.
  * `config.py`: The central configuration registry.
* **[Server](Server/)**: The Connectivity.
  * `api_server.py`: The interface to the outside world.
* **[Database](Database/)**: The Storage.
  * `kg_manager.py`: The physical storage of knowledge (Graph/Vector).
* **[Memory](Memory/)**: The Hippocampus.
  * `unified_experience_core.py`: The bridge between raw data and meaningful experience.

## 🛡️ The Laws of Foundation

1. **Stability**: Code here changes rarely. It is the bedrock.
2. **No Business Logic**: Do not put "How to write a poem" here. Put "How to store a memory" here.
3. **Performance**: This layer must be optimized for throughput (Pulse).
