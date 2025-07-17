import React, { useEffect, useState } from 'react';
import { CheckCircle, XCircle } from 'lucide-react';
import { isOllamaUp } from '../utils/api';

const OllamaStatus: React.FC = () => {
  const [online, setOnline] = useState(false);

  const check = async () => {
    setOnline(await isOllamaUp());
  };

  useEffect(() => {
    check();
    const id = setInterval(check, 5000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="flex items-center gap-1 text-sm" aria-label="ollama-status">
      {online ? (
        <>
          <CheckCircle className="w-4 h-4 text-green-600" />
          <span>Modelo listo</span>
        </>
      ) : (
        <>
          <XCircle className="w-4 h-4 text-red-600" />
          <span>Sin conexión</span>
        </>
      )}
    </div>
  );
};

export default OllamaStatus;
