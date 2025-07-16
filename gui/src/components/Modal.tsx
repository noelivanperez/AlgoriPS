import React from 'react';

interface ModalProps {
  open: boolean;
  onClose: () => void;
}

const Modal: React.FC<React.PropsWithChildren<ModalProps>> = ({ open, onClose, children }) => (
  open ? (
    <div className="modal">
      <div className="modal-content">
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  ) : null
);

export default Modal;
