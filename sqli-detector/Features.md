Feature selection is crucial in building effective SQL injection (SQLi) detection systems. Here's a list of some common features used in SQLi detection:

1. **SQL Keywords:** Presence of SQL keywords such as SELECT, INSERT, UPDATE, DELETE, etc., in the input query.

2. **Special Characters:** Presence of special characters like quotes (' or "), semicolons (;), and comments (-- or /* */) that could be indicative of SQL injection attempts.

3. **Length of Input:** Length of the input string, as SQL injection attacks often involve longer-than-usual input strings.

4. **Input Structure:** Structure of the input string, including the distribution and frequency of alphanumeric characters, digits, and special characters.

5. **Syntax Errors:** Detection of syntax errors or inconsistencies in the input query, which may indicate attempted SQL injection.

6. **HTTP Headers and Parameters:** Analysis of HTTP headers and parameters, such as Referer, User-Agent, and cookies, for anomalies or suspicious patterns.

7. **User Behavior:** Analysis of user behavior, such as unusual or unexpected sequences of requests, high frequency of requests, or attempts to access restricted resources.

8. **IP Reputation:** Evaluation of the reputation of the IP address from which the request originates, using threat intelligence feeds or reputation databases.

9. **Machine Learning Features:** Features extracted from input data for machine learning-based detection, such as n-grams, TF-IDF scores, or embeddings of input strings.

10. **HTTP Request Attributes:** Analysis of attributes of HTTP requests, including request method (GET, POST), URL structure, and query parameters.

11. **Response Content:** Inspection of response content for indications of SQL injection attempts, such as error messages returned by the database server.

12. **Behavioral Analysis:** Analysis of the behavior of the application or database server in response to input queries, such as timing differences or unusual resource consumption.

13. **Parameterized Queries Usage:** Detection of usage of parameterized queries or prepared statements, which are less susceptible to SQL injection.

14. **Normalization and Validation:** Application of normalization and validation techniques to input data, such as removing or escaping special characters, to prevent SQL injection.

15. **Historical Data Analysis:** Analysis of historical data or logs for patterns of SQL injection attempts or successful attacks.

These features can be combined and tailored to the specific requirements and characteristics of the application or system being protected against SQL injection attacks.