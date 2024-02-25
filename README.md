# Project Title: Atlantic Warriors - Combating Plastic Pollution in Rivers

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

## Demo Video:
[Link to Demo Video](insert link here)

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
Please refer to the Read.md file in the GitHub repository for detailed information about the project setup, implementation, feedback, success metrics, and future steps.
