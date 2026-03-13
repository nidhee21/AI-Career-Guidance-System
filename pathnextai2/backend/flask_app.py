"""
flask_app.py - Run from project root: python backend/flask_app.py
Website: http://localhost:5000
"""
from flask import Flask, request, jsonify, send_from_directory
import requests, os

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
app = Flask(__name__, static_folder=FRONTEND_DIR)
FASTAPI_URL = "http://localhost:8001"

CAREER_DETAILS = {
    "Software Engineer":      {"icon":"💻","color":"#00a8ff","why":"Your strong Mathematics background and interest in technology make Software Engineering a natural fit. Your analytical thinking and problem-solving scores show you can handle complex coding challenges.","skills":["Python / JavaScript","Data Structures & Algorithms","System Design","Git & Version Control","Problem Solving"],"roadmap":["Learn Python via CS50 or freeCodeCamp","Study Data Structures & Algorithms on LeetCode","Build 3–5 personal projects","Learn web development basics","Apply for internships in 2nd year"],"colleges":["IIT Bombay","VJTI Mumbai","SPIT Andheri","NMIMS Mumbai","DJ Sanghvi College"]},
    "Data Scientist":         {"icon":"📊","color":"#7c5cff","why":"Your mathematical aptitude and interest in AI align perfectly with Data Science. Your analytical thinking score shows you can extract meaningful insights from complex datasets.","skills":["Python & R Programming","Statistics & Probability","Machine Learning","SQL & Databases","Data Visualization"],"roadmap":["Learn Python + NumPy, Pandas, Matplotlib","Complete Andrew Ng ML course on Coursera","Study Statistics deeply","Work on Kaggle competitions","Build a portfolio with 3+ projects"],"colleges":["IIT Bombay","NMIMS Mumbai","Mumbai University","ICT Mumbai","KJ Somaiya"]},
    "Cybersecurity Analyst":  {"icon":"🔐","color":"#00e5ff","why":"Your technology interests and strong problem-solving instincts make Cybersecurity a great match. This field rewards analytical thinkers who can defend systems from attacks.","skills":["Network Security","Ethical Hacking","Linux OS","Python Scripting","CEH Certification"],"roadmap":["Learn networking fundamentals","Master Linux OS","Practice on TryHackMe & HackTheBox","Prepare for CEH certification","Pursue BTech CS/IT with security electives"],"colleges":["VJTI Mumbai","KJ Somaiya","Thakur College","SPIT Andheri","Mumbai University"]},
    "Doctor":                 {"icon":"🩺","color":"#00ff88","why":"Your high Biology and Chemistry scores combined with interest in Medicine and strong Empathy make Medicine a clear fit. You have both the academic foundation and the human touch required.","skills":["Human Anatomy","Clinical Diagnosis","Patient Communication","Medical Ethics","Research Methods"],"roadmap":["Prepare seriously for NEET-UG","Focus on Biology, Chemistry, Physics","Use NCERT + Allen/Aakash material","Complete MBBS (5.5 years)","Choose specialisation in MD/MS"],"colleges":["Seth GS Medical College (KEM)","Grant Medical College","Lokmanya Tilak Medical College","TNMC Nair Hospital","Dr DY Patil Medical College"]},
    "Biotechnologist":        {"icon":"🧬","color":"#4ade80","why":"Your Biology and Chemistry marks combined with interest in research make Biotechnology exciting. One of India's fastest-growing science fields with global opportunities.","skills":["Molecular Biology","Genetics & Genomics","Lab Techniques (PCR, ELISA)","Bioinformatics","Scientific Writing"],"roadmap":["Score well in NEET/JEE for BTech Biotech","Learn bioinformatics tools","Intern at pharma or research labs","Study Python for biological data","Pursue MSc or PhD for research"],"colleges":["IIT Bombay","ICT Mumbai","Homi Bhabha National Institute","Mumbai University","KJ Somaiya"]},
    "Chartered Accountant":   {"icon":"📋","color":"#fbbf24","why":"Your Commerce background and high Accounts scores directly align with a CA career. Strong analytical thinking and time management show you can handle the demanding CA curriculum.","skills":["Financial Accounting","Taxation & GST","Auditing","Financial Analysis","Business Law"],"roadmap":["Register for CA Foundation at ICAI","Clear CA Foundation (4 papers)","Complete CA Intermediate (8 papers)","Do 3-year articleship under a CA","Clear CA Final exam"],"colleges":["HR College of Commerce","KC College","Jai Hind College","NMIMS Mumbai","Narsee Monjee College"]},
    "Investment Banker":      {"icon":"📈","color":"#f59e0b","why":"Your Economics and Finance interests combined with strong Leadership and Analytical Thinking make Investment Banking a strong fit. One of India's highest-paying careers.","skills":["Financial Modeling","Valuation Techniques","Corporate Finance","Excel & Bloomberg","Communication & Negotiation"],"roadmap":["Pursue BCom/BBA/BSc Economics","Take CFA Level 1 in final year","Intern at banks or NBFCs","Join top MBA program (IIM/NMIMS/SPJIMR)","Apply for analyst roles at banks"],"colleges":["SP Jain School of Global Management","NMIMS Mumbai","HR College","Jamnalal Bajaj Institute","Mumbai University"]},
    "Entrepreneur":           {"icon":"🚀","color":"#f472b6","why":"Your Creativity, Leadership, and Business interests are exactly what successful founders share. India's startup ecosystem is booming and your profile shows entrepreneurial potential.","skills":["Business Strategy","Product Thinking","Financial Literacy","Marketing & Sales","Resilience & Adaptability"],"roadmap":["Read Zero to One & The Lean Startup","Build a side project in college","Join your college E-Cell","Attend startup events & hackathons","Apply to incubators like IIT Bombay E-Cell"],"colleges":["SP Jain School of Global Management","NMIMS Mumbai","KJ Somaiya","Narsee Monjee Institute","IIT Bombay E-Cell"]},
    "Lawyer":                 {"icon":"⚖️","color":"#a78bfa","why":"Your Arts background in Political Science and History combined with strong Communication and Public Speaking interests are exactly what a successful lawyer needs.","skills":["Legal Research & Writing","Oral Advocacy","Constitutional Law","Contract Law","Critical Analysis"],"roadmap":["Prepare for CLAT exam","Pursue BA LLB (5-year integrated)","Intern at law firms every summer","Enroll with Bar Council of India","Specialise in Corporate or Criminal Law"],"colleges":["Government Law College Mumbai","ILS Law College Pune","Mumbai University Law Dept","NMIMS School of Law","Symbiosis Law School Pune"]},
    "Journalist":             {"icon":"📰","color":"#fb923c","why":"Your Writing and Public Speaking interests combined with strong Communication and Creativity make Journalism a natural fit. Digital media has created vast new opportunities in India.","skills":["Investigative Reporting","Video Storytelling","Social Media & SEO","Interviewing Techniques","News Editing"],"roadmap":["Start a blog or YouTube channel now","Pursue BA Journalism & Mass Communication","Intern at newspapers/TV channels/digital outlets","Build your byline portfolio","Apply to The Hindu, NDTV, Scroll.in"],"colleges":["St Xavier's College Mumbai","Sophia College Mumbai","KC College Mumbai","Mumbai University","Asian College of Journalism"]},
    "UX Designer":            {"icon":"🎨","color":"#e879f9","why":"Your Design and Creativity interests combined with high Empathy ratings are the two most valuable UX traits. You think about how people feel using products — that is rare and extremely valuable.","skills":["Figma & Adobe XD","User Research","Wireframing & Prototyping","Visual Design Principles","HTML & CSS Basics"],"roadmap":["Learn Figma for free on YouTube","Complete Google UX Design Certificate","Build 3 UX case studies for portfolio","Participate in design hackathons","Apply for UX internships at startups"],"colleges":["IIT Bombay Industrial Design Centre","NID Ahmedabad","MIT Institute of Design Pune","Symbiosis Institute of Design","SNDT College Mumbai"]},
    "Psychologist":           {"icon":"🧠","color":"#818cf8","why":"Your high Empathy score and interest in Psychology and Social Work make you a natural counsellor. Mental health is one of India's most underserved and fastest-growing fields.","skills":["Counselling Techniques","Psychological Assessment","Research Methods","Active Listening","Report Writing"],"roadmap":["Pursue BA/BSc Psychology","Complete MA/MSc Psychology","Get supervised internship hours at a hospital","Register with Rehabilitation Council of India","Specialise in clinical or child psychology"],"colleges":["St Xavier's College Mumbai","Sophia College Mumbai","KC College Mumbai","Mumbai University","SNDT Women's University"]},
    "Architect":              {"icon":"🏛","color":"#34d399","why":"Your Design interests, spatial reasoning, and strong Mathematics score align perfectly with Architecture. A creative yet technical field that literally shapes the world around us.","skills":["AutoCAD & Revit","Design Theory","Structural Engineering Basics","3D Modelling (SketchUp)","Sustainability & Urban Planning"],"roadmap":["Appear for NATA exam","Complete B.Arch (5 years)","Intern at architecture firms every summer","Build a strong portfolio of design projects","Specialise in interior design or urban planning"],"colleges":["Sir JJ College of Architecture Mumbai","KRVIA Mumbai","Rachana Sansad Mumbai","Rizvi College of Architecture","MAEER's MIT Pune"]},
    "Digital Marketer":       {"icon":"📱","color":"#60a5fa","why":"Your Marketing and Creativity interests combined with strong Communication and Adaptability are exactly what brands need. You can start building these skills right now for free.","skills":["SEO & Content Strategy","Google & Meta Ads","Social Media Management","Google Analytics 4","Copywriting & Brand Storytelling"],"roadmap":["Get Google Digital Marketing Certificate (free)","Start a blog or Instagram and grow it","Learn SEO, email marketing, and paid ads","Intern at a digital agency or startup","Build a portfolio with real campaign results"],"colleges":["NMIMS Mumbai","SP Jain School of Global Management","HR College Mumbai","Jai Hind College","Narsee Monjee Institute"]},
    "Teacher":                {"icon":"📚","color":"#a3e635","why":"Your Communication skills, Empathy, and love of Social Work make teaching deeply rewarding. With ed-tech platforms growing rapidly, teachers now have more reach than ever before.","skills":["Curriculum Design","Classroom Management","Student Psychology","Subject Expertise","Digital Teaching Tools"],"roadmap":["Pursue BA/BSc in your subject of interest","Complete B.Ed degree (2 years)","Clear CTET or Maharashtra TET","Gain experience at schools or coaching centres","Explore BYJU's, Unacademy, Vedantu"],"colleges":["Mumbai University","SNDT Women's University","St Xavier's College of Education","TISS Mumbai","ICT Mumbai"]},
}

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/assessment")
@app.route("/assessment.html")
def assessment():
    return send_from_directory(FRONTEND_DIR, "assessment.html")

@app.route("/results")
@app.route("/results.html")
def results():
    return send_from_directory(FRONTEND_DIR, "results.html")

@app.route("/index.html")
def index_html():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)

@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "js"), filename)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        resp = requests.post(f"{FASTAPI_URL}/predict", json=data, timeout=10)
        if resp.status_code != 200:
            return jsonify({"error": "Prediction failed"}), 500
        predictions = resp.json()["top_careers"]
        for pred in predictions:
            d = CAREER_DETAILS.get(pred["career"], {})
            pred.update({"icon":d.get("icon","🎯"),"color":d.get("color","#00a8ff"),"why":d.get("why",""),"skills":d.get("skills",[]),"roadmap":d.get("roadmap",[]),"colleges":d.get("colleges",[])})
        return jsonify({"status":"success","predictions":predictions,"student_data":data})
    except requests.exceptions.ConnectionError:
        return jsonify(get_mock(data))
    except Exception as e:
        return jsonify({"error":str(e)}), 500

def get_mock(data):
    stream = data.get("stream","Science PCM")
    interests = data.get("interests",[])
    pool_map = {
        "Science PCM":["Software Engineer","Data Scientist","Cybersecurity Analyst"],
        "Science PCB":["Doctor","Biotechnologist","Psychologist"],
        "Commerce":   ["Chartered Accountant","Investment Banker","Entrepreneur"],
        "Arts":       ["Lawyer","Journalist","Teacher"],
    }
    imap = {"interest_tech":"Software Engineer","interest_ai":"Data Scientist","interest_cybersecurity":"Cybersecurity Analyst","interest_medicine":"Doctor","interest_biology":"Biotechnologist","interest_finance":"Investment Banker","interest_entrepreneurship":"Entrepreneur","interest_law":"Lawyer","interest_journalism":"Journalist","interest_design":"UX Designer","interest_psychology":"Psychologist","interest_architecture":"Architect","interest_marketing":"Digital Marketer","interest_teaching":"Teacher"}
    pool = pool_map.get(stream, pool_map["Science PCM"])
    scored = {c: 0.5+i*0.05 for i,c in enumerate(pool)}
    for interest in interests:
        career = imap.get(interest)
        if career and career in scored:
            scored[career] += 0.25
    top3 = sorted(scored.items(), key=lambda x: x[1], reverse=True)[:3]
    confs = [0.82, 0.71, 0.60]
    predictions = []
    for i,(career,_) in enumerate(top3):
        d = CAREER_DETAILS.get(career,{})
        predictions.append({"career":career,"confidence":confs[i],"icon":d.get("icon","🎯"),"color":d.get("color","#00a8ff"),"why":d.get("why",""),"skills":d.get("skills",[]),"roadmap":d.get("roadmap",[]),"colleges":d.get("colleges",[])})
    return {"status":"success","predictions":predictions,"student_data":data}

if __name__ == "__main__":
    print("PathNext AI → http://localhost:5000")
    app.run(debug=True, port=5000, host="0.0.0.0")
