Constants defined in le-utils
=============================


Content kinds (ContentNode subclasses)
--------------------------------------
Content items throughout the Kolibri ecosystem come in several kinds. The `kind`
attribute of each object can be one of ("topic", "video", "audio", "exercise"
"document", or "html5". See [constants/content_kinds.py](https://github.com/learningequality/le-utils/blob/master/le_utils/constants/content_kinds.py#L11-L17) for latest list.

The `kind` attribute identifies a subclass of the base content node class within
within the data model, which differs on Ricecooker, Studio, and Kolibri:
  - [ricecooker.classes.nodes.ContentNode](https://github.com/learningequality/ricecooker/blob/master/ricecooker/classes/nodes.py#L428-L506):
    in-memory content node used to store metadata needed to upload new content to Studio
  - [contentcuration.contentcuration.models.ContentNode](https://github.com/learningequality/studio/blob/develop/contentcuration/contentcuration/models.py#L775):
    node within one of the trees associated with a Studio channel.
  - [kolibri.core.content.models.ContentNode](https://github.com/learningequality/kolibri/blob/develop/kolibri/core/content/models.py#L175):
    node within tree for a particular version of a channel on Kolibri.

For details description of the common and different model attributes, available
on content nodes in each part of the platform see [this doc](https://docs.google.com/spreadsheets/d/181hSEwJ7yVmMh7LEwaHENqQetYSsbSDwybHTO_0zZM0/edit#gid=1640972430).




Format presets (ContentNode-File relation)
------------------------------------------
Every `ContentNode` is associated with one or more `File` objects and nature of
this association is represented though the `format_preset` attribute of the file.
The `format_preset` is the role the file is playing in the content node,
e.g., thumbnail, high resolution video, or low resolution video.
You can think of the different presets on a content node as "slots" to be filled
in with different files.

Represented redundantly as python string [constants/format_presets.py](https://github.com/learningequality/le-utils/blob/master/le_utils/constants/format_presets.py)
and json  [resources/presetlookup.json](https://github.com/learningequality/le-utils/blob/master/le_utils/resources/presetlookup.json).



File formats (extension)
------------------------
This is the low-level constant that represents what type of file and is essentially
synonymous with the file extension.
See [file_formats.py](https://github.com/learningequality/le-utils/blob/master/le_utils/constants/file_formats.py) and [resourcces/formatlookup.json](https://github.com/nucleogenesis/le-utils/blob/master/le_utils/resources/formatlookup.json).





File types (ricecooker.files.File subclasses)
---------------------------------------------
Used on Ricecooker to provide a "constants" that represnts what type of file
you are dealing with.





Roles
-----
  - 'learner' (default)
  - 'coach' == only visible to teachers


