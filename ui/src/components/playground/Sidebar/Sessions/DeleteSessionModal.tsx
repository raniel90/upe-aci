import { type FC } from 'react'

import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from '@/components/ui/dialog'
import { pt_BR } from '@/lib/i18n'

interface DeleteSessionModalProps {
  isOpen: boolean
  onClose: () => void
  onDelete: () => Promise<void>
  isDeleting: boolean
}

const DeleteSessionModal: FC<DeleteSessionModalProps> = ({
  isOpen,
  onClose,
  onDelete,
  isDeleting
}) => (
  <Dialog open={isOpen} onOpenChange={onClose}>
    <DialogContent className="font-geist">
      <DialogHeader>
        <DialogTitle>{pt_BR.sessions.deleteModal.title}</DialogTitle>
        <DialogDescription>
          {pt_BR.sessions.deleteModal.description}
        </DialogDescription>
      </DialogHeader>
      <DialogFooter>
        <Button
          variant="outline"
          className="border-border font-geist rounded-xl"
          onClick={onClose}
          disabled={isDeleting}
        >
          {pt_BR.sessions.deleteModal.cancel}
        </Button>
        <Button
          variant="destructive"
          onClick={onDelete}
          disabled={isDeleting}
          className="font-geist rounded-xl"
        >
          {pt_BR.sessions.deleteModal.delete}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
)

export default DeleteSessionModal
