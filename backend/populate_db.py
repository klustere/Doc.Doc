import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confluence_clone.settings')
django.setup()

from pages.models import Page

# Utility to create a page with markdown content

def create_page(title, content, chapter=None):
    page = Page.objects.create(title=title, content=content, chapter=chapter)
    return page

# Utility to link two pages (parent -> child)
def link_pages(parent, child):
    parent.links.add(child)
    parent.save()

# --- Main population logic ---

def main():
    # 1. Create main documents
    ml_doc = create_page(
        "Machine Learning",
        """
# Machine Learning

Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to learn from data, without being explicitly programmed.

## Key Concepts
- Supervised Learning
- Unsupervised Learning
- Reinforcement Learning

## Example: Linear Regression
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
```

> Machine learning enables systems to improve automatically through experience.
        """
    )
    dl_doc = create_page(
        "Deep Learning",
        """
# Deep Learning

Deep learning is a subset of machine learning focused on neural networks with many layers. It excels at learning representations from large amounts of data.

## Applications
- Image Recognition
- Natural Language Processing
- Speech Recognition

## Example: Simple Neural Network
```python
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

> Deep learning powers many modern AI systems.
        """
    )

    # 2. Create subpages for ML
    ml_subpages = []
    ml_topics = [
        ("Supervised Learning", "Supervised learning uses labeled data to train models. Common algorithms include decision trees, SVMs, and neural networks."),
        ("Unsupervised Learning", "Unsupervised learning finds patterns in unlabeled data. Clustering and dimensionality reduction are key techniques."),
        ("Reinforcement Learning", "Reinforcement learning trains agents to make sequences of decisions by rewarding desired behaviors."),
        ("Feature Engineering", "Feature engineering is the process of selecting and transforming variables to improve model performance."),
        ("Model Evaluation", "Model evaluation uses metrics like accuracy, precision, recall, and F1-score to assess performance.")
    ]
    for title, content in ml_topics:
        page = create_page(title, f"# {title}\n\n{content}\n\n## Example\n```python\n# Example code for {title.lower().replace(' ', '_')}\n```")
        ml_subpages.append(page)
        link_pages(ml_doc, page)

    # 3. Create subpages for DL
    dl_subpages = []
    dl_topics = [
        ("Neural Networks", "Neural networks are composed of layers of interconnected nodes. They learn complex functions from data."),
        ("Convolutional Networks", "CNNs are specialized for processing grid-like data such as images. They use convolutional layers."),
        ("Recurrent Networks", "RNNs are designed for sequential data and have memory of previous inputs."),
        ("Autoencoders", "Autoencoders learn efficient representations by encoding and decoding data."),
        ("Generative Models", "Generative models like GANs can create new data samples similar to the training data.")
    ]
    for title, content in dl_topics:
        page = create_page(title, f"# {title}\n\n{content}\n\n## Example\n```python\n# Example code for {title.lower().replace(' ', '_')}\n```")
        dl_subpages.append(page)
        link_pages(dl_doc, page)

    # 4. Create additional graph connections (cross-links)
    # Link ML and DL topics
    link_pages(ml_doc, dl_doc)
    link_pages(dl_doc, ml_doc)
    for ml_page in ml_subpages:
        link_pages(ml_page, dl_doc)
    for dl_page in dl_subpages:
        link_pages(dl_page, ml_doc)

    # 5. Create more child pages for ML (total 15 pages)
    extra_ml = []
    for i in range(6):
        page = create_page(
            f"ML Extra Topic {i+1}",
            f"# ML Extra Topic {i+1}\n\nThis is an additional topic in machine learning.\n\n## Key Point\n- Example bullet\n\n## Code\n```python\n# Extra ML code {i+1}\n```")
        extra_ml.append(page)
        link_pages(ml_doc, page)
    # 6. Create more child pages for DL (total 15 pages)
    extra_dl = []
    for i in range(6):
        page = create_page(
            f"DL Extra Topic {i+1}",
            f"# DL Extra Topic {i+1}\n\nThis is an additional topic in deep learning.\n\n## Key Point\n- Example bullet\n\n## Code\n```python\n# Extra DL code {i+1}\n```")
        extra_dl.append(page)
        link_pages(dl_doc, page)
    print("Database populated with ML/DL documents and graph links.")

if __name__ == "__main__":
    main()
