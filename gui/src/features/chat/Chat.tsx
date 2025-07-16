import React, { useState } from 'react';
import { executeQuery } from '../../utils/api';

const Chat: React.FC = () => {
  const [name, setName] = useState('');
  const [sql, setSql] = useState('');
  const [rows, setRows] = useState<any[]>([]);

  const runQuery = async () => {
    const data = await executeQuery(name, sql);
    setRows(data);
  };

  return (
    <div>
      <h2>DB Query</h2>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="connection name"
      />
      <textarea
        value={sql}
        onChange={e => setSql(e.target.value)}
        placeholder="SELECT * FROM table"
      />
      <button onClick={runQuery}>Run</button>
      <pre aria-label="query-results">{JSON.stringify(rows, null, 2)}</pre>
    </div>
  );
};

export default Chat;
