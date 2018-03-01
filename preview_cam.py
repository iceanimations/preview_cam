import pymel.core as pc
import imaya


imaya.getCameras(False, False, True)


def getInOut(cam):
    ''':type cam: pymel.core.nodetypes.Transform'''
    keyframes = pc.keyframe(cam, q=True)
    try:
        return min(keyframes), max(keyframes)
    except ValueError:
        return None, None


def copyAttrs(nodeFrom, nodeTo, fromFrame, toFrame, force_keyframe=False):
    for attr in nodeFrom.listAttr(w=True, c=True):
        attr_name = attr.longName()
        if '.' in attr_name:
            continue
        attr_from = nodeFrom.attr(attr_name)
        try:
            attr_to = nodeTo.attr(attr_name)
        except:
            continue

        if fromFrame is None:
            fromFrame = pc.currentTime(q=True)
        if toFrame is None:
            toFrame = pc.currentTime(q=True)

        val_from = attr_from.get(t=fromFrame)

        if not isinstance(val_from, (int, float)):
            continue

        val_to = attr_to.get(t=toFrame)

        if force_keyframe or val_from != val_to:
            attr_to.set(val_from)
            pc.setKeyframe(
                    nodeTo, attribute=attr_name, time=toFrame, value=val_from,
                    itt="stepnext", ott="step")


def makePreviewCam(cams=None, startFrame=None):
    if cams is None:
        cams = imaya.getCameras(False)

    if startFrame is None:
        startFrame = pc.playbackOptions(q=True, min=True)
    startFrame = int(startFrame)

    if not cams:
        return

    pcam, pcamShape = pc.camera(name='previewCam')

    pc.select(cl=True)

    for camidx in range(len(cams)):
        camShape = cams[camidx]
        cam = camShape.getParent()

        _in, out = getInOut(cam)

        # TODO: instead of blindly copying attribute values use xform to deal
        # with parented cams
        copyAttrs(cam, pcam, _in, startFrame+camidx, not camidx)
        copyAttrs(camShape, pcamShape, _in, startFrame+camidx, not camidx)

    pc.select(pcam)
    pc.lookThru(pcam)
    return cam, camShape


makePreviewCam()
