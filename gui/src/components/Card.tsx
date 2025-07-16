import React from 'react';

const Card: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="card" role="region">{children}</div>
);

export default Card;

