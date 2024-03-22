# Required imports
import requests
from bs4 import BeautifulSoup
import spacy
from googleapiclient.discovery import build
import os
# Load pre-trained SpanBERT model
from SpanBERT.spanbert import SpanBERT
from SpanBERT.spacy_help_functions import extract_relations
from bs4 import BeautifulSoup
import requests
import spacy
from SpanBERT.spanbert import SpanBERT
from SpanBERT.spacy_help_functions import get_entities, create_entity_pairs
# Add any other imports you might need

def google_search(query):
    # API key and search engine ID
    service = build("customsearch", "v1", developerKey="AIzaSyBOhMwSA8gL9naDgUfz3NlnFEFmXPfbzgM")
    res = service.cse().list(q=' '.join(query), cx='8567760ab337a4886').execute()
    return res['items']

# results = google_search('bill gates microsoft')

def get_clean_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.get_text()
    text = text[:10000]
    # Process and clean the text as needed
    return text

def get_relations(raw_text):
    # raw_text = "Zuckerberg attended Harvard University, where he launched the Facebook social networking service from his dormitory room on February 4, 2004, with college roommates Eduardo Saverin, Andrew McCollum, Dustin Moskovitz, and Chris Hughes. Bill Gates stepped down as chairman of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella. "

    # TODO: filter entities of interest based on target relation
    entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]

    # Load spacy model
    nlp = spacy.load("en_core_web_lg")

    # Load pre-trained SpanBERT model
    spanbert = SpanBERT("./pretrained_spanbert")

    # Apply spacy model to raw text (to split to sentences, tokenize, extract entities etc.)
    doc = nlp(raw_text)

    for sentence in doc.sents:
        print("\n\nProcessing entence: {}".format(sentence))
        print("Tokenized sentence: {}".format([token.text for token in sentence]))
        ents = get_entities(sentence, entities_of_interest)
        print("spaCy extracted entities: {}".format(ents))

        # create entity pairs
        candidate_pairs = []
        sentence_entity_pairs = create_entity_pairs(sentence, entities_of_interest)
        for ep in sentence_entity_pairs:
            # TODO: keep subject-object pairs of the right type for the target relation (e.g., Person:Organization for the "Work_For" relation)
            candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
            candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject

        # Classify Relations for all Candidate Entity Pairs using SpanBERT
        candidate_pairs = [p for p in candidate_pairs if
                           not p["subj"][1] in ["DATE", "LOCATION"]]  # ignore subject entities with date/location type
        print("Candidate entity pairs:")
        for p in candidate_pairs:
            print("Subject: {}\tObject: {}".format(p["subj"][0:2], p["obj"][0:2]))
        print("Applying SpanBERT for each of the {} candidate pairs. This should take some time...".format(
            len(candidate_pairs)))

        if len(candidate_pairs) == 0:
            continue

        relation_preds = spanbert.predict(candidate_pairs)  # get predictions: list of (relation, confidence) pairs

        # Print Extracted Relations
        print("\nExtracted relations:")
        for ex, pred in list(zip(candidate_pairs, relation_preds)):
            print("\tSubject: {}\tObject: {}\tRelation: {}\tConfidence: {:.2f}".format(ex["subj"][0], ex["obj"][0], pred[0],
                                                                                       pred[1]))

            # TODO: focus on target relations
            # '1':"per:schools_attended"
            # '2':"per:employee_of"
            # '3':"per:cities_of_residence"
            # '4':"org:top_members/employees"

if __name__ == "__main__":

    search_results = google_search("bill gates microsoft")

    for i, result in enumerate(search_results):
        print(f"Result {i + 1}:")
        relations = get_relations(result)
