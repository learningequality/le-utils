Release History
===============


0.1.15 Nov 28, 2018
-------------------
  - Added the following language codes:
   - ach = Acholi
   - fuv = Fulfulde Mbororo 
   - xog = Soga
   - tuv = Turkana
   - lwg = Oluwanga
   - nyn = Nyankore
   - myx = Masaaba



0.1.14 Nov 7, 2018
------------------
  - Duplicated python constants/ definitions as json files under resources/ (for easier integration with frontend)
  - Added tests to make sure python constants are in sync with json constants
  - Implemented first_native_name helper (used to set channel names in chefs)
  - Added list-like `convertible_formats` attribute for all presets
  - Added  `html5_dependency` and `video_dependency` presets
  - Updated constant mapping with epub -- The EPUB preset is used with document content type
  - Added the following language codes:
     - und = Undefined
     - mul = Multiple languages
     - arq = Algerian; Darja
     - lkt = Lakhota; Lakotiyapi; Teton
     - hdy = Hadiyya; Hadiya; Adea; Adiya; Hadia
     - sid = Sidamo; Sidaamu afii; Sidaama; Sidama
     - wal = Wolaytta; Borodda; Uba; Ometo


0.1.6 Mar 13, 2018
------------------
  - Added file format constants for ePub
  - Added RTL language lookup table in le_utils.constants.languages.RTL_LANG_CODES
  - Added the following language codes:
     - be-tarask = Belarusian
     - hrx = Hunsrik
     - lua = Luba-Kasai
     - pms = Piedmontese
     - sco = Scots
     - rue = Rusyn

0.1.5 Jan 11, 2018
------------------
  - Handle non-standard code `iw` for Hebrew used by YouTube API
  - Better classification of traditional and simplified Chinese scripts
  - Added basic README

0.1.4 Nov 22, 2017
------------------
  - Define constants for all file types
  - fix wrong default Spanish lookup by name
  - Added Sepedi and missing Tshivenda as discussed in previous PR

0.1.3 Oct 13, 2017
------------------
  - Implemented getlang_by_native_name for easier lookups

0.1.0 Aug 31, 2017
------------------
  - Language lookup helper functions
  - changed version numbering to use minor versions not patch

0.0.12 Aug 21, 2017
------------------
  - Added proquint

0.0.11 Aug 1, 2017
------------------
  - added language direction constants

0.0.10 Jul 27, 2017
------------------
  - added humanhash support

0.0.9rc24 May 17, 2017
------------------
  - changes to a few mimetypes


