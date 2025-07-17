import React from 'react';

const Spinner: React.FC = () => (
  <div className="w-8 h-8 border-4 border-gray-300 border-t-primary rounded-full animate-spin" role="status" aria-label="Loading" />
);

export default Spinner;

