import re


def normalize_whitespace(input_text):
    output_text = re.sub(r"_", " ", input_text)
    output_text = re.sub(r"\s+", " ", input_text)
    output_text = re.sub(r"^\s", "", output_text)
    output_text = re.sub(r"\s$", "", output_text)
    return output_text


def normalize_title(title_original):

    title_normalized = title_original
    
    title_normalized = re.sub("&", " and ", title_normalized)
    # e.g. Texas A&M University
    
    title_normalized = re.sub("-", " ", title_normalized)
    # Lots of universities with multiple campuses do this - e.g. Westwood
    # College-Aurora

    title_normalized = re.sub(r"\bSt.", "Saint ", title_normalized)
    # Bethel Seminary St. Paul

    title_normalized = re.sub("/", " ", title_normalized)
    # Correctly named:
    #  Delaware Technical Community College Stanton/Wilmington
    #  New York City College of Technology/CUNY
    #  Penn Commercial Business/Technical School

    title_normalized = re.sub(",", " ", title_normalized)
    # Penn State Fayette, The Eberly Campus

    title_normalized = normalize_whitespace(title_normalized)

    return title_normalized
