from redactor import Redactor

def test_redact_names():
    redactor = Redactor()
    doc = redactor.nlp("Meg Vai went to the store.")
    redacted_doc = redactor.redact_names(doc)
    assert "Meg" not in redacted_doc.text
    assert "Vai" not in redacted_doc.text
    assert "went to the store" in redacted_doc.text