
def validateTitle(title):
    """A title must be supplied for Works."""
    
    if not(title) or not(title.strip()):
        return _("You must supply a title.")
    else:
        return None
    
def validateDescription(description):
    """The Internet Archive requires that a description of 5 words is
    provided; we just split on whitespace to determine words."""
    
    if not(description) or len(description.split()) < 5:
        return _("You must supply a description of at least 5 words.")


def validateWorkFormat(format):
    """A work format must be selected."""

    if not(format):
        return "You must select a work format."

