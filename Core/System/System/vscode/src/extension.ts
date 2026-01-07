import * as vscode from 'vscode';
import fetch from 'node-fetch';

async function postJSON(url: string, body: any) {
    const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
}

export function activate(context: vscode.ExtensionContext) {
    const decide = vscode.commands.registerCommand('elysia.decideTool', async () => {
        const base = vscode.workspace.getConfiguration().get('elysia.baseUrl', 'http://127.0.0.1:5000');
        const editor = vscode.window.activeTextEditor;
        const sel = editor?.document.getText(editor.selection) || '';
        const prompt = sel || await vscode.window.showInputBox({ prompt: 'Enter prompt for Elysia' });
        if (!prompt) return;
        try {
            const data = await postJSON(`${base}/tool/decide`, { prompt });
            const decision = data.decision;
            vscode.window.showInformationMessage(`Decision: ${JSON.stringify(decision)}`);
            context.workspaceState.update('elysia.lastDecision', decision);
        } catch (e: any) {
            vscode.window.showErrorMessage(`Decide failed: ${e.message}`);
        }
    });

    const execute = vscode.commands.registerCommand('elysia.executeDecision', async () => {
        const base = vscode.workspace.getConfiguration().get('elysia.baseUrl', 'http://127.0.0.1:5000');
        let decision: any = context.workspaceState.get('elysia.lastDecision');
        if (!decision) {
            const raw = await vscode.window.showInputBox({ prompt: 'Paste decision JSON' });
            if (!raw) return; 
            try { decision = JSON.parse(raw); } catch { vscode.window.showErrorMessage('Invalid JSON'); return; }
        }
        if (decision?.confirm_required) {
            const pick = await vscode.window.showQuickPick(['Yes', 'No'], { placeHolder: 'Confirm execution?' });
            if (pick !== 'Yes') { vscode.window.showInformationMessage('Cancelled'); return; }
            decision.confirm = true; delete decision.confirm_required;
        }
        try {
            const data = await postJSON(`${base}/tool/execute`, { decision });
            vscode.window.showInformationMessage(`Result: ${JSON.stringify(data.result).slice(0, 500)}`);
        } catch (e: any) {
            vscode.window.showErrorMessage(`Execute failed: ${e.message}`);
        }
    });

    context.subscriptions.push(decide, execute);
}

export function deactivate() {}

