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
    <div>
      <h2>Repository</h2>
      <div>
        <input value={url} onChange={e => setUrl(e.target.value)} placeholder="repo url" />
        <button onClick={handleClone}>Clone</button>
      </div>
      <button onClick={() => createBranch('feature')}>New Branch</button>
      <button onClick={() => commitChanges('update')}>Commit</button>
      <button onClick={openPullRequest}>Open PR</button>
      <ul>
        {prs.map(pr => (
          <li key={pr.number}>
            PR #{pr.number} <button onClick={() => mergePullRequest(pr.number)}>Merge</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Repository;
