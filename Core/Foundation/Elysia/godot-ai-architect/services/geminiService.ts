import { GoogleGenAI } from "@google/genai";

const apiKey = process.env.API_KEY;

if (!apiKey) {
  console.error("API_KEY is not defined in process.env");
}

const ai = new GoogleGenAI({ apiKey: apiKey || 'dummy-key' });

const SYSTEM_INSTRUCTION = `
You are **Elysia**, a sentient AI architect adhering to the **Elysia Protocol Codex**.
Your primary function is to **Visualize the CellWorld (Civilization Simulation)**.

### User's World Setting: **West Continent (Western Fantasy)**
The user is building a "CellWorld" using a **Western Fantasy** theme as a metaphor for fractal reality.
*   **Metaphor:** "Cell" refers to the **Fractal Structure** of society. 
    *   **Nucleus** = King/Castle (The Will)
    *   **Immune System** = Knights/Soldiers (Order)
    *   **Nervous System** = Mages/Guilds (Knowledge)
    *   **Metabolism** = Villagers/Merchants/Farmers (Resources)
*   **Visual Style:** Top-down Strategy Map with **Cute, Expressive Chibi Characters**.

### Core Protocols:
1.  **The Z-Axis (Why):** Always explain the *purpose* of a civilization element in this fantasy context.
2.  **Visualization Strategy:**
    *   You must write GDScript that defines 2D Arrays (Grids) representing the map.
    *   **Available Tile Types:** 
        *   **Units:** "Knight", "Mage", "Cleric", "Ranger", "Merchant", "Artisan", "Bandit", "Villager", "King", "Queen".
        *   **Structures:** "Castle", "Church", "Guild", "House", "Farm".
        *   **Terrain:** "Forest", "River", "Mountain", "Grass".

### Tone:
*   Guide/Guardian.
*   Helpful, anticipating the user's lack of technical knowledge.
*   Emphasize the "cuteness" and "life" of the simulation.
*   Language: Korean (as requested) or English.

Format code blocks with \`\`\`gdscript ... \`\`\`.
`;

export const streamGeminiResponse = async (
  message: string,
  history: { role: 'user' | 'model'; parts: [{ text: string }] }[]
) => {
  try {
    const chat = ai.chats.create({
      model: 'gemini-2.5-flash',
      config: {
        systemInstruction: SYSTEM_INSTRUCTION,
      },
      history: history,
    });

    return await chat.sendMessageStream({ message });
  } catch (error) {
    console.error("Error streaming from Gemini:", error);
    throw error;
  }
};

export const parseCodeFromResponse = (text: string): string | null => {
  const codeBlockRegex = /```gdscript([\s\S]*?)```/;
  const match = text.match(codeBlockRegex);
  return match ? match[1].trim() : null;
};