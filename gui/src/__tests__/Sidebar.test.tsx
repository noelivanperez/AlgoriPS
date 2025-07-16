import React from 'react';
import { render } from '@testing-library/react';
import Sidebar from '../components/Sidebar';

test('renders sidebar', () => {
  const { getByText } = render(<Sidebar />);
  expect(getByText('Home')).toBeInTheDocument();
  expect(getByText('Repository')).toBeInTheDocument();
});
