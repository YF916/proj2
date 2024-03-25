## COMS E6111-Advanced Database Systems - Project 2

### **Name and Columbia UNI:**
- Shiying Chen: sc5299
- Yifan Li: yl5337

### **Files Submitted:**
- README.md
- README.pdf
- transcript_spanbert.pdf
- transcript_gemini.pdf
- main.py

### **How to run the program:**
1. Navigate to the folder containing `main.py`
2. Run `python3 project2.py [-spanbert|-gemini] <google api key> <google engine id> <google gemini api key> <r> <t> <q> <k>`

### **Internal Design Description:**
This project is designed to extract relationships from web pages using either the SpanBERT model or a Gemini-based approach. Below is an overview of the project's internal design and the external libraries it relies on:

1. **Parameter Initialization (`initialize_parameters`)**: This function is responsible for parsing and validating the input arguments provided to the script. It ensures that the correct number of arguments are passed and initializes variables that dictate the behavior of the script, such as the model to use (SpanBERT or Gemini), API keys, and other relevant parameters.

2. **Google Custom Search (`google_search`)**: This function constructs a URL for querying the Google Custom Search JSON API with the provided search query and parameters. It then sends a request to the API and returns the JSON response, which contains the search results.

3. **Web Page Fetching (`fetch_webpage_text`)**: Given a URL, this function fetches the content of the web page, extracts text using BeautifulSoup (for parsing HTML and XML documents), and handles any exceptions that occur during the request.

4. **Relation Extraction**: This functionality is divided into two main paths, depending on the model selected (`-spanbert` or `-gemini`):
   - **For SpanBERT (`process_spanbert`)**: This path involves creating candidate entity pairs from the text and using the SpanBERT model to predict the relationship between these entities based on the specified type.
   - **For Gemini (`process_gemini_option`)**: This path involves formulating prompts for the Gemini model based on sentences that contain potential relationship candidates, then parsing and extracting the relationships from the model's response.

5. **Seed Query Update (`update_seed_query`)**: This function is designed to modify the seed query used for the Google Custom Search based on the relationships extracted so far. This iterative refinement process aims to discover new and relevant content as the script progresses.

6. **Main Workflow (`main`)**: Orchestrates the entire process, from initializing parameters to conducting searches, fetching web pages, extracting relationships, and updating the seed query as necessary. It also handles output formatting and logs progress to the console.

### External Libraries:

- **requests**: Used for making HTTP requests to fetch web pages and to interact with the Google Custom Search API.
- **BeautifulSoup**: Utilized for parsing HTML content of web pages to extract text.
- **spacy**: A natural language processing (NLP) library used for sentence segmentation and named entity recognition, which are critical for identifying candidate sentences and entities for relationship extraction.
- **genai**: This library appears to be a fictional placeholder for the Gemini model's API interactions. In a real project, this would correspond to a library or API client that allows interfacing with a language model or an NLP service for generating text completions or predictions.
- **re**: Used for parsing the structured output from the Gemini model's text completions.

### **Step 3 Description:**

This step is broken down into several key activities, each leveraging specific libraries and methodologies:

#### 1. Web Page Retrieval and Text Extraction

1. **Checking for Unseen URLs**: The script maintains a set of URLs that have already been processed (`seen_pages`). For each URL fetched from the Google Custom Search results, it checks if the URL is in this set. If the URL is new, it proceeds with the retrieval; otherwise, it skips to the next URL.

2. **Fetching Web Page Content**: For each new URL, the script uses the `requests` library to make an HTTP GET request. If the request fails (due to timeouts or other exceptions), the script catches the exception and moves on to the next URL without terminating the program.

3. **Extracting Text with BeautifulSoup**: Upon successfully retrieving the web page content, the script uses BeautifulSoup to parse the HTML and extract the plain text from it. BeautifulSoup provides a convenient way to navigate and manipulate the HTML tree, allowing the script to isolate the text content from the markup.

4. **Text Truncation**: To manage processing efficiency, the script checks the length of the extracted text. If the text exceeds 10,000 characters, it is truncated to the first 10,000 characters. This limit ensures that the subsequent processing steps remain computationally manageable.

#### 2. Sentence Segmentation and Named Entity Recognition

1. **Sentence Segmentation with spaCy**: The extracted and possibly truncated text is then processed with the spaCy NLP library. spaCy is used to segment the text into individual sentences, which is a necessary step for analyzing the text at the sentence level, as relationships are typically expressed within single sentences.

2. **Named Entity Recognition (NER)**: For each sentence, spaCy's NER capabilities are utilized to identify and label entities with specific types such as PERSON, ORGANIZATION, etc. These entities are crucial for relation extraction, as the project focuses on relationships involving specific types of entities.

#### 3. Relation Extraction

- **For SpanBERT**: 
  1. **Candidate Entity Pairs**: Based on the entities recognized in each sentence, the script generates candidate pairs of entities that could potentially express the target relationship (specified by the input parameter `r`).
  2. **Relation Prediction with SpanBERT**: Each candidate pair, along with the sentence context, is inputted into SpanBERT, which predicts the type of relationship (if any) between the entities. 
  3. **Filtering and Storing Results**: Only the relations that match the target type and meet the confidence threshold (`t`) are added to the set of extracted relations (`X`). The confidence score for each extracted relation is a crucial parameter for filtering.

- **For Gemini**: 
  1. **Using Prompts for Gemini**: The sentences identified to contain potential relation candidates are formulated into prompts that are suitable for the Gemini model. These prompts include context about the relationship type and the specific entities involved.
  2. **Extraction with Gemini**: The prompts are sent to the Gemini API, and the responses are parsed to extract the specified relationships. 
  3. **Storing Results**: Since Gemini does not provide confidence scores, all extracted relations are added to the set `X` with a hardcoded confidence value of 1.0.

#### 4. Integration into the Workflow

This step is seamlessly integrated into the main workflow of the script. It iterates over the search results, processes each URL according to the steps outlined above, and accumulates the extracted relationships. The iterative approach, combined with the ability to refine the search query based on the results, allows the script to dynamically explore web content and extract relevant information efficiently.

### **Google Custom Search Engine JSON API Key:**

AIzaSyBOhMwSA8gL9naDgUfz3NlnFEFmXPfbzgM

### **Engine ID:**

8567760ab337a4886
