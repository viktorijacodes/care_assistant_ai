import os
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-5ebc0f028b72"
db = firestore.Client(project=PROJECT_ID)

patients = [
    {
        "patient_id": "001",
        "name": "Astrid Andersson",
        "age": 82,
        "room_number": "101-A",
        "mobility_status": "Walker assisted",
        "cognitive_status": "Mild cognitive impairment (MCI)",
        "routines": ["Morning garden walk", "Tea at 3 PM", "Classical music before bed"],
        "likes": ["Gardening", "Beethoven", "Earl Grey tea", "Watercolor painting"],
        "dislikes": ["Loud noises", "Crowded rooms", "Cold weather"],
        "dietary_restrictions": ["Low sodium", "Diabetic friendly"],
        "notes": "Responds very well to sensory garden activities and gentle classical music."
    },
    {
        "patient_id": "002",
        "name": "Erik Johansson",
        "age": 78,
        "room_number": "102-B",
        "mobility_status": "Wheelchair bound",
        "cognitive_status": "Moderate vascular dementia",
        "routines": ["Morning news reading", "Chess puzzle at 11 AM", "Evening porch sitting"],
        "likes": ["Chess", "History books", "Jazz music", "Black coffee"],
        "dislikes": ["Rushed conversations", "Bright flickering lights"],
        "dietary_restrictions": ["Puréed texture", "Thickened liquids level 2"],
        "notes": "Enjoys discussing historical events and listening to smooth jazz."
    },
    {
        "patient_id": "003",
        "name": "Ingrid Karlsson",
        "age": 89,
        "room_number": "105-A",
        "mobility_status": "Independent with cane",
        "cognitive_status": "Alert and oriented x4",
        "routines": ["Crossword puzzles", "Crochet group at 2 PM", "Call with daughter at 6 PM"],
        "likes": ["Knitting", "Crossword puzzles", "Classic movies", "Baking stories"],
        "dislikes": ["Being addressed by first name without permission", "Boredom"],
        "dietary_restrictions": ["Gluten-free"],
        "notes": "Highly social and loves leading crafting sessions with other residents."
    },
    {
        "patient_id": "004",
        "name": "Lars Nilsson",
        "age": 75,
        "room_number": "108-C",
        "mobility_status": "Bed rest / High assistance required",
        "cognitive_status": "Advanced Alzheimer's",
        "routines": ["Gentle hand massage at 10 AM", "Soothing audiobooks", "Aromatherapy"],
        "likes": ["Soft blankets", "Lavender scent", "Nature sounds", "Ocean waves"],
        "dislikes": ["Sudden touch without warning", "High pitched tones"],
        "dietary_restrictions": ["Soft mechanical diet"],
        "notes": "Calmed by lavender aromatherapy and soft tactile stimuli."
    },
    {
        "patient_id": "005",
        "name": "Birgitta Eriksson",
        "age": 84,
        "room_number": "112-B",
        "mobility_status": "Walker assisted",
        "cognitive_status": "Mild dementia",
        "routines": ["Bird watching at courtyard", "1950s sing-along at 4 PM"],
        "likes": ["Bird watching", "Sing-alongs", "Flower arranging", "Chamomile tea"],
        "dislikes": ["Isolation", "Dark rooms"],
        "dietary_restrictions": ["Low sugar"],
        "notes": "Retired school teacher who loves group singing and outdoor nature activities."
    },
    {
        "patient_id": "006",
        "name": "Sven Larsson",
        "age": 81,
        "room_number": "115-A",
        "mobility_status": "Wheelchair bound",
        "cognitive_status": "Moderate Lewy body dementia",
        "routines": ["Classic music hour", "10-minute upper body stretch"],
        "likes": ["Vintage cars", "Folk music", "Harmonica", "Woodworking tales"],
        "dislikes": ["Overcrowded hallways", "Flickering shadows"],
        "dietary_restrictions": ["Heart healthy", "Low sodium"],
        "notes": "Loves listening to classic folk tunes and holding vintage tool tactile prompts."
    },
    {
        "patient_id": "007",
        "name": "Margareta Olsson",
        "age": 86,
        "room_number": "118-B",
        "mobility_status": "Walker assisted",
        "cognitive_status": "Mild cognitive impairment (MCI)",
        "routines": ["Morning herb garden care", "Short story reading"],
        "likes": ["Baking recipes", "Rosemary scent", "Piano melodies", "Herbal tea"],
        "dislikes": ["Excessive background noise", "Cold drafts"],
        "dietary_restrictions": ["Diabetic friendly"],
        "notes": "Former bakery owner; responds wonderfully to baking scent prompts and recipe reminiscing."
    },
    {
        "patient_id": "008",
        "name": "Nils Persson",
        "age": 79,
        "room_number": "120-C",
        "mobility_status": "Independent with cane",
        "cognitive_status": "Alert and oriented x3",
        "routines": ["Origami practice", "Bonsai trimming", "Green tea ceremony"],
        "likes": ["Origami", "Nature gardens", "Instrumental music", "Green tea"],
        "dislikes": ["Loud intercoms", "Rushed staff"],
        "dietary_restrictions": ["Low sodium"],
        "notes": "Loves fine tactile activities like paper folding and tranquil garden scenery."
    },
    {
        "patient_id": "009",
        "name": "Eva Svensson",
        "age": 91,
        "room_number": "124-A",
        "mobility_status": "Wheelchair bound",
        "cognitive_status": "Moderate Alzheimer's",
        "routines": ["Gentle hand tactile therapy", "Lullaby listening"],
        "likes": ["Soft velvet fabric", "Classic melodies", "Warm tea", "Family photo books"],
        "dislikes": ["Sudden changes in illumination", "Cold room temperature"],
        "dietary_restrictions": ["Soft foods"],
        "notes": "Calmed by smooth music, warm blankets, and flipping through tactile fabric swatches."
    },
    {
        "patient_id": "010",
        "name": "Karl Gustafsson",
        "age": 77,
        "room_number": "128-B",
        "mobility_status": "Walker assisted",
        "cognitive_status": "Mild vascular dementia",
        "routines": ["Sports trivia review", "Afternoon sun porch rest"],
        "likes": ["Sports history", "Organ music", "Radio broadcasts"],
        "dislikes": ["Confusing multi-step instructions", "Noisy crowds"],
        "dietary_restrictions": ["Low salt", "No whole nuts"],
        "notes": "Avid sports fan; enjoys short nostalgia trivia and listening to radio broadcasts."
    }
]

for p in patients:
    doc_id = f"patient_{p['patient_id']}"
    db.collection("patients").document(doc_id).set(p)
    db.collection("patients").document(p['patient_id']).set(p)
    print(f"Successfully seeded patient {p['patient_id']} - {p['name']}")

print("All Swedish patient profiles seeded into Firestore successfully!")
