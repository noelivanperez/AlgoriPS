import React, { useEffect, useRef, useState } from 'react';
import { chatWithOllama } from '../../utils/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const DB_NAME = 'chat';
const STORE_NAME = 'messages';

async function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      req.result.createObjectStore(STORE_NAME, { autoIncrement: true });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function getAllMessages(): Promise<Message[]> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const store = tx.objectStore(STORE_NAME);
    const req = store.getAll();
    req.onsuccess = () => resolve(req.result as Message[]);
    req.onerror = () => reject(req.error);
  });
}

async function addMessage(msg: Message): Promise<void> {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).add(msg);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function exportMessages(): Promise<string> {
  const msgs = await getAllMessages();
  return JSON.stringify(msgs, null, 2);
}

import { executeQuery } from '../../utils/api';

const Chat: React.FC = () => {
  const [name, setName] = useState('');
  const [sql, setSql] = useState('');
  const [rows, setRows] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [dbConn, setDbConn] = useState('default');
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getAllMessages().then(setMessages).catch(() => {});
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = async (prompt: string) => {
    const userMsg: Message = { role: 'user', content: prompt };
    setMessages(prev => [...prev, userMsg]);
    await addMessage(userMsg);
    setInput('');

    try {
      const reader = await chatWithOllama(prompt, dbConn);
      let result = '';
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        result += decoder.decode(value);
        setMessages(prev => {
          const updated = prev.slice();
          const last = updated[updated.length - 1];
          if (last.role === 'assistant') {
            last.content = result;
          } else {
            updated.push({ role: 'assistant', content: result });
          }
          return [...updated];
        });
      }
      await addMessage({ role: 'assistant', content: result });
    } catch (err) {
      console.error(err);
    }
  };

  const runQuery = async () => {
    const data = await executeQuery(name, sql);
    setRows(data);
  };

  const onSend = () => {
    if (input.trim()) send(input.trim());
  };

  const onUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      send(reader.result as string);
    };
    reader.readAsText(file);
  };

  const onExport = async () => {
    const json = await exportMessages();
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat_history.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-full border rounded-2xl shadow-lg">
      <div className="flex-1 overflow-y-auto p-4 space-y-4" aria-label="messages">
        {messages.map((m, idx) => (
          <div key={idx} className="flex items-start gap-2" aria-label="message">
            <div className="w-8 h-8 rounded-full bg-gray-300 flex-shrink-0" />
            <div>
              <div className="text-sm text-gray-500">{m.role}</div>
              <div>{m.content}</div>
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>
      <div className="p-2 flex items-center gap-2 border-t">
        <input
          aria-label="prompt"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Escribe tu consulta…"
          className="flex-1 border rounded p-2"
        />
        <button onClick={onSend} className="px-4 py-2 rounded bg-primary text-white">Send</button>
        <input aria-label="upload" type="file" onChange={onUpload} />
        <select value={dbConn} onChange={e => setDbConn(e.target.value)} className="border rounded p-1">
          <option value="default">default</option>
          <option value="analytics">analytics</option>
        </select>
        <button onClick={onExport} className="px-4 py-2 rounded bg-primary text-white">Export</button>
      </div>
    </div>
  );
};

export default Chat;
