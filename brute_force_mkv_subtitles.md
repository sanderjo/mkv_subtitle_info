# Brute force analyse MKV for subtitles

```
$ cat 'something_dutch.mkv'  | strings | head -100 | grep -A2 -e S_TEXT
S_TEXT/UTF8"
nlSn
Dutch (forced)
S_TEXT/UTF8"
nlSn
Dutch (SDH)

```

```
$ cat 'vliegzak.mkv' | strings | head -100 | grep -A2 -e S_TEXT
S_TEXT/UTF8"
en-US
S_TEXT/UTF8"
en-USSn
SDHU
S_TEXT/UTF8"
ar-EGSn
Arabic
--
S_TEXT/UTF8"
cs-CZSn
Czech
S_TEXT/UTF8"
da-DKSn
Danish
S_TEXT/UTF8"
de-DESn
German
S_TEXT/UTF8"
el-GRSn
Modern Greek (1453-)
S_TEXT/UTF8"
es-419Sn
Spanish
S_TEXT/UTF8"
es-ESSn
Spanish
S_TEXT/UTF8"
fi-FISn
Finnish
S_TEXT/UTF8"
fil-PHSn
Filipino
S_TEXT/UTF8"
fr-FRSn
French
S_TEXT/UTF8"
he-ILSn
Hebrew
S_TEXT/UTF8"
hi-INSn
Hindi
S_TEXT/UTF8"
hu-HUSn
Hungarian
S_TEXT/UTF8"
id-IDSn
Indonesian
S_TEXT/UTF8"
it-ITSn
Italian
S_TEXT/UTF8"
ja-JPSn
Japanese
S_TEXT/UTF8"
ko-KRSn
Korean
S_TEXT/UTF8"
ms-MYSn
Malay (macrolanguage)
--
S_TEXT/UTF8"
nb-NOSn
Norwegian Bokm
S_TEXT/UTF8"
nl-NLSn
Dutch
S_TEXT/UTF8"
pl-PLSn
Polish
S_TEXT/UTF8"
pt-BRSn
Portuguese
S_TEXT/UTF8"
pt-PTSn
Portuguese
S_TEXT/UTF8"
ro-ROSn
Romanian
S_TEXT/UTF8"
ru-RUSn
Russian
S_TEXT/UTF8"
sv-SESn
Swedish
S_TEXT/UTF8"
ta-INSn
Tamil
S_TEXT/UTF8"
te-INSn
Telugu

```
