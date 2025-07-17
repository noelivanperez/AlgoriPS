import '@testing-library/jest-dom';
import {
  cloneRepo,
  createBranch,
  commitChanges,
  listPullRequests,
  openPullRequest,
  mergePullRequest,
  listPlugins,
  installPlugin,
  uninstallPlugin,
} from '../utils/api';

afterEach(() => {
  jest.resetAllMocks();
});

test('cloneRepo posts to /repo/clone', async () => {
  global.fetch = jest.fn().mockResolvedValue({} as any);
  await cloneRepo('url', 'dest');
  expect(fetch).toHaveBeenCalledWith('/repo/clone', expect.objectContaining({
    method: 'POST',
  }));
});

test('openPullRequest hits /repo/pr/create', async () => {
  global.fetch = jest.fn().mockResolvedValue({} as any);
  await openPullRequest();
  expect(fetch).toHaveBeenCalledWith('/repo/pr/create', expect.objectContaining({ method: 'POST' }));
});

test('uninstallPlugin uses DELETE', async () => {
  global.fetch = jest.fn().mockResolvedValue({} as any);
  await uninstallPlugin('plug');
  expect(fetch).toHaveBeenCalledWith('/plugins/plug', expect.objectContaining({ method: 'DELETE' }));
});

test('listPlugins returns data', async () => {
  global.fetch = jest.fn().mockResolvedValue({ json: () => Promise.resolve([{ name: 'p' }]) } as any);
  const data = await listPlugins();
  expect(data[0].name).toBe('p');
});
