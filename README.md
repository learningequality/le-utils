LE Utils
========
Utilities and constants shared across Ricecooker, Kolibri, and Kolibri Studio.



Languages
---------
The file [le_utils/constants/languages.py](./le_utils/constants/languages.py) and
the lookup table in [le_utils/resources/languagelookup.json](./le_utils/resources/languagelookup.json)
define the internal representation for languages codes used by Ricecooker, Kolibri,
and Kolibri Studio to identify educational content in different languages.

The internal representation uses a mixture of two-letter codes (e.g. `en`),
two-letter-and-country code (e.g. `pt-BR` for Brazilian Portuguese),
and three-letter codes (e.g., `zul` for Zulu).

In order to make sure you have the correct language code when interfacing with
the Kolibri ecosystem (e.g. when uploading new content to Kolibri Studio), you
must lookup the language object using the helper method `getlang`:

```
>>> from le_utils.constants.languages import getlang
>>> language_obj = getlang('en')       # lookup language using language code
>>> language_obj
Language(native_name='English', primary_code='en', subcode=None, name='English', ka_name=None)
```
The function `getlang` will return `None` if the lookup fails. In such cases, you
can try lookup by name or lookup by alpha2 code (ISO_639-1) methods defined below.

Once you've successfully looked up the language object, you can obtain the internal
representation language code from the language object's `code` attribute:
```
>>> language_obj.code
'en'
```
The Ricecooker API expects these internal representation language codes will be
supplied for all `language` attributes (channel language, node language, and files language).


### More lookup helper methods
The helper method `getlang_by_name` allows you to lookup a language by name:
```
>>> from le_utils.constants.languages import getlang_by_name
>>> language_obj = getlang_by_name('English')  # lookup language by name
>>> language_obj
Language(native_name='English', primary_code='en', subcode=None, name='English', ka_name=None)
```

The module `le_utils.constants.languages` defines two other language lookup methods:
  - Use `getlang_by_native_name` for lookup up names by native language name,
    e.g., you look for 'Français' to find French.
 -  Use `getlang_by_alpha2` to perform lookups using the standard two-letter codes
    defined in [ISO_639-1](https://en.wikipedia.org/wiki/ISO_639-1) that are
    supported by the `pycountries` library.


#### Useful links

The following websites are usful for researching language codes:

  - https://www.ethnologue.com/
  - https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes



Licenses
--------
All content nodes within Kolibri and Kolibri Studio must have a license. The file
[le_utils/constants/licenses.py](./le_utils/constants/licenses.py) contains the
constants used to identify the license types. These constants are meant to be
used in conjunction with the helper method `ricecooker.classes.licenses.get_license`
to create `Licence` objects.

To initialize a license object, you must specify the license type and the
`copyright_holder` (str) which identifies a person or an organization. For example:
```
from ricecooker.classes.licenses import get_license
from le_utils.constants import licenses
license = get_license(licenses.CC_BY, copyright_holder="Khan Academy")
```

Note: The `copyright_holder` field is required for all License types except for
the public domain license for which `copyright_holder` can be None.




Content kinds (ContentNode subclasses)
--------------------------------------
Content items throughout the Kolibri ecosystem come in several kinds. The `kind`
attribute of each object can be one of ("topic", "video", "audio", "exercise"
"document", or "html5".
See [constants/content_kinds.py](https://github.com/learningequality/le-utils/blob/master/le_utils/constants/content_kinds.py#L11-L17) for latest list.

The currently supported content kinds are:
  - Topic node (folder)
  - Video content nodes backed by a video files and subtitles
  - Audio content nodes backed by an audio files
  - Document content nodes backed by a document files (PDF or ePub)
  - HTML5 app content nodes backed by a HTML5 zip files
  - Exercise content nodes

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
and as json [resources/presetlookup.json](https://github.com/learningequality/le-utils/blob/master/le_utils/resources/presetlookup.json).



File formats (extensions)
-------------------------
This is the low-level constant that represents what type of file and is essentially
synonymous with the file extension.
See [file_formats.py](https://github.com/learningequality/le-utils/blob/master/le_utils/constants/file_formats.py) and [resourcces/formatlookup.json](https://github.com/nucleogenesis/le-utils/blob/master/le_utils/resources/formatlookup.json).


The figure below illustrates the structure between content nodes, files, and format presets.

![Illustration of the relationships between content kinds, files, and format presets](docs/img/le-utils_constants_and_mapping.png)




File types (ricecooker.files.File subclasses)
---------------------------------------------
Used on Ricecooker to provide a "constants" that represnts what type of file
you are dealing with.






Exercises
---------
The file [le_utils/constants/exercises.py](./le_utils/constants/exercises.py)
contains identifiers for different question types and mastery models.



Proquint Channel Tokens
-----------------------
The file [le_utils/proquint.py](./le_utils/proquint.py) contains helper methods
for generating proquint identifiers for content channels. These are short strings
that are easy to enter on devices without a full keyboard, e.g. `sutul-hakuh`.



Roles
-----
  - `learner` (default)
  - `coach` == only visible to teachers



