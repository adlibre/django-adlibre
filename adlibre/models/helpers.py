import os.path

from django.db.models import Model
from django.utils.encoding import force_unicode
from django.template.defaultfilters import slugify


class AutoSlug(object):
    """
    Automatically slugify the 'slug' field on save if empty

    AUTOSLUG_FIELDS = { 'slug_field': ('source', 'data', 'fields',),}

    """

    def save(self, *args, **kwargs):

        autoslug_fields = getattr(self, 'AUTOSLUG_FIELDS', None)

        # Call super, save() to get us an ID.
        super(AutoSlug, self).save(*args, **kwargs)

        if autoslug_fields is None:
            # Default
            if getattr(self, 'slug') == "":
                slug_content = slugify(getattr(self, 'name'))
                setattr(self, 'slug', slug_content)
        else:
            # Custom slug options set
            for slug_name, fields in autoslug_fields.items():
                if getattr(self, slug_name) == "":
                    # Get slug content from fields
                    content = str()
                    for f in fields:
                        content += ' ' + str(getattr(self, f, ''))
                    slug_content = slugify(content)
                    # Set slug content
                    setattr(self, slug_name, slug_content)

        # then call super, save() to persist updated slug info
        super(AutoSlug, self).save()


# RenameFilesModel Originally from http://djangosnippets.org/snippets/1129/
class RenameFilesModel(Model):
    """
    Abstract model implementing a two-phase save in order to rename
    `FileField` and `ImageField` filenames after saving.  This allows the
    final filenames to contain information like the primary key of the model.

    Example:

        class Photo(RenameFilesModel):
            file = models.ImageField(upload_to='uploads/temp')

            RENAME_FILES = {
                'file': {'dest': 'uploads/photos', 'keep_ext': True}
            }

        >>> photo = Photo(file='uploads/temp/photo.jpg')
        >>> photo.pk

        >>> photo.save()
        >>> photo.pk
        1
        >>> photo.file
        <ImageFieldFile: uploads/photos/1.jpg>

    If the 'dest' option is a callable, it will be called with the model
    instance (guaranteed to be saved) and the currently saved filename, and
    must return the new filename.  Otherwise, the filename is determined by
    'dest' and the model's primary key.

    If a file already exists at the resulting path, it is deleted.  This is
    desirable if the filename should always be the primary key, for instance.
    To avoid this behavior, write a 'dest' handler that results in a unique
    filename.

    If 'keep_ext' is True (the default), the extension of the previously saved
    filename will be appended to the primary key to construct the filename.
    The value of 'keep_ext' is not considered if 'dest' is a callable.

    """
    RENAME_FILES = {}

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False):
        rename_files = getattr(self, 'RENAME_FILES', None)
        if rename_files:
            super(RenameFilesModel, self).save(force_insert, force_update)
            force_insert, force_update = False, True

            for field_name, options in rename_files.iteritems():
                field = getattr(self, field_name)
                file_name = force_unicode(field)
                name, ext = os.path.splitext(file_name)
                keep_ext = options.get('keep_ext', True)
                final_dest = options['dest']
                if callable(final_dest):
                    final_name = final_dest(self, file_name)
                else:
                    final_name = os.path.join(final_dest, '%s' % (self.pk,))
                    if keep_ext:
                        final_name += ext
                if file_name != final_name and field.name != '':
                    field.storage.delete(final_name)
                    field.storage.save(final_name, field)
                    field.storage.delete(file_name)
                    setattr(self, field_name, final_name)

        super(RenameFilesModel, self).save(force_insert, force_update)
