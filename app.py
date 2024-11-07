from flask import Flask, render_template, jsonify, request
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import uuid
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import numpy as np
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_mail import Mail, Message  # Add at top with other imports if not already there

app = Flask(__name__)

# Initialize Mail after creating Flask app
mail = Mail(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aiskillcraft@gmail.com'
app.config['MAIL_PASSWORD'] = 'wgkt scvh ybhm bzdw'  # Your new App Password

# Skills data
skills_data = pd.DataFrame({
    'Skill Name': [
        'Frontend Development', 
        'Backend Development', 
        'DevOps', 
        'Full Stack Development',
        'Android Development',
        'Blockchain Development',
        'Software Architect',
        'Cyber Security',
        'Data Science',
        'DevRel Engineer',
        'Technical Writer',
        'Product Manager',
        'QA Engineer',
        'PostgreSQL DBA',
        'MLOps Engineer'
    ],
    'Rating': [
        4.8, 4.7, 4.9, 4.8, 
        4.6, 4.7, 4.8, 4.9,
        4.8, 4.6, 4.5, 4.7,
        4.6, 4.7, 4.8
    ],
    'Domain': [
        'Web Development', 'Web Development', 'Infrastructure', 'Web Development',
        'Mobile Development', 'Blockchain', 'Software Architecture',
        'Security', 'Data Science', 'Developer Relations', 'Technical Writing',
        'Product Management', 'Quality Assurance', 'Database', 'Machine Learning'
    ],
    'Level': [
        'Beginner', 'Intermediate', 'Advanced', 'Advanced',
        'Intermediate', 'Advanced', 'Expert',
        'Advanced', 'Advanced', 'Intermediate', 'Intermediate',
        'Intermediate', 'Beginner', 'Advanced', 'Advanced'
    ],
    'Duration (hours)': [
        300, 350, 400, 500,
        400, 450, 500,
        400, 500, 300, 250,
        350, 300, 400, 450
    ],
    'Learning Path': [
        'HTML → CSS → JavaScript → Framework',
        'Language → Database → API → Security',
        'Linux → Networking → Cloud → CI/CD',
        'Frontend → Backend → Database → Deployment',
        'Java/Kotlin → Android SDK → UI → APIs',
        'Cryptography → Smart Contracts → Web3 → DApps',
        'Design Patterns → Systems → Cloud → Scalability',
        'Networks → Systems → Cryptography → Security',
        'Statistics → Python → ML → Visualization',
        'Coding → Documentation → Community → Speaking',
        'Writing → Tools → API Docs → User Guides',
        'Market Research → Strategy → Agile → Launch',
        'Testing → Automation → CI/CD → Performance',
        'SQL → Administration → Performance → Security',
        'ML Engineering → DevOps → Pipelines → Monitoring'
    ]
})

# Helper function to convert hours to a readable duration format
def format_duration(hours):
    days = hours / 3  # Changed to 3 hours per day
    months = days / 30  # Approximate days per month
    
    if months >= 1:
        return f"{round(months, 1)} months"
    else:
        return f"{round(days)} days"

# Update the skills DataFrame to include formatted duration
skills_data['Formatted Duration'] = skills_data['Duration (hours)'].apply(format_duration)

# Add routes for all pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/skills')
def skills():
    return render_template('skills.html', skills=skills_data)

@app.route('/start-learning/<skill_name>')
def start_learning(skill_name):
    try:
        # Get skill info
        skill_info = skills_data[skills_data['Skill Name'] == skill_name].iloc[0]
        
        # Calculate learning timeline with 3 hours per day
        start_date = datetime.now()
        days_needed = skill_info['Duration (hours)'] / 3  # Changed to 3 hours per day
        end_date = start_date + timedelta(days=days_needed)
        
        timeline = {
            'start_date': start_date.strftime('%B %d, %Y'),
            'end_date': end_date.strftime('%B %d, %Y'),
            'total_days': int(days_needed),
            'hours_per_day': 3  # Updated to 3 hours
        }
        
        return render_template('learning_journey.html', 
                             skill=skill_info, 
                             timeline=timeline)
                             
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/learning_journey/<skill_name>')
def learning_journey(skill_name):
    try:
        # Get the skill data from your DataFrame
        skill_info = skills_data[skills_data['Skill Name'] == skill_name].iloc[0]
        
        # Convert to dictionary and ensure the name is properly set
        skill = {
            'name': skill_info['Skill Name'],  # This ensures we get the actual name
            'Domain': skill_info['Domain'],
            'Level': skill_info['Level'],
            'Duration (hours)': skill_info['Duration (hours)']
        }
        
        return render_template('learning_journey.html', skill=skill)
    except Exception as e:
        print(f"Error in learning_journey route: {str(e)}")
        return render_template('404.html'), 404

class ModernFlowchartGenerator:
    def __init__(self):
        self.graph_dir = 'static/flowcharts'
        os.makedirs(self.graph_dir, exist_ok=True)
        
        # Update available skills list
        self.available_skills = [
            'Frontend Development',
            'Backend Development',
            'DevOps',
            'Full Stack Development',
            'Android Development',
            'Blockchain Development',
            'Software Architect',
            'Cyber Security',
            'Data Science',
            'DevRel Engineer',
            'Technical Writer',
            'Product Manager',
            'QA Engineer',
            'PostgreSQL DBA',
            'MLOps Engineer'
        ]

    def generate_flowchart(self, skill_name):
        try:
            plt.clf()
            G = nx.DiGraph()
            
            nodes, edges = self.get_skill_data(skill_name)
            
            if not nodes or not edges:
                print(f"No data found for {skill_name}")
                return None
                
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            
            plt.figure(figsize=(20, 10))
            pos = nx.get_node_attributes(G, 'pos')
            
            node_colors = {
                'start': '#98FB98',    # Light green
                'basic': '#87CEEB',    # Sky blue
                'decision': '#FFD700',  # Gold
                'framework': '#DDA0DD', # Plum
                'advanced': '#F08080',  # Light coral
                'tool': '#B8860B',     # Dark golden
                'end': '#98FB98'       # Light green
            }
            
            for node, attr in G.nodes(data=True):
                if attr['type'] == 'decision':
                    plt.scatter(pos[node][0], pos[node][1], s=1000, 
                              marker='D', c=node_colors['decision'])
                else:
                    plt.scatter(pos[node][0], pos[node][1], s=1000,
                              c=node_colors[attr['type']])
                
                plt.annotate(node, xy=pos[node], xytext=(0, 0),
                           textcoords='offset points', ha='center', va='center',
                           bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.7),
                           fontsize=10)
            
            nx.draw_networkx_edges(G, pos, edge_color='gray',
                                 arrows=True, arrowsize=20,
                                 connectionstyle='arc3,rad=0.1')
            
            plt.axis('off')
            plt.margins(0.2)

            filename = f"{skill_name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(self.graph_dir, filename)
            
            plt.savefig(filepath, bbox_inches='tight', dpi=300,
                       facecolor='white', edgecolor='none', pad_inches=0.5)
            plt.close()
            
            return filename

        except Exception as e:
            print(f"Error generating flowchart: {str(e)}")
            return None

    def get_skill_data(self, skill_name):
        try:
            # Special handling for AI/ML Engineer
            if skill_name in ["AI/ML Engineer", "AI_ML Engineer", "AI ML Engineer"]:
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Mathematics & Statistics
                    ('Mathematics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Linear Algebra', {'pos': (2, 6), 'type': 'basic'}),
                    ('Statistics', {'pos': (2, 2), 'type': 'basic'}),
                    ('Calculus', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Programming
                    ('Programming', {'pos': (4, 4), 'type': 'basic'}),
                    ('Python', {'pos': (4, 6), 'type': 'basic'}),
                    ('NumPy', {'pos': (4, 2), 'type': 'tool'}),
                    ('Pandas', {'pos': (4, 0), 'type': 'tool'}),
                    
                    # Machine Learning
                    ('Machine Learning', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Supervised Learning', {'pos': (6, 6), 'type': 'advanced'}),
                    ('Unsupervised Learning', {'pos': (6, 2), 'type': 'advanced'}),
                    ('Scikit-learn', {'pos': (6, 0), 'type': 'framework'}),
                    
                    # Deep Learning
                    ('Deep Learning', {'pos': (8, 4), 'type': 'advanced'}),
                    ('Neural Networks', {'pos': (8, 6), 'type': 'advanced'}),
                    ('TensorFlow', {'pos': (8, 2), 'type': 'framework'}),
                    ('PyTorch', {'pos': (8, 0), 'type': 'framework'}),
                    
                    # MLOps
                    ('MLOps', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Model Deployment', {'pos': (10, 6), 'type': 'advanced'}),
                    ('Model Monitoring', {'pos': (10, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (12, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Mathematics'),
                    ('Mathematics', 'Linear Algebra'),
                    ('Mathematics', 'Statistics'),
                    ('Mathematics', 'Calculus'),
                    
                    ('Mathematics', 'Programming'),
                    ('Programming', 'Python'),
                    ('Programming', 'NumPy'),
                    ('Programming', 'Pandas'),
                    
                    ('Programming', 'Machine Learning'),
                    ('Machine Learning', 'Supervised Learning'),
                    ('Machine Learning', 'Unsupervised Learning'),
                    ('Machine Learning', 'Scikit-learn'),
                    
                    ('Machine Learning', 'Deep Learning'),
                    ('Deep Learning', 'Neural Networks'),
                    ('Deep Learning', 'TensorFlow'),
                    ('Deep Learning', 'PyTorch'),
                    
                    ('Deep Learning', 'MLOps'),
                    ('MLOps', 'Model Deployment'),
                    ('MLOps', 'Model Monitoring'),
                    
                    ('MLOps', 'End')
                ]
                
                return nodes, edges
                
            elif skill_name == "Frontend Development":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    # Internet
                    ('Internet', {'pos': (2, 4), 'type': 'basic'}),
                    ('How it works', {'pos': (2, 6), 'type': 'basic'}),
                    ('Browsers', {'pos': (2, 2), 'type': 'basic'}),
                    
                    # HTML
                    ('HTML', {'pos': (4, 4), 'type': 'basic'}),
                    ('Semantic HTML', {'pos': (4, 6), 'type': 'basic'}),
                    ('Forms & Validation', {'pos': (4, 2), 'type': 'basic'}),
                    
                    # CSS
                    ('CSS', {'pos': (6, 4), 'type': 'basic'}),
                    ('Layouts', {'pos': (6, 6), 'type': 'basic'}),
                    ('Responsive Design', {'pos': (6, 2), 'type': 'basic'}),
                    
                    # JavaScript
                    ('JavaScript', {'pos': (8, 4), 'type': 'basic'}),
                    ('DOM', {'pos': (8, 6), 'type': 'basic'}),
                    ('Fetch API', {'pos': (8, 2), 'type': 'basic'}),
                    
                    # Framework
                    ('Choose Framework', {'pos': (10, 4), 'type': 'decision'}),
                    ('React', {'pos': (10, 6), 'type': 'framework'}),
                    ('Vue', {'pos': (10, 4), 'type': 'framework'}),
                    ('Angular', {'pos': (10, 2), 'type': 'framework'}),
                    
                    # Package Managers
                    ('Package Manager', {'pos': (12, 4), 'type': 'tool'}),
                    ('npm', {'pos': (12, 6), 'type': 'tool'}),
                    ('yarn', {'pos': (12, 2), 'type': 'tool'}),
                    
                    # Build Tools
                    ('Build Tools', {'pos': (14, 4), 'type': 'tool'}),
                    ('Vite', {'pos': (14, 6), 'type': 'tool'}),
                    ('Webpack', {'pos': (14, 2), 'type': 'tool'}),
                    
                    ('End', {'pos': (16, 4), 'type': 'end'})
                ]
                
                edges = [
                    # Internet
                    ('Start', 'Internet'),
                    ('Internet', 'How it works'),
                    ('Internet', 'Browsers'),
                    
                    # HTML
                    ('Internet', 'HTML'),
                    ('HTML', 'Semantic HTML'),
                    ('HTML', 'Forms & Validation'),
                    
                    # CSS
                    ('HTML', 'CSS'),
                    ('CSS', 'Layouts'),
                    ('CSS', 'Responsive Design'),
                    
                    # JavaScript
                    ('CSS', 'JavaScript'),
                    ('JavaScript', 'DOM'),
                    ('JavaScript', 'Fetch API'),
                    
                    # Framework
                    ('JavaScript', 'Choose Framework'),
                    ('Choose Framework', 'React'),
                    ('Choose Framework', 'Vue'),
                    ('Choose Framework', 'Angular'),
                    
                    # Package Manager
                    ('Choose Framework', 'Package Manager'),
                    ('Package Manager', 'npm'),
                    ('Package Manager', 'yarn'),
                    
                    # Build Tools
                    ('Package Manager', 'Build Tools'),
                    ('Build Tools', 'Vite'),
                    ('Build Tools', 'Webpack'),
                    
                    ('Build Tools', 'End')
                ]

            elif skill_name == "Backend Development":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    # Internet
                    ('Internet', {'pos': (2, 4), 'type': 'basic'}),
                    ('HTTP/HTTPS', {'pos': (2, 6), 'type': 'basic'}),
                    ('DNS', {'pos': (2, 2), 'type': 'basic'}),
                    
                    # OS and General Knowledge
                    ('OS Knowledge', {'pos': (4, 4), 'type': 'basic'}),
                    ('Terminal Usage', {'pos': (4, 6), 'type': 'basic'}),
                    ('Process Management', {'pos': (4, 2), 'type': 'basic'}),
                    
                    # Programming Language
                    ('Choose Language', {'pos': (6, 4), 'type': 'decision'}),
                    ('Python', {'pos': (6, 6), 'type': 'basic'}),
                    ('Java', {'pos': (6, 5), 'type': 'basic'}),
                    ('Node.js', {'pos': (6, 3), 'type': 'basic'}),
                    ('Go', {'pos': (6, 2), 'type': 'basic'}),
                    
                    # Version Control
                    ('Version Control', {'pos': (8, 4), 'type': 'tool'}),
                    ('Git', {'pos': (8, 6), 'type': 'tool'}),
                    ('GitHub', {'pos': (8, 2), 'type': 'tool'}),
                    
                    # Database Concepts
                    ('Databases', {'pos': (10, 4), 'type': 'decision'}),
                    ('Relational', {'pos': (10, 6), 'type': 'basic'}),
                    ('NoSQL', {'pos': (10, 2), 'type': 'basic'}),
                    ('PostgreSQL', {'pos': (10, 7), 'type': 'tool'}),
                    ('MongoDB', {'pos': (10, 1), 'type': 'tool'}),
                    
                    # APIs
                    ('API', {'pos': (12, 4), 'type': 'advanced'}),
                    ('REST', {'pos': (12, 6), 'type': 'advanced'}),
                    ('GraphQL', {'pos': (12, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Internet'),
                    ('Internet', 'HTTP/HTTPS'),
                    ('Internet', 'DNS'),
                    
                    ('Internet', 'OS Knowledge'),
                    ('OS Knowledge', 'Terminal Usage'),
                    ('OS Knowledge', 'Process Management'),
                    
                    ('OS Knowledge', 'Choose Language'),
                    ('Choose Language', 'Python'),
                    ('Choose Language', 'Java'),
                    ('Choose Language', 'Node.js'),
                    ('Choose Language', 'Go'),
                    
                    ('Choose Language', 'Version Control'),
                    ('Version Control', 'Git'),
                    ('Version Control', 'GitHub'),
                    
                    ('Version Control', 'Databases'),
                    ('Databases', 'Relational'),
                    ('Databases', 'NoSQL'),
                    ('Relational', 'PostgreSQL'),
                    ('NoSQL', 'MongoDB'),
                    
                    ('Databases', 'API'),
                    ('API', 'REST'),
                    ('API', 'GraphQL'),
                    
                    ('API', 'End')
                ]

            elif skill_name == "DevOps":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Programming Language
                    ('Language Basics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Python', {'pos': (2, 6), 'type': 'basic'}),
                    ('Shell Scripting', {'pos': (2, 2), 'type': 'basic'}),
                    
                    # OS Concepts
                    ('Operating Systems', {'pos': (4, 4), 'type': 'basic'}),
                    ('Linux', {'pos': (4, 6), 'type': 'basic'}),
                    ('Process Management', {'pos': (4, 2), 'type': 'basic'}),
                    
                    # Server
                    ('Server Management', {'pos': (6, 4), 'type': 'basic'}),
                    ('Terminal', {'pos': (6, 6), 'type': 'basic'}),
                    ('SSH', {'pos': (6, 2), 'type': 'basic'}),
                    
                    # Networking
                    ('Networking', {'pos': (8, 4), 'type': 'basic'}),
                    ('Protocols', {'pos': (8, 6), 'type': 'basic'}),
                    ('Security', {'pos': (8, 2), 'type': 'basic'}),
                    
                    # Cloud Platforms
                    ('Cloud Platform', {'pos': (10, 4), 'type': 'decision'}),
                    ('AWS', {'pos': (10, 6), 'type': 'tool'}),
                    ('Azure', {'pos': (10, 2), 'type': 'tool'}),
                    
                    # CI/CD
                    ('CI/CD', {'pos': (12, 4), 'type': 'advanced'}),
                    ('Jenkins', {'pos': (12, 6), 'type': 'tool'}),
                    ('GitHub Actions', {'pos': (12, 2), 'type': 'tool'}),
                    
                    # Containers
                    ('Containers', {'pos': (14, 4), 'type': 'advanced'}),
                    ('Docker', {'pos': (14, 6), 'type': 'tool'}),
                    ('Kubernetes', {'pos': (14, 2), 'type': 'tool'}),
                    
                    ('End', {'pos': (16, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Language Basics'),
                    ('Language Basics', 'Python'),
                    ('Language Basics', 'Shell Scripting'),
                    
                    ('Language Basics', 'Operating Systems'),
                    ('Operating Systems', 'Linux'),
                    ('Operating Systems', 'Process Management'),
                    
                    ('Operating Systems', 'Server Management'),
                    ('Server Management', 'Terminal'),
                    ('Server Management', 'SSH'),
                    
                    ('Server Management', 'Networking'),
                    ('Networking', 'Protocols'),
                    ('Networking', 'Security'),
                    
                    ('Networking', 'Cloud Platform'),
                    ('Cloud Platform', 'AWS'),
                    ('Cloud Platform', 'Azure'),
                    
                    ('Cloud Platform', 'CI/CD'),
                    ('CI/CD', 'Jenkins'),
                    ('CI/CD', 'GitHub Actions'),
                    
                    ('CI/CD', 'Containers'),
                    ('Containers', 'Docker'),
                    ('Containers', 'Kubernetes'),
                    
                    ('Containers', 'End')
                ]

            elif skill_name == "Full Stack Development":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Frontend Track
                    ('Frontend Basics', {'pos': (2, 6), 'type': 'basic'}),
                    ('HTML/CSS', {'pos': (4, 6), 'type': 'basic'}),
                    ('JavaScript', {'pos': (6, 6), 'type': 'basic'}),
                    ('React/Angular/Vue', {'pos': (8, 6), 'type': 'framework'}),
                    
                    # Backend Track
                    ('Backend Basics', {'pos': (2, 2), 'type': 'basic'}),
                    ('Python/Node.js', {'pos': (4, 2), 'type': 'basic'}),
                    ('SQL Basics', {'pos': (6, 2), 'type': 'basic'}),
                    ('Backend Framework', {'pos': (8, 2), 'type': 'framework'}),
                    
                    # Common Skills
                    ('Version Control', {'pos': (10, 4), 'type': 'tool'}),
                    ('Database Design', {'pos': (12, 4), 'type': 'advanced'}),
                    ('API Development', {'pos': (14, 4), 'type': 'advanced'}),
                    ('Authentication', {'pos': (16, 4), 'type': 'advanced'}),
                    ('Deployment', {'pos': (18, 4), 'type': 'advanced'}),
                    
                    ('End', {'pos': (20, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Frontend Basics'),
                    ('Start', 'Backend Basics'),
                    
                    ('Frontend Basics', 'HTML/CSS'),
                    ('HTML/CSS', 'JavaScript'),
                    ('JavaScript', 'React/Angular/Vue'),
                    
                    ('Backend Basics', 'Python/Node.js'),
                    ('Python/Node.js', 'SQL Basics'),
                    ('SQL Basics', 'Backend Framework'),
                    
                    ('React/Angular/Vue', 'Version Control'),
                    ('Backend Framework', 'Version Control'),
                    ('Version Control', 'Database Design'),
                    ('Database Design', 'API Development'),
                    ('API Development', 'Authentication'),
                    ('Authentication', 'Deployment'),
                    ('Deployment', 'End')
                ]

            elif skill_name == "Blockchain Development":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Fundamentals
                    ('Blockchain Basics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Cryptography', {'pos': (2, 6), 'type': 'basic'}),
                    ('Distributed Systems', {'pos': (2, 2), 'type': 'basic'}),
                    
                    # Programming
                    ('Programming', {'pos': (4, 4), 'type': 'basic'}),
                    ('Solidity', {'pos': (4, 6), 'type': 'basic'}),
                    ('Web3.js', {'pos': (4, 2), 'type': 'tool'}),
                    ('JavaScript', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # Smart Contracts
                    ('Smart Contracts', {'pos': (6, 4), 'type': 'advanced'}),
                    ('ERC Standards', {'pos': (6, 6), 'type': 'advanced'}),
                    ('Security', {'pos': (6, 2), 'type': 'advanced'}),
                    ('Gas Optimization', {'pos': (6, 0), 'type': 'advanced'}),
                    
                    # Development Tools
                    ('Development Tools', {'pos': (8, 4), 'type': 'tool'}),
                    ('Truffle', {'pos': (8, 6), 'type': 'tool'}),
                    ('Hardhat', {'pos': (8, 2), 'type': 'tool'}),
                    ('Ganache', {'pos': (8, 0), 'type': 'tool'}),
                    
                    # DApps
                    ('DApp Development', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Frontend', {'pos': (10, 6), 'type': 'basic'}),
                    ('IPFS', {'pos': (10, 2), 'type': 'tool'}),
                    ('MetaMask', {'pos': (10, 0), 'type': 'tool'}),
                    
                    # Testing & Deployment
                    ('Testing & Deployment', {'pos': (12, 4), 'type': 'advanced'}),
                    ('Unit Testing', {'pos': (12, 6), 'type': 'advanced'}),
                    ('Networks', {'pos': (12, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Blockchain Basics'),
                    ('Blockchain Basics', 'Cryptography'),
                    ('Blockchain Basics', 'Distributed Systems'),
                    
                    ('Blockchain Basics', 'Programming'),
                    ('Programming', 'Solidity'),
                    ('Programming', 'Web3.js'),
                    ('Programming', 'JavaScript'),
                    
                    ('Programming', 'Smart Contracts'),
                    ('Smart Contracts', 'ERC Standards'),
                    ('Smart Contracts', 'Security'),
                    ('Smart Contracts', 'Gas Optimization'),
                    
                    ('Smart Contracts', 'Development Tools'),
                    ('Development Tools', 'Truffle'),
                    ('Development Tools', 'Hardhat'),
                    ('Development Tools', 'Ganache'),
                    
                    ('Development Tools', 'DApp Development'),
                    ('DApp Development', 'Frontend'),
                    ('DApp Development', 'IPFS'),
                    ('DApp Development', 'MetaMask'),
                    
                    ('DApp Development', 'Testing & Deployment'),
                    ('Testing & Deployment', 'Unit Testing'),
                    ('Testing & Deployment', 'Networks'),
                    
                    ('Testing & Deployment', 'End')
                ]

            elif skill_name == "Software Architect":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Programming Fundamentals
                    ('Programming', {'pos': (2, 4), 'type': 'basic'}),
                    ('Multiple Languages', {'pos': (2, 6), 'type': 'basic'}),
                    ('Design Patterns', {'pos': (2, 2), 'type': 'basic'}),
                    ('Clean Code', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # System Design
                    ('System Design', {'pos': (4, 4), 'type': 'advanced'}),
                    ('Scalability', {'pos': (4, 6), 'type': 'advanced'}),
                    ('Performance', {'pos': (4, 2), 'type': 'advanced'}),
                    ('Security', {'pos': (4, 0), 'type': 'advanced'}),
                    
                    # Architecture Patterns
                    ('Architecture Patterns', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Microservices', {'pos': (6, 6), 'type': 'advanced'}),
                    ('Event-Driven', {'pos': (6, 2), 'type': 'advanced'}),
                    ('Domain-Driven', {'pos': (6, 0), 'type': 'advanced'}),
                    
                    # Infrastructure
                    ('Infrastructure', {'pos': (8, 4), 'type': 'advanced'}),
                    ('Cloud Platforms', {'pos': (8, 6), 'type': 'tool'}),
                    ('Containers', {'pos': (8, 2), 'type': 'tool'}),
                    ('CI/CD', {'pos': (8, 0), 'type': 'tool'}),
                    
                    # Data Architecture
                    ('Data Architecture', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Database Design', {'pos': (10, 6), 'type': 'advanced'}),
                    ('Data Modeling', {'pos': (10, 2), 'type': 'advanced'}),
                    
                    # Leadership
                    ('Leadership', {'pos': (12, 4), 'type': 'advanced'}),
                    ('Team Management', {'pos': (12, 6), 'type': 'advanced'}),
                    ('Communication', {'pos': (12, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Programming'),
                    ('Programming', 'Multiple Languages'),
                    ('Programming', 'Design Patterns'),
                    ('Programming', 'Clean Code'),
                    
                    ('Programming', 'System Design'),
                    ('System Design', 'Scalability'),
                    ('System Design', 'Performance'),
                    ('System Design', 'Security'),
                    
                    ('System Design', 'Architecture Patterns'),
                    ('Architecture Patterns', 'Microservices'),
                    ('Architecture Patterns', 'Event-Driven'),
                    ('Architecture Patterns', 'Domain-Driven'),
                    
                    ('Architecture Patterns', 'Infrastructure'),
                    ('Infrastructure', 'Cloud Platforms'),
                    ('Infrastructure', 'Containers'),
                    ('Infrastructure', 'CI/CD'),
                    
                    ('Infrastructure', 'Data Architecture'),
                    ('Data Architecture', 'Database Design'),
                    ('Data Architecture', 'Data Modeling'),
                    
                    ('Data Architecture', 'Leadership'),
                    ('Leadership', 'Team Management'),
                    ('Leadership', 'Communication'),
                    
                    ('Leadership', 'End')
                ]

            elif skill_name == "Cyber Security":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Fundamentals
                    ('Security Basics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Networking', {'pos': (2, 6), 'type': 'basic'}),
                    ('Operating Systems', {'pos': (2, 2), 'type': 'basic'}),
                    ('Linux', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Programming
                    ('Programming', {'pos': (4, 4), 'type': 'basic'}),
                    ('Python', {'pos': (4, 6), 'type': 'basic'}),
                    ('Shell Scripting', {'pos': (4, 2), 'type': 'basic'}),
                    
                    # Network Security
                    ('Network Security', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Firewalls', {'pos': (6, 6), 'type': 'tool'}),
                    ('IDS/IPS', {'pos': (6, 2), 'type': 'tool'}),
                    ('VPN', {'pos': (6, 0), 'type': 'tool'}),
                    
                    # Application Security
                    ('Application Security', {'pos': (8, 4), 'type': 'advanced'}),
                    ('Web Security', {'pos': (8, 6), 'type': 'advanced'}),
                    ('API Security', {'pos': (8, 2), 'type': 'advanced'}),
                    ('OWASP', {'pos': (8, 0), 'type': 'advanced'}),
                    
                    # Penetration Testing
                    ('Penetration Testing', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Tools', {'pos': (10, 6), 'type': 'tool'}),
                    ('Methodologies', {'pos': (10, 2), 'type': 'advanced'}),
                    
                    # Incident Response
                    ('Incident Response', {'pos': (12, 4), 'type': 'advanced'}),
                    ('Forensics', {'pos': (12, 6), 'type': 'advanced'}),
                    ('Threat Hunting', {'pos': (12, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Security Basics'),
                    ('Security Basics', 'Networking'),
                    ('Security Basics', 'Operating Systems'),
                    ('Security Basics', 'Linux'),
                    
                    ('Security Basics', 'Programming'),
                    ('Programming', 'Python'),
                    ('Programming', 'Shell Scripting'),
                    
                    ('Programming', 'Network Security'),
                    ('Network Security', 'Firewalls'),
                    ('Network Security', 'IDS/IPS'),
                    ('Network Security', 'VPN'),
                    
                    ('Network Security', 'Application Security'),
                    ('Application Security', 'Web Security'),
                    ('Application Security', 'API Security'),
                    ('Application Security', 'OWASP'),
                    
                    ('Application Security', 'Penetration Testing'),
                    ('Penetration Testing', 'Tools'),
                    ('Penetration Testing', 'Methodologies'),
                    
                    ('Penetration Testing', 'Incident Response'),
                    ('Incident Response', 'Forensics'),
                    ('Incident Response', 'Threat Hunting'),
                    
                    ('Incident Response', 'End')
                ]

            elif skill_name == "Data Science":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Mathematics
                    ('Mathematics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Statistics', {'pos': (2, 6), 'type': 'basic'}),
                    ('Probability', {'pos': (2, 2), 'type': 'basic'}),
                    ('Linear Algebra', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Programming
                    ('Programming', {'pos': (4, 4), 'type': 'basic'}),
                    ('Python', {'pos': (4, 6), 'type': 'basic'}),
                    ('SQL', {'pos': (4, 2), 'type': 'basic'}),
                    ('R', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # Data Processing
                    ('Data Processing', {'pos': (6, 4), 'type': 'basic'}),
                    ('Pandas', {'pos': (6, 6), 'type': 'tool'}),
                    ('NumPy', {'pos': (6, 2), 'type': 'tool'}),
                    ('Data Cleaning', {'pos': (6, 0), 'type': 'basic'}),
                    
                    # Data Visualization
                    ('Data Visualization', {'pos': (8, 4), 'type': 'basic'}),
                    ('Matplotlib', {'pos': (8, 6), 'type': 'tool'}),
                    ('Seaborn', {'pos': (8, 2), 'type': 'tool'}),
                    ('Tableau', {'pos': (8, 0), 'type': 'tool'}),
                    
                    # Machine Learning
                    ('Machine Learning', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Scikit-learn', {'pos': (10, 6), 'type': 'framework'}),
                    ('Model Selection', {'pos': (10, 2), 'type': 'advanced'}),
                    ('Feature Engineering', {'pos': (10, 0), 'type': 'advanced'}),
                    
                    # Big Data
                    ('Big Data', {'pos': (12, 4), 'type': 'advanced'}),
                    ('Spark', {'pos': (12, 6), 'type': 'tool'}),
                    ('Hadoop', {'pos': (12, 2), 'type': 'tool'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Mathematics'),
                    ('Mathematics', 'Statistics'),
                    ('Mathematics', 'Probability'),
                    ('Mathematics', 'Linear Algebra'),
                    
                    ('Mathematics', 'Programming'),
                    ('Programming', 'Python'),
                    ('Programming', 'SQL'),
                    ('Programming', 'R'),
                    
                    ('Programming', 'Data Processing'),
                    ('Data Processing', 'Pandas'),
                    ('Data Processing', 'NumPy'),
                    ('Data Processing', 'Data Cleaning'),
                    
                    ('Data Processing', 'Data Visualization'),
                    ('Data Visualization', 'Matplotlib'),
                    ('Data Visualization', 'Seaborn'),
                    ('Data Visualization', 'Tableau'),
                    
                    ('Data Visualization', 'Machine Learning'),
                    ('Machine Learning', 'Scikit-learn'),
                    ('Machine Learning', 'Model Selection'),
                    ('Machine Learning', 'Feature Engineering'),
                    
                    ('Machine Learning', 'Big Data'),
                    ('Big Data', 'Spark'),
                    ('Big Data', 'Hadoop'),
                    
                    ('Big Data', 'End')
                ]

            elif skill_name == "DevRel Engineer":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Technical Skills
                    ('Technical Skills', {'pos': (2, 4), 'type': 'basic'}),
                    ('Programming', {'pos': (2, 6), 'type': 'basic'}),
                    ('API Knowledge', {'pos': (2, 2), 'type': 'basic'}),
                    ('Documentation', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Communication
                    ('Communication', {'pos': (4, 4), 'type': 'basic'}),
                    ('Technical Writing', {'pos': (4, 6), 'type': 'basic'}),
                    ('Public Speaking', {'pos': (4, 2), 'type': 'basic'}),
                    ('Social Media', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # Community
                    ('Community Building', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Event Management', {'pos': (6, 6), 'type': 'advanced'}),
                    ('Developer Support', {'pos': (6, 2), 'type': 'advanced'}),
                    
                    # Content Creation
                    ('Content Creation', {'pos': (8, 4), 'type': 'advanced'}),
                    ('Blog Posts', {'pos': (8, 6), 'type': 'advanced'}),
                    ('Video Tutorials', {'pos': (8, 2), 'type': 'advanced'}),
                    ('Code Examples', {'pos': (8, 0), 'type': 'advanced'}),
                    
                    # Analytics
                    ('Analytics', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Metrics', {'pos': (10, 6), 'type': 'advanced'}),
                    ('User Feedback', {'pos': (10, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (12, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Technical Skills'),
                    ('Technical Skills', 'Programming'),
                    ('Technical Skills', 'API Knowledge'),
                    ('Technical Skills', 'Documentation'),
                    
                    ('Technical Skills', 'Communication'),
                    ('Communication', 'Technical Writing'),
                    ('Communication', 'Public Speaking'),
                    ('Communication', 'Social Media'),
                    
                    ('Communication', 'Community Building'),
                    ('Community Building', 'Event Management'),
                    ('Community Building', 'Developer Support'),
                    
                    ('Community Building', 'Content Creation'),
                    ('Content Creation', 'Blog Posts'),
                    ('Content Creation', 'Video Tutorials'),
                    ('Content Creation', 'Code Examples'),
                    
                    ('Content Creation', 'Analytics'),
                    ('Analytics', 'Metrics'),
                    ('Analytics', 'User Feedback'),
                    
                    ('Analytics', 'End')
                ]

            elif skill_name == "Technical Writer":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Writing Fundamentals
                    ('Writing Fundamentals', {'pos': (2, 4), 'type': 'basic'}),
                    ('Grammar', {'pos': (2, 6), 'type': 'basic'}),
                    ('Style Guides', {'pos': (2, 2), 'type': 'basic'}),
                    ('Clarity', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Technical Skills
                    ('Technical Skills', {'pos': (4, 4), 'type': 'basic'}),
                    ('Markdown', {'pos': (4, 6), 'type': 'tool'}),
                    ('Git', {'pos': (4, 2), 'type': 'tool'}),
                    ('HTML/CSS', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # Documentation
                    ('Documentation', {'pos': (6, 4), 'type': 'advanced'}),
                    ('API Docs', {'pos': (6, 6), 'type': 'advanced'}),
                    ('User Guides', {'pos': (6, 2), 'type': 'advanced'}),
                    ('Release Notes', {'pos': (6, 0), 'type': 'advanced'}),
                    
                    # Tools
                    ('Documentation Tools', {'pos': (8, 4), 'type': 'tool'}),
                    ('Static Site Generators', {'pos': (8, 6), 'type': 'tool'}),
                    ('Doc Management', {'pos': (8, 2), 'type': 'tool'}),
                    
                    # Process
                    ('Documentation Process', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Planning', {'pos': (10, 6), 'type': 'advanced'}),
                    ('Review', {'pos': (10, 2), 'type': 'advanced'}),
                    ('Maintenance', {'pos': (10, 0), 'type': 'advanced'}),
                    
                    ('End', {'pos': (12, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Writing Fundamentals'),
                    ('Writing Fundamentals', 'Grammar'),
                    ('Writing Fundamentals', 'Style Guides'),
                    ('Writing Fundamentals', 'Clarity'),
                    
                    ('Writing Fundamentals', 'Technical Skills'),
                    ('Technical Skills', 'Markdown'),
                    ('Technical Skills', 'Git'),
                    ('Technical Skills', 'HTML/CSS'),
                    
                    ('Technical Skills', 'Documentation'),
                    ('Documentation', 'API Docs'),
                    ('Documentation', 'User Guides'),
                    ('Documentation', 'Release Notes'),
                    
                    ('Documentation', 'Documentation Tools'),
                    ('Documentation Tools', 'Static Site Generators'),
                    ('Documentation Tools', 'Doc Management'),
                    
                    ('Documentation Tools', 'Documentation Process'),
                    ('Documentation Process', 'Planning'),
                    ('Documentation Process', 'Review'),
                    ('Documentation Process', 'Maintenance'),
                    
                    ('Documentation Process', 'End')
                ]

            elif skill_name == "Product Manager":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Business Fundamentals
                    ('Business Skills', {'pos': (2, 4), 'type': 'basic'}),
                    ('Market Research', {'pos': (2, 6), 'type': 'basic'}),
                    ('Strategy', {'pos': (2, 2), 'type': 'basic'}),
                    ('Analytics', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Technical Knowledge
                    ('Technical Knowledge', {'pos': (4, 4), 'type': 'basic'}),
                    ('Development Process', {'pos': (4, 6), 'type': 'basic'}),
                    ('UX Principles', {'pos': (4, 2), 'type': 'basic'}),
                    ('API Basics', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # Product Development
                    ('Product Development', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Requirements', {'pos': (6, 6), 'type': 'advanced'}),
                    ('Roadmapping', {'pos': (6, 2), 'type': 'advanced'}),
                    ('Prioritization', {'pos': (6, 0), 'type': 'advanced'}),
                    
                    # Agile & Scrum
                    ('Agile Methods', {'pos': (8, 4), 'type': 'framework'}),
                    ('Scrum', {'pos': (8, 6), 'type': 'framework'}),
                    ('Kanban', {'pos': (8, 2), 'type': 'framework'}),
                    
                    # Stakeholder Management
                    ('Stakeholders', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Communication', {'pos': (10, 6), 'type': 'advanced'}),
                    ('Leadership', {'pos': (10, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (12, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Business Skills'),
                    ('Business Skills', 'Market Research'),
                    ('Business Skills', 'Strategy'),
                    ('Business Skills', 'Analytics'),
                    
                    ('Business Skills', 'Technical Knowledge'),
                    ('Technical Knowledge', 'Development Process'),
                    ('Technical Knowledge', 'UX Principles'),
                    ('Technical Knowledge', 'API Basics'),
                    
                    ('Technical Knowledge', 'Product Development'),
                    ('Product Development', 'Requirements'),
                    ('Product Development', 'Roadmapping'),
                    ('Product Development', 'Prioritization'),
                    
                    ('Product Development', 'Agile Methods'),
                    ('Agile Methods', 'Scrum'),
                    ('Agile Methods', 'Kanban'),
                    
                    ('Agile Methods', 'Stakeholders'),
                    ('Stakeholders', 'Communication'),
                    ('Stakeholders', 'Leadership'),
                    
                    ('Stakeholders', 'End')
                ]

            elif skill_name == "QA Engineer":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Testing Fundamentals
                    ('Testing Basics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Test Types', {'pos': (2, 6), 'type': 'basic'}),
                    ('Test Cases', {'pos': (2, 2), 'type': 'basic'}),
                    ('Bug Reports', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Manual Testing
                    ('Manual Testing', {'pos': (4, 4), 'type': 'basic'}),
                    ('UI Testing', {'pos': (4, 6), 'type': 'basic'}),
                    ('Usability', {'pos': (4, 2), 'type': 'basic'}),
                    ('Test Plans', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # Automation
                    ('Test Automation', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Selenium', {'pos': (6, 6), 'type': 'tool'}),
                    ('TestNG', {'pos': (6, 2), 'type': 'tool'}),
                    ('Cypress', {'pos': (6, 0), 'type': 'tool'}),
                    
                    # API Testing
                    ('API Testing', {'pos': (8, 4), 'type': 'advanced'}),
                    ('Postman', {'pos': (8, 6), 'type': 'tool'}),
                    ('REST APIs', {'pos': (8, 2), 'type': 'advanced'}),
                    
                    # Performance Testing
                    ('Performance', {'pos': (10, 4), 'type': 'advanced'}),
                    ('JMeter', {'pos': (10, 6), 'type': 'tool'}),
                    ('Load Testing', {'pos': (10, 2), 'type': 'advanced'}),
                    
                    # CI/CD
                    ('CI/CD', {'pos': (12, 4), 'type': 'advanced'}),
                    ('Jenkins', {'pos': (12, 6), 'type': 'tool'}),
                    ('Git', {'pos': (12, 2), 'type': 'tool'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'Testing Basics'),
                    ('Testing Basics', 'Test Types'),
                    ('Testing Basics', 'Test Cases'),
                    ('Testing Basics', 'Bug Reports'),
                    
                    ('Testing Basics', 'Manual Testing'),
                    ('Manual Testing', 'UI Testing'),
                    ('Manual Testing', 'Usability'),
                    ('Manual Testing', 'Test Plans'),
                    
                    ('Manual Testing', 'Test Automation'),
                    ('Test Automation', 'Selenium'),
                    ('Test Automation', 'TestNG'),
                    ('Test Automation', 'Cypress'),
                    
                    ('Test Automation', 'API Testing'),
                    ('API Testing', 'Postman'),
                    ('API Testing', 'REST APIs'),
                    
                    ('API Testing', 'Performance'),
                    ('Performance', 'JMeter'),
                    ('Performance', 'Load Testing'),
                    
                    ('Performance', 'CI/CD'),
                    ('CI/CD', 'Jenkins'),
                    ('CI/CD', 'Git'),
                    
                    ('CI/CD', 'End')
                ]

            elif skill_name == "PostgreSQL DBA":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # SQL Fundamentals
                    ('SQL Basics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Queries', {'pos': (2, 6), 'type': 'basic'}),
                    ('Joins', {'pos': (2, 2), 'type': 'basic'}),
                    ('Indexing', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Database Design
                    ('Database Design', {'pos': (4, 4), 'type': 'basic'}),
                    ('Normalization', {'pos': (4, 6), 'type': 'basic'}),
                    ('Schema Design', {'pos': (4, 2), 'type': 'basic'}),
                    ('Data Types', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # Administration
                    ('Administration', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Installation', {'pos': (6, 6), 'type': 'advanced'}),
                    ('Configuration', {'pos': (6, 2), 'type': 'advanced'}),
                    ('User Management', {'pos': (6, 0), 'type': 'advanced'}),
                    
                    # Performance
                    ('Performance', {'pos': (8, 4), 'type': 'advanced'}),
                    ('Query Optimization', {'pos': (8, 6), 'type': 'advanced'}),
                    ('Monitoring', {'pos': (8, 2), 'type': 'advanced'}),
                    ('Tuning', {'pos': (8, 0), 'type': 'advanced'}),
                    
                    # Backup & Recovery
                    ('Backup & Recovery', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Backup Strategies', {'pos': (10, 6), 'type': 'advanced'}),
                    ('Point-in-Time Recovery', {'pos': (10, 2), 'type': 'advanced'}),
                    
                    # High Availability
                    ('High Availability', {'pos': (12, 4), 'type': 'advanced'}),
                    ('Replication', {'pos': (12, 6), 'type': 'advanced'}),
                    ('Clustering', {'pos': (12, 2), 'type': 'advanced'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'SQL Basics'),
                    ('SQL Basics', 'Queries'),
                    ('SQL Basics', 'Joins'),
                    ('SQL Basics', 'Indexing'),
                    
                    ('SQL Basics', 'Database Design'),
                    ('Database Design', 'Normalization'),
                    ('Database Design', 'Schema Design'),
                    ('Database Design', 'Data Types'),
                    
                    ('Database Design', 'Administration'),
                    ('Administration', 'Installation'),
                    ('Administration', 'Configuration'),
                    ('Administration', 'User Management'),
                    
                    ('Administration', 'Performance'),
                    ('Performance', 'Query Optimization'),
                    ('Performance', 'Monitoring'),
                    ('Performance', 'Tuning'),
                    
                    ('Performance', 'Backup & Recovery'),
                    ('Backup & Recovery', 'Backup Strategies'),
                    ('Backup & Recovery', 'Point-in-Time Recovery'),
                    
                    ('Backup & Recovery', 'High Availability'),
                    ('High Availability', 'Replication'),
                    ('High Availability', 'Clustering'),
                    
                    ('High Availability', 'End')
                ]

            elif skill_name == "MLOps Engineer":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # ML Fundamentals
                    ('ML Basics', {'pos': (2, 4), 'type': 'basic'}),
                    ('ML Lifecycle', {'pos': (2, 6), 'type': 'basic'}),
                    ('Model Training', {'pos': (2, 2), 'type': 'basic'}),
                    ('Evaluation', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Programming
                    ('Programming', {'pos': (4, 4), 'type': 'basic'}),
                    ('Python', {'pos': (4, 6), 'type': 'basic'}),
                    ('SQL', {'pos': (4, 2), 'type': 'basic'}),
                    ('Shell Scripting', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # DevOps
                    ('DevOps', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Git', {'pos': (6, 6), 'type': 'tool'}),
                    ('Docker', {'pos': (6, 2), 'type': 'tool'}),
                    ('Kubernetes', {'pos': (6, 0), 'type': 'tool'}),
                    
                    # ML Engineering
                    ('ML Engineering', {'pos': (8, 4), 'type': 'advanced'}),
                    ('Feature Store', {'pos': (8, 6), 'type': 'advanced'}),
                    ('Model Registry', {'pos': (8, 2), 'type': 'advanced'}),
                    ('Pipeline Orchestration', {'pos': (8, 0), 'type': 'advanced'}),
                    
                    # Monitoring
                    ('Monitoring', {'pos': (10, 4), 'type': 'advanced'}),
                    ('Model Performance', {'pos': (10, 6), 'type': 'advanced'}),
                    ('Data Drift', {'pos': (10, 2), 'type': 'advanced'}),
                    ('Alerts', {'pos': (10, 0), 'type': 'advanced'}),
                    
                    # Tools & Platforms
                    ('MLOps Tools', {'pos': (12, 4), 'type': 'tool'}),
                    ('MLflow', {'pos': (12, 6), 'type': 'tool'}),
                    ('Kubeflow', {'pos': (12, 2), 'type': 'tool'}),
                    ('DVC', {'pos': (12, 0), 'type': 'tool'}),
                    
                    ('End', {'pos': (14, 4), 'type': 'end'})
                ]
                
                edges = [
                    ('Start', 'ML Basics'),
                    ('ML Basics', 'ML Lifecycle'),
                    ('ML Basics', 'Model Training'),
                    ('ML Basics', 'Evaluation'),
                    
                    ('ML Basics', 'Programming'),
                    ('Programming', 'Python'),
                    ('Programming', 'SQL'),
                    ('Programming', 'Shell Scripting'),
                    
                    ('Programming', 'DevOps'),
                    ('DevOps', 'Git'),
                    ('DevOps', 'Docker'),
                    ('DevOps', 'Kubernetes'),
                    
                    ('DevOps', 'ML Engineering'),
                    ('ML Engineering', 'Feature Store'),
                    ('ML Engineering', 'Model Registry'),
                    ('ML Engineering', 'Pipeline Orchestration'),
                    
                    ('ML Engineering', 'Monitoring'),
                    ('Monitoring', 'Model Performance'),
                    ('Monitoring', 'Data Drift'),
                    ('Monitoring', 'Alerts'),
                    
                    ('Monitoring', 'MLOps Tools'),
                    ('MLOps Tools', 'MLflow'),
                    ('MLOps Tools', 'Kubeflow'),
                    ('MLOps Tools', 'DVC'),
                    
                    ('MLOps Tools', 'End')
                ]

            elif skill_name == "Android Development":
                nodes = [
                    ('Start', {'pos': (0, 4), 'type': 'start'}),
                    
                    # Programming Fundamentals
                    ('Programming Basics', {'pos': (2, 4), 'type': 'basic'}),
                    ('Java', {'pos': (2, 6), 'type': 'basic'}),
                    ('Kotlin', {'pos': (2, 2), 'type': 'basic'}),
                    ('OOP Concepts', {'pos': (2, 0), 'type': 'basic'}),
                    
                    # Android Basics
                    ('Android Fundamentals', {'pos': (4, 4), 'type': 'basic'}),
                    ('Activity Lifecycle', {'pos': (4, 6), 'type': 'basic'}),
                    ('UI Components', {'pos': (4, 2), 'type': 'basic'}),
                    ('Layouts', {'pos': (4, 0), 'type': 'basic'}),
                    
                    # UI Development
                    ('UI Development', {'pos': (6, 4), 'type': 'advanced'}),
                    ('Material Design', {'pos': (6, 6), 'type': 'framework'}),
                    ('Custom Views', {'pos': (6, 2), 'type': 'advanced'}),
                    ('Animations', {'pos': (6, 0), 'type': 'advanced'}),
                    
                    # Data Management
                    ('Data Management', {'pos': (8, 4), 'type': 'advanced'}),
                    ('SQLite', {'pos': (8, 6), 'type': 'tool'}),
                    ('Room Database', {'pos': (8, 2), 'type': 'framework'}),
                    ('SharedPreferences', {'pos': (8, 0), 'type': 'tool'}),
                    
                    # Networking
                    ('Networking', {'pos': (10, 4), 'type': 'advanced'}),
                    ('REST APIs', {'pos': (10, 6), 'type': 'advanced'}),
                    ('Retrofit', {'pos': (10, 2), 'type': 'tool'}),
                    ('JSON Parsing', {'pos': (10, 0), 'type': 'basic'}),
                    
                    # Architecture
                    ('Architecture', {'pos': (12, 4), 'type': 'advanced'}),
                    ('MVVM', {'pos': (12, 6), 'type': 'framework'}),
                    ('LiveData', {'pos': (12, 2), 'type': 'framework'}),
                    ('ViewModel', {'pos': (12, 0), 'type': 'framework'}),
                    
                    # Advanced Concepts
                    ('Advanced Topics', {'pos': (14, 4), 'type': 'advanced'}),
                    ('Services', {'pos': (14, 6), 'type': 'advanced'}),
                    ('WorkManager', {'pos': (14, 2), 'type': 'tool'}),
                    ('Firebase', {'pos': (14, 0), 'type': 'tool'}),
                    
                    ('End', {'pos': (16, 4), 'type': 'end'})
                ]
                
                edges = [
                    # Programming Fundamentals
                    ('Start', 'Programming Basics'),
                    ('Programming Basics', 'Java'),
                    ('Programming Basics', 'Kotlin'),
                    ('Programming Basics', 'OOP Concepts'),
                    
                    # Android Basics
                    ('Programming Basics', 'Android Fundamentals'),
                    ('Android Fundamentals', 'Activity Lifecycle'),
                    ('Android Fundamentals', 'UI Components'),
                    ('Android Fundamentals', 'Layouts'),
                    
                    # UI Development
                    ('Android Fundamentals', 'UI Development'),
                    ('UI Development', 'Material Design'),
                    ('UI Development', 'Custom Views'),
                    ('UI Development', 'Animations'),
                    
                    # Data Management
                    ('UI Development', 'Data Management'),
                    ('Data Management', 'SQLite'),
                    ('Data Management', 'Room Database'),
                    ('Data Management', 'SharedPreferences'),
                    
                    # Networking
                    ('Data Management', 'Networking'),
                    ('Networking', 'REST APIs'),
                    ('Networking', 'Retrofit'),
                    ('Networking', 'JSON Parsing'),
                    
                    # Architecture
                    ('Networking', 'Architecture'),
                    ('Architecture', 'MVVM'),
                    ('Architecture', 'LiveData'),
                    ('Architecture', 'ViewModel'),
                    
                    # Advanced Topics
                    ('Architecture', 'Advanced Topics'),
                    ('Advanced Topics', 'Services'),
                    ('Advanced Topics', 'WorkManager'),
                    ('Advanced Topics', 'Firebase'),
                    
                    ('Advanced Topics', 'End')
                ]

            else:
                print(f"Unknown skill: {skill_name}")
                return [], []

            return nodes, edges
            
        except Exception as e:
            print(f"Error in get_skill_data: {str(e)}")
            return [], []

@app.route('/roadmap/<skill_name>')
def roadmap(skill_name):
    try:
        flowchart_generator = ModernFlowchartGenerator()
        skill_info = skills_data[skills_data['Skill Name'] == skill_name].to_dict(orient='records')[0]
        
        flowchart_path = flowchart_generator.generate_flowchart(skill_name)
        
        if flowchart_path:
            return render_template('roadmap.html', 
                                 skill=skill_info, 
                                 flowchart_path=flowchart_path)
        else:
            return render_template('roadmap.html', 
                                 skill=skill_info,
                                 error="Could not generate roadmap",
                                 flowchart_path=None)
                                 
    except Exception as e:
        print(f"Error in roadmap route: {str(e)}")
        return render_template('roadmap.html', 
                             error=f"Error: {str(e)}",
                             flowchart_path=None)

# Add error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Complete skill features dictionary for all skills
skill_features = {
    'Frontend Development': {
        'complexity': 0.7,
        'market_demand': 0.9,
        'learning_curve': 0.6,
        'resource_availability': 0.9
    },
    'Backend Development': {
        'complexity': 0.8,
        'market_demand': 0.85,
        'learning_curve': 0.75,
        'resource_availability': 0.7
    },
    'DevOps': {
        'complexity': 0.85,
        'market_demand': 0.95,
        'learning_curve': 0.8,
        'resource_availability': 0.6
    },
    'Full Stack Development': {
        'complexity': 0.9,
        'market_demand': 0.9,
        'learning_curve': 0.8,
        'resource_availability': 0.75
    },
    'Android Development': {
        'complexity': 0.75,
        'market_demand': 0.8,
        'learning_curve': 0.7,
        'resource_availability': 0.85
    },
    'Blockchain Development': {
        'complexity': 0.9,
        'market_demand': 0.85,
        'learning_curve': 0.85,
        'resource_availability': 0.6
    },
    'Software Architect': {
        'complexity': 0.95,
        'market_demand': 0.9,
        'learning_curve': 0.9,
        'resource_availability': 0.7
    },
    'Cyber Security': {
        'complexity': 0.9,
        'market_demand': 0.95,
        'learning_curve': 0.85,
        'resource_availability': 0.7
    },
    'Data Science': {
        'complexity': 0.85,
        'market_demand': 0.9,
        'learning_curve': 0.8,
        'resource_availability': 0.8
    },
    'DevRel Engineer': {
        'complexity': 0.7,
        'market_demand': 0.75,
        'learning_curve': 0.65,
        'resource_availability': 0.7
    },
    'Technical Writer': {
        'complexity': 0.5,
        'market_demand': 0.7,
        'learning_curve': 0.5,
        'resource_availability': 0.8
    },
    'Product Manager': {
        'complexity': 0.75,
        'market_demand': 0.9,
        'learning_curve': 0.7,
        'resource_availability': 0.85
    },
    'QA Engineer': {
        'complexity': 0.65,
        'market_demand': 0.8,
        'learning_curve': 0.6,
        'resource_availability': 0.85
    },
    'PostgreSQL DBA': {
        'complexity': 0.8,
        'market_demand': 0.85,
        'learning_curve': 0.75,
        'resource_availability': 0.75
    },
    'MLOps Engineer': {
        'complexity': 0.9,
        'market_demand': 0.9,
        'learning_curve': 0.85,
        'resource_availability': 0.7
    }
}

class SkillRatingEnsemble:
    def __init__(self):
        self.models = {
            'rf': RandomForestRegressor(n_estimators=100, random_state=42),
            'gb': GradientBoostingRegressor(n_estimators=100, random_state=42),
        }
        
        # Adjusted feature weights for better differentiation
        self.feature_weights = {
            'complexity': 0.30,        # Higher weight for difficulty level
            'market_demand': 0.35,     # Highest weight for industry relevance
            'learning_curve': 0.20,    # Moderate weight for learning difficulty
            'resource_availability': 0.15  # Lower weight for resource availability
        }
    
    def calculate_ensemble_rating(self, skill_features):
        try:
            # Calculate base score using weighted features
            base_score = (
                skill_features['complexity'] * self.feature_weights['complexity'] +
                skill_features['market_demand'] * self.feature_weights['market_demand'] +
                skill_features['learning_curve'] * self.feature_weights['learning_curve'] +
                skill_features['resource_availability'] * self.feature_weights['resource_availability']
            )
            
            # Apply non-linear transformation for better distribution
            transformed_score = np.power(base_score, 1.2)  # Non-linear scaling
            
            # Scale to 1-5 range with more variation
            rating = 1 + (transformed_score * 4)  # Ensures minimum 1, maximum 5
            
            # Add small random variation to prevent identical ratings
            rating += np.random.uniform(-0.1, 0.1)
            
            # Round to 1 decimal place and ensure bounds
            final_rating = min(max(round(rating, 1), 1.0), 5.0)
            
            return final_rating
            
        except Exception as e:
            print(f"Error calculating ensemble rating: {str(e)}")
            return 4.0  # Default fallback rating

    def get_rating_explanation(self, skill_features):
        """
        Generate an explanation for the rating
        """
        try:
            rating = self.calculate_ensemble_rating(skill_features)
            
            # Calculate individual feature contributions
            contributions = {
                'Complexity': skill_features['complexity'] * self.feature_weights['complexity'],
                'Market Demand': skill_features['market_demand'] * self.feature_weights['market_demand'],
                'Learning Curve': skill_features['learning_curve'] * self.feature_weights['learning_curve'],
                'Resource Availability': skill_features['resource_availability'] * self.feature_weights['resource_availability']
            }
            
            # Generate explanation text
            explanation = f"Rating {rating}/5 based on:\n"
            for factor, value in contributions.items():
                explanation += f"- {factor}: {value:.2f}\n"
            
            return explanation
            
        except Exception as e:
            print(f"Error generating rating explanation: {str(e)}")
            return "Rating explanation unavailable"

# Initialize the ensemble
rating_ensemble = SkillRatingEnsemble()

# Update all skill ratings using the ensemble
for skill_name in skills_data['Skill Name']:
    if skill_name in skill_features:
        features = skill_features[skill_name]
        ensemble_rating = rating_ensemble.calculate_ensemble_rating(features)
        skills_data.loc[skills_data['Skill Name'] == skill_name, 'Rating'] = ensemble_rating

# Update the documentation content with more concepts
@app.route('/documentation/<skill>/<topic>')
def get_documentation(skill, topic):
    # Part 1: First 5 Skills (Frontend, Backend, DevOps, Full Stack, Android Development)
    documentation_content = {
        'Frontend Development': {
            'HTML': {
                'title': 'HTML Documentation',
                'source': 'MDN & W3Schools',
                'content': """
                    <div class="doc-grid">
                        <!-- HTML Fundamentals -->
                        <div class="doc-section">
                            <h3>HTML Basics</h3>
                            <div class="content-list">
                                <a href="#html-intro" class="doc-item">
                                    <i class="fas fa-info-circle"></i>
                                    <span>Introduction to HTML</span>
                                </a>
                                <a href="#html-structure" class="doc-item">
                                    <i class="fas fa-sitemap"></i>
                                    <span>Document Structure</span>
                                </a>
                                <a href="#html-elements" class="doc-item">
                                    <i class="fas fa-cube"></i>
                                    <span>Elements & Tags</span>
                                </a>
                                <a href="#html-attributes" class="doc-item">
                                    <i class="fas fa-tags"></i>
                                    <span>Attributes</span>
                                </a>
                                <a href="#html-comments" class="doc-item">
                                    <i class="fas fa-comment"></i>
                                    <span>Comments</span>
                                </a>
                                <a href="#html-doctype" class="doc-item">
                                    <i class="fas fa-file-code"></i>
                                    <span>DOCTYPE Declaration</span>
                                </a>
                                <a href="#html-meta" class="doc-item">
                                    <i class="fas fa-globe"></i>
                                    <span>Meta Tags</span>
                                </a>
                            </div>
                        </div>

                        <!-- Text Content -->
                        <div class="doc-section">
                            <h3>Text Content</h3>
                            <div class="content-list">
                                <a href="#html-headings" class="doc-item">
                                    <i class="fas fa-heading"></i>
                                    <span>Headings (h1-h6)</span>
                                </a>
                                <a href="#html-paragraphs" class="doc-item">
                                    <i class="fas fa-paragraph"></i>
                                    <span>Paragraphs</span>
                                </a>
                                <a href="#html-formatting" class="doc-item">
                                    <i class="fas fa-font"></i>
                                    <span>Text Formatting</span>
                                </a>
                                <a href="#html-quotes" class="doc-item">
                                    <i class="fas fa-quote-right"></i>
                                    <span>Quotations</span>
                                </a>
                                <a href="#html-colors" class="doc-item">
                                    <i class="fas fa-palette"></i>
                                    <span>Colors</span>
                                </a>
                                <a href="#html-links" class="doc-item">
                                    <i class="fas fa-link"></i>
                                    <span>Links & Navigation</span>
                                </a>
                                <a href="#html-images" class="doc-item">
                                    <i class="fas fa-image"></i>
                                    <span>Images</span>
                                </a>
                            </div>
                        </div>

                        <!-- Lists & Tables -->
                        <div class="doc-section">
                            <h3>Lists & Tables</h3>
                            <div class="content-list">
                                <a href="#html-lists-ordered" class="doc-item">
                                    <i class="fas fa-list-ol"></i>
                                    <span>Ordered Lists</span>
                                </a>
                                <a href="#html-lists-unordered" class="doc-item">
                                    <i class="fas fa-list-ul"></i>
                                    <span>Unordered Lists</span>
                                </a>
                                <a href="#html-lists-description" class="doc-item">
                                    <i class="fas fa-indent"></i>
                                    <span>Description Lists</span>
                                </a>
                                <a href="#html-tables-basic" class="doc-item">
                                    <i class="fas fa-table"></i>
                                    <span>Basic Tables</span>
                                </a>
                                <a href="#html-tables-advanced" class="doc-item">
                                    <i class="fas fa-border-all"></i>
                                    <span>Advanced Tables</span>
                                </a>
                                <a href="#html-tables-layout" class="doc-item">
                                    <i class="fas fa-th"></i>
                                    <span>Table Layout</span>
                                </a>
                            </div>
                        </div>

                        <!-- Forms & Input -->
                        <div class="doc-section">
                            <h3>Forms & Input</h3>
                            <div class="content-list">
                                <a href="#html-forms-basic" class="doc-item">
                                    <i class="fas fa-wpforms"></i>
                                    <span>Basic Forms</span>
                                </a>
                                <a href="#html-input-types" class="doc-item">
                                    <i class="fas fa-keyboard"></i>
                                    <span>Input Types</span>
                                </a>
                                <a href="#html-form-attributes" class="doc-item">
                                    <i class="fas fa-sliders-h"></i>
                                    <span>Form Attributes</span>
                                </a>
                                <a href="#html-form-elements" class="doc-item">
                                    <i class="fas fa-check-square"></i>
                                    <span>Form Elements</span>
                                </a>
                                <a href="#html-input-validation" class="doc-item">
                                    <i class="fas fa-check-circle"></i>
                                    <span>Form Validation</span>
                                </a>
                            </div>
                        </div>

                        <!-- Semantic HTML -->
                        <div class="doc-section">
                            <h3>Semantic HTML</h3>
                            <div class="content-list">
                                <a href="#html-semantic-elements" class="doc-item">
                                    <i class="fas fa-code"></i>
                                    <span>Semantic Elements</span>
                                </a>
                                <a href="#html-layout-elements" class="doc-item">
                                    <i class="fas fa-th-large"></i>
                                    <span>Layout Elements</span>
                                </a>
                                <a href="#html-header-footer" class="doc-item">
                                    <i class="fas fa-window-maximize"></i>
                                    <span>Header & Footer</span>
                                </a>
                                <a href="#html-nav-aside" class="doc-item">
                                    <i class="fas fa-bars"></i>
                                    <span>Navigation & Aside</span>
                                </a>
                                <a href="#html-article-section" class="doc-item">
                                    <i class="fas fa-newspaper"></i>
                                    <span>Article & Section</span>
                                </a>
                            </div>
                        </div>

                        <!-- Multimedia -->
                        <div class="doc-section">
                            <h3>Multimedia</h3>
                            <div class="content-list">
                                <a href="#html-audio" class="doc-item">
                                    <i class="fas fa-volume-up"></i>
                                    <span>Audio</span>
                                </a>
                                <a href="#html-video" class="doc-item">
                                    <i class="fas fa-video"></i>
                                    <span>Video</span>
                                </a>
                                <a href="#html-iframe" class="doc-item">
                                    <i class="fas fa-square"></i>
                                    <span>iframes</span>
                                </a>
                                <a href="#html-svg" class="doc-item">
                                    <i class="fas fa-bezier-curve"></i>
                                    <span>SVG</span>
                                </a>
                                <a href="#html-canvas" class="doc-item">
                                    <i class="fas fa-paint-brush"></i>
                                    <span>Canvas</span>
                                </a>
                            </div>
                        </div>
                    </div>
                """
            },
            'CSS': {
                'title': 'CSS Documentation',
                'source': 'MDN & W3Schools',
                'content': """
                    <div class="doc-grid">
                        <!-- CSS Fundamentals -->
                        <div class="doc-section">
                            <h3>CSS Basics</h3>
                            <div class="content-list">
                                <a href="#css-intro" class="doc-item">
                                    <i class="fas fa-info-circle"></i>
                                    <span>Introduction to CSS</span>
                                </a>
                                <a href="#css-syntax" class="doc-item">
                                    <i class="fas fa-code"></i>
                                    <span>CSS Syntax</span>
                                </a>
                                <a href="#css-selectors" class="doc-item">
                                    <i class="fas fa-mouse-pointer"></i>
                                    <span>Selectors</span>
                                </a>
                                <a href="#css-comments" class="doc-item">
                                    <i class="fas fa-comment"></i>
                                    <span>Comments</span>
                                </a>
                                <a href="#css-cascade" class="doc-item">
                                    <i class="fas fa-stream"></i>
                                    <span>Cascading & Inheritance</span>
                                </a>
                                <a href="#css-specificity" class="doc-item">
                                    <i class="fas fa-layer-group"></i>
                                    <span>Specificity</span>
                                </a>
                            </div>
                        </div>

                        <!-- Box Model -->
                        <div class="doc-section">
                            <h3>Box Model</h3>
                            <div class="content-list">
                                <a href="#css-box-model" class="doc-item">
                                    <i class="fas fa-box"></i>
                                    <span>Box Model Concept</span>
                                </a>
                                <a href="#css-margin" class="doc-item">
                                    <i class="fas fa-external-link-square-alt"></i>
                                    <span>Margin</span>
                                </a>
                                <a href="#css-padding" class="doc-item">
                                    <i class="fas fa-expand"></i>
                                    <span>Padding</span>
                                </a>
                                <a href="#css-border" class="doc-item">
                                    <i class="fas fa-border-style"></i>
                                    <span>Border</span>
                                </a>
                                <a href="#css-outline" class="doc-item">
                                    <i class="fas fa-square-full"></i>
                                    <span>Outline</span>
                                </a>
                                <a href="#css-dimensions" class="doc-item">
                                    <i class="fas fa-arrows-alt"></i>
                                    <span>Width & Height</span>
                                </a>
                            </div>
                        </div>

                        <!-- Layout & Positioning -->
                        <div class="doc-section">
                            <h3>Layout & Positioning</h3>
                            <div class="content-list">
                                <a href="#css-display" class="doc-item">
                                    <i class="fas fa-desktop"></i>
                                    <span>Display Property</span>
                                </a>
                                <a href="#css-position" class="doc-item">
                                    <i class="fas fa-arrows-alt"></i>
                                    <span>Position Property</span>
                                </a>
                                <a href="#css-float" class="doc-item">
                                    <i class="fas fa-water"></i>
                                    <span>Float & Clear</span>
                                </a>
                                <a href="#css-flexbox" class="doc-item">
                                    <i class="fas fa-box-open"></i>
                                    <span>Flexbox</span>
                                </a>
                                <a href="#css-grid" class="doc-item">
                                    <i class="fas fa-th"></i>
                                    <span>Grid</span>
                                </a>
                                <a href="#css-columns" class="doc-item">
                                    <i class="fas fa-columns"></i>
                                    <span>Multi-column Layout</span>
                                </a>
                            </div>
                        </div>

                        <!-- Visual Styling -->
                        <div class="doc-section">
                            <h3>Visual Styling</h3>
                            <div class="content-list">
                                <a href="#css-colors" class="doc-item">
                                    <i class="fas fa-palette"></i>
                                    <span>Colors & Opacity</span>
                                </a>
                                <a href="#css-background" class="doc-item">
                                    <i class="fas fa-fill-drip"></i>
                                    <span>Backgrounds</span>
                                </a>
                                <a href="#css-gradients" class="doc-item">
                                    <i class="fas fa-gradient"></i>
                                    <span>Gradients</span>
                                </a>
                                <a href="#css-shadows" class="doc-item">
                                    <i class="fas fa-clone"></i>
                                    <span>Shadows</span>
                                </a>
                                <a href="#css-filters" class="doc-item">
                                    <i class="fas fa-adjust"></i>
                                    <span>Filters</span>
                                </a>
                            </div>
                        </div>

                        <!-- Typography -->
                        <div class="doc-section">
                            <h3>Typography</h3>
                            <div class="content-list">
                                <a href="#css-fonts" class="doc-item">
                                    <i class="fas fa-font"></i>
                                    <span>Fonts</span>
                                </a>
                                <a href="#css-text" class="doc-item">
                                    <i class="fas fa-text-height"></i>
                                    <span>Text Properties</span>
                                </a>
                                <a href="#css-web-fonts" class="doc-item">
                                    <i class="fas fa-globe"></i>
                                    <span>Web Fonts</span>
                                </a>
                                <a href="#css-text-effects" class="doc-item">
                                    <i class="fas fa-magic"></i>
                                    <span>Text Effects</span>
                                </a>
                            </div>
                        </div>

                        <!-- Transforms & Animations -->
                        <div class="doc-section">
                            <h3>Transforms & Animations</h3>
                            <div class="content-list">
                                <a href="#css-transforms" class="doc-item">
                                    <i class="fas fa-vector-square"></i>
                                    <span>Transforms</span>
                                </a>
                                <a href="#css-transitions" class="doc-item">
                                    <i class="fas fa-exchange-alt"></i>
                                    <span>Transitions</span>
                                </a>
                                <a href="#css-animations" class="doc-item">
                                    <i class="fas fa-film"></i>
                                    <span>Animations</span>
                                </a>
                                <a href="#css-keyframes" class="doc-item">
                                    <i class="fas fa-key"></i>
                                    <span>Keyframes</span>
                                </a>
                            </div>
                        </div>

                        <!-- Responsive Design -->
                        <div class="doc-section">
                            <h3>Responsive Design</h3>
                            <div class="content-list">
                                <a href="#css-media-queries" class="doc-item">
                                    <i class="fas fa-mobile-alt"></i>
                                    <span>Media Queries</span>
                                </a>
                                <a href="#css-responsive-images" class="doc-item">
                                    <i class="fas fa-image"></i>
                                    <span>Responsive Images</span>
                                </a>
                                <a href="#css-viewport" class="doc-item">
                                    <i class="fas fa-tablet-alt"></i>
                                    <span>Viewport</span>
                                </a>
                                <a href="#css-units" class="doc-item">
                                    <i class="fas fa-ruler"></i>
                                    <span>Responsive Units</span>
                                </a>
                            </div>
                        </div>
                    </div>
                """
            },
            'JavaScript': {
                'title': 'JavaScript Documentation',
                'source': 'MDN & JavaScript.info',
                'content': """
                    <div class="doc-grid">
                        <!-- JS Fundamentals -->
                        <div class="doc-section">
                            <h3>JavaScript Basics</h3>
                            <div class="content-list">
                                <a href="#js-intro" class="doc-item">
                                    <i class="fas fa-info-circle"></i>
                                    <span>Introduction to JavaScript</span>
                                </a>
                                <a href="#js-syntax" class="doc-item">
                                    <i class="fas fa-code"></i>
                                    <span>Syntax & Comments</span>
                                </a>
                                <a href="#js-variables" class="doc-item">
                                    <i class="fas fa-box"></i>
                                    <span>Variables & Scope</span>
                                </a>
                                <a href="#js-datatypes" class="doc-item">
                                    <i class="fas fa-list"></i>
                                    <span>Data Types</span>
                                </a>
                                <a href="#js-operators" class="doc-item">
                                    <i class="fas fa-calculator"></i>
                                    <span>Operators</span>
                                </a>
                                <a href="#js-control-flow" class="doc-item">
                                    <i class="fas fa-random"></i>
                                    <span>Control Flow</span>
                                </a>
                                <a href="#js-loops" class="doc-item">
                                    <i class="fas fa-redo"></i>
                                    <span>Loops</span>
                                </a>
                            </div>
                        </div>

                        <!-- Functions -->
                        <div class="doc-section">
                            <h3>Functions</h3>
                            <div class="content-list">
                                <a href="#js-functions-basic" class="doc-item">
                                    <i class="fas fa-code"></i>
                                    <span>Function Basics</span>
                                </a>
                                <a href="#js-arrow-functions" class="doc-item">
                                    <i class="fas fa-arrow-right"></i>
                                    <span>Arrow Functions</span>
                                </a>
                                <a href="#js-parameters" class="doc-item">
                                    <i class="fas fa-exchange-alt"></i>
                                    <span>Parameters & Arguments</span>
                                </a>
                                <a href="#js-callbacks" class="doc-item">
                                    <i class="fas fa-phone-volume"></i>
                                    <span>Callbacks</span>
                                </a>
                                <a href="#js-closures" class="doc-item">
                                    <i class="fas fa-lock"></i>
                                    <span>Closures</span>
                                </a>
                            </div>
                        </div>

                        <!-- Objects & Arrays -->
                        <div class="doc-section">
                            <h3>Objects & Arrays</h3>
                            <div class="content-list">
                                <a href="#js-objects" class="doc-item">
                                    <i class="fas fa-cube"></i>
                                    <span>Objects</span>
                                </a>
                                <a href="#js-arrays" class="doc-item">
                                    <i class="fas fa-layer-group"></i>
                                    <span>Arrays</span>
                                </a>
                                <a href="#js-array-methods" class="doc-item">
                                    <i class="fas fa-tools"></i>
                                    <span>Array Methods</span>
                                </a>
                                <a href="#js-destructuring" class="doc-item">
                                    <i class="fas fa-boxes"></i>
                                    <span>Destructuring</span>
                                </a>
                                <a href="#js-spread-rest" class="doc-item">
                                    <i class="fas fa-ellipsis-h"></i>
                                    <span>Spread & Rest</span>
                                </a>
                            </div>
                        </div>

                        <!-- DOM Manipulation -->
                        <div class="doc-section">
                            <h3>DOM Manipulation</h3>
                            <div class="content-list">
                                <a href="#js-dom-intro" class="doc-item">
                                    <i class="fas fa-sitemap"></i>
                                    <span>DOM Introduction</span>
                                </a>
                                <a href="#js-dom-selectors" class="doc-item">
                                    <i class="fas fa-search"></i>
                                    <span>DOM Selectors</span>
                                </a>
                                <a href="#js-dom-manipulation" class="doc-item">
                                    <i class="fas fa-edit"></i>
                                    <span>Manipulating Elements</span>
                                </a>
                                <a href="#js-events" class="doc-item">
                                    <i class="fas fa-bolt"></i>
                                    <span>Events</span>
                                </a>
                                <a href="#js-event-handling" class="doc-item">
                                    <i class="fas fa-hand-pointer"></i>
                                    <span>Event Handling</span>
                                </a>
                            </div>
                        </div>

                        <!-- Asynchronous JS -->
                        <div class="doc-section">
                            <h3>Asynchronous JavaScript</h3>
                            <div class="content-list">
                                <a href="#js-promises" class="doc-item">
                                    <i class="fas fa-handshake"></i>
                                    <span>Promises</span>
                                </a>
                                <a href="#js-async-await" class="doc-item">
                                    <i class="fas fa-clock"></i>
                                    <span>Async/Await</span>
                                </a>
                                <a href="#js-fetch" class="doc-item">
                                    <i class="fas fa-download"></i>
                                    <span>Fetch API</span>
                                </a>
                                <a href="#js-ajax" class="doc-item">
                                    <i class="fas fa-exchange-alt"></i>
                                    <span>AJAX</span>
                                </a>
                            </div>
                        </div>

                        <!-- ES6+ Features -->
                        <div class="doc-section">
                            <h3>Modern JavaScript</h3>
                            <div class="content-list">
                                <a href="#js-modules" class="doc-item">
                                    <i class="fas fa-puzzle-piece"></i>
                                    <span>Modules</span>
                                </a>
                                <a href="#js-classes" class="doc-item">
                                    <i class="fas fa-cube"></i>
                                    <span>Classes</span>
                                </a>
                                <a href="#js-iterators" class="doc-item">
                                    <i class="fas fa-redo"></i>
                                    <span>Iterators & Generators</span>
                                </a>
                                <a href="#js-map-set" class="doc-item">
                                    <i class="fas fa-map"></i>
                                    <span>Map & Set</span>
                                </a>
                            </div>
                        </div>
                    </div>
                """
            },
            'Framework': {  # This matches the node name from your graph
                'title': 'Frontend Frameworks',
                'content': """
                    <div class="doc-section">
                        <h3>Frontend Frameworks</h3>
                        <div class="content-list">
                            <a href="#react" class="doc-item">
                                <i class="fab fa-react"></i>
                                <span>React</span>
                                <ul>
                                    <li>Components & Props</li>
                                    <li>Hooks & State</li>
                                    <li>Context API</li>
                                    <li>Redux/MobX</li>
                                </ul>
                            </a>
                            <a href="#vue" class="doc-item">
                                <i class="fab fa-vuejs"></i>
                                <span>Vue.js</span>
                                <ul>
                                    <li>Vue Components</li>
                                    <li>Vue Router</li>
                                    <li>Vuex State</li>
                                    <li>Composition API</li>
                                </ul>
                            </a>
                            <a href="#angular" class="doc-item">
                                <i class="fab fa-angular"></i>
                                <span>Angular</span>
                                <ul>
                                    <li>Components & Services</li>
                                    <li>Angular Router</li>
                                    <li>RxJS & NgRx</li>
                                    <li>Dependency Injection</li>
                                </ul>
                            </a>
                            <a href="#svelte" class="doc-item">
                                <i class="fas fa-code"></i>
                                <span>Svelte</span>
                                <ul>
                                    <li>Reactive Declarations</li>
                                    <li>Stores</li>
                                    <li>Animations</li>
                                    <li>SvelteKit</li>
                                </ul>
                            </a>
                        </div>

                        <div class="doc-section mt-4">
                            <h3>Build Tools & Ecosystem</h3>
                            <div class="content-list">
                                <a href="#bundlers" class="doc-item">
                                    <i class="fas fa-box"></i>
                                    <span>Build Tools</span>
                                    <ul>
                                        <li>Vite</li>
                                        <li>Webpack</li>
                                        <li>Rollup</li>
                                        <li>ESBuild</li>
                                    </ul>
                                </a>
                                <a href="#testing" class="doc-item">
                                    <i class="fas fa-vial"></i>
                                    <span>Testing Tools</span>
                                    <ul>
                                        <li>Jest</li>
                                        <li>React Testing Library</li>
                                        <li>Cypress</li>
                                        <li>Vitest</li>
                                    </ul>
                                </a>
                                <a href="#deployment" class="doc-item">
                                    <i class="fas fa-rocket"></i>
                                    <span>Deployment</span>
                                    <ul>
                                        <li>Vercel</li>
                                        <li>Netlify</li>
                                        <li>GitHub Pages</li>
                                        <li>Firebase Hosting</li>
                                    </ul>
                                </a>
                            </div>
                        </div>
                    </div>
                """
            }
        },
        'Backend Development': {
            'Express.js': {
                'title': 'Express.js Framework',
                'content': """
                    <div class="doc-section">
                        <h3>Express Fundamentals</h3>
                        <div class="content-list">
                            <a href="#express-basics" class="doc-item">
                                <i class="fas fa-server"></i>
                                <span>Express Basics</span>
                            </a>
                            <a href="#routing" class="doc-item">
                                <i class="fas fa-route"></i>
                                <span>Routing</span>
                            </a>
                            <a href="#middleware" class="doc-item">
                                <i class="fas fa-plug"></i>
                                <span>Middleware</span>
                            </a>
                            <a href="#error-handling" class="doc-item">
                                <i class="fas fa-exclamation-triangle"></i>
                                <span>Error Handling</span>
                            </a>
                            <a href="#template-engines" class="doc-item">
                                <i class="fas fa-file-code"></i>
                                <span>Template Engines</span>
                            </a>
                            <a href="#database-integration" class="doc-item">
                                <i class="fas fa-database"></i>
                                <span>Database Integration</span>
                            </a>
                            <a href="#authentication" class="doc-item">
                                <i class="fas fa-lock"></i>
                                <span>Authentication</span>
                            </a>
                        </div>
                    </div>
                """
            },
            
            'Databases': {
                'title': 'Database Systems',
                'content': """
                    <div class="doc-section">
                        <h3>SQL Databases</h3>
                        <div class="content-list">
                            <a href="#sql-basics" class="doc-item">
                                <i class="fas fa-database"></i>
                                <span>SQL Fundamentals</span>
                            </a>
                            <a href="#mysql" class="doc-item">
                                <i class="fas fa-dolphin"></i>
                                <span>MySQL</span>
                            </a>
                            <a href="#postgresql" class="doc-item">
                                <i class="fas fa-elephant"></i>
                                <span>PostgreSQL</span>
                            </a>
                        </div>

                        <h3>NoSQL Databases</h3>
                        <div class="content-list">
                            <a href="#mongodb" class="doc-item">
                                <i class="fas fa-leaf"></i>
                                <span>MongoDB</span>
                            </a>
                            <a href="#redis" class="doc-item">
                                <i class="fas fa-bolt"></i>
                                <span>Redis</span>
                            </a>
                        </div>
                    </div>
                """
            }
        },
        'DevOps': {
            'title': 'DevOps Engineering',
            'content': """
                <div class="doc-grid">
                    <!-- Version Control -->
                    <div class="doc-section">
                        <h3>Version Control & Git</h3>
                        <div class="content-list">
                            <a href="#git-basics" class="doc-item">
                                <i class="fab fa-git-alt"></i>
                                <span>Git Fundamentals</span>
                                <ul>
                                    <li>Basic Git Commands</li>
                                    <li>Repository Management</li>
                                    <li>Commit History</li>
                                    <li>Git Config & Setup</li>
                                </ul>
                            </a>
                            <a href="#git-branching" class="doc-item">
                                <i class="fas fa-code-branch"></i>
                                <span>Branching & Merging</span>
                                <ul>
                                    <li>Branch Management</li>
                                    <li>Merge Strategies</li>
                                    <li>Conflict Resolution</li>
                                    <li>Rebasing</li>
                                </ul>
                            </a>
                            <a href="#git-workflow" class="doc-item">
                                <i class="fas fa-project-diagram"></i>
                                <span>Git Workflows</span>
                                <ul>
                                    <li>GitFlow</li>
                                    <li>Trunk-Based Development</li>
                                    <li>Feature Branch Workflow</li>
                                    <li>Pull Request Process</li>
                                </ul>
                            </a>
                        </div>
                    </div>

                    <!-- CI/CD -->
                    <div class="doc-section">
                        <h3>CI/CD Pipeline</h3>
                        <div class="content-list">
                            <a href="#jenkins" class="doc-item">
                                <i class="fas fa-infinity"></i>
                                <span>Jenkins</span>
                                <ul>
                                    <li>Pipeline as Code</li>
                                    <li>Jenkinsfile</li>
                                    <li>Build Automation</li>
                                    <li>Plugin Management</li>
                                </ul>
                            </a>
                            <a href="#github-actions" class="doc-item">
                                <i class="fab fa-github"></i>
                                <span>GitHub Actions</span>
                                <ul>
                                    <li>Workflow Configuration</li>
                                    <li>Action Types</li>
                                    <li>Environment Secrets</li>
                                    <li>Matrix Builds</li>
                                </ul>
                            </a>
                            <a href="#gitlab-ci" class="doc-item">
                                <i class="fab fa-gitlab"></i>
                                <span>GitLab CI</span>
                                <ul>
                                    <li>CI/CD Configuration</li>
                                    <li>Pipeline Stages</li>
                                    <li>Artifacts & Caching</li>
                                    <li>Runner Management</li>
                                </ul>
                            </a>
                        </div>
                    </div>

                    <!-- Containerization -->
                    <div class="doc-section">
                        <h3>Containerization</h3>
                        <div class="content-list">
                            <a href="#docker" class="doc-item">
                                <i class="fab fa-docker"></i>
                                <span>Docker</span>
                                <ul>
                                    <li>Dockerfile</li>
                                    <li>Container Management</li>
                                    <li>Docker Networks</li>
                                    <li>Volume Management</li>
                                </ul>
                            </a>
                            <a href="#docker-compose" class="doc-item">
                                <i class="fas fa-cubes"></i>
                                <span>Docker Compose</span>
                                <ul>
                                    <li>Service Definition</li>
                                    <li>Multi-container Apps</li>
                                    <li>Environment Variables</li>
                                    <li>Network Configuration</li>
                                </ul>
                            </a>
                            <a href="#kubernetes" class="doc-item">
                                <i class="fas fa-dharmachakra"></i>
                                <span>Kubernetes</span>
                                <ul>
                                    <li>Pod Management</li>
                                    <li>Deployments & Services</li>
                                    <li>ConfigMaps & Secrets</li>
                                    <li>Helm Charts</li>
                                </ul>
                            </a>
                        </div>
                    </div>

                    <!-- Infrastructure as Code -->
                    <div class="doc-section">
                        <h3>Infrastructure as Code</h3>
                        <div class="content-list">
                            <a href="#terraform" class="doc-item">
                                <i class="fas fa-network-wired"></i>
                                <span>Terraform</span>
                                <ul>
                                    <li>HCL Syntax</li>
                                    <li>Resource Management</li>
                                    <li>State Management</li>
                                    <li>Modules & Workspaces</li>
                                </ul>
                            </a>
                            <a href="#ansible" class="doc-item">
                                <i class="fas fa-cogs"></i>
                                <span>Ansible</span>
                                <ul>
                                    <li>Playbooks</li>
                                    <li>Roles & Tasks</li>
                                    <li>Inventory Management</li>
                                    <li>Vault & Security</li>
                                </ul>
                            </a>
                            <a href="#cloudformation" class="doc-item">
                                <i class="fab fa-aws"></i>
                                <span>CloudFormation</span>
                                <ul>
                                    <li>Template Structure</li>
                                    <li>Stack Management</li>
                                    <li>Resource Dependencies</li>
                                    <li>Nested Stacks</li>
                                </ul>
                            </a>
                        </div>
                    </div>

                    <!-- Cloud Platforms -->
                    <div class="doc-section">
                        <h3>Cloud Services</h3>
                        <div class="content-list">
                            <a href="#aws" class="doc-item">
                                <i class="fab fa-aws"></i>
                                <span>AWS</span>
                                <ul>
                                    <li>EC2 & ECS</li>
                                    <li>S3 & RDS</li>
                                    <li>Lambda & API Gateway</li>
                                    <li>CloudWatch & IAM</li>
                                </ul>
                            </a>
                            <a href="#azure" class="doc-item">
                                <i class="fab fa-microsoft"></i>
                                <span>Azure</span>
                                <ul>
                                    <li>Virtual Machines</li>
                                    <li>App Services</li>
                                    <li>Azure Functions</li>
                                    <li>Azure DevOps</li>
                                </ul>
                            </a>
                            <a href="#gcp" class="doc-item">
                                <i class="fab fa-google"></i>
                                <span>Google Cloud</span>
                                <ul>
                                    <li>Compute Engine</li>
                                    <li>Cloud Run</li>
                                    <li>Cloud Functions</li>
                                    <li>Cloud Build</li>
                                </ul>
                            </a>
                        </div>
                    </div>

                    <!-- Monitoring & Logging -->
                    <div class="doc-section">
                        <h3>Observability</h3>
                        <div class="content-list">
                            <a href="#monitoring" class="doc-item">
                                <i class="fas fa-chart-line"></i>
                                <span>Monitoring Tools</span>
                                <ul>
                                    <li>Prometheus</li>
                                    <li>Grafana</li>
                                    <li>Datadog</li>
                                    <li>New Relic</li>
                                </ul>
                            </a>
                            <a href="#logging" class="doc-item">
                                <i class="fas fa-clipboard-list"></i>
                                <span>Logging Solutions</span>
                                <ul>
                                    <li>ELK Stack</li>
                                    <li>Fluentd</li>
                                    <li>Splunk</li>
                                    <li>Loki</li>
                                </ul>
                            </a>
                            <a href="#tracing" class="doc-item">
                                <i class="fas fa-route"></i>
                                <span>Distributed Tracing</span>
                                <ul>
                                    <li>Jaeger</li>
                                    <li>Zipkin</li>
                                    <li>OpenTelemetry</li>
                                    <li>X-Ray</li>
                                </ul>
                            </a>
                        </div>
                    </div>
                </div>
            """
        },
        'Full Stack Development': {
            'title': 'Full Stack Web Development',
            'url': 'https://fullstackopen.com/',
            'content': """
                <!-- Full Stack development content -->
            """
        },
        'Android Development': {
            'title': 'Android App Development',
            'url': 'https://developer.android.com/docs',
            'content': """
                <!-- Android development content -->
            """
        }
    }

    # Part 2: Next 5 Skills (Blockchain, Software Architect, Cyber Security, Data Science, DevRel Engineer)
    documentation_content.update({
        'Blockchain Development': {
            'title': 'Blockchain & Smart Contracts',
            'url': 'https://ethereum.org/developers',
            'content': """
                <div class="doc-grid">
                    <div class="doc-section">
                        <h3>Blockchain Fundamentals</h3>
                        <div class="content-list">
                            <a href="https://docs.soliditylang.org/en/latest/" class="doc-item">
                                <i class="fas fa-link"></i>
                                <span>Solidity Programming</span>
                            </a>
                            <a href="https://web3js.readthedocs.io/" class="doc-item">
                                <i class="fas fa-network-wired"></i>
                                <span>Web3.js Integration</span>
                            </a>
                            <a href="https://docs.ethers.org/v5/" class="doc-item">
                                <i class="fas fa-ethernet"></i>
                                <span>Ethers.js Library</span>
                            </a>
                        </div>
                        <div class="interactive-element">
                            <h4>Smart Contract Playground:</h4>
                            <a href="https://remix.ethereum.org/" class="practice-link">
                                <i class="fas fa-code"></i>
                                Try Remix IDE
                            </a>
                        </div>
                    </div>
                    <div class="doc-section">
                        <h3>DApp Development</h3>
                        <div class="content-list">
                            <a href="https://docs.openzeppelin.com/" class="doc-item">
                                <i class="fas fa-shield-alt"></i>
                                <span>OpenZeppelin</span>
                            </a>
                            <a href="https://hardhat.org/docs" class="doc-item">
                                <i class="fas fa-hammer"></i>
                                <span>Hardhat Framework</span>
                            </a>
                        </div>
                    </div>
                </div>
            """
        },
        'Software Architect': {
            'title': 'Software Architecture',
            'url': 'https://martinfowler.com/architecture/',
            'content': """
                <div class="doc-grid">
                    <div class="doc-section">
                        <h3>Architecture Patterns</h3>
                        <div class="content-list">
                            <a href="https://microservices.io/patterns/microservices.html" class="doc-item">
                                <i class="fas fa-cubes"></i>
                                <span>Microservices Architecture</span>
                            </a>
                            <a href="https://docs.microsoft.com/en-us/azure/architecture/" class="doc-item">
                                <i class="fas fa-cloud"></i>
                                <span>Cloud Architecture</span>
                            </a>
                        </div>
                    </div>
                </div>
            """
        },
        # ... Similar detailed content for Cyber Security, Data Science, DevRel Engineer
    })

    # Part 3: Final 5 Skills (Technical Writer, Product Manager, QA Engineer, PostgreSQL DBA, MLOps Engineer)
    documentation_content.update({
        'Technical Writer': {
            'title': 'Technical Writing',
            'url': 'https://developers.google.com/tech-writing',
            'content': """
                <div class="doc-grid">
                    <div class="doc-section">
                        <h3>Documentation Best Practices</h3>
                        <div class="content-list">
                            <a href="https://www.writethedocs.org/guide/" class="doc-item">
                                <i class="fas fa-book"></i>
                                <span>Write the Docs Guide</span>
                            </a>
                            <a href="https://developers.google.com/style" class="doc-item">
                                <i class="fas fa-pencil-alt"></i>
                                <span>Google Developer Documentation Style Guide</span>
                            </a>
                        </div>
                        <div class="interactive-element">
                            <h4>Practice Exercise:</h4>
                            <div class="writing-prompt">
                                <p>Create API documentation for a simple REST endpoint</p>
                                <!-- Interactive documentation exercise -->
                            </div>
                        </div>
                    </div>
                </div>
            """
        },
        'MLOps Engineer': {
            'title': 'MLOps Engineering',
            'content': """
                <div class="doc-grid">
                    <div class="doc-section">
                        <h3>ML Infrastructure</h3>
                        <div class="content-list">
                            <a href="#ml-pipelines" class="doc-item">
                                <i class="fas fa-stream"></i>
                                <span>ML Pipelines</span>
                            </a>
                            <a href="#model-serving" class="doc-item">
                                <i class="fas fa-server"></i>
                                <span>Model Serving</span>
                            </a>
                            <a href="#feature-stores" class="doc-item">
                                <i class="fas fa-database"></i>
                                <span>Feature Stores</span>
                            </a>
                            <a href="#model-registry" class="doc-item">
                                <i class="fas fa-archive"></i>
                                <span>Model Registry</span>
                            </a>
                        </div>
                    </div>

                    <div class="doc-section">
                        <h3>ML Tools</h3>
                        <div class="content-list">
                            <a href="#kubeflow" class="doc-item">
                                <i class="fas fa-dharmachakra"></i>
                                <span>Kubeflow</span>
                            </a>
                            <a href="#mlflow" class="doc-item">
                                <i class="fas fa-project-diagram"></i>
                                <span>MLflow</span>
                            </a>
                            <a href="#airflow" class="doc-item">
                                <i class="fas fa-wind"></i>
                                <span>Airflow</span>
                            </a>
                            <a href="#tensorflow-extended" class="doc-item">
                                <i class="fab fa-tensorflow"></i>
                                <span>TensorFlow Extended</span>
                            </a>
                        </div>
                    </div>

                    <div class="doc-section">
                        <h3>Monitoring & Logging</h3>
                        <div class="content-list">
                            <a href="#model-monitoring" class="doc-item">
                                <i class="fas fa-chart-line"></i>
                                <span>Model Monitoring</span>
                            </a>
                            <a href="#data-drift" class="doc-item">
                                <i class="fas fa-random"></i>
                                <span>Data Drift Detection</span>
                            </a>
                            <a href="#logging-systems" class="doc-item">
                                <i class="fas fa-clipboard-list"></i>
                                <span>Logging Systems</span>
                            </a>
                            <a href="#alerting" class="doc-item">
                                <i class="fas fa-bell"></i>
                                <span>Alerting</span>
                            </a>
                        </div>
                    </div>
                </div>
            """
        },
        'PostgreSQL DBA': {
            'title': 'PostgreSQL Database Administration',
            'url': 'https://www.postgresql.org/docs/current/',
            'content': """
                <div class="doc-grid">
                    <div class="doc-section">
                        <h3>Database Administration</h3>
                        <div class="content-list">
                            <a href="https://www.postgresql.org/docs/current/admin.html" class="doc-item">
                                <i class="fas fa-database"></i>
                                <span>Database Management</span>
                            </a>
                            <a href="https://www.postgresql.org/docs/current/performance-tips.html" class="doc-item">
                                <i class="fas fa-tachometer-alt"></i>
                                <span>Performance Tuning</span>
                            </a>
                        </div>
                        <div class="interactive-element">
                            <h4>SQL Practice:</h4>
                            <!-- Interactive SQL exercises -->
                        </div>
                    </div>
                </div>
            """
        }
        # ... Similar detailed content for Product Manager and QA Engineer
    })

    # Common helper functions
    def get_skill_progress(skill_name):
        """Calculate and return skill progress"""
        pass

    def get_interactive_elements(skill_name):
        """Return interactive elements for skill"""
        pass

    def get_recommended_resources(skill_name):
        """Return curated learning resources"""
        pass

    try:
        skill_docs = documentation_content.get(skill, {})
        topic_docs = skill_docs.get(topic, {
            'title': 'Backend Development',
            'url': '#',
            'content': f"""
                <div class="doc-section">
                    {
                        # Choose Language section
                        '<h3>Choose Your Language & Framework</h3><div class="content-list">' + """
                            <a href="#python" class="doc-item">
                                <i class="fab fa-python"></i>
                                <span>Python</span>
                                <ul>
                                    <li>Django</li>
                                    <li>Flask</li>
                                    <li>FastAPI</li>
                                    <li>SQLAlchemy</li>
                                </ul>
                            </a>
                            <a href="#nodejs" class="doc-item">
                                <i class="fab fa-node-js"></i>
                                <span>Node.js</span>
                                <ul>
                                    <li>Express.js</li>
                                    <li>NestJS</li>
                                    <li>Prisma ORM</li>
                                    <li>Mongoose</li>
                                </ul>
                            </a>
                            <a href="#java" class="doc-item">
                                <i class="fab fa-java"></i>
                                <span>Java</span>
                                <ul>
                                    <li>Spring Boot</li>
                                    <li>Hibernate</li>
                                    <li>Maven/Gradle</li>
                                    <li>JPA</li>
                                </ul>
                            </a>
                            <a href="#go" class="doc-item">
                                <i class="fab fa-golang"></i>
                                <span>Go</span>
                                <ul>
                                    <li>Gin</li>
                                    <li>Echo</li>
                                    <li>GORM</li>
                                    <li>Go Modules</li>
                                </ul>
                        </div>""" if topic == 'Choose Language' else

                        # Database section
                        '<h3>Database Systems</h3><div class="content-list">' + """
                            <a href="#sql" class="doc-item">
                                <i class="fas fa-database"></i>
                                <span>SQL Databases</span>
                                <ul>
                                    <li>PostgreSQL</li>
                                    <li>MySQL</li>
                                    <li>SQL Queries</li>
                                    <li>Database Design</li>
                                </ul>
                            </a>
                            <a href="#nosql" class="doc-item">
                                <i class="fas fa-leaf"></i>
                                <span>NoSQL Databases</span>
                                <ul>
                                    <li>MongoDB</li>
                                    <li>Redis</li>
                                    <li>Elasticsearch</li>
                                    <li>Cassandra</li>
                                </ul>
                            </a>
                            <a href="#orm" class="doc-item">
                                <i class="fas fa-project-diagram"></i>
                                <span>ORM Concepts</span>
                                <ul>
                                    <li>Data Modeling</li>
                                    <li>Migrations</li>
                                    <li>Relationships</li>
                                    <li>Query Optimization</li>
                                </ul>
                            </a>
                        </div>""" if topic == 'Database' else

                        # API section
                        '<h3>API Development</h3><div class="content-list">' + """
                            <a href="#rest" class="doc-item">
                                <i class="fas fa-exchange-alt"></i>
                                <span>REST APIs</span>
                                <ul>
                                    <li>HTTP Methods</li>
                                    <li>Status Codes</li>
                                    <li>API Versioning</li>
                                    <li>Documentation (Swagger/OpenAPI)</li>
                                </ul>
                            </a>
                            <a href="#graphql" class="doc-item">
                                <i class="fas fa-project-diagram"></i>
                                <span>GraphQL</span>
                                <ul>
                                    <li>Schema Design</li>
                                    <li>Resolvers</li>
                                    <li>Mutations</li>
                                    <li>Subscriptions</li>
                                </ul>
                            </a>
                            <a href="#websockets" class="doc-item">
                                <i class="fas fa-plug"></i>
                                <span>WebSockets</span>
                                <ul>
                                    <li>Real-time Communication</li>
                                    <li>Socket.IO</li>
                                    <li>Event Handling</li>
                                    <li>Connection Management</li>
                                </ul>
                            </a>
                        </div>""" if topic == 'API' else

                        # Security section
                        '<h3>Security & Authentication</h3><div class="content-list">' + """
                            <a href="#auth" class="doc-item">
                                <i class="fas fa-shield-alt"></i>
                                <span>Authentication</span>
                                <ul>
                                    <li>JWT</li>
                                    <li>OAuth 2.0</li>
                                    <li>Session Management</li>
                                    <li>Password Hashing</li>
                                </ul>
                            </a>
                            <a href="#security" class="doc-item">
                                <i class="fas fa-lock"></i>
                                <span>Security Best Practices</span>
                                <ul>
                                    <li>CORS</li>
                                    <li>XSS Prevention</li>
                                    <li>CSRF Protection</li>
                                    <li>Input Validation</li>
                                </ul>
                            </a>
                            <a href="#authorization" class="doc-item">
                                <i class="fas fa-user-shield"></i>
                                <span>Authorization</span>
                                <ul>
                                    <li>Role-Based Access Control</li>
                                    <li>Permission Systems</li>
                                    <li>Middleware</li>
                                    <li>API Security</li>
                                </ul>
                        </div>""" if topic == 'Security' else ''
                    }
                </div>
            """
        })
        
        # Enhance response with additional features
        response_data = {
            **topic_docs,
            'progress': get_skill_progress(skill),
            'interactive_elements': get_interactive_elements(skill),
            'recommended_resources': get_recommended_resources(skill)
        }
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        recipient_email = data['email']
        subject = data['subject']
        content = data['content']

        # Create message
        msg = Message(
            subject=subject,
            sender=app.config['MAIL_USERNAME'],
            recipients=[recipient_email]
        )
        msg.body = content

        # Send email
        mail.send(msg)
        
        print(f"Email sent successfully to {recipient_email}")  # Debug log
        return jsonify({"success": True, "message": "Email sent successfully"})
        
    except Exception as e:
        print(f"Email Error: {str(e)}")  # Debug log
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/send_reminder_emails', methods=['POST'])
def send_reminder_emails():
    try:
        data = request.get_json()
        user_name = data.get('user_name')
        user_email = data.get('user_email')
        skill_name = data.get('skill_name')

        # Send notification to admin
        admin_msg = Message(
            'New Learning Journey Subscription',
            sender='aiskillcraft@gmail.com',
            recipients=['aiskillcraft@gmail.com']
        )
        admin_msg.body = f"""
            New Learning Journey Subscription:
            
            User Name: {user_name}
            User Email: {user_email}
            Selected Skill: {skill_name}
            
            This user has subscribed to receive reminders for the {skill_name} learning journey.
        """
        mail.send(admin_msg)

        return jsonify({"success": True}), 200

    except Exception as e:
        print(f"Email Error: {str(e)}")  # For debugging
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
