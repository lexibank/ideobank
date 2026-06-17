import pathlib
import dataclasses
from collections import defaultdict
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Lexeme, Concept
from lingpy import Wordlist


@dataclasses.dataclass
class CustomConcept(Concept):
    Spanish: Optional[str] = None
    Portuguese: Optional[str] = None
    Simplified: Optional[str] = None
    SemanticField: Optional[str] = None
    SensoryCategory: Optional[str] = None


@dataclasses.dataclass
class CustomLexeme(Lexeme):
    Reduplication: Optional[str] = None
    ReduplicationNotes: Optional[str] = None
    Page: Optional[str] = None


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "ideobank"
    writer_options = {"keep_languages": False, "keep_parameters": False}
    lexeme_class = CustomLexeme
    concept_class = CustomConcept

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = defaultdict()
        for concept in self.concepts:
            args.writer.add_concept(
                    ID=concept["ID"],
                    Name=concept["ENGLISH"],
                    Spanish=concept["SPANISH"],
                    Portuguese=concept["PORTUGUESE"],
                    Simplified=concept["SIMPLIFIED"],
                    SemanticField=concept["SEMANTIC FIELD"],
                    SensoryCategory=concept["SENSORY CATEGORY"],
                    Concepticon_ID='',
                    Concepticon_Gloss=''
            )

            if concept["ENGLISH"] == '':
                concepts[concept["SPANISH"]] = concept["ID"]
            else:
                concepts[concept["ENGLISH"]] = concept["ID"]

        args.log.info("added concepts")

        # add language
        languages = defaultdict()
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Language"],
                    Glottocode=language["Glottocode"]
                    )
            languages[language["Glottocode"]] = language["ID"]

        args.log.info("added languages")

        errors = set()
        wl = Wordlist(str(self.raw_dir.joinpath("raw.tsv")))

        # add data
        for (
            _,
            doculect,
            form,
            reduplication,
            reduplication_note,
            english,
            spanish,
            notes,
            source,
            page
        ) in pb(
            wl.iter_rows(
                "doculect",
                "form",
                "reduplication",
                "reduplication_notes",
                "concept",
                "significado_español",
                "notas",
                "fuente",
                "página"
            ),
            desc="cldfify"
        ):

            if doculect not in languages:
                errors.add(("doculect", doculect))
                print('Missing language:', doculect)

            else:
                args.writer.add_forms_from_value(
                    Language_ID=languages[doculect],
                    Parameter_ID=concepts[english] if english != '' else concepts[spanish],
                    Value=form,
                    Reduplication=reduplication,
                    ReduplicationNotes=reduplication_note,
                    Source=source,
                    Page=page,
                    # Segments=tokens,
                    Comment=notes,
                )
