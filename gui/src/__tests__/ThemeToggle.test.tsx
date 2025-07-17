import '@testing-library/jest-dom';
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import ThemeToggle from '../components/ThemeToggle';

afterEach(() => {
  localStorage.clear();
});

test('toggles and persists theme', () => {
  const { getByLabelText } = render(<ThemeToggle />);
  const btn = getByLabelText('toggle-theme');
  fireEvent.click(btn);
  expect(localStorage.getItem('theme')).toBe('dark');
});
