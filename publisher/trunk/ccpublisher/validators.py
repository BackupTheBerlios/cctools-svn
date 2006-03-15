
def validateTitle(title):
    """A title must be supplied for Works."""
    
    if not(title) or not(title.strip()):
        return "You must supply a title."
    else:
        return None
    
def validateDescription(description):
    """The Internet Archive requires that a description of 5 words is
    provided; we just split on whitespace to determine words."""
    
    if not(description) or len(description.split()) < 5:
        return "You must supply a description of at least 5 words."

