# Abstract:
The Information Retrieval System (IRS) is a Python-based application designed to facilitate the retrieval of relevant information from web documents.

# Overview:
The IRS project aims to create a robust system for crawling web documents with a max depth and max no of pages, constructing an inverted index using TF-ID and cosine similarity, and processing user queries to retrieve relevant information using top-k retrievals.

# Design:
The system's design encompasses a range of capabilities, including web crawling utilizing Scrapy, document indexing, query processing, and search result presentation. It is modularized into three parts, each responsible for generating intermediate files for subsequent subsystems to utilize and ultimately generate results. The system is implemented in Python, leveraging powerful libraries such as Scrapy, Scikit-learn, and Flask for web crawling, indexing, and query processing.

# Architecture:
The architecture of the IRS is built around three primary components: the crawler, indexer, and processor. These components work together to perform specific tasks, including crawling web documents and storing them into a pickle file, constructing an inverted index pickle file using these documents, and processing user queries. The system's design emphasizes well-defined interfaces between components, which promotes modular development and facilitates extensibility.

# Operation:
To operate the IRS, follow these steps:

1. **Installation**:
   - Ensure Python 3.10+ or higher is installed on your system.
   - Install the required dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

2. **Running the System**:
   - Start with the crawler module:
     ```bash
     scrapy runspider crawler.py -a start_url=https://www.iit.edu/ -a max_depth=3 -a max_pages=500
     ```
   - Next, run the indexer module to construct the inverted index:
     ```bash
     python indexer.py
     ```
   - Finally, execute the processor module to start the flask app handle user queries:
     ```bash
     python processor.py
     ```
   - Hit the api, to process your query to get JSON response:
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"query": "<Your Query>", "top_k": <TOP K NUMBER>}' http://127.0.0.1:50000/process_query
     ```

By following these steps, you can effectively operate the IRS, from crawling web documents to processing user queries.

# Conclusion:
The Information Retrieval System demonstrates success in efficiently retrieving relevant information from web documents. However, challenges such as scalability and handling of diverse document formats should be addressed in future iterations. Overall, the system provides a valuable tool for information retrieval tasks.

# Data Sources:
Data for the IRS is sourced from web documents accessible via URLs provided to the crawler module. No specific downloads or access information are required, as the system dynamically retrieves documents from the web.
Please make sure of the scrapping policies before running the crawler.

# Test Cases:
The IRS is equipped with a suite of test cases to ensure functionality and robustness. Test cases cover various scenarios, including crawling, indexing, query processing, and search result accuracy. Test coverage is comprehensive, ensuring the reliability of the system.

# Source Code:
The source code for the Information Retrieval System is available in the following files:
- crawler.py
- indexer.py
- processor.py

The code is well-documented and follows best practices for readability and maintainability. Dependencies on open-source libraries such as Scrapy, Scikit-learn, and Flask are clearly stated in the documentation.

# Bibliography:
References to relevant literature, libraries, and frameworks used in the development of the Information Retrieval System are provided within the code comments and documentation. Citations follow the Chicago style for consistency and clarity.

Stack Overflow. Accessed April 21, 2024.  
https://stackoverflow.com/questions/24253117/dynamic-start-urls-value. 
  
OpenAI. "OpenAI Chat." Accessed April 21, 2024.  
https://chat.openai.com.
  
Python Software Foundation. "re — Regular expression operations." Accessed April 21, 2024.   
https://docs.python.org/3/library/re.html.

scikit-learn developers. "scikit-learn: Machine Learning in Python." Accessed April 21, 2024. 
https://scikit-learn.org.

Pallets Projects. "Flask 3.0.x documentation." Accessed April 21, 2024. 
https://flask.palletsprojects.com/en/3.0.x/.
