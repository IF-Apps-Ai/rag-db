#!/usr/bin/env python3
"""
Script untuk membuat file teks yang dapat digunakan sebagai alternatif PDF
atau dikonversi ke PDF menggunakan tool lain
"""
import os

def create_text_file(filename, title, content):
    """
    Membuat file teks
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{title}\n")
            f.write("=" * len(title) + "\n\n")
            f.write(content)
        print(f"✅ Created: {filename}")
    except Exception as e:
        print(f"❌ Error creating file {filename}: {e}")

def create_sample_documents():
    """
    Membuat dokumen contoh untuk testing
    """
    # Create pdf_documents folder
    docs_folder = "pdf_documents"
    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)
        print(f"📁 Created folder: {docs_folder}")
    
    # Sample Document 1: Python Programming Guide
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

Untuk memulai dengan Python, Anda perlu menginstall Python dari python.org dan memilih text editor atau IDE favorit seperti VSCode, PyCharm, atau Sublime Text.

Python Package Manager (pip):
pip install package_name
pip install -r requirements.txt
pip list
pip freeze > requirements.txt

Virtual Environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows

Python Data Types:
- Numeric: int, float, complex
- Sequence: str, list, tuple
- Mapping: dict
- Set: set, frozenset
- Boolean: bool
- Binary: bytes, bytearray

Control Structures:
- if/elif/else statements
- for loops
- while loops
- try/except/finally
- with statements
"""
    
    create_text_file(
        os.path.join(docs_folder, "python_guide.txt"),
        "Python Programming Guide",
        python_content
    )
    
    # Sample Document 2: Machine Learning Basics
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
- Monitoring: Memantau performa model di production

Machine Learning Algorithms:

Classification:
- Logistic Regression
- Decision Trees
- Random Forest
- Support Vector Machine (SVM)
- Naive Bayes
- K-Nearest Neighbors (KNN)
- Neural Networks

Regression:
- Linear Regression
- Polynomial Regression
- Ridge Regression
- Lasso Regression
- Elastic Net

Clustering:
- K-Means
- Hierarchical Clustering
- DBSCAN
- Gaussian Mixture Models

Evaluation Metrics:
- Classification: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Regression: MSE, RMSE, MAE, R-squared
- Clustering: Silhouette Score, Inertia

Deep Learning:
- Neural Networks
- Convolutional Neural Networks (CNN)
- Recurrent Neural Networks (RNN)
- Long Short-Term Memory (LSTM)
- Transformer Models
- Generative Adversarial Networks (GAN)
"""
    
    create_text_file(
        os.path.join(docs_folder, "machine_learning_basics.txt"),
        "Machine Learning Basics",
        ml_content
    )
    
    # Sample Document 3: Database Fundamentals
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

Basic SQL Commands:
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

INSERT INTO users (id, name, email) VALUES (1, 'John', 'john@email.com');
SELECT * FROM users WHERE name = 'John';
UPDATE users SET email = 'newemail@email.com' WHERE id = 1;
DELETE FROM users WHERE id = 1;

Normalization:
- 1NF (First Normal Form): Eliminate duplicate columns
- 2NF (Second Normal Form): Meet 1NF + remove partial dependencies
- 3NF (Third Normal Form): Meet 2NF + remove transitive dependencies
- BCNF (Boyce-Codd Normal Form): Stricter version of 3NF

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
- SQLite: Lightweight embedded database
- Oracle: Enterprise-grade database
- Microsoft SQL Server: Microsoft's database solution

Database Performance Optimization:
- Indexing strategies
- Query optimization
- Partitioning
- Caching
- Connection pooling
- Database normalization/denormalization
"""
    
    create_text_file(
        os.path.join(docs_folder, "database_fundamentals.txt"),
        "Database Fundamentals",
        db_content
    )
    
    # Sample Document 4: Web Development Guide
    web_content = """Web Development adalah proses pembuatan aplikasi web dan website.

Frontend Development:
- HTML: Struktur halaman web
- CSS: Styling dan layout
- JavaScript: Interactivity dan dynamic behavior

HTML Basics:
- Tags dan elements
- Semantic HTML
- Forms dan input
- Tables dan lists
- Media elements (img, video, audio)

CSS Fundamentals:
- Selectors
- Box model
- Flexbox dan Grid
- Responsive design
- Animations dan transitions

JavaScript Essentials:
- Variables dan data types
- Functions dan scope
- DOM manipulation
- Event handling
- Asynchronous programming (Promises, async/await)
- ES6+ features

Backend Development:
- Server-side programming
- Database integration
- API development
- Authentication dan authorization
- Security considerations

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
- Ruby on Rails (Ruby)

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
- Bundlers: Webpack, Rollup, Parcel

Web Development Best Practices:
- Responsive design
- Performance optimization
- Security considerations
- SEO optimization
- Accessibility (WCAG guidelines)
- Clean code dan maintainability
- Progressive Web Apps (PWA)
- Mobile-first design

HTTP Methods:
- GET: Retrieve data
- POST: Create new resource
- PUT: Update entire resource
- PATCH: Partial update
- DELETE: Remove resource

Web Security:
- HTTPS/SSL
- Cross-Site Scripting (XSS) prevention
- SQL Injection prevention
- Cross-Site Request Forgery (CSRF) protection
- Authentication dan authorization
- Input validation dan sanitization
"""
    
    create_text_file(
        os.path.join(docs_folder, "web_development_guide.txt"),
        "Web Development Guide",
        web_content
    )
    
    print(f"\n🎉 Berhasil membuat {4} file dokumen contoh!")
    print(f"📁 Lokasi: {docs_folder}/")
    print("📋 File yang dibuat:")
    print("   - python_guide.txt")
    print("   - machine_learning_basics.txt") 
    print("   - database_fundamentals.txt")
    print("   - web_development_guide.txt")
    print("\n💡 Tips:")
    print("- Anda dapat menggunakan file txt ini langsung dengan RAG system")
    print("- Atau konversi ke PDF menggunakan online converter")
    print("- Atau gunakan command: pandoc file.txt -o file.pdf")

if __name__ == "__main__":
    print("📝 Membuat file dokumen contoh untuk RAG system...")
    create_sample_documents()
