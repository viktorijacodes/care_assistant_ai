# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Any, Dict, List, Optional
import google.auth
from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.cloud import firestore
from google.genai import types

from .a2ui_utils import a2ui_callback

MODEL = "gemini-2.5-flash"
PROJECT_ID = "qwiklabs-gcp-04-5ebc0f028b72"
LOCATION = "us-central1"
BUCKET_NAME = "care-assistant-assets-5ebc0f02"

# Agent Engine Code Execution Sandbox
sandbox_code_executor = AgentEngineSandboxCodeExecutor()

_db_client = None

def _get_db():
    global _db_client
    if _db_client is None:
        try:
            _db_client = firestore.Client(project=PROJECT_ID)
        except Exception:
            pass
    return _db_client

# In-memory synthetic patients fallback in case Firestore API is unreachable or fails auth
_SYNTHETIC_PATIENTS = [
    {
        "patient_id": "001",
        "name": "Astrid Andersson",
        "age": 82,
        "room_number": "101-A",
        "mobility_status": "Walker assisted",
        "cognitive_status": "Mild cognitive impairment (MCI)",
        "likes": ["Gardening", "Beethoven", "Earl Grey tea", "Watercolor painting"],
        "dislikes": ["Loud noises", "Crowded rooms", "Cold weather"],
        "routines": ["Morning garden walk", "Tea at 3 PM", "Classical music before bed"],
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
        "likes": ["Chess", "History books", "Jazz music", "Black coffee"],
        "dislikes": ["Rushed conversations", "Bright flickering lights"],
        "routines": ["Morning news reading", "Chess puzzle at 11 AM", "Evening porch sitting"],
        "dietary_restrictions": ["Pureed diet", "Thickened liquids"],
        "notes": "Enjoys discussing historical events and listening to smooth jazz."
    },
    {
        "patient_id": "003",
        "name": "Ingrid Karlsson",
        "age": 89,
        "room_number": "105-A",
        "mobility_status": "Independent with cane",
        "cognitive_status": "Alert and oriented x4",
        "likes": ["Knitting", "Crossword puzzles", "Classic movies", "Baking stories"],
        "dislikes": ["Being addressed by first name without permission", "Boredom"],
        "routines": ["Crossword puzzles", "Crochet group at 2 PM", "Call with daughter at 6 PM"],
        "dietary_restrictions": ["Regular diet", "Gluten-free"],
        "notes": "Highly social and loves leading crafting sessions with other residents."
    },
    {
        "patient_id": "004",
        "name": "Lars Nilsson",
        "age": 75,
        "room_number": "108-C",
        "mobility_status": "Bed rest / High assistance required",
        "cognitive_status": "Advanced Alzheimer's",
        "likes": ["Soft blankets", "Lavender scent", "Nature sounds", "Ocean waves"],
        "dislikes": ["Sudden touch without warning", "High pitched tones"],
        "routines": ["Gentle hand massage at 10 AM", "Soothing audiobooks", "Aromatherapy"],
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
        "likes": ["Bird watching", "Sing-alongs", "Flower arranging", "Chamomile tea"],
        "dislikes": ["Isolation", "Dark rooms"],
        "routines": ["Bird watching at courtyard", "1950s sing-along at 4 PM"],
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
        "likes": ["Vintage cars", "Folk music", "Harmonica", "Woodworking tales"],
        "dislikes": ["Overcrowded hallways", "Flickering shadows"],
        "routines": ["Classic music hour", "10-minute upper body stretch"],
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
        "likes": ["Baking recipes", "Rosemary scent", "Piano melodies", "Herbal tea"],
        "dislikes": ["Excessive background noise", "Cold drafts"],
        "routines": ["Morning herb garden care", "Short story reading"],
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
        "likes": ["Origami", "Nature gardens", "Instrumental music", "Green tea"],
        "dislikes": ["Loud intercoms", "Rushed staff"],
        "routines": ["Origami practice", "Bonsai trimming", "Green tea ceremony"],
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
        "likes": ["Soft velvet fabric", "Classic melodies", "Warm tea", "Family photo books"],
        "dislikes": ["Sudden changes in illumination", "Cold room temperature"],
        "routines": ["Gentle hand tactile therapy", "Lullaby listening"],
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
        "likes": ["Sports history", "Organ music", "Radio broadcasts"],
        "dislikes": ["Confusing multi-step instructions", "Noisy crowds"],
        "routines": ["Sports trivia review", "Afternoon sun porch rest"],
        "dietary_restrictions": ["Low salt", "No whole nuts"],
        "notes": "Avid sports fan; enjoys short nostalgia trivia and listening to radio broadcasts."
    }
]


def list_patients() -> List[Dict[str, Any]]:
    """Lists all synthetic patient profiles stored in the system.

    Returns:
        A list of patient summaries including patient_id, name, age, room_number, and mobility.
    """
    try:
        db = _get_db()
        if db is not None:
            patients_ref = db.collection("patients")
            results = []
            for doc in patients_ref.stream():
                data = doc.to_dict()
                results.append({
                    "patient_id": data.get("patient_id", doc.id),
                    "name": data.get("name"),
                    "age": data.get("age"),
                    "room_number": data.get("room_number"),
                    "mobility_status": data.get("mobility_status"),
                    "cognitive_status": data.get("cognitive_status"),
                })
            if results:
                return results
    except Exception:
        pass

    return [
        {
            "patient_id": p["patient_id"],
            "name": p["name"],
            "age": p["age"],
            "room_number": p["room_number"],
            "mobility_status": p["mobility_status"],
            "cognitive_status": p["cognitive_status"],
        }
        for p in _SYNTHETIC_PATIENTS
    ]


def get_patient_profile(name_or_id: str) -> Dict[str, Any]:
    """Retrieves full profile data for a specific patient by name or patient ID.

    Args:
        name_or_id: The full/partial name of the patient (e.g. 'Eleanor', 'Arthur') or their ID ('001', 'patient_001').

    Returns:
        A dictionary containing full demographics, preferences, routines, health status, and dietary restrictions.
    """
    clean_id = name_or_id.strip()
    try:
        db = _get_db()
        if db is not None:
            patients_ref = db.collection("patients")
            
            # Direct document ID check
            doc = patients_ref.document(clean_id).get()
            if doc.exists:
                return doc.to_dict()

            if clean_id.startswith("patient_"):
                alt_id = clean_id.replace("patient_", "")
                doc = patients_ref.document(alt_id).get()
                if doc.exists:
                    return doc.to_dict()
            elif clean_id.isdigit():
                alt_id = f"patient_{clean_id}"
                doc = patients_ref.document(alt_id).get()
                if doc.exists:
                    return doc.to_dict()

            # Search by partial or full name match
            query_lower = clean_id.lower()
            for doc in patients_ref.stream():
                data = doc.to_dict()
                patient_name = data.get("name", "").lower()
                pid = str(data.get("patient_id", "")).lower()
                if query_lower in patient_name or patient_name in query_lower or query_lower == pid:
                    return data
    except Exception:
        pass

    # Fallback to local synthetic patient list
    q_lower = clean_id.lower().replace("patient_", "")
    for p in _SYNTHETIC_PATIENTS:
        if (
            q_lower == p["patient_id"].lower()
            or q_lower in p["name"].lower()
            or p["name"].lower() in q_lower
        ):
            return p

    return {"error": f"Patient '{name_or_id}' not found in system."}


def log_patient_activity(
    patient_id: str,
    activity_name: str,
    duration_minutes: int,
    nurse_notes: str,
    receptivity_rating: Optional[str] = "Positive"
) -> Dict[str, Any]:
    """Logs a completed activity and nurse notes for a patient into the care activity history.

    Args:
        patient_id: The ID of the patient (e.g. '001', 'patient_001').
        activity_name: Name of the activity conducted.
        duration_minutes: Duration of the activity in minutes.
        nurse_notes: Observations or feedback from the nurse.
        receptivity_rating: Patient receptivity (e.g., 'Positive', 'Neutral', 'Fatigued', 'Declined').

    Returns:
        A confirmation status dictionary with the log ID.
    """
    log_entry = {
        "patient_id": patient_id,
        "activity_name": activity_name,
        "duration_minutes": duration_minutes,
        "nurse_notes": nurse_notes,
        "receptivity_rating": receptivity_rating,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    
    try:
        db = _get_db()
        if db is not None:
            doc_ref = db.collection("activity_logs").document()
            doc_ref.set(log_entry)
            return {"status": "success", "log_id": doc_ref.id, "entry": log_entry}
    except Exception:
        pass

    return {"status": "success", "log_id": "local_fallback_log", "entry": log_entry}


def get_shift_context(time_of_day: Optional[str] = None) -> Dict[str, Any]:
    """Provides current nursing shift context, meal schedule, and upcoming floor routine windows.

    Args:
        time_of_day: Optional specific time description (e.g., 'morning', 'afternoon', '11:30 AM'). If omitted, current time is used.

    Returns:
        A dictionary with shift name, upcoming floor events (meals, quiet hours), and recommended activity pacing.
    """
    now = datetime.datetime.now()
    hour = now.hour

    if time_of_day:
        t_lower = time_of_day.lower()
        if "morn" in t_lower or "breakfast" in t_lower:
            hour = 9
        elif "noon" in t_lower or "lunch" in t_lower or "midday" in t_lower:
            hour = 12
        elif "afternoon" in t_lower:
            hour = 14
        elif "eve" in t_lower or "dinner" in t_lower:
            hour = 18
        elif "night" in t_lower or "sleep" in t_lower:
            hour = 21

    if 7 <= hour < 15:
        shift = "Day Shift (07:00 - 15:00)"
        next_event = "Lunch service at 12:00 PM" if hour < 12 else "Afternoon rest window at 13:30"
        pacing = "Higher alertness window; good for cognitive, reminiscing, and outdoor window activities."
    elif 15 <= hour < 23:
        shift = "Evening Shift (15:00 - 23:00)"
        next_event = "Dinner service at 17:30 PM" if hour < 18 else "Quiet hours / wind-down preparation at 20:00"
        pacing = "Calming, low-stimulation activities; sensory relaxation and gentle music."
    else:
        shift = "Night Shift (23:00 - 07:00)"
        next_event = "Morning breakfast tray delivery at 07:30 AM"
        pacing = "Rest and sleep support; quiet comforting presence if patient wakes up."

    return {
        "shift": shift,
        "simulated_hour": f"{hour:02d}:00",
        "upcoming_floor_event": next_event,
        "floor_pacing_guidance": pacing,
    }


def get_historical_memory_prompts(month: Optional[int] = None, day: Optional[int] = None) -> List[Dict[str, Any]]:
    """Fetches uplifting historical events and milestones for today (or a given date) from Wikimedia's 'On this day' feed.
    Useful for conversation starters, reminiscence prompts, and trivia tailored to older adults.

    Args:
        month: Optional month number (1-12). Defaults to current month.
        day: Optional day number (1-31). Defaults to current day.

    Returns:
        A list of curated historical memory events (year and event description).
    """
    now = datetime.datetime.now()
    m = month or now.month
    d = day or now.day

    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/{m}/{d}"
    try:
        import json
        import urllib.request
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "CareAssistantAI/1.0 (careapp@example.com)"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            events = data.get("selected", [])
            # Filter and take 3-4 interesting historical events
            results = []
            for ev in events[:4]:
                results.append({
                    "year": ev.get("year"),
                    "event": ev.get("text")
                })
            return results if results else [{"year": now.year, "event": "Today is a wonderful day to share memories and favorite stories."}]
    except Exception as e:
        return [{"year": 1969, "event": "Apollo astronauts and historic world events provide great conversation starters."}]


def geocode_address(address: str) -> Dict[str, Any]:
    """Converts a street address, city, or landmark into latitude and longitude coordinates using the Google Geocoding API.

    Args:
        address: The address or place string to geocode (e.g. '1600 Amphitheatre Pkwy, Mountain View, CA' or 'Central Park, NY').

    Returns:
        A dictionary containing formatted address, latitude, and longitude.
    """
    import json
    import os
    import urllib.parse
    import urllib.request
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    if not api_key or api_key == "PASTE_KEY_HERE":
        return {"error": "GOOGLE_MAPS_API_KEY is not configured in .env"}

    params = urllib.parse.urlencode({"address": address, "key": api_key})
    url = f"https://maps.googleapis.com/maps/api/geocode/json?{params}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "OK" and data.get("results"):
                res = data["results"][0]
                loc = res["geometry"]["location"]
                return {
                    "formatted_address": res.get("formatted_address"),
                    "latitude": loc.get("lat"),
                    "longitude": loc.get("lng"),
                }
            return {"error": f"Geocoding failed: {data.get('status')} - {data.get('error_message', '')}"}
    except Exception as e:
        return {"error": f"Geocoding request failed: {str(e)}"}


def search_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "park",
    radius_meters: float = 1500.0,
    max_results: int = 5,
) -> List[Dict[str, Any]]:
    """Searches for nearby places (parks, libraries, botanical gardens, cafes) using the Places API (New) REST endpoint.

    Args:
        latitude: Latitude coordinate for search center.
        longitude: Longitude coordinate for search center.
        place_type: The place type to search (e.g., 'park', 'library', 'cafe', 'botanical_garden', 'museum').
        radius_meters: Radius in meters around the center (default: 1500.0).
        max_results: Maximum number of results to return (default: 5).

    Returns:
        A list of nearby places with display name, formatted address, and location coordinates.
    """
    import json
    import os
    import urllib.request
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    if not api_key or api_key == "PASTE_KEY_HERE":
        return [{"error": "GOOGLE_MAPS_API_KEY is not configured in .env"}]

    url = "https://places.googleapis.com/v1/places:searchNearby"
    payload = {
        "includedTypes": [place_type],
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": radius_meters,
            }
        },
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location",
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            places = data.get("places", [])
            results = []
            for p in places:
                results.append({
                    "name": p.get("displayName", {}).get("text", "Unknown"),
                    "address": p.get("formattedAddress", "Unknown"),
                    "location": p.get("location", {}),
                })
            return results if results else [{"message": f"No {place_type} found within {radius_meters}m"}]
    except Exception as e:
        return [{"error": f"Places search failed: {str(e)}"}]


def generate_memory_video(
    prompt: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """Generates a short memory video for a patient activity or prompt using Google's Omni model (gemini-omni-flash-preview) in the global region.

    Saves the video with tool_context.save_artifact for the Playground Artifacts panel and uploads it to public Cloud Storage, returning the public HTTPS URL.

    Args:
        prompt: Detailed description of the video scene tailored to the patient (e.g., 'A calm, beautiful rose garden with gentle sunlight for Astrid').
        tool_context: ToolContext instance for saving the artifact.

    Returns:
        A dictionary containing the status, public_url, and artifact_name.
    """
    import base64
    import uuid
    from google import genai
    from google.cloud import storage

    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    interaction = client.interactions.create(
        model="gemini-omni-flash-preview",
        input=prompt,
    )

    video_bytes = None
    if hasattr(interaction, "output_video") and interaction.output_video and hasattr(interaction.output_video, "data"):
        raw_data = interaction.output_video.data
        if isinstance(raw_data, str):
            video_bytes = base64.b64decode(raw_data)
        elif isinstance(raw_data, bytes):
            video_bytes = raw_data

    if not video_bytes:
        return {"error": "Failed to generate video or extract video data from interaction response."}

    video_id = str(uuid.uuid4())[:8]
    filename = f"memory_video_{video_id}.mp4"

    # 1. Save artifact for Playground's Artifacts panel using tool_context.save_artifact
    artifact_part = types.Part.from_bytes(data=video_bytes, mime_type="video/mp4")
    tool_context.save_artifact(filename=filename, artifact=artifact_part)

    # 2. Upload video bytes directly to public Cloud Storage bucket (without writing local file)
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"videos/{filename}")
    blob.upload_from_string(video_bytes, content_type="video/mp4")

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/videos/{filename}"

    return {
        "status": "success",
        "public_url": public_url,
        "artifact_name": filename,
    }


_schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

INSTRUCTION = _schema_manager.generate_system_prompt(
    role_description=(
        "You are a specialized Care Assistant AI for nursing staff. "
        "Your goal is to help nurses plan meaningful, personalized, and safe activities for patients "
        "based on saved profile data, available time, and shift context."
    ),
    workflow_description=(
        "1. Always look up the patient profile using get_patient_profile or list_patients.\n"
        "2. Generate a SIMPLIFIED, concise health memory activity tailored to the patient and selected duration.\n"
        "3. Output MUST contain ONLY TWO SECTIONS:\n"
        "   - 'Suggested activity': A short, warm 1-2 sentence description personalized to the patient explaining what activity to do and why it suits them.\n"
        "   - 'Conversation starters': Exactly 3 short, natural, open-ended questions for the caregiver to ask.\n"
        "4. STRICTLY PROHIBITED: Do NOT include materials lists, equipment setup, shift context, clinical explanations, step-by-step procedures, or 'Why This Activity Fits' sections.\n"
        "5. Return structured A2UI UI components or text adhering strictly to this simplified 2-section format."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        '{"Image": {"url": {"literalString": "https://..."}}}. Never point an '
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

# WRITE: after each turn, send the session events to Memory Bank for durable extraction.
async def generate_memories_callback(callback_context: CallbackContext):
    try:
        await callback_context.add_session_to_memory()
    except Exception:
        pass
    return None


root_agent = Agent(
    name="simple_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=INSTRUCTION,
    tools=[
        list_patients,
        get_patient_profile,
        get_shift_context,
        get_historical_memory_prompts,
        geocode_address,
        search_nearby_places,
        log_patient_activity,
        generate_memory_video,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)



