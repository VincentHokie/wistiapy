from schematics import types, models


class Asset(models.Model):
    """
    Wrapper for asset objects (embedded in Media objects) for results from
    the Wistia API
    """

    url = types.URLType(
        metadata=dict(description="A direct-access URL to the content of the asset")
    )
    width = types.IntType(
        metadata=dict(
            description="(optional) The width of this specific asset, if applicable"
        )
    )
    height = types.IntType(
        metadata=dict(
            description="(optional) The height of this specific asset, if applicable"
        )
    )
    file_size = types.IntType(
        serialized_name="fileSize",
        metadata=dict(
            description="The size of the asset file that's referenced by url, measured in bytes"
        ),
    )
    content_type = types.StringType(
        serialized_name="contentType",
        metadata=dict(description="The asset's content type"),
    )
    type = types.StringType(
        metadata=dict(
            description="The internal type of the asset, describing how the asset should be used"
        ),
        choices=[
            "OriginalFile",
            "FlashVideoFile",
            "MdFlashVideoFile",
            "HdFlashVideoFile",
            "Mp4VideoFile",
            "MdMp4VideoFile",
            "HdMp4VideoFile",
            "HlsVideoFile",
            "IphoneVideoFile",
            "StoryboardFile",
            "StillImageFile",
            "SwfFile",
            "Mp3AudioFile",
            "LargeImageFile",
        ],
    )


class ProjectReference(models.Model):
    id = types.IntType(metadata=dict(description=""))
    name = types.StringType(metadata=dict(description=""))
    hashed_id = types.StringType(metadata=dict(description=""))


class Thumbnail(models.Model):
    url = types.URLType(metadata=dict(description=""))
    width = types.IntType(metadata=dict(description=""))
    height = types.IntType(metadata=dict(description=""))


class Media(models.Model):
    """ Wrapper for Wistia Media results """

    id = types.IntType(
        metadata=dict(
            description="A unique numeric identifier for the media within the system."
        )
    )
    name = types.StringType(metadata=dict(description="The display name of the media."))
    hashed_id = types.StringType(
        metadata=dict(description="A unique alphanumeric identifier for this media.")
    )
    description = types.StringType(
        metadata=dict(
            description=(
                "A description for the media which usually appears near the top of the"
                "sidebar on the media’s page"
            )
        )
    )
    project = types.ModelType(
        ProjectReference,
        required=False,
        metadata=dict(
            description="Information about the project in which the media resides"
        ),
    )
    type = types.StringType(
        metadata=dict(description="A string representing what type of media this is"),
        choices=[
            "Video",
            "Image",
            "Audio",
            "Swf",
            "MicrosoftOfficeDocument",
            "PdfDocument",
            "UnknownType",
        ],
    )
    status = types.StringType(
        metadata=dict(description="Post upload processing status"),
        choices=["queued", "processing", "ready", "failed"],
    )
    progress = types.FloatType(
        metadata=dict(
            description=(
                "(optional) After a file has been uploaded to Wistia, it needs to be"
                "processed before it is available for online viewing. This field is"
                "a floating point value between 0 and 1 that indicates the progress of"
                "that processing."
            )
        )
    )
    section = types.StringType(
        required=False,
        metadata=dict(
            description=(
                "(optional) The title of the section in which the media appears."
                "This attribute is omitted if the media is not in a section (default)."
            )
        ),
    )
    thumbnail = types.ModelType(
        Thumbnail,
        metadata=dict(
            description="An object representing the thumbnail for this media"
        ),
    )
    duration = types.FloatType(
        metadata=dict(
            description=(
                "(optional) For Audio or Video files, this field specifies the length"
                "(in seconds). For Document files, this field specifies the number of"
                "pages in the document. For other types of media, or if the duration"
                "is unknown, this field is omitted."
            )
        )
    )
    created = types.DateTimeType(
        metadata=dict(description="The date when the media was originally uploaded.")
    )
    updated = types.DateTimeType(
        metadata=dict(description="The date when the media was last changed.")
    )
    assets = types.ListType(
        types.ModelType(Asset),
        metadata=dict(description="An array of the assets available for this media"),
    )
    embed_code = types.StringType(
        serialized_name="embedCode",
        required=False,
        metadata=dict(
            description=r"""
            DEPRECATED
            The HTML code that would be used for embedding the media into a web page.
            Please note that in JSON format, all quotes are escaped with a
            backslash (\) character. In XML, angle brackets (< and >) and
            ampersands (&) are converted to their equivalent XML entities
            ("&lt;", "&gt;", and "&amp;" respectively) to prevent XML parser errors.
            """
        ),
    )

    # Undocumented "transcript" field
    # transcript = types.DictType(required=False)


class Project(models.Model):
    """Wrapper for project results."""

    id = types.IntType(
        metadata=dict(
            description="A unique numeric identifier for the project within the system."
        )
    )
    name = types.StringType(metadata=dict(description="The project's display name."))
    hashed_id = types.StringType(
        metadata=dict(
            description=(
                "A private hashed id, uniquely identifying the project within the"
                "system. Used for playlists and RSS feeds"
            )
        )
    )
    media_count = types.IntType(
        serialized_name="mediaCount",
        metadata=dict(
            description="The number of different medias that have been uploaded to the project."
        ),
    )
    created = types.DateTimeType(
        metadata=dict(description="The date that the project was originally created.")
    )
    updated = types.DateTimeType(
        metadata=dict(description="The date that the project was last updated")
    )
    anonymous_can_upload = types.BooleanType(
        serialized_name="anonymousCanUpload",
        metadata=dict(
            description=(
                "A boolean indicating whether or not anonymous uploads are enabled for the project"
            )
        ),
    )
    anonymous_can_download = types.BooleanType(
        serialized_name="anonymousCanDownload",
        metadata=dict(
            description=(
                "A boolean indicating whether or not anonymous downloads are enabled for this project"
            )
        ),
    )
    public = types.BooleanType(
        metadata=dict(
            description=(
                "A boolean indicating whether the project is available for public (anonymous) viewing"
            )
        )
    )
    public_id = types.StringType(
        serialized_name="publicId",
        metadata=dict(
            description=(
                "If the project is public, this field contains a string representing the "
                "ID used for referencing the project in public URLs"
            )
        ),
    )
    medias = types.ListType(
        types.ModelType(Media),
        metadata=dict(description="A list of the media associated with a project"),
    )


class CaptionTrack(models.Model):
    language = types.StringType(
        metadata=dict(
            description="A 3 character language code as specified by ISO-639–2"
        )
    )
    text = types.StringType(
        metadata=dict(
            description="The text of the captions for the specified language in SRT format"
        )
    )
    english_name = types.StringType(
        metadata=dict(description="The English name of the language")
    )
    native_name = types.StringType(
        metadata=dict(description="The native name of the language")
    )
    is_draft = types.BooleanType(
        metadata=dict(description="Presumably for internal use only")
    )
