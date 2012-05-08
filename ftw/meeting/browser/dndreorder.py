from Products.Five.browser import BrowserView


class SaveDragndropOrderView(BrowserView):
    """Stores the new order"""

    def __call__(self, uids):
        uids = uids.split(',')
        for i in range(len(uids)):
            uid = uids[i]
            uid = uid.replace('uid_', '')
            obj = self.context.reference_catalog.lookupObject(uid)
            id_ = obj.id
            self.context.moveObject(id_, i)
            obj.reindexObject(idxs=['getObjPositionInParent'])
        return 'ok'
