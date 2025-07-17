import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import Chat from '../features/chat/Chat';

afterEach(() => {
  jest.resetAllMocks();
});

test('renders chat input', () => {
  const { getByLabelText, getByText } = render(<Chat />);
  expect(getByLabelText('prompt')).toBeInTheDocument();
  expect(getByText('Send')).toBeInTheDocument();
});

test('sends prompt to backend', async () => {
  const fakeReader = { read: jest.fn().mockResolvedValue({ done: true }) };
  global.fetch = jest.fn().mockResolvedValue({ body: { getReader: () => fakeReader } } as any);

  const { getByLabelText, getByText } = render(<Chat />);
  fireEvent.change(getByLabelText('prompt'), { target: { value: 'hello' } });
  fireEvent.click(getByText('Send'));

  await waitFor(() => expect(fetch).toHaveBeenCalled());
  expect((fetch as jest.Mock).mock.calls[0][0]).toBe('/chat');
});
