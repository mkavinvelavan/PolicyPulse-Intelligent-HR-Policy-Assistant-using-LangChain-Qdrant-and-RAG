📁 Policies Folder

This folder is intentionally empty in the public repository.

Your actual HR policy PDFs are not included because they contain confidential company information.
However, when running the project locally, you must place all your policy PDF files inside this directory.
---------------------------------------------------------------------------------------------------------
📌 What This Folder Is Used For

The ingestion script:

python app/ingest_pdfs.py


automatically reads all PDFs from this /policies directory and converts them into vector embeddings stored in Qdrant.
---------------------------------------------------------------------------------------------------------
📝 How to Use

Place your HR policy PDF files in this folder.

Ensure all files are in .pdf format.

Run the ingestion script:

python app/ingest_pdfs.py


The system will split, embed, and upload all policy data into the Qdrant vector database.
---------------------------------------------------------------------------------------------------------
🔒 Why PDFs Are Not Included in GitHub?

They contain internal HR policy details

They may be copyrighted or sensitive

Best practice: never upload internal company documents into public repos

Instead, you must keep your own policy PDFs locally when running the system.

📂 Expected Folder Structure
policies/
│
├── LeavePolicy.pdf
├── WorkFromHomePolicy.pdf
├── ITSecurityPolicy.pdf
├── AttendancePolicy.pdf
└── (Your other documents...)
---------------------------------------------------------------------------------------------------------
📌 Note for Users

If you clone this repository, the /policies folder will be empty.
Please add your own PDF files manually before running the ingestion pipeline.