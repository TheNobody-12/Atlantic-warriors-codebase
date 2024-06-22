# Project Title: Atlantic Warriors - Combating Plastic Pollution in Rivers

## Demonstartion 
Here is a video that explains more about this project:

[![Watch the video](https://img.youtube.com/vi/jtcj3WGw5WI/0.jpg)](https://youtu.be/jtcj3WGw5WI?si=QtWc7lHMZapXku6t)

## Problem Statement:
Plastic pollution in rivers poses a significant threat to both natural ecosystems and human societies. As plastics accumulate in waterways, they degrade into microplastics, harming aquatic life and posing risks to human health. Traditional monitoring methods are often cumbersome and expensive, hindering effective solutions to address this urgent issue.

## United Nations' Sustainable Development Goals (SDGs) Alignment:
- Goal 14: Life Below Water
   - Target 14.1: Prevent and significantly reduce marine pollution, including plastic debris, originating from rivers.
- Goal 15: Life on Land
   - Target 15.1: Ensure the conservation, restoration, and sustainable use of terrestrial and inland freshwater ecosystems, including rivers, in line with international agreements.

## Solution Overview:
We, the Atlantic Warriors from PDEU, are leveraging cutting-edge technology to combat plastic pollution in rivers. Our solution involves:
- Utilizing AI-driven technology for real-time monitoring and analysis of river images to detect plastic debris.
- Providing insights to environmental communities for safeguarding aquatic ecosystems.

## Architecture Overview:
1. **Machine Learning Component:**
   - Utilizes machine learning techniques for detecting plastic pollution in drone images.
   - Trained using Google Colab Notebooks with GPU/TPU acceleration.
   - Integrates annotations from the Google Annotation Data Labeling service for accurate training data.

2. **Flask Backend:**
   - Provides the user interface for image uploads, object detection initiation, and result retrieval.
   - Stores detection results and metadata in Google Cloud SQL.
   - Connects to Google Cloud SQL using the Cloud SQL Connector for efficient data storage and retrieval.

3. **Google Cloud Storage Bucket:**
   - Stores detection results, including images with annotations.

4. **Cloud Run and Google Container Registry:**
   - Deploys Flask backend code in a containerized environment for scalability and reliability.

5. **Google .app Domain with Custom Domain Mapping:**
   - Hosts the Flask application, making it accessible over the internet with a secure, HTTPS-enabled domain.

6. **Google Annotation Data Labeling Service:**
   - Provides annotation capabilities for labeling images with plastic pollution instances.

## Technologies Used:
- Google Colab Notebooks
- Flask
- Google Cloud SQL
- Google Cloud Storage
- Cloud Run
- Google Container Registry
- Google .app Domain
- Google Annotation Data Labeling Service

## Feedback and Iteration:
We conducted user testing sessions and received feedback to improve our solution, including:
1. Streamlining the user interface.
2. Enhancing data visualizations.
3. Optimizing performance and reliability.

## Code Testing and Iteration:
One significant challenge we faced was deploying the codebase to a cloud server, which we addressed by:
1. Optimizing algorithms for faster processing.
2. Implementing parallelization and multithreading.
3. Setting up requirements and Dockerfile for containerization.
4. Connecting database and storage with the application.
5. Mapping a custom domain for hosting.

## Success Metrics:
We track the success of our solution by monitoring:
- Number of plastic pollution instances detected.
- Accuracy of detection results.
- User engagement metrics.
- Performance and uptime of the application.


## Future Steps:
1. Enhance data coverage.
2. Implement community engagement initiatives.
3. Develop a mobile application version.
4. Integrate with environmental monitoring networks.
5. Continuous improvement and innovation.

## Scalability:
Our solution's technical architecture supports scalability through:
- Cloud infrastructure.
- Microservices architecture.
- Load balancing.
- Caching and CDN integration.
- Horizontal and vertical scaling.

## Read.md File for GitHub Repository:
Please refer to the Read.md file in the GitHub repository for detailed information about the project setup, implementation, feedback, success metrics, future steps, and installation process.

## Installation Process
1. **Clone this repository:**
    ```bash
    git clone <repository-url>
    ```

2. **Install Python version 3.9 or higher:**
    Download and install Python from the [official website](https://www.python.org/).

3. **Install Virtual Environment using Pip in the command line:**
    ```bash
    pip install virtualenv
    ```

4. **Create a Virtual Environment in the command line:**
    ```bash
    python<version> -m venv <virtual-environment-name>
    ```

5. **Activate the Environment in the command line:**
    - For Windows:
        ```bash
        .\<virtual-environment-name>\Scripts\activate
        ```
    - For macOS/Linux:
        ```bash
        source <virtual-environment-name>/bin/activate
        ```

6. **Install all Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

7. **Run the code file using the following command:**
    ```bash
    python app.py
    ```


## License
```
MIT License

Copyright (c) 2024 SARTHAK KAPALIYA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
