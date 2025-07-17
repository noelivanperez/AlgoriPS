import React from 'react';

const Card: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="rounded-2xl shadow-lg bg-surface p-4" role="region">{children}</div>
);

export default Card;

