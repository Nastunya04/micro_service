# Microservice
### Text Translation Pipeline
This project demonstrates a microservice-based text translation pipeline built with FastAPI. The pipeline includes a Business Service that processes the text (normalizing, detecting language, and translating), a Database Service that simulates data storage in memory, and a Client Service that provides token-based, public access and orchestrates calls between services.
#### Project Structure
```
text_translation_pipeline/
├── business_service/
│   ├── business_service.py      # Contains preprocessing and translation logic
│   ├── Dockerfile
│   └── requirements.txt
├── client_service/
│   ├── client_service.py        # Manages calls to Business and Database services; token-based security applied
│   ├── Dockerfile
│   └── requirements.txt
├── database_service/
│   ├── database_service.py      # In-memory database with endpoints to write and read records
│   ├── Dockerfile
│   └── requirements.txt
├── .env                         # should be created!
└── docker-compose.yml           # Links the services into a single network.
```
#### Setup Instructions
1. **Prerequisites:**
	- Install [Docker](https://docs.docker.com/get-docker/)
	- Install [Docker Compose](https://docs.docker.com/compose/install/)
2. **Clone the Project:**
   - Clone or download the project into your local directory.

3. **Configure Environment Variables:**
   - Create a file named `.env`(if not created) in the project root with the following content:
     ```dotenv
     CLIENT_SERVICE_TOKEN=mysecret-token
     ```
## Running the Application
1.	In the project root, open a terminal and run:
```bash
   docker-compose build --no-cache
   docker-compose up
```
2. The services will start with the following host-port mappings:
- **Client Service:** Accessible at [http://localhost:5005](http://localhost:5005)
- **Business Service:** Accessible internally via http://localhost:5006 (for internal use only)
- **Database Service:** Accessible internally via http://localhost:5007 (for internal use only)

#### Token-Based Authentication

**Mechanism:**  
The Client Service requires an `Authorization` header with the value:
```
Authorization: Bearer mysecret-token
```
where `mysecret-token` is defined in the `.env` file as `CLIENT_SERVICE_TOKEN`.

**How It Works:**  
When a request is made to the Client Service, the FastAPI endpoint retrieves the `Authorization` header and checks if it matches `Bearer {CLIENT_SERVICE_TOKEN}`. If not, it raises an HTTP 401 Unauthorized error.

##### Request Flow

1. **Client → Client Service:**  
   The client sends a POST request to `/translate` (or calls a protected route) and includes the `Authorization` header.

2. **Client Service → Business Service:**  
   The Client Service forwards the text and target language to the Business Service’s `/process` endpoint for normalization, language detection, and translation.

3. **Business Service → Client Service:**  
   The Business Service returns the processed data (including the detected language and translated text) to the Client Service.

4. **Client Service → Database Service:**  
   The Client Service saves the processed record to the Database Service by calling its `/write` endpoint.

5. **Database Service → Client Service → Client:**  
   After storing the data, the Database Service returns a success message to the Client Service, which then returns the final translation result to the client.


## Translation Request using curl

Submit a POST request to the Client Service's `/translate` endpoint:

```bash
curl -X POST http://localhost:5005/translate \
  -H "Authorization: Bearer mysecret-token" \
  -H "Content-Type: application/json" \
  -d '{"text": "Я б хотів купити лосось", "target_language": "en"}'
```
In this curl example, the JSON payload contains two key-value pairs:
- “text”:
This is the original piece of text that you want to translate. In the example, "Я б хотів купити лосось" is the input text that will be processed by the Business Service.
- “target_language”:
This specifies the language into which the text should be translated. In the example, "en" is provided as the target language, which stands for English.

Thus, when you send this request, the system will take the text “Я б хотів купити лосось” and translate it into English.

**Expected Response:**
```json
{"detected_language_of_request":"uk","target_language":"en","translated_text":"I would like to buy salmon"}
```
## Testing Other Endpoints

### Business Service Endpoints

- **Root Endpoint**  
  - **URL:** `http://localhost:5006/`  
  - **Method:** GET  
  - **Description:** Returns a short description of the Business Service.  
  - **Example:**
    ```bash
    curl http://localhost:5006/
    ```

- **Health Check Endpoint**  
  - **URL:** `http://localhost:5006/health`  
  - **Method:** GET  
  - **Description:** Returns `{"status": "ok"}` to indicate the service is running.  
  - **Example:**
    ```bash
    curl http://localhost:5006/health
    ```

- **Processing Endpoint**  
  - **URL:** `http://localhost:5006/process`  
  - **Method:** POST  
  - **Description:** Accepts a JSON payload with `text` and `target_language`, normalizes the text, detects its language, and returns the translated text.  
  - **Example:**
    ```bash
    curl -X POST http://localhost:5006/process \
      -H "Content-Type: application/json" \
      -d '{"text": "Hello, how are you?", "target_language": "es"}'
    ```

---

### Client Service Endpoints

- **Root Endpoint**  
  - **URL:** `http://localhost:5005/`  
  - **Method:** GET  
  - **Description:** Returns a short description of the Client Service.  
  - **Example:**
    ```bash
    curl http://localhost:5005/
    ```

- **Health Check Endpoint**  
  - **URL:** `http://localhost:5005/health`  
  - **Method:** GET  
  - **Description:** Returns `{"status": "ok"}` indicating that the service is operational.  
  - **Example:**
    ```bash
    curl http://localhost:5005/health
    ```

- **Protected Route**  
  - **URL:** `http://localhost:5005/some-protected-route`  
  - **Method:** GET  
  - **Description:** Validates the token passed in the `Authorization` header. Returns an authorization success message if the token is correct.  
  - **Example:**
    ```bash
    curl -X GET http://localhost:5005/some-protected-route \
      -H "Authorization: Bearer mysecret-token"
    ```
---

### Database Service Endpoints

- **Root Endpoint**  
  - **URL:** `http://localhost:5007/`  
  - **Method:** GET  
  - **Description:** Returns a short description of the Database Service.  
  - **Example:**
    ```bash
    curl http://localhost:5007/
    ```

- **Health Check Endpoint**  
  - **URL:** `http://localhost:5007/health`  
  - **Method:** GET  
  - **Description:** Returns `{"status": "ok"}` to confirm that the service is running.  
  - **Example:**
    ```bash
    curl http://localhost:5007/health
    ```

- **Write Endpoint**  
  - **URL:** `http://localhost:5007/write`  
  - **Method:** POST  
  - **Description:** Accepts a JSON record and saves it to the in-memory database.
  - **Example:**
    ```bash
    curl -X POST http://localhost:5007/write \
      -H "Content-Type: application/json" \
      -d '{"original_text": "Hello, how are you?", "translated_text": "¿hola, cómo estás?", "target_language": "es", "detected_language": "en"}'
    ```

- **Read Endpoint**  
  - **URL:** `http://localhost:5007/read`  
  - **Method:** GET  
  - **Description:** Returns all stored translation records as a JSON array.
  - **Example:**
    ```bash
    curl http://localhost:5007/read
    ```
## Stopping the application
To stop the application and remove the running containers, open a terminal in the project root and run:
```bash
   docker-compose down
```
This command stops and removes all containers defined in the docker-compose.yml, as well as the network created by Docker Compose. If you want to additionally remove the images, you can use:
```bash
   docker-compose down --rmi all
```
