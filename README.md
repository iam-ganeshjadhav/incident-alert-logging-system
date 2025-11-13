# 🚨 Incident Alert & Logging System

A lightweight, serverless incident-logging system that captures Jenkins build failures and stores them in DynamoDB using an AWS Lambda endpoint.  
This project demonstrates a clean **CI/CD → Serverless → NoSQL** workflow without unnecessary services.

---

## 📌 Project Status

**Status:** ✔️ Active & Working  
This project is fully functional and ready for deployment.  
Additional enhancements like SNS notifications or dashboard integration can be added anytime.

---

## 📌 Overview

This project automatically logs Jenkins build failures into DynamoDB through an **API Gateway → Lambda** workflow.  
Every time a Jenkins pipeline fails, it sends a **POST request** containing the incident details.  
The Lambda function processes the data and writes a structured record to DynamoDB.


## 🏗️ Architecture




## 🧰 Services Used

| Service     | Purpose                                |
|-------------|----------------------------------------|
| **Jenkins** | Detect build failure & send incident data |
| **API Gateway** | Receives webhook from Jenkins |
| **Lambda**  | Processes incident & writes to DynamoDB |
| **DynamoDB** | Stores structured incident logs |



## 🎯 Features

✔ Automatically logs Jenkins build failures  
✔ Stores structured incident history  
✔ Clean DynamoDB schema  
✔ Simple HTTP-based integration  
✔ Optional email/SNS notifications  
✔ CI/CD friendly architecture  


## 🛠️ Setup Instructions

### 1️⃣ Create the DynamoDB Table

1. Open **AWS DynamoDB** → Click **Create Table**
2. Use the following configuration:

   - **Table Name:** `IncidentLogs`  
   - **Partition Key:** `incident_id` (String)

3. Click **Create**

## 🗄️ DynamoDB Table Structure

| Attribute       | Type   | Description                         |
|-----------------|--------|-------------------------------------|
| **incident_id** | String | Unique ID for each incident         |
| **build_name**  | String | Jenkins job name                    |
| **status**      | String | FAILED / SUCCESS (usually FAILED)   |
| **error_message** | String | Short description of failure      |
| **timestamp**   | String | UTC timestamp                       |

### 2️⃣ Create the Lambda Function

1. Go to **AWS Lambda** → Click **Create function**
2. Configure the function:
   - **Runtime:** Python 3.12  
   - **Name:** `incidentLoggerLambda`
3. Attach IAM policy:
   - **AmazonDynamoDBFullAccess**

**Lambda Code**
```bash
import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('IncidentLogs')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        build_name = body.get('build_name', 'unknown')
        status = body.get('status', 'FAILED')
        error_message = body.get('error_message', 'N/A')

        table.put_item(
            Item={
                'incident_id': str(uuid.uuid4()),
                'build_name': build_name,
                'status': status,
                'error_message': error_message,
                'timestamp': datetime.utcnow().isoformat()
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Incident logged successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```
### 3️⃣ Create the API Gateway Endpoint

1. Open **API Gateway** → Click **Create HTTP API**
2. Integrate the API with your Lambda function:
   - **incidentLoggerLambda**
3. Deploy the API
4. Copy the **Invoke URL**, for example:

```
https://abcd1234.execute-api.ap-south-1.amazonaws.com/log
```

### 4️⃣ Configure Jenkins

#### Install AWS CLI

```
sudo apt update
sudo apt install awscli -y
```

#### Configure AWS Credentials

```
aws configure
```
### 5️⃣ Jenkins Pipeline (Jenkinsfile)

Create a `Jenkinsfile` in your repository:

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building project...'
                sh 'exit 1'  // simulate failure
            }
        }
    }

    post {
        failure {
            script {
                def incident = [
                    build_name: env.JOB_NAME,
                    status: "FAILED",
                    error_message: currentBuild.description ?: "Build failed"
                ]
                def payload = groovy.json.JsonOutput.toJson(incident)

                sh """
                curl -X POST \
                -H "Content-Type: application/json" \
                -d '${payload}' \
                https://abcd1234.execute-api.ap-south-1.amazonaws.com/log
                """
            }
        }
    }
}
```
## 📸 Screenshots (Add When Running)

### 🗄️ DynamoDB Entry Sample

| Field          | Example Value              | Screenshot |
|----------------|----------------------------|------------|
| **incident_id** | f03a-44cc-91ab-1312        | *(add image)* |
| **build_name**  | MyPipeline_main            | *(add image)* |
| **status**      | FAILED                     | *(add image)* |
| **error_message** | Unit tests failed        | *(add image)* |
| **timestamp**   | 2025-11-12T16:30:45Z       | *(add image)* |

> To insert screenshots later, replace ***(add image)*** with:  
> `![screenshot](images/filename.png)`  


## 📁 Project Structure

```
incident-alert-logging-system/
│
├── README.md
├── Jenkinsfile
└── lambda/
    └── lambda_function.py
```


  ## 🧪 Testing the Project

1. Run the Jenkins pipeline  
2. Make it fail (use `exit 1`)  
3. Open **DynamoDB** → Check for a new incident entry  
4. Verify that the JSON data is stored correctly  

---

## 🏁 Conclusion

This project demonstrates how Jenkins can integrate with AWS serverless services to build a real-time incident logging system.  
It is **lightweight, scalable, cost-efficient**, and ideal for DevOps automation workflows.  

You can extend it further with:  

- Dashboards  
- SNS/Email notifications  
- Multi-environment support  

---

## 👨‍💻 Author

**Ganesh Jadhav**  
DevOps & Cloud Engineer  
**GitHub:**  https://github.com/iam-ganeshjadhav/incident-alert-logging-system.git  
**LinkedIn:** https://www.linkedin.com/in/ganesh-jadhav-30813a267/