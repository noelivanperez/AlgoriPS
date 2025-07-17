import '@testing-library/jest-dom';
import React from 'react';
import { render } from '@testing-library/react';
import Dashboard from '../features/dashboard/Dashboard';

test('renders dashboard metrics', () => {
  const { getAllByLabelText } = render(<Dashboard />);
  expect(getAllByLabelText('metric-value').length).toBeGreaterThan(0);
});
