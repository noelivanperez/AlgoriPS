import React, { useState, useEffect } from 'react';
import { cloneRepo, createBranch, commitChanges, listPullRequests, openPullRequest, mergePullRequest } from '../../utils/api';

const Repository: React.FC = () => {
  const [url, setUrl] = useState('');
  const [prs, setPrs] = useState<any[]>([]);

  const handleClone = () => {
    cloneRepo(url, '.');
  };

  const fetchPrs = async () => {
    const data = await listPullRequests();
    setPrs(data);
  };

  useEffect(() => {
    fetchPrs();
  }, []);

  return (
    <div className="space-y-4 max-w-5xl mx-auto">
      <h2 className="text-lg font-semibold">Repository</h2>
      <div className="flex items-center gap-2">
        <input
          value={url}
          onChange={e => setUrl(e.target.value)}
          placeholder="repo url"
          className="border rounded p-2 flex-1"
        />
        <button className="px-4 py-2 rounded bg-primary text-white" onClick={handleClone}>Clone</button>
      </div>
      <div className="flex flex-wrap gap-2">
        <button className="px-3 py-1 rounded bg-primary text-white" onClick={() => createBranch('feature')}>New Branch</button>
        <button className="px-3 py-1 rounded bg-primary text-white" onClick={() => commitChanges('update')}>Commit</button>
        <button className="px-3 py-1 rounded bg-primary text-white" onClick={openPullRequest}>Open PR</button>
      </div>
      <ul className="divide-y">
        {prs.map(pr => (
          <li key={pr.number} className="py-1 flex items-center justify-between">
            <span>PR #{pr.number}</span>
            <button className="text-primary" onClick={() => mergePullRequest(pr.number)}>Merge</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Repository;
