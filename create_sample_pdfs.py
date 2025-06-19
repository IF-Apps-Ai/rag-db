#!/usr/bin/env python3
"""
Script untuk membuat file PDF contoh untuk testing RAG system
"""
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_sample_pdf_simple(filename, title, content):
    """
    Membuat file PDF sederhana menggunakan canvas
    """
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, title)
        
        # Content
        c.setFont("Helvetica", 12)
        y_position = height - 100
        
        # Split content into lines
        lines = content.split('\n')
        for line in lines:
            if y_position < 50:  # New page if needed
                c.showPage()
                y_position = height - 50
                c.setFont("Helvetica", 12)
            
            if line.strip():
                # Wrap long lines
                max_width = 500
                words = line.split(' ')
                current_line = ""
                
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if c.stringWidth(test_line, "Helvetica", 12) < max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            c.drawString(50, y_position, current_line)
                            y_position -= 15
                        current_line = word
                
                if current_line:
                    c.drawString(50, y_position, current_line)
                    y_position -= 15
            else:
                y_position -= 10  # Empty line spacing
        
        c.save()
        print(f"✅ Created: {filename}")
        
    except Exception as e:
        print(f"❌ Error creating PDF {filename}: {e}")

def create_sample_pdfs():
    """
    Membuat beberapa file PDF contoh untuk testing
    """
    # Create pdf_documents folder
    pdf_folder = "pdf_documents"
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        print(f"📁 Created folder: {pdf_folder}")
    
    # Sample PDF 1: Python Programming Guide
    python_content = """Python adalah bahasa pemrograman tingkat tinggi yang mudah dipelajari dan powerful.
Python mendukung multiple programming paradigms, termasuk procedural, object-oriented, dan functional programming.

Fitur-fitur utama Python:
- Syntax yang sederhana dan mudah dibaca
- Interpreted language
- Dynamic typing
- Extensive standard library
- Large ecosystem of third-party packages

Python sangat populer untuk:
- Web development (Django, Flask)
- Data science dan machine learning
- Automation dan scripting
- Desktop applications
- Scientific computing

Contoh kode Python sederhana:
print("Hello, World!")

for i in range(5):
    print(f"Number: {i}")

Python memiliki philosophy "The Zen of Python" yang menekankan pada code readability dan simplicity.
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.

Python juga mendukung berbagai paradigma pemrograman:
1. Procedural Programming
2. Object-Oriented Programming
3. Functional Programming

Untuk memulai dengan Python, Anda perlu menginstall Python dari python.org dan memilih text editor atau IDE favorit seperti VSCode, PyCharm, atau Sublime Text."""
    
    create_sample_pdf_simple(
        os.path.join(pdf_folder, "python_guide.pdf"),
        "Python Programming Guide",
        python_content
    )
    
    # Sample PDF 2: Machine Learning Basics
    ml_content = """Machine Learning adalah subset dari Artificial Intelligence yang memungkinkan komputer untuk belajar tanpa explicitly programmed.

Jenis-jenis Machine Learning:

1. Supervised Learning
- Menggunakan labeled data untuk training
- Contoh: Classification, Regression
- Algoritma: Linear Regression, Decision Trees, Random Forest, SVM

2. Unsupervised Learning
- Menggunakan unlabeled data
- Contoh: Clustering, Dimensionality Reduction
- Algoritma: K-Means, PCA, Hierarchical Clustering

3. Reinforcement Learning
- Learning through interaction dengan environment
- Reward-based learning
- Contoh: Game playing, Robot control

Popular ML Libraries:
- Scikit-learn: General-purpose ML library
- TensorFlow: Deep learning framework by Google
- PyTorch: Deep learning framework by Facebook
- Pandas: Data manipulation and analysis
- NumPy: Numerical computing

Machine Learning Pipeline:
1. Data Collection
2. Data Preprocessing
3. Feature Engineering
4. Model Selection
5. Training
6. Evaluation
7. Deployment

Tahapan dalam ML Project:
- Problem Definition: Menentukan masalah yang ingin diselesaikan
- Data Collection: Mengumpulkan data yang relevan
- Data Exploration: Memahami karakteristik data
- Data Preprocessing: Membersihkan dan mempersiapkan data
- Feature Engineering: Membuat fitur yang berguna untuk model
- Model Selection: Memilih algoritma yang tepat
- Training: Melatih model dengan data training
- Validation: Menguji performa model
- Deployment: Menerapkan model ke production
- Monitoring: Memantau performa model di production"""
    
    create_sample_pdf_simple(
        os.path.join(pdf_folder, "machine_learning_basics.pdf"),
        "Machine Learning Basics",
        ml_content
    )
    
    # Sample PDF 3: Database Fundamentals
    db_content = """Database adalah kumpulan data yang terorganisir dan dapat diakses secara elektronik.

Jenis-jenis Database:

1. Relational Database (SQL)
- Menggunakan tabel dengan rows dan columns
- ACID properties (Atomicity, Consistency, Isolation, Durability)
- Contoh: MySQL, PostgreSQL, SQLite, Oracle

2. NoSQL Database
- Document-based: MongoDB, CouchDB
- Key-value: Redis, DynamoDB
- Column-family: Cassandra, HBase
- Graph: Neo4j, Amazon Neptune

Database Operations (CRUD):
- Create: Menambahkan data baru
- Read: Membaca atau mengambil data
- Update: Mengubah data yang sudah ada
- Delete: Menghapus data

SQL (Structured Query Language):
- DDL (Data Definition Language): CREATE, ALTER, DROP
- DML (Data Manipulation Language): INSERT, UPDATE, DELETE
- DQL (Data Query Language): SELECT
- DCL (Data Control Language): GRANT, REVOKE

Normalization:
- 1NF (First Normal Form)
- 2NF (Second Normal Form)
- 3NF (Third Normal Form)
- BCNF (Boyce-Codd Normal Form)

Database Design Principles:
1. Identify entities and relationships
2. Define primary and foreign keys
3. Normalize tables to reduce redundancy
4. Create indexes for better performance
5. Implement constraints for data integrity

Popular Database Management Systems:
- MySQL: Open-source relational database
- PostgreSQL: Advanced open-source database
- MongoDB: Document-oriented NoSQL database
- Redis: In-memory key-value store
- SQLite: Lightweight embedded database"""
    
    create_sample_pdf_simple(
        os.path.join(pdf_folder, "database_fundamentals.pdf"),
        "Database Fundamentals",
        db_content
    )
    
    # Sample PDF 4: Web Development Guide
    web_content = """Web Development adalah proses pembuatan aplikasi web dan website.

Frontend Development:
- HTML: Struktur halaman web
- CSS: Styling dan layout
- JavaScript: Interaktivity dan dynamic behavior

Backend Development:
- Server-side programming
- Database integration
- API development
- Authentication dan authorization

Popular Frontend Frameworks:
- React: JavaScript library untuk UI
- Vue.js: Progressive JavaScript framework
- Angular: Full-featured framework by Google
- Svelte: Compile-time framework

Popular Backend Frameworks:
- Express.js (Node.js)
- Django (Python)
- Flask (Python)
- Spring Boot (Java)
- Laravel (PHP)

Web Development Process:
1. Planning dan requirement analysis
2. Design dan wireframing
3. Frontend development
4. Backend development
5. Database design
6. Testing
7. Deployment
8. Maintenance

Modern Web Development Tools:
- Version Control: Git, GitHub, GitLab
- Package Managers: npm, yarn, pip
- Build Tools: Webpack, Vite, Parcel
- CSS Preprocessors: Sass, Less
- Task Runners: Gulp, Grunt

Web Development Best Practices:
- Responsive design
- Performance optimization
- Security considerations
- SEO optimization
- Accessibility (WCAG guidelines)
- Clean code dan maintainability"""
    
    create_sample_pdf_simple(
        os.path.join(pdf_folder, "web_development_guide.pdf"),
        "Web Development Guide",
        web_content
    )
    
    print(f"\n🎉 Berhasil membuat {4} file PDF contoh!")
    print(f"📁 Lokasi: {pdf_folder}/")
    print("📋 File yang dibuat:")
    print("   - python_guide.pdf")
    print("   - machine_learning_basics.pdf") 
    print("   - database_fundamentals.pdf")
    print("   - web_development_guide.pdf")

if __name__ == "__main__":
    print("📝 Membuat file PDF contoh untuk RAG system...")
    create_sample_pdfs()
