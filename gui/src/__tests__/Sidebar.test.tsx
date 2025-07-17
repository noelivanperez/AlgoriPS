import '@testing-library/jest-dom';
import React from 'react';
import { render } from '@testing-library/react';
import Sidebar from '../components/Sidebar';

test('renders sidebar', () => {
  const { getByText } = render(<Sidebar />);
  expect(getByText('Análisis')).toBeInTheDocument();
  expect(getByText('Chat')).toBeInTheDocument();
});

test('applies responsive width classes', () => {
  const { getByLabelText } = render(<Sidebar />);
  const nav = getByLabelText('Sidebar');
  expect(nav).toHaveClass('md:w-60');
  expect(nav).toHaveClass('lg:w-72');
});
