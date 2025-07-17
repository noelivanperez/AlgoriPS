import '@testing-library/jest-dom';
import React from 'react';
import { render, waitFor } from '@testing-library/react';
import OllamaStatus from '../components/OllamaStatus';
import * as api from '../utils/api';

afterEach(() => {
  jest.resetAllMocks();
});

test('shows online message', async () => {
  jest.spyOn(api, 'isOllamaUp').mockResolvedValue(true);
  const { getByLabelText } = render(<OllamaStatus />);
  await waitFor(() => {
    expect(getByLabelText('ollama-status')).toHaveTextContent('Modelo listo');
  });
});

test('shows offline message', async () => {
  jest.spyOn(api, 'isOllamaUp').mockResolvedValue(false);
  const { getByLabelText } = render(<OllamaStatus />);
  await waitFor(() => {
    expect(getByLabelText('ollama-status')).toHaveTextContent('Sin conexión');
  });
});
