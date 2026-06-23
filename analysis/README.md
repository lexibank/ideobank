# Accessing the data

## SQLite3

The easiest way to access any CLDF dataset is to convert the dataset into a sqlite3 database. You can do this through the `createdb` command from `pycldf`:

```shell
cldf createdb cldf/cldf-metadata.json ideobank.sqlite3
```

You can then easily access the data with sqlite queries.

## Spreadsheet tables

If you want to go the traditional way, you can convert the data into a single csv-file. However, this will make for a large file size and include many columns you might not be interested in. It also repeats much of the information.

To do this, you need to install `edictor3`:

```shell
pip install "pyedictor[lingpy]"
```

Now you can run the `wordlist` command and add all columns you want:

```shell
edictor wordlist --name=ideobank --addon="language_glottocode:glottocode","page:page","reduplication:reduplication","reduplucationnotes:reduplicationnotes","concept_spanish:spanish","concept_portuguese:portuguese","concept_simplified:simplified","concept_semanticfield:semanticfield","concept_sensorycategory:sensorycategory","concept_concepticon_gloss:concepticon_gloss","concept_concepticon_id:concepticon_id","source:source"
```

The output is the complete tsv-file `ideobank.tsv` with all the columns you selected.
