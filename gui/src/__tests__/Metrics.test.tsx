import '@testing-library/jest-dom';
import React from 'react';
import { render, waitFor } from '@testing-library/react';
import Metrics from '../features/metrics/Metrics';

afterEach(() => {
  jest.resetAllMocks();
});

test('shows error when metrics cannot be parsed', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    text: () => Promise.resolve('bad line')
  }) as any;

  const { getByRole } = render(<Metrics />);
  await waitFor(() => {
    expect(getByRole('alert')).toHaveTextContent('Could not parse metrics');
  });
});

