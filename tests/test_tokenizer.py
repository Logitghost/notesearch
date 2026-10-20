"""SPEC for notesearch/tokenizer.py. These encode ONE reasonable set of choices.
If you decide differently (e.g. keep underscores), change the test AND write the reason in the README."""
from notesearch.tokenizer import Tokenizer


def test_basic_split_and_lowercase():
    assert Tokenizer(keep_compounds=False)("Error_Code v1.2 foo-bar") == ["error", "code", "v1", "2", "foo", "bar"]


def test_compounds_are_kept_as_extra_tokens():
    toks = Tokenizer(keep_compounds=True)("pin v1.2 please")
    assert "v1.2" in toks and "v1" in toks and "please" in toks


def test_stopword_switch():
    assert "the" not in Tokenizer(stopwords=True)("the cat")
    assert "the" in Tokenizer(stopwords=False)("the cat")


def test_stem_switch():
    assert Tokenizer(stem=True)("running cats") != ["running", "cats"]  # needs nltk or your own stemmer
    assert Tokenizer(stem=False)("running cats") == ["running", "cats"]


def test_config_roundtrip():
    t = Tokenizer(stopwords=True, stem=True, keep_compounds=False)
    assert Tokenizer.from_config(t.to_config()).to_config() == t.to_config()
