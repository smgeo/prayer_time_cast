# prayer_time_cast
a very simple python project to automate prayer call casting throug your local network device. 
## Usage

1.  **Install Python:** If you don't have Python installed, download and install it from the official Python website ([https://www.python.org/downloads/](https://www.python.org/downloads/)).

2.  **Create a Virtual Environment:**

    *   Open your terminal or command prompt.
    *   Navigate to your project directory.
    *   Create a virtual environment using the following command:

        ```bash
        python -m venv venv
        ```
    *   Activate the virtual environment:

        *   On Windows:

            ```bash
            .\venv\Scripts\activate
            ```
        *   On macOS and Linux:

            ```bash
            source venv/bin/activate
            ```

3.  **Install Requirements:**

    *   Install the required packages using pip:

        ```bash
        pip install -r requirements.txt
        ```

4.  **Create .env File:**

    *   Create a `.env` file in your project directory.
    *   Add the following variables to the `.env` file, adjusting the values as needed:

        ```
        MOSQUE_LINK=YOUR_MOSQUE_GOOGLE_SEARCH_LINK
        HOME_ASSISTANT_IP=YOUR_HOME_ASSISTANT_IP
        HOME_ASSISTANT_PORT=YOUR_HOME_ASSISTANT_PORT
        HOME_ASSISTANT_TOKEN=YOUR_LONG_LIVED_ACCESS_TOKEN
        CALENDAR_ID=YOUR_HOME_ASSISTANT_CALENDAR_ID
        ```

5.  **Find Your Mosque Link:**

    *   Search for your mosque on Google.
    *   Copy the link to the Google search results page and paste it into the `MOSQUE_LINK` variable in your `.env` file.

6.  **Home Assistant Setup:**

    *   **Get a Long-Lived Access Token:**
        *   In Home Assistant, click on your profile (usually in the bottom left corner).
        *   Scroll down to the "Long-Lived Access Tokens" section.
        *   Create a new token and give it a descriptive name.
        *   Copy the generated token and paste it into the `HOME_ASSISTANT_TOKEN` variable in your `.env` file.  Important:  Store this token securely.
    *   **Create a New Local Calendar:**
        *   In Home Assistant, go to Configuration -> Integrations.
        *   Click the "+" button to add a new integration.
        *   Search for "Local Calendar" and add it.
        *   Give your calendar a name.
        *   After creating the calendar, find its `entity_id` (e.g., `calendar.prayer_times`).  This is your `CALENDAR_ID`.  You can find this in the Home Assistant UI, often in the Developer Tools -> States section.
        *   Add the `entity_id` to the `CALENDAR_ID` variable in your `.env` file.

7.  **Run the Script:**

    *   Make sure your virtual environment is activated.
    *   Run the Python script:

        ```bash
        python your_script_name.py
8.  **Home Assistant Automation:**

    *   In Home Assistant, create a new automation.
    *   Use a "Calendar" trigger, selecting your prayer times calendar (`CALENDAR_ID`).
    *   Configure the trigger to fire at the "start" of the event.
    *   As the action, choose to cast a video to your desired media player. Ensure the video file is accessible within your Home Assistant media library.

