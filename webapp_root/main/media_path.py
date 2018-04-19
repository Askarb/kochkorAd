import uuid


def ad_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/ad/ad_id/<filename>
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'ad/{0}/{1}'.format(instance.ad.id, filename)


