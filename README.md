[![Docker Image CI](https://github.com/dkruyt/minio-backup/actions/workflows/docker-image.yml/badge.svg)](https://github.com/dkruyt/minio-backup/actions/workflows/docker-image.yml)

# 📁 MinIO Backup Service 

This Dockerized Python project creates backups from a specified directory and uploads them to a MinIO or S3 bucket. The script logs each step of the process, including a progress update, to help track how the backup is proceeding. 

## 📘 Table of Contents

- [Installation](#💿-installation)
- [Configuration](#⚙️-configuration)
- [Usage](#🖥️-usage)
- [Running with Crontab](#📟-running-with-crontab)
- [Contribution](#🤝-contribution)
- [License](#📜-license)
  
## 💿 Installation

1. Clone the repository to your local machine.
2. Install Docker and Docker Compose, if they're not already.
3. Build the Docker image with the following command:
    ```bash
    docker-compose build
    ``` 

## ⚙️ Configuration 

Replace the following values in your `.env` file within the project root:

- **MINIO_URL**: URL of your MinIO server
- **MINIO_ACCESS_KEY**: Your MinIO server access key
- **MINIO_SECRET_KEY**: Your MinIO server secret key
- **MINIO_BUCKET**: The bucket in your MinIO server where the backups will be stored

The `.env` file should look like this:

```
MINIO_URL=<your-minio-url>
MINIO_ACCESS_KEY=<your-access-key>
MINIO_SECRET_KEY=<your-secret-key>
MINIO_BUCKET=<your-bucket-name>
```

## 🖥️ Usage 

1. Make sure to map the backup directory(`/opt` in the example) correctly in the Docker Compose file.
2. Run the Docker container via Docker Compose:

    ```bash
    docker-compose up
    ```

## 📟 Running with Crontab

For running this service periodically, you can leverage crontab.

1. Open the crontab editor with:

   ```
   crontab -e
   ```

2. Add the following line to run the script at your prefered time (this example runs it every day at 3 a.m.):

   ```
   0 3 * * * docker run --env-file=/path/to/your/.env -v /opt:/backup:ro ghcr.io/dkruyt/minio-backup/minio-backup:latest
   ```

   Be sure to replace `/path/to/your/.env` with the path to your .env file.

3. Save and close the file.

## 🤝 Contribution

1. Fork the project. 
2. Create a new branch for your feature (`git checkout -b feature/YourFeature`). 
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## 📜 License

This project is licensed under the terms of the General Public License v3.0 license.