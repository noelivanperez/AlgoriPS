import React from 'react';

const Card: React.FC<React.PropsWithChildren> = ({ children }) => (
  <div className="card">{children}</div>
);

export default Card;
