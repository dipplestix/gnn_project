import os
import pandas as pd
import xml.etree.ElementTree as ET

from tqdm import tqdm


def extract_title(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # Extract the title
    title_elem = root.find('.//tei:titleStmt/tei:title[@level="a"][@type="main"]', namespaces)
    title = title_elem.text if title_elem is not None and title_elem.text else "Title not found"

    return title


def extract_abstract(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # Extract the abstract
    abstract_elem = root.find('.//tei:div/tei:p', namespaces)
    abstract = abstract_elem.text if abstract_elem is not None else "Abstract not found"

    return abstract


def extract_introduction(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    
    bib_titles = {}
    # Iterate through all <biblStruct> elements and extract the title
    for bibl in root.findall('.//tei:biblStruct', namespaces):
        bib_id = bibl.get('{http://www.w3.org/XML/1998/namespace}id')
        
        # Find the main title within the <biblStruct>
        title_elem = bibl.find('.//tei:title[@level="a"][@type="main"]', namespaces)
        if title_elem is not None and title_elem.text:
            bib_titles[bib_id] = title_elem.text

    # Find the div with the head containing "Introduction" (case-insensitive)
    all_div = root.findall('.//tei:div', namespaces)
    for idx, div in enumerate(all_div):
        head_elem = div.find('tei:head', namespaces)
        paragraphs = []
        if head_elem is not None and head_elem.text and "introduction" in head_elem.text.lower():
    
            curr_div = all_div[idx]
            if "I." in head_elem.text:
                while head_elem is not None and "II." not in head_elem.text:
                    for ref in curr_div.findall('.//tei:ref', namespaces):
                        target = ref.get('target')  # Get the target, like "#b6"
                        if target and target.startswith('#'):
                            bib_id = target[1:]
                        if bib_id in bib_titles:
                            ref.text = f'({bib_titles[bib_id]})'
                            ref.tag = 'span'
                    content = ''.join(curr_div.itertext())
                    paragraphs.append(content)

                    idx += 1
                    curr_div = all_div[idx]
                    head_elem = curr_div.find('tei:head', namespaces)
            else:
                for ref in curr_div.findall('.//tei:ref', namespaces):
                    target = ref.get('target')  # Get the target, like "#b6"
                    if target and target.startswith('#'):
                        bib_id = target[1:]
                    if bib_id in bib_titles:
                        ref.text = f'({bib_titles[bib_id]})'
                        ref.tag = 'span'
                content = ''.join(curr_div.itertext())
                paragraphs.append(content)
            return ''.join(paragraphs)
    return "Introduction section not found"


def preprocess(file_path):
    title = extract_title(file_path)
    abs = extract_abstract(file_path)
    intro = extract_introduction(file_path)
    file = os.path.basename(file_path)
    file_name, extension = os.path.splitext(file)
    content = f"Title: {title}. Abstract: {abs}. Introduction: {intro}"
    return file_name, content


def main():
    root_path = './data/paper-xml'
    data = []
    for _f in tqdm(os.listdir(root_path)):
        file_path = os.path.join(root_path, _f)
        file_name, content = preprocess(file_path)
        data.append([file_name, content])

    df = pd.DataFrame(data, columns=['File Name', 'Content'])
    output_excel = './data/paper_pro.xlsx'
    df.to_excel(output_excel, index=False)


if __name__ == '__main__':
    main()