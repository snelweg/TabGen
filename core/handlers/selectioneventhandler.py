import traceback

from adsk.core import SelectionEventHandler

from .. import fusion
from .. import definitions as defs


class SelectionValidationError(Exception): pass


class SelectionEventHandler(SelectionEventHandler):

    def __init__(self, app, ui):
        super().__init__()
        self.app = app
        self.ui = ui

    def valid_selection(self, selection):
        return selection.id in [defs.selectedFaceInputId, defs.dualEdgeSelectId]

    def check_edge_selection(self, entity, inputs):
        if not inputs.alternate_edge(entity):
            return False

        return inputs.face_parallel_to_edge(entity)

    def check_face_selection(self, entity, inputs):
        if not (fusion.check_if_edge(entity)):
            return False

        if entity.objectType == 'Sketch':
            return False

        return True

    def check_selection(self, entity, selection, inputs):
        if not self.valid_selection(selection):
            return True

        try:
            if self.check_face_selection(entity, inputs):
                if selection.id == defs.dualEdgeSelectId:
                    return self.check_edge_selection(entity, inputs)
                else:
                    return True
            else:
                return False
        except:
            raise SelectionValidationError

    def notify(self, args):
        try:
            entity = args.selection.entity
            firingEvent = args.firingEvent
            selection = firingEvent.activeInput
            inputs = fusion.InputReader(self.app, firingEvent.sender.commandInputs)

            args.isSelectable = self.check_selection(entity, selection, inputs)
        except:
            self.ui.messageBox(traceback.format_exc(3))
