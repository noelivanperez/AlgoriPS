import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';

interface ModalProps {
  open: boolean;
  onClose: () => void;
}

const Modal: React.FC<React.PropsWithChildren<ModalProps>> = ({ open, onClose, children }) => (
  <AnimatePresence>
    {open && (
      <motion.div
        className="fixed inset-0 bg-black/40 flex items-center justify-center"
        role="dialog"
        aria-modal="true"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          className="bg-surface rounded-2xl p-4 w-11/12 max-w-lg"
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0.9 }}
        >
          {children}
          <button onClick={onClose} aria-label="Close modal" className="mt-4 px-4 py-2 rounded bg-primary text-white">Close</button>
        </motion.div>
      </motion.div>
    )}
  </AnimatePresence>
);

export default Modal;

