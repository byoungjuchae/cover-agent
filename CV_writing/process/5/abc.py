from pylatex import Document, Section, Subsection, Command, Itemize, Enumerate, NoEscape
from pylatex.utils import bold, italic

def generate_cv():
    doc = Document('cv')

    # Name and contact
    doc.append(bold("BYUNGJOO CHAE"))
    doc.append(NoEscape(r'\\'))
    doc.append("wpdhkd1642@gmail.com | +82-10-2803-0965 | www.linkedin.com/in/byungjoo-chae-baa661198")
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\hrule'))
    doc.append(NoEscape(r'\\[1em]'))

    # EDUCATION Section
    with doc.create(Section("EDUCATION", numbering=False)):
        doc.append(bold("M.S. Electronic Engineering ") + italic("(Advisor: Donghyeon Cho)"))
        doc.append(NoEscape(r'\\'))
        doc.append("Chungnam National University, Daejeon, Republic of Korea")
        doc.append(NoEscape(r'\\'))
        doc.append("Mar 2022 – Feb 2024")
        doc.append(NoEscape(r'\\[0.5em]'))

        doc.append(bold("B.S. Electronic Engineering"))
        doc.append(NoEscape(r'\\'))
        doc.append("Chungnam National University, Daejeon, Republic of Korea")
        doc.append(NoEscape(r'\\'))
        doc.append("Mar 2016 – Feb 2022")
        doc.append(NoEscape(r'\\[1em]'))
        doc.append(NoEscape(r'\hrule'))
        doc.append(NoEscape(r'\\[1em]'))

    # PROFESSIONAL EXPERIENCE
    with doc.create(Section("PROFESSIONAL EXPERIENCE", numbering=False)):
        doc.append(bold("Machine Learning Engineer – Dexter Studios"))
        doc.append(NoEscape(r'\\'))
        doc.append("Mar 2024 – Jan 2025")
        with doc.create(Itemize()) as itemize:
            itemize.add_item("Designed and optimized high-performance computing pipelines for video processing, "
                             "enhancing inference time by 90%, reflecting expertise in hardware-software co-design "
                             "and performance optimization.")
            itemize.add_item("Curated and labeled specialized datasets to improve model accuracy, aligning with "
                             "cloud storage and big data workload management demands.")
            itemize.add_item("Developed scalable and easy-to-operate pipelines tailored to cloud product "
                             "performance and cost-efficiency requirements.")
        doc.append(NoEscape(r'\\'))

        doc.append(bold("Researcher – Chungnam National University"))
        doc.append(NoEscape(r'\\'))
        doc.append("Mar 2022 – Feb 2024")
        with doc.create(Itemize()) as itemize:
            itemize.add_item("Architected patch-based harmonization using local and global image features, simulating "
                             "system-level architectural design optimizing performance and accuracy.")
            itemize.add_item("Led development of synthetic data generation pipelines with Unreal Engine to simulate "
                             "complex environments for cloud product prototype evaluations and PoC.")
            itemize.add_item("Built and fine-tuned extensive training datasets (26,157+ synthetic images), showcasing "
                             "skills in data-centric computing, distributed data generation, and model optimization.")
        doc.append(NoEscape(r'\\[1em]'))
        doc.append(NoEscape(r'\hrule'))
        doc.append(NoEscape(r'\\[1em]'))

    # PERSONAL PROJECTS
    with doc.create(Section("PERSONAL PROJECTS", numbering=False)):
        doc.append(bold("Light Weight Ultra Style Transfer Model"))
        doc.append(NoEscape(r'\\'))
        doc.append("Dec 2023 – Feb 2024")
        with doc.create(Itemize()) as itemize:
            itemize.add_item("Engineered a lightweight neural network backbone using ConvMixer and Triple Modulator modules "
                             "to reduce model parameters and GFLOPs by 30% without compromising performance, "
                             "demonstrating power optimization and computing systems tuning expertise.")
        doc.append(NoEscape(r'\\[1em]'))
        doc.append(NoEscape(r'\hrule'))
        doc.append(NoEscape(r'\\[1em]'))

    # PUBLICATIONS
    with doc.create(Section("PUBLICATIONS", numbering=False)):
        with doc.create(Itemize()) as itemize:
            itemize.add_item("Chae, B.*, Park, J.*, Kim, T-H., Cho, D., “Online Learning for Reference-Based Super-Resolution” " +
                             italic("MDPI Electronics") + ", 2022.")
            itemize.add_item("Ko, S.*, Park, J.*, Chae, B., Cho, D., “Learning Lightweight Low-Light Enhancement Network "
                             "using Pseudo Well-Exposed Images,” " + italic("IEEE Signal Processing Letters (SPL)") + ", 2021.")
        doc.append(NoEscape(r'\\[1em]'))
        doc.append(NoEscape(r'\hrule'))
        doc.append(NoEscape(r'\\[1em]'))

    # TECHNICAL SKILLS
    with doc.create(Section("TECHNICAL SKILLS", numbering=False)):
        with doc.create(Itemize()) as itemize:
            itemize.add_item(bold("Advanced: ") + "Python, PyTorch (hardware-software co-design for performance-optimized solutions)")
            itemize.add_item(bold("Intermediate: ") + "Docker, GitHub (collaborative development in cross-functional teams)")
            itemize.add_item(bold("Beginner: ") + "FastAPI, HTTPx")
        doc.append(NoEscape(r'\\[1em]'))
        doc.append(NoEscape(r'\hrule'))
        doc.append(NoEscape(r'\\[1em]'))

    # KEY COMPETENCIES
    with doc.create(Section("KEY COMPETENCIES", numbering=False)):
        with doc.create(Itemize()) as itemize:
            itemize.add_item("Cloud Hardware System Architecture & High-Performance Computing")
            itemize.add_item("Server and Storage System Design and Optimization")
            itemize.add_item("Hardware and Software Performance, Power Optimization")
            itemize.add_item("Computing, Storage, Database & Big Data Solutions")
            itemize.add_item("Edge Computing and Distributed Storage Systems")
            itemize.add_item("Deep Learning Architecture Integration")
            itemize.add_item("Prototype Evaluation & Proof of Concept (PoC) Implementation")
            itemize.add_item("Cross-Functional Team Collaboration & Communication")
            itemize.add_item("Knowledge of CPU, Memory, SSD, Network Component Design")
            itemize.add_item("Familiar with Virtualization Technology and Industry Standards")
            itemize.add_item("Self-motivated with Demonstrated Research and Development Contributions")
        doc.append(NoEscape(r'\\[1em]'))
        doc.append(NoEscape(r'\hrule'))
        doc.append(NoEscape(r'\\[1em]'))

    # Remarks
    doc.append(bold("Remarks: "))
    doc.append("Willing to participate in international travel and collaboration (China, Europe, South Asia) as required "
               "for cloud product ecosystem development and industry consortium engagement.")
    doc.append(NoEscape(r'\\[1em]'))
    doc.append(NoEscape(r'\hrule'))

    return doc

if __name__ == "__main__":
    cv_doc = generate_cv()
    cv_doc.generate_pdf(clean_tex=False)

