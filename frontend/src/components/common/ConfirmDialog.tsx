import { Modal } from "./Modal";
import { AlertTriangle } from "lucide-react";

interface ConfirmDialogProps {
  title: string;
  message: string;
  confirmLabel?: string;
  danger?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

export function ConfirmDialog({
  title,
  message,
  confirmLabel = "Confirm",
  danger = true,
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  return (
    <Modal
      title={title}
      onClose={onCancel}
      footer={
        <>
          <button className="btn btn--ghost" onClick={onCancel}>
            Cancel
          </button>
          <button
            className={danger ? "btn btn--danger" : "btn btn--primary"}
            onClick={onConfirm}
          >
            {confirmLabel}
          </button>
        </>
      }
    >
      <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
        {danger && (
          <div style={{ color: "var(--risk-severe)", marginTop: 2 }}>
            <AlertTriangle size={18} />
          </div>
        )}
        <p style={{ margin: 0, color: "var(--text-secondary)", fontSize: 13.5, lineHeight: 1.6 }}>
          {message}
        </p>
      </div>
    </Modal>
  );
}
