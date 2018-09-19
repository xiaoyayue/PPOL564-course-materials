def report_internals(obj,grab_attributes=False):
    '''
    Produce Markdown table of object attributes and methods.

    Arguments:
        - obj: python object
        - grab_attributes: boolean. Report dunder if True, else report methods.
        - threshold: number of lines to report given a method is wordy. Truncates the number of lines
    '''
    methods = dir(obj)


    if grab_attributes:
        type = "Attribute"
        attributes = [method for method in methods if "__" in method]
    else:
        type = "Method"
        attributes = [method for method in methods if "__" not in method]

    message = f"| {type}  | Description |\n|:---------:|:---------:|\n"
    for attr in attributes:
        doc = getattr(obj,attr).__doc__
        if doc is not None:
            doc = doc.split("\n\n")[0]
            doc = doc.replace("\n\n"," ").replace("\n"," ").strip()
            if grab_attributes:
                message += f"|**`{attr}`**| {doc}|\n"
            else:
                message += f"|**`.{attr}()`**| {doc}|\n"
    out_message = f"**<center>Methods in object type `{obj.__class__.__name__}`</center>**\n\n{message}"

    return(out_message)
