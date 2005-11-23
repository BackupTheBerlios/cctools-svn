
def validateTitle(title):
    """A title must be supplied for Works."""
    
    if not(title) or not(title.strip()):
        return "You must supply a title."
    else:
        return None
    
