import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';

interface ModalProps {
  open: boolean;
  onClose: () => void;
}

const Modal: React.FC<React.PropsWithChildren<ModalProps>> = ({ open, onClose, children }) => (
  <AnimatePresence>
    {open && (
      <motion.div className="modal" role="dialog" aria-modal="true" initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}}>
        <motion.div className="modal-content" initial={{scale:0.9}} animate={{scale:1}} exit={{scale:0.9}}>
          {children}
          <button onClick={onClose} aria-label="Close modal">Close</button>
        </motion.div>
      </motion.div>
    )}
  </AnimatePresence>
);

export default Modal;

